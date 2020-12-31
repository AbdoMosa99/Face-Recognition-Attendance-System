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
    
class FaceEncoding(db.Model):
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
    code = db.Column(db.String(10), nullable=False, unique=True)
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

#===== Functions ======

def addStudent(id, name, gender, email, university, faculty, courses, face_enc):
    faculty = Faculty.query.filter(Faculty.name == faculty).first()
    if not faculty:
        return None
    
    university = University.query.filter(University.name == university).first()
    if not university:
        return None
    
    fac_uni = UniversityHasFaculties.query.filter(and_(UniversityHasFaculties.university_id == university.id, UniversityHasFaculties.faculty_id == faculty.id)).first()
    if not fac_uni:
        return None
    
    encoding = FaceEncoding(encoding=face_enc)
    db.session.add(encoding)
    db.session.flush()
    
    student = Student(id=id, name=name, gender=gender, email=email, face_enc_id=encoding.id, fac_uni_id=fac_uni.id)
    db.session.add(student)
    db.session.flush()
    
    for course_code in courses:
        course = Course.query.filter(Course.code == course_code).first()
        if not course:
            continue
        
        student_courses = StudentEnrollment(student_id=student.id, course_id=course.id)
        db.session.add(student_courses)
    
    db.session.commit()
    return student.id

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
    return uni_fac.id
        
def addDoctor(name):
    doctor = Doctor.query.filter(Doctor.name == name).first()
    if not doctor:
        doctor = Doctor(name=name)
        db.session.add(doctor)
    
    db.session.commit()
    return doctor.id

def addCourse(code, name, semester, n_lectures, doctorName):
    doctor = Doctor.query.filter(Doctor.name == doctorName).first()
    if not doctor: 
        return None
    
    course = Course(code=code, name=name, semester=semester, n_lectures=n_lectures, doctor_id=doctor.id)
    db.session.add(course)

    db.session.commit()
    return course.id

def addAttendance(lecture_number, student_id, course_id):
    attendance = Attendance(time=datetime.now(), lecture_number=lecture_number,student_id=student_id, course_id=course_id)
    db.session.add(attendance)

    db.session.commit()

def addLog(activity):
    log = Log(time=datetime.now(), activity=activity)
    db.session.add(log)
    db.session.commit()
    
    
# Update Functions

def updateStudent(name, gender, email, university, faculty, courses, id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return None
    
    student.name = name
    student.gender = gender
    student.email = email
    student.courses = courses

    faculty = Faculty.query.filter(Faculty.name == faculty).first()
    if not faculty:
        return None
        
    university = University.query.filter(University.name == university).first()
    if not university:
        return None
    
    fac_uni = UniversityHasFaculties.query.filter(and_(UniversityHasFaculties.university_id == university.id, UniversityHasFaculties.faculty_id == faculty.id)).first()
    if not fac_uni:
        return None
    
    student.fac_uni_id = fac_uni.id

    db.session.commit()
    return id

def updateCourse(code, name, semester, n_lectures, doctorName, id):
    course = Course.query.filter(Course.id == id).first()
    doctor = Doctor.query.filter(Doctor.name == doctorName).first()
    
    course.code = code
    course.name = name
    course.semester = semester
    course.n_lectures = n_lectures
    course.doctor_id = doctor.id
 
    db.session.commit()

# Deleting Functions

def deleteStudent(id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return None
    
    FaceEncoding.query.filter(FaceEncoding.id == student.face_enc_id).delete()
    Student.query.filter(Student.id == id).delete()
    db.session.commit()
    return id

def deleteFaculty(id):
    uni_fac = UniversityHasFaculties.query.filter(UniversityHasFaculties.id == id).delete()
    db.session.commit()
    return id

def deleteCourse(id):
    Course.query.filter(Course.id == id).delete()
    db.session.commit()
    return id

def deleteDoctor(id):  
    Doctor.query.filter(Doctor.id == id).delete()
    db.session.commit()
    return id
    
# Getting Functions


def getStudents():
    studentObjs = Student.query.all()
    students = []
    
    for studentObj in studentObjs:        
        fac_uni = UniversityHasFaculties.query.filter(UniversityHasFaculties.id == studentObj.fac_uni_id).first()
        faculty = Faculty.query.filter(Faculty.id == fac_uni.faculty_id).first()
        university = University.query.filter(University.id == fac_uni.university_id).first()
        
        student = {}
        student["id"] = studentObj.id
        student["name"] = studentObj.name
        student["gender"] = studentObj.gender
        student["email"] = studentObj.email
        student["university"] = university.name
        student["faculty"] = faculty.name
        # student["courses"] = studentObj.courses
        
        students.append(student)
    return students

def getFaculties():
    fac_uni_objs = UniversityHasFaculties.query.all()
    faculties = []
    
    for fac_uni_obj in fac_uni_objs:        
        faculty = Faculty.query.filter(Faculty.id == fac_uni_obj.faculty_id).first()
        university = University.query.filter(University.id == fac_uni_obj.university_id).first()
        
        fac_uni = {}
        fac_uni["id"] = fac_uni_obj.id
        fac_uni["faculty"] = faculty.name
        fac_uni["university"] = university.name
        
        faculties.append(fac_uni)
        
    return faculties

def getDoctors():
    doctor_objs = Doctor.query.all()
    doctors = []
    
    for doctor_obj in doctor_objs:        
        doctor = {}
        doctor["id"] = doctor_obj.id
        doctor["name"] = doctor_obj.name
        
        doctors.append(doctor)
        
    return doctors
def getCourses():
    course_objs = Course.query.all()
    courses = []
    
    for course_obj in course_objs:
        doctor = Doctor.query.filter(Doctor.id == course_obj.doctor_id).first()
        
        course = {}
        course["id"] = course_obj.id
        course["name"] = course_obj.name
        course["semester"] = course_obj.semester
        course["n_lectures"] = course_obj.n_lectures
        course["doctor"] = doctor.name
        
        courses.append(course)
        
    return courses

def getAttendance():
    attendace_objs = Attendance.query.all()
    attendances = []
    
    for attendace_obj in attendace_objs:
        student = Student.query.filter(Student.id == attendace_obj.student_id).first()
        course = Course.query.filter(Course.id == attendace_obj.course_id).first()
        
        attendance = {}
        attendance["id"] = attendace_obj.id
        attendance["time"] = attendace_obj.time
        attendance["student"] = student.name
        attendance["course"] = course.name
        attendance["lecture_number"] = attendace_obj.lecture_number
        
        attendances.append(attendance)
        
    return attendances
        