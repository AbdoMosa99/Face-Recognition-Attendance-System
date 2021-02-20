import cv2
import numpy as np
import face_recognition
from imutils.video import WebcamVideoStream
from datetime import datetime
from app import models


def file2RGB(fileObj):
    filestr = fileObj.read()
    npimg = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
    
def getEncoding(img):
    enc = face_recognition.face_encodings(img)
    return enc[0]

def analyze(img):
    unknown_enc = models.getEncoding(img)
    encodings = models.FaceEncoding.query.all()
    now = datetime.now()
    
    for encc in encodings:
        enc = np.array(eval(encc.encoding))
        result = face_recognition.compare_faces([enc], unknown_enc)
        if result[0] == True:
            student = models.Student.query.filter(encc.id == models.Student.face_enc_id).first()
            if student:
                return student
            return None
    return None


def getImage(stream):
    image = stream.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def predict(img, known_encs_objs):
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    face_locs = face_recognition.face_locations(imgS)
    face_encs = face_recognition.face_encodings(imgS, face_locs)
    identified = False
    
    for (face_enc, face_loc) in zip(face_encs, face_locs):
        if identified:
            break
        for known_encs_obj in known_encs_objs:
            enc = np.array(eval(known_encs_obj.encoding))
            matches = face_recognition.compare_faces([enc], face_enc)
            if matches[0] == True:
                student = models.Student.query.filter(known_encs_obj.id == models.Student.face_enc_id).first()
                if student:
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y1), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, student.name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    models.addAttendance(1, "CS50", student.id)
                    identified = True
                    break 
                               
    return identified, img
    

def gen():
    stream = WebcamVideoStream(src=0).start()
    known_encs = models.FaceEncoding.query.all()
    done = False
    
    while True:
        if done:
            stream.stop()
            return "Success"
        image = getImage(stream)
        res, image = predict(image, known_encs)
        if res:
            done = True
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        