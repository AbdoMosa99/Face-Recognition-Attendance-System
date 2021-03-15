from flask import render_template, redirect, url_for, Response
from app import app
from app.face_recog import StreamProcessing

# Camera openning and face processing page
@app.route('/camfeed')
def cam_feed():
    return render_template("cam_feed.html")

# Live video feedback window
@app.route('/video_feed')
def video_feed():
    return Response(StreamProcessing.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ish don't think so
@app.route('/error')
def error():
    return render_template('error.html')


