from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import Admin, Company, Student as StudentModel, User


class UserRegistration(Resource):
    def post(self):
        data = request.get_json() or {}
        role = data.get("role")

        if role == "Student":
            roll_no = data.get("roll_no")
            existing_student = db.session.query(StudentModel).filter_by(roll_no=roll_no).first()
            if existing_student:
                return {"message": "user already exists"}, 409

            password = generate_password_hash(data.get("password"))
            cgpa = data.get("cgpa", 0)
            if cgpa < 0 or cgpa > 10:
                return {"message": "CGPA must be from 0 to 10"}, 400

            try:
                new_user = User(
                    role=role,
                    email=data.get("email"),
                    password=password,
                )
                db.session.add(new_user)
                db.session.flush()

                new_student = StudentModel(
                    student_id=new_user.user_id,
                    name=data.get("name"),
                    department=data.get("department"),
                    roll_no=roll_no,
                    cgpa=cgpa,
                )
                db.session.add(new_student)
                db.session.commit()
                return {"message": "user created successfully"}, 201
            except Exception as exc:
                print(exc)
                db.session.rollback()
                return {"message": str(exc)}, 500

        if role == "Company":
            gst_number = data.get("gst_number")
            existing_company = db.session.query(Company).filter_by(gst_number=gst_number).first()
            if existing_company:
                return {"message": "company already exists"}, 409

            password = generate_password_hash(data.get("password"))
            try:
                new_user = User(
                    role=role,
                    email=data.get("email"),
                    password=password,
                )
                db.session.add(new_user)
                db.session.flush()

                new_company = Company(
                    company_id=new_user.user_id,
                    gst_number=gst_number,
                    name=data.get("name"),
                    hr_contact=data.get("hr_contact"),
                    description=data.get("description"),
                )
                db.session.add(new_company)
                db.session.commit()
                return {"message": "user created successfully"}, 201
            except Exception as exc:
                print(exc)
                db.session.rollback()
                return {"message": "Something went wrong"}, 500

        return {"message": "bad request"}, 400


class UserLogin(Resource):
    def post(self):
        data = request.get_json() or {}
        role = data.get("role")
        password = data.get("password")

        if role == "Student":
            roll_no = data.get("roll_no")
            if not roll_no or not password:
                return {"message": "roll_no and password are required"}, 400

            student = db.session.query(StudentModel).filter_by(roll_no=roll_no).first()
            if not student:
                return {"message": "user not found"}, 404
            if student.status == "Blacklisted":
                return {"message": "you are not allowed for login"}, 403
            if not student.user:
                return {"message": "user account is not linked"}, 500
            if not check_password_hash(student.user.password, password):
                return {"message": "invalid credentials"}, 401

            token = create_access_token(identity=str(student.student_id))
            return {"role": "Student", "token": token, "id": student.student_id}

        if role == "Company":
            gst_number = data.get("gst_number")
            if not gst_number or not password:
                return {"message": "gst_number and password are required"}, 400

            company = db.session.query(Company).filter_by(gst_number=gst_number).first()
            if not company:
                return {"message": "company not found"}, 404
            if company.status == "Blacklisted":
                return {"message": "you are not allowed for login"}, 403
            if company.status == "Pending":
                return {"message": "Your approval pending"}, 403
            if not company.user:
                return {"message": "user account is not linked"}, 500
            if not check_password_hash(company.user.password, password):
                return {"message": "invalid credentials"}, 401

            token = create_access_token(identity=str(company.company_id))
            return {"role": "Company", "token": token, "id": company.company_id}

        if role != "Admin":
            return {"message": "invalid role"}, 400

        email = data.get("email")
        if not email or not password:
            return {"message": "email and password are required"}, 400

        user = db.session.query(User).filter_by(email = email, role = "Admin").first()
        if not user:
            return {"message": "admin not found"}, 404
        
        if not check_password_hash(user.password, password):
            return {"message": "invalid credentials"}, 401

        token = create_access_token(identity=str(user.user_id))
        return {"role": "Admin", "token": token, "id": user.user_id}
