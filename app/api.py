from flask_restful import Resource, abort, reqparse
from flask import request
from app import db, api, models
from app.face_recog import FaceRecognition
import pickle

attendance_args = reqparse.RequestParser()
attendance_args.add_argument("courseCode", type=str, required=True)
attendance_args.add_argument("lectureNUM", type=int, required=True)

class Attendance(Resource):
    def get(self):
        attendance = models.getAttendance()
        return attendance
    
    def post(self):
        try:
            args = attendance_args.parse_args()
            
            course_code = request.form["courseCode"]
            lecture_number = request.form["lectureNUM"]
            file = request.files["UploadImg"]

            course = models.Course.query.filter(models.Course.code == course_code).one()

            img = FaceRecognition.file2RGB(file)
            recognized_students = FaceRecognition.process_image(img)
            if not recognized_students:
                return {"message": "Sorry! We couldn't identify anyone."}, 204
            
            for recognized_student in recognized_students:
                attendance = models.Attendance(lecture_number = lecture_number,
                                               student = recognized_student["student"],
                                               course = course)
                db.session.add(attendance)
            
            db.session.commit()
            names = [student["student"].name for student in recognized_students]
            return {"message": f"Hey {names}! You have been successfuly submited."}, 201
        except:
            return {"message": "Invalid request!"}, 400

    
class Registration(Resource):
    def get(self):
        return "Hello"
        students = models.getStudents()
        return students

    def post(self):
        # try:
            id = request.form["studentid"]
            name = request.form["fullname"]
            gender = request.form["gender"]
            email = request.form["email"]
            university_name = request.form["university"]
            faculty_name = request.form["faculty"]
            course_codes = request.form["courses"].split(",")
            file = request.files["uploadImg"]
            
            img = FaceRecognition.file2RGB(file)
            encoding = FaceRecognition.get_encoding(img)
            encoding_db = pickle.dumps(encoding)
            
            university_faculty = models.UniversityFaculty.query.filter(
                models.Faculty.name == faculty_name 
                and models.University.name == models.University.name).one()
            face_encoding = models.FaceEncoding(encoding = encoding_db)
            
            courses = [models.Course.query.filter(models.Course.code == course_code).one() 
                       for course_code in course_codes]
            
            student = models.Student(id = id, name = name, gender = gender, email = email,
                                     university_faculty = university_faculty,
                                     face_encoding = face_encoding)
            
            db.session.add(student)
            db.session.commit()
            return {"message": f"Student {name} Added Successfully"}, 201
            
        # except:
            return {"message": "Invalid request!"}, 400
         

#api.add_resource(Attendance, '/api/attendance')
#api.add_resource(Registration, '/api/registration')
