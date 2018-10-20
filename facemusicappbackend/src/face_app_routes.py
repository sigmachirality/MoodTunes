from flask import Flask, request, render_template
import requests
import numpy as np
from PIL import Image
import base64
import re
import io
import json
import random

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

auth_code = ""
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/spotify')
def welcome_message():
    global auth_code
    auth_code = request.args.get('code')
    return 'Welcome!'
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('video.html')

@app.route('/get_auth_code')
def get_auth_code():
    return auth_code

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
Get spotify parameters for specific emotion
"""
def emotion_to_spotify(emotion):
    if emotion == "Anger" or emotion == "Contempt":
        spotifyData = {
                "Energy" : random.uniform(0.2,0.5),
                "Valence" : random.uniform(0.6,0.8),
                "Tempo" : random.uniform(0.0,0.3),
                "Loudness" : random.uniform(0.3,0.5),
                "Danceability" : random.uniform(0.1,0.6)  
            }
    elif emotion == "Disgust":
        spotifyData = {
                "Energy" : random.uniform(0.2,0.6),
                "Valence" : random.uniform(0.8,1.0),
                "Tempo" : random.uniform(0.3,0.5),
                "Loudness" : random.uniform(0.2,0.5),
                "Danceability" : random.uniform(0.2,0.5)  
            }
    elif emotion == "Fear":
        spotifyData = {
                "Energy" : random.uniform(0.1,0.4),
                "Valence" : random.uniform(0.0,1.0),
                "Tempo" : random.uniform(0.0,0.3),
                "Loudness" : random.uniform(0.1,0.3),
                "Danceability" : random.uniform(0.1,0.5)  
            }
    elif emotion == "Happiness":
        spotifyData = {
                "Energy" : random.uniform(0.8,1.0),
                "Valence" : random.uniform(0.0,1.0),
                "Tempo" : random.uniform(0.5,1.0),
                "Loudness" : random.uniform(0.4,1.0),
                "Danceability" : random.uniform(0.7,1.0)  
            }
    elif emotion == "Neutral":
        spotifyData = {
                "Energy" : random.uniform(0.6,0.9),
                "Valence" : random.uniform(0.5,1.0),
                "Tempo" : random.uniform(0.4,0.8),
                "Loudness" : random.uniform(0.5,0.8),
                "Danceability" : random.uniform(0.5,0.9)  
            }
    elif emotion == "Surprise":
        spotifyData = {
                "Energy" : random.uniform(0.4,0.8),
                "Valence" : random.uniform(0.1,1.0),
                "Tempo" : random.uniform(0.5,0.7),
                "Loudness" : random.uniform(0.4,0.7),
                "Danceability" : random.uniform(0.4,0.8)  
            }
    elif emotion == "Sadness":
        spotifyData = {
                "Energy" : random.uniform(0.2,0.6),
                "Valence" : random.uniform(0.1,1.0),
                "Tempo" : random.uniform(0.1,0.5),
                "Loudness" : random.uniform(0.2,0.6),
                "Danceability" : random.uniform(0.3,0.4)  
            }
    else:
        spotifyData = {}
    spotifyData['Tempo'] = spotifyData['Tempo'] * 180
    spotifyData['Loudness'] = spotifyData['Loudness'] * -70
    return spotifyData


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
    
