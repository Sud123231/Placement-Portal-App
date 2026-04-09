from extensions import db

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(255),nullable=False) # Admin, Company, Student

    #relationships
    company = db.relationship("Company", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)
    student = db.relationship("Student", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)
    admin = db.relationship("Admin", back_populates="user", uselist=False,cascade="all, delete-orphan",passive_deletes=True)

class Company(db.Model):
    __tablename__='company'
    company_id=db.Column(db.Integer,db.ForeignKey('user.user_id', ondelete="CASCADE"),primary_key=True)
    name=db.Column(db.String(355),nullable=False)
    gst_number = db.Column(db.String(30), unique=True,nullable=False)
    description=db.Column(db.Text,nullable=True)
    status=db.Column(db.String(255),default='Pending') # Pending/Approved/Rejected/Blacklisted
    hr_contact = db.Column(db.Text, nullable=False)

    #Relationships
    user = db.relationship("User", back_populates="company", uselist=False)
    placement_drive = db.relationship("Placement_Drive", back_populates="company",cascade="all, delete-orphan",passive_deletes=True)
    def to_dict(self):
        return {
            "id": self.company_id,
            "description":self.description,
            "name": self.name,
            "gst_number": self.gst_number,
            "hr_contact": self.hr_contact,
            "status":self.status
        }

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), primary_key = True)
    name = db.Column(db.String(355), nullable = False)
    roll_no = db.Column(db.String(255), nullable = False)
    department = db.Column(db.String(355), nullable = False)
    cgpa = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(255), default = "Active") # Active/Blacklisted

    #Relationships
    user = db.relationship("User", back_populates = "student", uselist = False)
    applications=db.relationship("Application", back_populates = "student", cascade = "all, delete-orphan", passive_deletes = True)
    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "status": self.status,
            "department": self.department,
            "roll_no": self.roll_no,
            "cgpa": self.cgpa
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), primary_key = True)
    name = db.Column(db.String(355), nullable = False)

    #Relationships
    user = db.relationship("User", back_populates = "admin", uselist = False)

class Placement_Drive(db.Model):
    __tablename__ = "placement_drive"
    drive_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(355), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id", ondelete = "CASCADE"), nullable = False)
    job_title = db.Column(db.String(255), nullable = False)
    job_description = db.Column(db.Text, nullable = False)
    min_cgpa = db.Column(db.Integer, nullable = False)
    eligibility_criteria = db.Column(db.Text, nullable = False)
    application_deadline = db.Column(db.Date, nullable = False)
    salary = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String(355), nullable = False)
    status = db.Column(db.String(255), default = "Ongoing") #Ongoing, Completed, Cancelled

    #Relationships
    company = db.relationship("Company", back_populates = "placement_drive")
    applications = db.relationship("Application", back_populates = "placement_drive", cascade = "all,delete-orphan", passive_deletes = True)
    def to_dict(self):
        return {
            "id": self.drive_id,
            "name": self.name,
            "company_id": self.company_id,
            "company_name":self.company.name,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "location": self.location,
            "salary":self.salary,
            "eligibility_criteria":self.eligibility_criteria,
            "deadline":str(self.application_deadline),
            "status":self.status,
            "min_cgpa": self.min_cgpa
        }


class Application(db.Model):         
    application_id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("student.student_id",ondelete="CASCADE"),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drive.drive_id",ondelete="CASCADE"),nullable=False)
    application_date=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(255),default='Applied')   #Applied / Shortlisted / Selected / Rejected
    resume = db.Column(db.String(500), nullable=True)  
    remark=db.Column(db.Text,default='None', nullable=True)

    #Relationships
    student=db.relationship("Student", back_populates="applications")
    placement_drive=db.relationship("Placement_Drive", back_populates="applications")
    def to_dict(self):
        return{           
            "id": self.application_id,
            "drive_id":self.placement_drive.drive_id,
            "drive": self.placement_drive.name,
            "student_name":self.student.name,
            "company": self.placement_drive.company.name,
            "date": self.application_date.strftime('%d/%m/%Y'),
            "status":self.status,
            "resume_url": self.resume,
            "job_title": self.placement_drive.job_title, 
            'remark':self.remark       
        }

