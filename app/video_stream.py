import cv2
from imutils.video import WebcamVideoStream
from app.face_recog import FaceRecognition


class StreamProcessing():
    stream = None
    running = False
    
    
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

        while StreamProcessing.running:
            frame = StreamProcessing.get_frame()
            
            # resize frame of video to 1/4 size for faster processing
            processing_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
            recognized_students = FaceRecognition.process_image(processing_frame)
            
            # scale back up face locations as the processing frame was scaled to 1/4 size
            for recognized_student in recognized_students:
                recognized_student["location"] = (recognized_student["location"][0] * 4,
                                                  recognized_student["location"][1] * 4,
                                                  recognized_student["location"][2] * 4,
                                                  recognized_student["location"][3] * 4)
            
            out_frame = FaceRecognition.represent_image(frame, recognized_students)
            
            # convert frame back to jpg format bytes and send it
            ret, jpeg = cv2.imencode('.jpg', out_frame)
            out_frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + out_frame + b'\r\n\r\n')
           
        
    def stop():
        """A function that stops the stream and closes cam"""
        StreamProcessing.running = False
        StreamProcessing.stream.stop() 
        StreamProcessing.stream.stream.release()

 