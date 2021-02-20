from app import db
from datetime import datetime


# Stand-alone Tables

class Admin(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'Admin {self.username} created'

    
class Log(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.now())
    activity = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'Log {self.activity} created'


# Universities and faculties
    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    faculties = db.relationship('UniversityFaculties', 
                                backref='university', lazy=True)
    
    def __repr__(self):
        return f'University {self.name} created'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    universities = db.relationship('UniversityFaculties', 
                                   backref='faculty', lazy=True)
    
    def __repr__(self):
        return f'Faculty {self.name} created'


# Association Table for university-faculty many-to-many relationship
class UniversityFaculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey(University.id), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey(Faculty.id), nullable=False)
    
    courses = db.relationship('Course', backref='faculty', lazy=True)
    doctors = db.relationship('Doctor', backref='faculty', lazy=True)
    students = db.relationship('Student', backref='faculty', lazy=True)
    
    def __repr__(self):
        return f'Faculty {self.faculty_id} added to University {self.university_id}'
    

# Doctors and Courses

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    
    faculty_university_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculties.id),
                                      nullable=False)
    
    courses = db.relationship('Course', backref='doctor', lazy=True)
    
    def __repr__(self):
        return f'Doctor {self.name} added'   


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(255), nullable=False)
    n_lectures = db.Column(db.Integer, nullable=False)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id), nullable=False)
    faculty_university_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculties.id),
                                      nullable=False)
    
    students = db.relationship('StudentCourses', backref='course', lazy=True)
    attendances = db.relationship('Attendance', backref='course', lazy=True)

    def __repr__(self):
        return f'Course {self.name} added for semester {self.semester}' 

    
# Student Related Tables

class FaceEncoding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.PickleType, nullable=False)
    
    student = db.relationship('Student', backref='face_encoding', 
                              uselist=False, lazy=True)
    
    def __repr__(self):
        return f'Encoding {self.id} created'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    faculty_university_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculties.id),
                                      nullable=False)
    face_encoding_id = db.Column(db.Integer, 
                                 db.ForeignKey(FaceEncoding.id), 
                                 nullable=False)
    
    courses = db.relationship('StudentCourses', backref='student', lazy=True)
    attendances = db.relationship('Attendance', backref='student', lazy=True)
    
    def __repr__(self):
        return f'Student {self.name} added'


# Association Table for Student-Courses many-to-many relationship
class StudentCourses(db.Model):
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
        return f'Student {self.student_id} attended course {self.course_id}' 
