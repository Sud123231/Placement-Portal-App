from datetime import datetime

from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from cache_utils import (
    cache_key_all_drives,
    cache_key_drive_applications,
    invalidate_all_student_applications_cache,
    invalidate_company_drives_cache,
    invalidate_drive_cache,
    invalidate_drive_applications_cache,
    invalidate_student_applied_drives_cache,
    invalidate_student_applications_cache,
)
from extensions import cache, db
from models import Application, Placement_Drive


class Drives(Resource):
    @jwt_required()
    def get(self):
        cache_key = cache_key_all_drives()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        drives = db.session.query(Placement_Drive).all()
        response = {"drives": [drive.to_dict() for drive in drives]}, 200
        cache.set(cache_key, response, timeout=60)
        return response

    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        required_fields = [
            "name",
            "application_deadline",
            "job_title",
            "eligibility_criteria",
            "salary",
            "location",
            "id",
        ]

        for field in required_fields:
            if not data.get(field):
                return {"message": f"{field} is required"}, 400

        application_deadline = datetime.strptime(
            data.get("application_deadline"),
            "%Y-%m-%d",
        ).date()
        min_cgpa = data.get("min_cgpa")
        if min_cgpa in (None, ""):
            min_cgpa = 0

        if application_deadline < datetime.now().date():
            return {"message": "Application deadline must be today or a future date"}, 400
        if min_cgpa < 0 or min_cgpa > 10:
            return {"message": "CGPA must be from 0 to 10"}, 400

        try:
            drive = Placement_Drive(
                name=data.get("name"),
                min_cgpa=min_cgpa,
                job_description=data.get("job_description"),
                job_title=data.get("job_title"),
                eligibility_criteria=data.get("eligibility_criteria"),
                application_deadline=application_deadline,
                salary=data.get("salary"),
                location=data.get("location"),
                company_id=data.get("id"),
            )
            db.session.add(drive)
            db.session.commit()

            invalidate_drive_cache()
            invalidate_company_drives_cache(drive.company_id)
            invalidate_drive_applications_cache(drive.drive_id)
            invalidate_all_student_applications_cache()
            return {"message": "drive created successfully"}, 201
        except Exception:
            db.session.rollback()
            return {"error": "Something went wrong"}, 500


class Drive(Resource):
    @jwt_required()
    def get(self, id):

        drive = db.session.query(Placement_Drive).filter_by(drive_id=id).first()
        if not drive:
            return {"message": "drive doesn't exist"}, 404

        response = {"drive": drive.to_dict()}, 200
        return response

    @jwt_required()
    def patch(self, id):
        data = request.get_json() or {}
        drive = db.session.query(Placement_Drive).filter_by(drive_id=id).first()
        if not drive:
            return {"message": "drive doesn't exist"}, 404

        if data.get("status") == "Cancelled":
            applications = db.session.query(Application).filter_by(drive_id=id).all()
            for application in applications:
                application.remark = "Drive Cancelled"
                invalidate_student_applications_cache(application.student_id)
                invalidate_student_applied_drives_cache(application.student_id)

        drive.status = data.get("status", drive.status)
        company_id = drive.company_id
        db.session.commit()
        invalidate_drive_cache(id)
        invalidate_company_drives_cache(company_id)
        invalidate_drive_applications_cache(id)
        invalidate_all_student_applications_cache()
        return {"drive": drive.to_dict()}, 200

    def put(self, id):
        data = request.get_json() or {}
        drive = db.session.query(Placement_Drive).filter_by(drive_id=id).first()
        if not drive:
            return {"message": "drive doesn't exist"}, 404

        drive.name = data.get("name", drive.name)
        drive.job_title = data.get("job_title", drive.job_title)
        drive.job_description = data.get("job_description", drive.job_description)
        drive.eligibility_criteria = data.get(
            "eligibility_criteria",
            drive.eligibility_criteria,
        )
        drive.salary = data.get("salary", drive.salary)
        drive.location = data.get("location", drive.location)
        applications = db.session.query(Application).filter_by(drive_id=id).all()
        for application in applications:
            invalidate_student_applications_cache(application.student_id)
            invalidate_student_applied_drives_cache(application.student_id)
        company_id = drive.company_id
        db.session.commit()

        invalidate_drive_cache(id)
        invalidate_company_drives_cache(company_id)
        invalidate_drive_applications_cache(id)
        invalidate_all_student_applications_cache()
        return {"drive": drive.to_dict()}, 200


class DriveApplications(Resource):
    @jwt_required()
    def get(self, id):
        cache_key = cache_key_drive_applications(id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        drive = db.session.query(Placement_Drive).filter_by(drive_id=id).first()
        if not drive:
            return {"message": "drive doesn't exist"}, 404

        applications = db.session.query(Application).filter_by(drive_id=id).all()
        response = {
            "applications": [application.to_dict() for application in applications],
            "job_title": drive.job_title,
        }, 200
        cache.set(cache_key, response, timeout=60)
        return response
