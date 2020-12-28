from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime

db = SQLAlchemy(app)

class Admin(db.Model):
    username = db.Column(db.String(45), primary_key=True)
    hashpass = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'admin {username} created'
    
class Log(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.now())
    activity = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'Faculty {name} created'
    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'University {name} created'
    
class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'Faculty {name} created'
    
class UniversityHasFaculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey(University.id), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey(Faculty.id), nullable=False)
    
    def __repr__(self):
        return f'University {university_id} has faculty {faculty_id}.'
    
class FaceEncoding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.String(2000), nullable=False)
    
    def __repr__(self):
        return f'Encoding {id} created'
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    fac_uni_id = db.Column(db.Integer, db.ForeignKey(UniversityHasFaculties.id), nullable=False)
    face_enc_id = db.Column(db.Integer, db.ForeignKey(FaceEncoding.id), nullable=False)
    
    def __repr__(self):
        return f'Student {name} added'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def __repr__(self):
        return f'Doctor {name} added'   
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    semester = db.Column(db.String(45), nullable=False)
    n_lectures = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id), nullable=False)
                            
    def __repr__(self):
        return f'Course {name} added for semester {semester}' 

class StudentEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
                            
    def __repr__(self):
        return f'Student {student_id} enrolled to course {course_id}' 
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now())
    lecture_number = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
                            
    def __repr__(self):
        return f'Student {student_id} attended course {course_id} lecture {lecture_number}' 
