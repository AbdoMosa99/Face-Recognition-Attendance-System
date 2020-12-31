import cv2
import numpy as np
import face_recognition
from datetime import datetime
from models import *


def file2RGB(fileObj):
    filestr = fileObj.read()
    npimg = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
    
def getEncoding(img):
    enc = face_recognition.face_encodings(img)
    return enc[0]

def register(name, img):
    enc = getEncoding(img)

def analyze(img):
    unknown_enc = getEncoding(img)
    encodings = FaceEncoding.query.all()
    now = datetime.now()
    
    for encc in encodings:
        enc = np.array(eval(encc.encoding))
        result = face_recognition.compare_faces([enc], unknown_enc)
        if result[0] == True:
            student = Student.query.filter(encc.id == Student.face_enc_id).first()
            if student:
                return student
            return None
    return None
    
    