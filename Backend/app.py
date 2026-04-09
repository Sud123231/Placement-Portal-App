import sqlite3

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from kombu.exceptions import OperationalError
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.security import generate_password_hash

from config import Config
from extensions import cache, celery, db, jwt, mail, migrate
from models import Admin, User
from routes.Application import Application
from routes.auth import UserLogin, UserRegistration
from routes.company import Companies, CompaniesApplications, Company, CompanyDrives
from routes.drive import Drive, DriveApplications, Drives
from routes.student import (
    AllStudentsApplications,
    ApplicationResume,
    ExportDownload,
    ExportStatus,
    ExportStudentApplications,
    Student,
    StudentApplications,
    StudentAppliedDrives,
    Students,
)

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cache.init_app(app)
mail.init_app(app)

celery.conf.update(
    broker_url=app.config["BROKER_URL"],
    result_backend=app.config["RESULT_BACKEND"],
    beat_schedule=app.config["BEAT_SCHEDULE"],
)


class ContextTask(celery.Task):
    """Make Celery tasks run inside the Flask app context."""

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@event.listens_for(Engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.close()


def seed_admin():
    """Adding the admin user if not already present."""
    if User.query.filter_by(role="Admin").first():
        return

    user = User(
        role="Admin",
        email="dummyemail",
        password=generate_password_hash("admin123"),
    )
    db.session.add(user)
    db.session.flush()
    db.session.add(Admin(name="Admin", admin_id=user.user_id))
    db.session.commit()


def register_resources(api_instance):
    api_instance.add_resource(UserRegistration, "/api/auth/register")
    api_instance.add_resource(UserLogin, "/api/auth/login")

    api_instance.add_resource(Companies, "/api/companies")
    api_instance.add_resource(Company, "/api/companies/<int:id>")

    api_instance.add_resource(Students, "/api/students")
    api_instance.add_resource(Student, "/api/students/<int:id>")

    api_instance.add_resource(Drives, "/api/drives")
    api_instance.add_resource(Drive, "/api/drives/<int:id>")
    api_instance.add_resource(CompanyDrives, "/api/companies/<int:id>/drives")
    api_instance.add_resource(StudentAppliedDrives, "/api/students/<int:id>/drives")

    api_instance.add_resource(AllStudentsApplications, "/api/students/applications")
    api_instance.add_resource(StudentApplications, "/api/students/<int:student_id>/applications")
    api_instance.add_resource(ApplicationResume, "/api/students/applications/<int:id>/resume")
    api_instance.add_resource(CompaniesApplications, "/api/companies/applications")
    api_instance.add_resource(DriveApplications, "/api/drives/<int:id>/applications")
    api_instance.add_resource(Application, "/api/applications/<int:id>")

    api_instance.add_resource(ExportStudentApplications, "/api/students/<int:student_id>/export-applications")
    api_instance.add_resource(ExportStatus, "/api/export-status/<task_id>")
    api_instance.add_resource(ExportDownload, "/api/exports/<path:filename>")


with app.app_context():   
    #db.create_all()
    seed_admin()
    # query to inject dummy email to admin row
    """"" 
    user =db.session.query(User).filter_by(role="Admin").first()
    if user:
        user.email = "dummyemail"
        db.session.commit()
    """  

register_resources(api)


if __name__ == "__main__":
    app.run(debug=True)
