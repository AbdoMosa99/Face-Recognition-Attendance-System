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
    
    def __repr__(self):
        return f'University {self.name} created'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'Faculty {self.name} created'


# Association Table for university-faculty many-to-many relationship
class UniversityFaculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey(University.id), nullable=False)
    university = db.relationship(University, backref="university_faculties")
    
    faculty_id = db.Column(db.Integer, db.ForeignKey(Faculty.id), nullable=False)
    faculty = db.relationship(Faculty, backref="university_faculties")
    
    def __repr__(self):
        return f'Faculty {self.faculty_id} added to University {self.university_id}'
    

# Doctors and Courses

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    
    university_faculty_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculty.id),
                                      nullable=False)
    university_faculty = db.relationship('UniversityFaculty', backref='doctors')
    
    def __repr__(self):
        return f'Doctor {self.name} added'   


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(255), nullable=False)
    n_lectures = db.Column(db.Integer, nullable=False)
    
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id), nullable=False)
    doctor = db.relationship('Doctor', backref='courses')
    
    university_faculty_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculty.id),
                                      nullable=False)
    university_faculty = db.relationship('UniversityFaculty', backref='courses')

    def __repr__(self):
        return f'Course {self.name} added for semester {self.semester}' 

    
# Student Related Tables

class FaceEncoding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.PickleType, nullable=False)
    
    def __repr__(self):
        return f'Encoding {self.id} created'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    university_faculty_id = db.Column(db.Integer,
                                      db.ForeignKey(UniversityFaculty.id),
                                      nullable=False)
    university_faculty = db.relationship('UniversityFaculty', backref='students')
    
    face_encoding_id = db.Column(db.Integer, 
                                 db.ForeignKey(FaceEncoding.id), 
                                 nullable=False)
    face_encoding = db.relationship('FaceEncoding', backref='student', uselist=False)
    
    def __repr__(self):
        return f'Student {self.name} added'


# Association Table for Student-Courses many-to-many relationship
class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    student = db.relationship('Student', backref='student_courses')
    
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    course = db.relationship('Course', backref='student_courses')
                            
    def __repr__(self):
        return f'Student {self.student_id} enrolled to course {self.course_id}' 


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now())
    lecture_number = db.Column(db.Integer, nullable=False)
    
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    student = db.relationship('Student', backref='attendances')
    
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    course = db.relationship('Course', backref='attendances')
                            
    def __repr__(self):
        return f'Student {self.student_id} attended course {self.course_id}' 
