from flask import render_template, redirect, url_for, Response
from app import app
from app.video_stream import StreamProcessing
from app import models


# Camera openning and face processing page
@app.route('/camfeed')
def cam_feed():
    return render_template("cam_feed.html")


# Live video feedback window
@app.route('/video_feed')
def video_feed():
    known_encodings_db = models.FaceEncoding.query.all()
    StreamProcessing.start()
    return Response(StreamProcessing.process(known_encodings_db),
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
