from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from cache_utils import (
    invalidate_all_student_applications_cache,
    invalidate_drive_applications_cache,
    invalidate_student_applications_cache,
)
from extensions import db
from models import Application as ApplicationModel


class Application(Resource):
    @jwt_required()
    def get(self, id):
        if id is None:
            return {"message": "id not provided"}, 400

        application = db.session.query(ApplicationModel).filter_by(application_id=id).first()
        if not application:
            return {"message": "application not found"}, 404

        return {
            "name": application.student.name,
            "status": application.status,
            "department": application.student.department,
            "drive": application.placement_drive.name,
            "job_title": application.placement_drive.job_title,
        }, 200

    @jwt_required()
    def patch(self, id):
        data = request.get_json() or {}
        application = db.session.query(ApplicationModel).filter_by(application_id=id).first()
        if not application:
            return {"message": "application not found"}, 404

        application.status = data.get("status", application.status)
        drive_id = application.drive_id
        student_id = application.student_id
        db.session.commit()
        invalidate_drive_applications_cache(drive_id)
        invalidate_student_applications_cache(student_id)
        invalidate_all_student_applications_cache()
        return {"application": application.to_dict()}, 200
