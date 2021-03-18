from flask_restful import Resource, abort
from flask import request
from app import db, api, models
from app.face_recog import FaceRecognition
from app.forms import AttendanceForm, RegistrationForm
import pickle


# An attendace API that handles taking the attendance by images 
class Attendance(Resource):
    def get(self):
        attendance = models.Attendance.query.all()
        return attendance
    
    def post(self):
        try:
            form = AttendanceForm()
            if not form.validate():
                raise Exception("Invalid Form")
            
            # get the course object from the given course code,
            # and raise exception if the course code is invalid
            course = models.Course.query.filter(models.Course.code == form.course_code).one()
            
            # get students in the image from db through face recognition
            img = FaceRecognition.file2RGB(form.uploaded_file)
            known_encodings_db = models.FaceEncoding.query.all()
            recognized_students = FaceRecognition.process_image(img, known_encodings_db)
            if not recognized_students:
                return {"message": "Sorry! We couldn't identify anyone."}, 204
            
            # mark their attendance in the database
            for recognized_student in recognized_students:
                attendance = models.Attendance(lecture_number = form.lecture_number,
                                               student = recognized_student["student"],
                                               course = course)
                db.session.add(attendance)
            
            # commit and send a message with their names
            db.session.commit()
            names = [student["student"].name for student in recognized_students]
            return {"message": f"Hey {names}! You have been successfuly submited."}, 201
        
        except:
            return {"message": "Invalid request!"}, 400


    
# A registration API that handles registering students faces and info into the database 
class Registration(Resource):
    def get(self):
        students = models.Student.query.all()
        return students

    def post(self):
        try:
            form = RegistrationForm()
            if not form.validate():
                raise Exception("Invalid Form")
                
            course_codes = form.course_codes.split(",")
            
            # get student face encoding
            img = FaceRecognition.file2RGB(form.uploaded_file)
            encoding = FaceRecognition.get_encoding(img)
            
            # convert their face encoding into a pickle type for the db
            encoding_db = pickle.dumps(encoding)
            
            # get his faculty and university object from db 
            # and raise exception if not found
            university_faculty = models.UniversityFaculty.query.filter(
                models.Faculty.id == form.faculty_id 
                and models.University.id == form.university_id).one()
            
            # create a db face encoding object
            face_encoding = models.FaceEncoding(encoding = encoding_db)
            
            # get the list of courses they provided from db
            courses = [models.Course.query.filter(models.Course.code == course_code).one() 
                       for course_code in course_codes]
            
            # make the student object with all their information and add into the database
            student = models.Student(id = form.student_id, name = form.full_name,
                                     gender = form.gender, email = form.email,
                                     university_faculty = university_faculty,
                                     face_encoding = face_encoding)
            db.session.add(student)
            
            # commit and return a success message
            db.session.commit()
            return {"message": f"Student {name} Added Successfully"}, 201
            
        except:
            return {"message": "Invalid request!"}, 400
         
