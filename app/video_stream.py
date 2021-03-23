import cv2
from imutils.video import WebcamVideoStream
from app.face_recog import FaceRecognition
from app import models, db

class StreamProcessing():
    stream = None
    running = False
    already_added_students = []
    
    
    def start():
        """A function that opens and starts webcam stream."""
        StreamProcessing.stream = WebcamVideoStream(src=0).start()
        StreamProcessing.running = True
        
     
    def get_frame():
        """A function that get a frame from the webcam video stream."""
        frame = StreamProcessing.stream.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert it to RGB image
        return frame

    
    def process():
        """A function that do the actual work of reading from the webcam stream,
        and processes it and sends the new image to represent,
        then repeats until the stream stops."""
        
        frame = StreamProcessing.get_frame()

        # resize frame of video to 1/4 size for faster processing
        
            
           
        
    def stop():
        """A function that stops the stream and closes cam"""
        StreamProcessing.running = False
        StreamProcessing.stream.stop() 
        StreamProcessing.stream.stream.release()

 