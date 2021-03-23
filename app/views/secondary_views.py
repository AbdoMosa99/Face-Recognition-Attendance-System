from flask import render_template, redirect, url_for, Response
from app import app, socketio
from app.face_recog import FaceRecognition
from app import models
from flask_socketio import emit
import cv2
from PIL import Image
import io
import base64
import numpy as np


# Camera openning and face processing page
@app.route('/camfeed')
def cam_feed():
    return render_template("cam_feed.html")


# Live video feedback window
@app.route('/video_feed')
def video_feed():
    StreamProcessing.start()
    return Response(StreamProcessing.process(),
                    mimetype = 'multipart/x-mixed-replace; boundary=frame')


# Close Camera and stop processing
@app.route('/close_cam')
def close_cam():
    StreamProcessing.stop()
    return redirect('/')


# Handling Internal Errors
@app.errorhandler(500)
def error(e):
    return render_template('error.html'), 500


@socketio.on('image')
def image(data_image):    
    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    
    # Process the image frame
    # processing_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
    recognized_students = FaceRecognition.process_image(frame)

    # scale back up face locations as the processing frame was scaled to 1/4 size
#    for recognized_student in recognized_students:
#        recognized_student["location"] = (recognized_student["location"][0] * 4,
#                                          recognized_student["location"][1] * 4,
#                                          recognized_student["location"][2] * 4,
#                                          recognized_student["location"][3] * 4)

#        if recognized_student["student"] not in StreamProcessing.already_added_students:
#            attendance = models.Attendance(lecture_number = 3,
#                                      student = recognized_student["student"],
#                                      course_id = 1)
#            db.session.add(attendance)
#            db.session.commit()
#            already_added_students.append(recognized_student["student"])


    out_frame = FaceRecognition.represent_image(frame, recognized_students)
    
    
    imgencode = cv2.imencode('.jpg', out_frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)
