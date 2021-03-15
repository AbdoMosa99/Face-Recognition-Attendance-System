from flask_restful import Resource, abort, reqparse
from flask import request
from app import db, api, models
from app.face_recog import FaceRecognition
import pickle

# make a request parser for attendance to validate arguments
attendance_args = reqparse.RequestParser()
attendance_args.add_argument("courseCode", type=str, required=True)
attendance_args.add_argument("lectureNUM", type=int, required=True)


# An attendace API that handles taking the attendance by images 
class Attendance(Resource):
    def get(self):
        attendance = models.Attendance.query.all()
        return attendance
    
    def post(self):
        try:
            # validate request arguments
            args = attendance_args.parse_args()
            
            # take form data into variables
            course_code = request.form["courseCode"]
            lecture_number = request.form["lectureNUM"]
            file = request.files["UploadImg"]
            
            # get the course object from the given course code,
            # and raise exception if the course code is invalid
            course = models.Course.query.filter(models.Course.code == course_code).one()
            
            # get students in the image from db through face recognition
            img = FaceRecognition.file2RGB(file)
            known_encodings_db = models.FaceEncoding.query.all()
            recognized_students = FaceRecognition.process_image(img, known_encodings_db)
            if not recognized_students:
                return {"message": "Sorry! We couldn't identify anyone."}, 204
            
            # mark their attendance in the database
            for recognized_student in recognized_students:
                attendance = models.Attendance(lecture_number = lecture_number,
                                               student = recognized_student["student"][0],
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
            # take form data into variables
            id = request.form["studentid"]
            name = request.form["fullname"]
            gender = request.form["gender"]
            email = request.form["email"]
            university_name = request.form["university"]
            faculty_name = request.form["faculty"]
            course_codes = request.form["courses"].split(",")
            file = request.files["uploadImg"]
            
            # get student face encoding
            img = FaceRecognition.file2RGB(file)
            encoding = FaceRecognition.get_encoding(img)
            
            # convert their face encoding into a pickle type for the db
            encoding_db = pickle.dumps(encoding)
            
            # get his faculty and university object from db 
            # and raise exception if not found
            university_faculty = models.UniversityFaculty.query.filter(
                models.Faculty.name == faculty_name 
                and models.University.name == models.University.name).one()
            
            # create a db face encoding object
            face_encoding = models.FaceEncoding(encoding = encoding_db)
            
            # get the list of courses they provided from db
            courses = [models.Course.query.filter(models.Course.code == course_code).one() 
                       for course_code in course_codes]
            
            # make the student object with all their information and add into the database
            student = models.Student(id = id, name = name, gender = gender, email = email,
                                     university_faculty = university_faculty,
                                     face_encoding = face_encoding)
            db.session.add(student)
            
            # commit and return a success message
            db.session.commit()
            return {"message": f"Student {name} Added Successfully"}, 201
            
        except:
            return {"message": "Invalid request!"}, 400
         
