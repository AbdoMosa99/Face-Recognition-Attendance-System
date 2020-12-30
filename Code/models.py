from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from app import app
from datetime import datetime

db = SQLAlchemy(app)

class Admin(db.Model):
    username = db.Column(db.String(45), primary_key=True)
    hashpass = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'Admin: username({self.username}), hash({self.hashpass})'
    
class Log(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.now())
    activity = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'Faculty {self.activity} created'
    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'University {self.name} created'
    
class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'Faculty {self.name} created'
    
class UniversityHasFaculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey(University.id), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey(Faculty.id), nullable=False)
    
    def __repr__(self):
        return f'University {self.university_id} has faculty {self.faculty_id}.'
    
class   FaceEncoding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.String(4000), nullable=False)
    
    def __repr__(self):
        return f'Encoding {self.id} created'
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    fac_uni_id = db.Column(db.Integer, db.ForeignKey(UniversityHasFaculties.id), nullable=False)
    face_enc_id = db.Column(db.Integer, db.ForeignKey(FaceEncoding.id), nullable=False)
    
    def __repr__(self):
        return f'Student {self.name} added'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'Doctor {self.name} added'   
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    semester = db.Column(db.String(45), nullable=False)
    n_lectures = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id), nullable=False)
                            
    def __repr__(self):
        return f'Course {self.name} added for semester {self.semester}' 

class StudentEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
                            
    def __repr__(self):
        return f'Student {self.student_id} enrolled to course {self.course_id}' 
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now())
    lecture_number = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
                            
    def __repr__(self):
        return f'Student {self.student_id} attended course {self.course_id} lecture {self.lecture_number}' 

    
# Functions 

def addStudent(name, gender, email, university, faculty, courses, face_enc):
    faculty = Faculty.query.filter(Faculty.name == faculty).first()
    university = University.query.filter(University.name == university).first()
    fac_uni = UniversityHasFaculties.query.filter(and_(UniversityHasFaculties.university_id == university.id, UniversityHasFaculties.faculty_id == faculty.id)).first()
    
    encoding = FaceEncoding(encoding=str(face_enc.tolist()))
    db.session.add(encoding)
    db.session.commit()
    encoding = FaceEncoding.query.order_by(FaceEncoding.id.desc()).first()
    student = Student(name=name, gender=gender, email=email, face_enc_id=encoding.id, fac_uni_id=fac_uni.id)
    
    # db.session.add(encoding)
    db.session.add(student)
    
    db.session.commit()

def addFaculty(fac, uni):
    university = University.query.filter(University.name == uni).first()
    if not university:
        university = University(name=uni)
        db.session.add(university)
        
    faculty = Faculty.query.filter(Faculty.name == fac).first()
    if not faculty:
        faculty = Faculty(name=fac)
        db.session.add(faculty)
        
    uni_fac = UniversityHasFaculties.query.filter(and_(university.id == UniversityHasFaculties.university_id, faculty.id == UniversityHasFaculties.faculty_id)).first()
    if not uni_fac:
        uni_fac = UniversityHasFaculties(university_id=university.id, faculty_id=faculty.id)
        db.session.add(uni_fac)
                                                  
    db.session.commit()
        
        
        
        
        
        
        
        
        
    
    