from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from cache_utils import (
    cache_key_all_companies,
    cache_key_company_applications,
    cache_key_company_drives,
    invalidate_company_drives_cache,
    invalidate_drive_cache,
)
from extensions import cache, db
from models import Company as CompanyModel, Placement_Drive


class Company(Resource):
    @jwt_required()
    def get(self, id):
        company = db.session.query(CompanyModel).filter_by(company_id=id).first()
        if not company:
            return {"message": "Company not found"}, 404

        return {"company": company.to_dict()}, 200

    @jwt_required()
    def patch(self, id):
        data = request.get_json() or {}
        company = db.session.query(CompanyModel).filter_by(company_id=id).first()
        if not company:
            return {"message": "Company not found"}, 404

        company.status = data.get("status", company.status)
        if company.status == "Blacklisted":
            drives = db.session.query(Placement_Drive).filter_by(company_id=id).all()
            for drive in drives:
                if drive.status == "Ongoing":
                    drive.status = "Cancelled"

        db.session.commit()
        invalidate_company_drives_cache(id)
        invalidate_drive_cache()
        return {"company": company.to_dict()}, 200


class Companies(Resource):
    @jwt_required()
    def get(self):
        cache_key = cache_key_all_companies()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        companies = db.session.query(CompanyModel).filter_by(status="Approved").all()
        response = {"companies": [company.to_dict() for company in companies]}, 200
        cache.set(cache_key, response, timeout=60)
        return response


class CompaniesApplications(Resource):
    @jwt_required()
    def get(self):
        cache_key = cache_key_company_applications()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        applications = db.session.query(CompanyModel).filter_by(status="Pending").all()
        response = {"companyapplications": [app.to_dict() for app in applications]}, 200
        cache.set(cache_key, response, timeout=60)
        return response


class CompanyDrives(Resource):
    def get(self, id):
        cache_key = cache_key_company_drives(id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        drives = db.session.query(Placement_Drive).filter_by(company_id=id).all()
        response = {"drives": [drive.to_dict() for drive in drives]}, 200
        cache.set(cache_key, response, timeout=60)
        return response
