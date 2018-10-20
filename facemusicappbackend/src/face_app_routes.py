from flask import Flask, request, render_template
import requests
import numpy as np
from PIL import Image
import base64
import re
import io
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('video.html')


"""
Gets the image of the face from post body.
Stores the image in face_img variable.
"""
@app.route('/raw', methods=['POST'])
def get_face_data():
    if 'file' not in request.files:
        print('no file recieved')
        return ''
    file = request.files['file']
    faces = get_microsoft_data(file.stream.read())
    print(faces)
    return ''

"""
Return current emotional state of user given a webcam image
"""
@app.route('/emotion', methods=['POST'])
def get_emotion():
    if 'file' not in request.files:
        print('no file recieved')
        return ''
    file = request.files['file']
    faces = get_microsoft_data(file.stream.read())
    if len(faces) == 0:
        return "N/A"
    else:
        emotion = faces[0]['faceAttributes']['emotion']
        return analyze_emotion(emotion).capitalize()

"""
Send request to microsoft and return json of emotion data
"""
subscription_key = 'cd103fed3d9f4756b1b11bf6531e844d' 
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
def get_microsoft_data(image):
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
        }
    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'gender,smile,emotion'
    }
    response = requests.post(face_api_url, params=params, headers=headers, data=image)
    faces = response.json()
    return faces


"""
Analyzes a emotion dictionary for emotions
"""
def analyze_emotion(emotion):
    inverse = [(value, key) for key, value in emotion.items()]
    return max(inverse)[1]
    


"""
Sends a request to spotify to recommend songs with [emotion]
"""
def recommend_songs(emotion):
    pass


"""
Creates a new spotify playlist from the songs passed in a list
"""
def create_playlist(songs):
    pass
    