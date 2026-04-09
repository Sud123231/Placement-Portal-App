import os
from datetime import datetime

from flask import send_from_directory
from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from kombu.exceptions import OperationalError
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from cache_utils import (
    cache_key_all_student_applications,
    cache_key_all_students,
    cache_key_student_applied_drives,
    cache_key_student_applications,
    invalidate_all_student_applications_cache,
    invalidate_drive_applications_cache,
    invalidate_student_applied_drives_cache,
    invalidate_student_applications_cache
)
from extensions import cache, celery, db
from models import Application, Student as StudentModel
from tasks import export_student_applications_csv


class Student(Resource):
    @jwt_required()
    def get(self, id):
        student = db.session.query(StudentModel).filter_by(student_id=id).first()
        if not student:
            return {"message": "Student not found"}, 404

        return {"student": student.to_dict()}, 200

    @jwt_required()
    def patch(self, id):
        data = request.get_json() or {}
        student = db.session.query(StudentModel).filter_by(student_id=id).first()
        if not student:
            return {"message": "Student not found"}, 404

        student.status = data.get("status", student.status)

        if data.get("name"):
            student.name = data.get("name")
        if data.get("department"):
            student.department = data.get("department")
        if data.get("password") and student.user:
            student.user.password = generate_password_hash(data.get("password"))

        db.session.commit()
        return {"student": student.to_dict()}, 200


class StudentApplications(Resource):
    @jwt_required()
    def get(self, student_id):
        cache_key = cache_key_student_applications(student_id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        student = db.session.query(StudentModel).filter_by(student_id=student_id).first()
        if not student:
            return {"message": "Student not found"}, 404

        applications = db.session.query(Application).filter_by(student_id=student_id).all()
        response = {
            "student_name": student.name,
            "department": student.department,
            "applications": [application.to_dict() for application in applications],
        }, 200
        cache.set(cache_key, response, timeout=60)
        return response

    @jwt_required()
    def post(self, student_id):
        drive_id = request.form.get("drive_id")
        resume_file = request.files.get("resume")

        if not resume_file:
            return {"message": "upload resume"}, 400
        if not drive_id:
            return {"message": "drive_id is missing"}, 400

        existing = Application.query.filter_by(
            student_id=student_id,
            drive_id=drive_id,
        ).first()
        if existing:
            return {"message": "You have already applied"}, 400

        application = Application(
            student_id=student_id,
            drive_id=drive_id,
            application_date=datetime.now(),
        )
        db.session.add(application)
        db.session.flush()

        os.makedirs("uploads/resumes", exist_ok=True)
        filename = secure_filename(f"application_{application.application_id}.pdf")
        resume_file.save(os.path.join("uploads/resumes", filename))
        application.resume = f"uploads/resumes/{filename}"

        db.session.commit()
        invalidate_drive_applications_cache(drive_id)
        invalidate_student_applications_cache(student_id)
        invalidate_student_applied_drives_cache(student_id)
        invalidate_all_student_applications_cache()
        return {
            "message": "successfully created application",
            "application_id": application.application_id,
        }, 201


class Students(Resource):
    @jwt_required()
    def get(self):
        cache_key = cache_key_all_students()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        students = db.session.query(StudentModel).filter_by(status="Active").all()
        response = {"students": [student.to_dict() for student in students]}, 200
        cache.set(cache_key, response, timeout=60)
        return response


class AllStudentsApplications(Resource):
    @jwt_required()
    def get(self):
        cache_key = cache_key_all_student_applications()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        applications = db.session.query(Application).all()
        response = {"applications": [application.to_dict() for application in applications]}, 200
        cache.set(cache_key, response, timeout=60)
        return response


class ApplicationResume(Resource):
    def get(self, id):
        application = Application.query.get_or_404(id)
        if not application.resume:
            return {"message": "No resume found"}, 404

        filename = application.resume.split("/")[-1]
        return send_from_directory("uploads/resumes", filename)


class StudentAppliedDrives(Resource):
    def get(self, id):
        cache_key = cache_key_student_applied_drives(id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        applications = db.session.query(Application).filter_by(student_id=id).all()
        response = {"applied_drives": []}

        for application in applications:
            response["applied_drives"].append(
                {
                    "drive_id": application.placement_drive.drive_id,
                    "application_id": application.application_id,
                    "drive_name": application.placement_drive.name,
                    "applied_date": str(application.application_date),
                    "company_name": application.placement_drive.company.name,
                }
            )

        response = response, 200
        cache.set(cache_key, response, timeout=60)
        return response


class ExportStudentApplications(Resource):
    @jwt_required()
    def post(self, student_id):
        try:
            task = export_student_applications_csv.delay(student_id)
        except OperationalError:
            return {
                "message": "Task broker is unavailable. Start Redis/Celery and try again.",
                "status": "error",
            }, 503

        return {
            "message": "Export job started",
            "task_id": task.id,
            "status": "processing",
        }, 202


class ExportStatus(Resource):
    @jwt_required()
    def get(self, task_id):
        try:
            if celery.backend.__class__.__name__ == "DisabledBackend":
                return {
                    "task_id": task_id,
                    "status": "error",
                    "message": "Celery result backend is not configured.",
                }, 503

            result = celery.AsyncResult(task_id)
            if result.state == "PENDING":
                return {
                    "task_id": task_id,
                    "status": "pending",
                    "message": "Task is waiting to be processed",
                }, 200
            if result.state == "SUCCESS":
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "result": result.result,
                }, 200

            return {
                "task_id": task_id,
                "status": "error",
                "message": "Task failed or was revoked",
            }, 400
        except Exception as exc:
            return {
                "task_id": task_id,
                "status": "error",
                "message": str(exc),
            }, 500


class ExportDownload(Resource):
    @jwt_required()
    def get(self, filename):
        safe_filename = secure_filename(filename)
        if safe_filename != filename:
            return {"message": "Invalid filename"}, 400

        return send_from_directory("uploads/exports", safe_filename, as_attachment = True)
