import cv2
import numpy as np
import face_recognition
import pickle
from imutils.video import WebcamVideoStream
from datetime import datetime
from app import models


class FaceRecognition():
    
    def file2RGB(file):
        """A function that convert uploaded file (jpg, png, etc.) to cv2 RGB image."""
        filestr = file.read()
        np_arr = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb

    
    def get_encoding(img):
        """A function that takes an RGB image,
        and returns the face encoding of the first face in it."""
        
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            raise Exception("No faces found in the image")
            
        return encodings[0]

    
    def process_image(img):
        """A function that takes an RGB image,
        and returns the students in it with their face locations."""
        recognized_students = []
        
        face_locations = face_recognition.face_locations(img)
        unknown_encodings = face_recognition.face_encodings(img, face_locations)

        known_encodings_db = models.FaceEncoding.query.all()
        known_encodings = list(map(
            lambda enc: pickle.loads(enc.encoding),
            known_encodings_db))
        
        for unknown_encoding in unknown_encodings:
            matches = face_recognition.compare_faces(known_encodings, unknown_encoding)

            if True in matches:
                first_match_index = matches.index(True)               
                recognized_students.append({
                    "student": known_encodings_db[first_match_index].student,
                    "location": face_locations[first_match_index]
                })

        return recognized_students
    
    
    def represent_image(img, recognized_students):
        """A function that takes a frame from the video or live camera,
        And processes it to get """
        
        for recognized_student in recognized_students:
            top, right, bottom, left = recognized_student["location"]
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            
            cv2.rectangle(img, (left, bottom - 35), (right, bottom),
                          (0, 0, 255), cv2.FILLED)
            cv2.putText(img, recognized_student["student"].name, 
                        (left + 6, right - 6), cv2.FONT_HERSHEY_DUPLEX,
                        1.0, (255, 255, 255), 1)

        return img


class StreamProcessing():
    stream = None
    running = False
    
    def get_frame(stream):
        image = stream.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def gen():
        stream = WebcamVideoStream(src=0).start()
        known_encs = models.FaceEncoding.query.all()

        while True:
            frame = stream.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            recognized_students = FaceRecognition.process_image(frame)
            out_frame = FaceRecognition.represent_image(frame, recognized_students)
            ret, jpeg = cv2.imencode('.jpg', out_frame)
            out_frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + out_frame + b'\r\n\r\n')

        