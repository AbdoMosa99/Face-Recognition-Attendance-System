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
    pass


api.add_resource(Attendance, '/api/attendance')
