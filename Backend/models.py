from extensions import db

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True)
    role=db.Column(db.String(255),nullable=False) # Admin, Company, Student

    #relationships
    company = db.relationship("Company", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)
    student = db.relationship("Student", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)
    admin = db.relationship("Admin", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)

class Company(db.Model):
    __tablename__='company'
    company_id=db.Column(db.Integer,db.ForeignKey('user.user_id'),primary_key=True)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String(355),nullable=False)
    gst_number = db.Column(db.String(30), unique=True,nullable=False)
    approval_status=db.Column(db.String(255),default='Pending') # Pending, Approved, Rejected
    hr_contact = db.Column(db.Text, nullable=False)
    website=db.Column(db.String(255),nullable=False)

    #Relationships
    user = db.relationship("User", back_populates="company", uselist=False)
    placement_drive = db.relationship("Placement_Drive", back_populates="company",cascade="all, delete-orphan",passive_deletes=True)

class Student(db.Model):
    __tablename__='student'
    student_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),primary_key=True)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String(355),nullable=False)
    department=db.Column(db.String(355),nullable=False)
    roll_no=db.Column(db.String(255),nullable=False)

    #Relationships
    user = db.relationship("User", back_populates="student", uselist=False)
    applications=db.relationship("Application",back_populates="student",cascade="all, delete-orphan",passive_deletes=True)

class Admin(db.Model):
    __tablename__='admin'
    admin_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),primary_key=True)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String(355), nullable=False)

    #Relationships
    user = db.relationship("User", back_populates="admin", uselist=False)

class Placement_Drive(db.Model):
    __tablename__="placement_drive"
    drive_id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey("company.company_id",ondelete="CASCADE"),nullable=False)
    job_title=db.Column(db.String(255),nullable=False)
    job_description=db.Column(db.Text,nullable=False)
    eligibility_criteria=db.Column(db.Text,nullable=False)
    application_deadline=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(255),default="Pending") #Pending, Approved, Closed

    #Relationships
    company=db.relationship("Company",back_populates="placement_drive")
    applications=db.relationship("Application",back_populates="placement_drive",cascade="all,delete-orphan",passive_deletes=True)


class Application(db.Model):         
    application_id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("student.student_id",ondelete="CASCADE"),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drive.drive_id",ondelete="CASCADE"),nullable=False)
    application_date=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(255),default='Applied')   #Applied / Shortlisted / Selected / Rejected

    #Relationships
    student=db.relationship("Student", back_populates="applications")
    placement_drive=db.relationship("Placement_Drive",back_populates="applications")

