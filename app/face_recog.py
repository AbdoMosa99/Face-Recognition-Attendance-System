import cv2
import numpy as np
import face_recognition
import pickle


# A class that handles all face recoginition processes and representation 
class FaceRecognition():
    
    def file2RGB(file):
        """A function that convert uploaded file (jpg, png, etc.) to cv2 RGB image."""
        file_content_str = file.read() # read file content
        np_arr = np.fromstring(file_content_str, np.uint8) # convert to np array
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # decode it into image
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert image to RGB
        return rgb

    
    def get_encoding(img):
        """A function that takes an RGB image,
        and returns the face encoding of the first face in it."""
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            raise Exception("No faces found in the image")
            
        return encodings[0]

    
    def process_image(img, known_encodings_db):
        """A function that takes an RGB image,
        and returns the students in it with their face locations."""
        
        # get faces locations and encodings
        face_locations = face_recognition.face_locations(img)
        unknown_encodings = face_recognition.face_encodings(img, face_locations)

        # convert known encodings from db objects to a normal list
        known_encodings = list(map(
            lambda enc: pickle.loads(enc.encoding),
            known_encodings_db))
        
        # for all encodings in the image,
        # get the matches of students if exists in the db
        recognized_students = []
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
        """A function that takes an image and a list of locations and students,
        And represent these information on the image itself."""
        
        for recognized_student in recognized_students:
            top, right, bottom, left = recognized_student["location"]
            
            # draw a box around the face
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # draw a label with a name below the face
            cv2.rectangle(img, (left, bottom - 35), (right, bottom),
                          (0, 0, 255), cv2.FILLED)
            cv2.putText(img, recognized_student["student"].name, 
                        (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX,
                        1.0, (255, 255, 255), 1)

        return img
       