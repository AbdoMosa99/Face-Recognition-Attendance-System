import cv2
import numpy as np
import face_recognition
from datetime import datetime

encodings_DB = []
attendace_DB = []

def upload(path):
    img = face_recognition.load_image_file(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    enc = face_recognition.face_encodings(img)[0] # should loop
    return enc

def register(name, path):
    enc = upload(path)
    encodings_DB.append((name, enc))

def compare(path):
    unknown_enc = upload(path)
    now = datetime.now()
    for name, enc in encodings_DB:
        result = face_recognition.compare_faces([enc], unknown_enc)
        if result[0] == True:
            print(now, name)
            attendace_DB.append((now, name))
            return 
    print("Unknown")
    
def main():
    register("Bill Gates", "../res/Bill_Gates.jpg")
    register("Elon Musk", "../res/Elon_Musk.jpg")
    compare("../res/unknown.jpg")
    compare("../res/unknown2.jpg")
    

main()