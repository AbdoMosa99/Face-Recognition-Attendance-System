import cv2
import numpy as np
import face_recognition
from datetime import datetime

encodings_DB = []
attendace_DB = []

def convertImg(fileObj):
    filestr = fileObj.read()
    npimg = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img
    

def getEncodings(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    enc = face_recognition.face_encodings(img)
    return enc[0]

def register(name, img):
    enc = getEncodings(img)
    encodings_DB.append((name, enc))

def analyze(img):
    unknown_enc = getEncodings(img)
    now = datetime.now()
    for name, enc in encodings_DB:
        result = face_recognition.compare_faces([enc], unknown_enc)
        if result[0] == True:
            attendace_DB.append((now, name))
            return name
    return None
    
def main():
    img1 = cv2.imread("../res/Bill_Gates.jpg")
    img2 = cv2.imread("../res/Elon_Musk.jpg")
    register("Bill Gates", img1)
    register("Elon Musk", img2)
    