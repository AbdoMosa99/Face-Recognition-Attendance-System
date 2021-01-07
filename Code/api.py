from flask_restful import Resource, abort, reqparse
from flask import request
from app import api
import models
import face_recog

attendance_args = reqparse.RequestParser()
attendance_args.add_argument("courseCode", type=str, required=True)
attendance_args.add_argument("lectureNUM", type=int, required=True)

class Attendance(Resource):
    def get(self):
        attendance = models.getAttendance()
        return attendance
    
    def post(self):
        args = attendance_args.parse_args()
        if request.files:
            course_code = request.form['courseCode']
            lec_n = request.form['lectureNUM']
            file = request.files["UploadImg"]
            
            img = face_recog.file2RGB(file)
            res = face_recog.analyze(img)
            if res:
                x = models.addAttendance(lec_n, course_code, res.id)
                if not x:
                    return {"message": "Bad Request"}, 400
                
                return {"message": f"{res.name}"}, 201
            else:
                return {"message": "Could Not Identify"}, 204
        return {"message": "Bad Request"}, 400
    
class Registration(Resource):
    def get(self):
        students = models.getStudents()
        return students

    def post(self):
        id = request.form["studentid"]
        name = request.form["fullname"]
        gender = request.form["gender"]
        email = request.form["email"]
        university = request.form["university"]
        faculty = request.form["faculty"]
        courses = request.form["courses"]
        file = request.files['uploadImg']

        img = face_recog.file2RGB(file)
        enc = face_recog.getEncoding(img)
        face_enc = str(enc.tolist())
        courses = courses.split(',')

        s = models.addStudent(id, name, gender, email, university, faculty, courses, face_enc)
        if not s:
            return {"message": "Bad Request"}, 400
        return {"message": f"{s.name}"}, 201 

api.add_resource(Attendance, '/api/attendance')
api.add_resource(Registration, '/api/registration')