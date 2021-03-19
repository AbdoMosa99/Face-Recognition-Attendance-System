from flask_restful import Resource, abort
from flask import request
from app import db, models
from app.face_recog import FaceRecognition
from app.forms import AttendanceForm, RegistrationForm
from app.services import add_log
import pickle


# An attendace API that handles taking the attendance by images 
class Attendance(Resource):
    def get(self):
        attendance = models.Attendance.query.all()
        return attendance
    
    def post(self):
        try:
            form = AttendanceForm()

            # get the course object from the given course code,
            # and raise exception if the course code is invalid
            course = models.Course.query.filter(models.Course.code == form.course_code.data).one()
            
            # get students in the image from db through face recognition
            img = FaceRecognition.file2RGB(form.uploaded_file.data)
            recognized_students = FaceRecognition.process_image(img)
            if not recognized_students:
                add_log(f"There has been a failed attempt of attendance due to no identified students in the image.")
                return {"message": "Sorry! We couldn't identify anyone."}
            
            # mark their attendance in the database
            for recognized_student in recognized_students:
                attendance = models.Attendance(lecture_number = form.lecture_number.data,
                                               student = recognized_student["student"],
                                               course = course)
                db.session.add(attendance)
            
            # Commit Changes and getting students names
            names = [student["student"].name for student in recognized_students]
            db.session.commit()
            
            # Adding success logs
            add_log(f"{names} have made a successful attendance to {course.name}.")
                        
            return {"message": f"Hey {names}! You have been successfuly submited."}, 201
        
        except Exception as e:
            add_log(f"There has been a failed attempt of attendance with the exception {e}.")
            return {"message": "Invalid request!"}, 400


    
# A registration API that handles registering students faces and info into the database 
class Registration(Resource):
    def get(self):
        students = models.Student.query.all()
        return students

    def post(self):
        try:
            form = RegistrationForm()
               
            course_codes = form.courses_codes.data.split(",")
            
            # get student face encoding
            img = FaceRecognition.file2RGB(form.uploaded_file.data)
            encoding = FaceRecognition.get_encoding(img)
            
            # convert their face encoding into a pickle type for the db
            encoding_db = pickle.dumps(encoding)
            
            # get his faculty and university object from db 
            # and raise exception if not found
            university_faculty = models.UniversityFaculty.query.filter(
                models.Faculty.name == form.faculty_name.data 
                and models.University.name == form.university_name.data).one()
            
            # create a db face encoding object
            face_encoding = models.FaceEncoding(encoding = encoding_db)
            
            # get the list of courses they provided from db
            courses = [models.Course.query.filter(models.Course.code == course_code).one() 
                       for course_code in course_codes]
            
            # make the student object with all their information and add into the database
            student = models.Student(id = form.student_id.data, name = form.full_name.data,
                                     gender = form.gender.data, email = form.email.data,
                                     university_faculty = university_faculty,
                                     face_encoding = face_encoding)
            db.session.add(student)
            db.session.commit()
            
            # Adding to logs and return
            add_log(f"{form.full_name.data} has made a successful registration.")
            return {"message": f"Student {form.full_name.data} Added Successfully"}, 201
            
        except Exception as e:
            add_log(f"There has been a failed attempt of registration with the exception {e}.")
            return {"message": "Invalid request!"}, 400
         
