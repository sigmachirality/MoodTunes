from flask import Flask, request, render_template
import requests
import numpy as np
from PIL import Image
import base64
import re
import io
import json
import random
import spotify_backend as sp
import requests

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

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

def make_playlist(target_values, access_token):
    rec_tracks = sp.get_tracks_by_attributes(sp.find_good_seed(target_values, access_token), target_values, access_token)
    playlist = sp.create_playlist(rec_tracks, access_token)
    return playlist

# @app.route('/playlist')
# def playlist():
#     token = get_token(request)
#     top_tracks = sp.get_top_tracks(token)
#     return top_tracks

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
        print(emotion)
        return analyze_emotion(emotion).capitalize()
"""
From image generate emotion, then generate playlist from emotion
"""
@app.route('/playlist', methods=['POST'])
def get_playlist():
    access_token = get_token(request)
    if 'file' not in request.files:
        print('no file recieved')
        return ''
    file = request.files['file']
    faces = get_microsoft_data(file.stream.read())
    if len(faces) == 0:
        return "www.google.com"
    else:
        emotion = faces[0]['faceAttributes']['emotion']
        spotify_dict = emotion_to_spotify(analyze_emotion(emotion).capitalize())
        playlist_id = make_playlist(spotify_dict, access_token)
        url = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers={'Authorization' : 'Bearer ' + access_token})
        url_dict = json.loads(url.text)
        playlist_url = url_dict['external_urls']['spotify']
        return playlist_url

"""
Return full emotional state of user given webcam image
"""
@app.route('/visualize', methods=['POST'])
def get_emotion_full():
    if 'file' not in request.files:
        print('no file recieved')
        return ''
    file = request.files['file']
    faces = get_microsoft_data(file.stream.read())
    if len(faces) == 0:
        return "N/A"
    else:
        emotion = faces[0]['faceAttributes']['emotion']
        return render_template('visualize.html', data=list(emotion.values()))


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
                "energy" : random.uniform(0.2,0.5),
                "valence" : random.uniform(0.6,0.8),
                "tempo" : random.uniform(0.0,0.3),
                "loudness" : random.uniform(0.3,0.5),
                "danceability" : random.uniform(0.1,0.6)  
            }
    elif emotion == "Disgust":
        spotifyData = {
                "energy" : random.uniform(0.2,0.6),
                "valence" : random.uniform(0.8,1.0),
                "tempo" : random.uniform(0.3,0.5),
                "loudness" : random.uniform(0.2,0.5),
                "danceability" : random.uniform(0.2,0.5)  
            }
    elif emotion == "Fear":
        spotifyData = {
                "energy" : random.uniform(0.1,0.4),
                "valence" : random.uniform(0.0,1.0),
                "tempo" : random.uniform(0.0,0.3),
                "loudness" : random.uniform(0.1,0.3),
                "danceability" : random.uniform(0.1,0.5)  
            }
    elif emotion == "Happiness":
        spotifyData = {
                "energy" : random.uniform(0.8,1.0),
                "valence" : random.uniform(0.0,1.0),
                "tempo" : random.uniform(0.5,1.0),
                "loudness" : random.uniform(0.4,1.0),
                "danceability" : random.uniform(0.7,1.0)  
            }
    elif emotion == "Neutral":
        spotifyData = {
                "energy" : random.uniform(0.6,0.9),
                "valence" : random.uniform(0.5,1.0),
                "tempo" : random.uniform(0.4,0.8),
                "loudness" : random.uniform(0.5,0.8),
                "danceability" : random.uniform(0.5,0.9)  
            }
    elif emotion == "Surprise":
        spotifyData = {
                "energy" : random.uniform(0.4,0.8),
                "valence" : random.uniform(0.1,1.0),
                "tempo" : random.uniform(0.5,0.7),
                "loudness" : random.uniform(0.4,0.7),
                "danceability" : random.uniform(0.4,0.8)  
            }
    elif emotion == "Sadness":
        spotifyData = {
                "energy" : random.uniform(0.2,0.6),
                "valence" : random.uniform(0.1,1.0),
                "tempo" : random.uniform(0.1,0.5),
                "loudness" : random.uniform(0.2,0.6),
                "danceability" : random.uniform(0.3,0.4)  
            }
    else:
        spotifyData = {}
    spotifyData['tempo'] = spotifyData['tempo'] * 180
    spotifyData['loudness'] = spotifyData['loudness'] * -70
    return spotifyData


"""
Reads the request args for an auth code, and sends to spotify for an access token
"""
def get_token(request):
    auth_code = ""
    if not request.args == None:
        auth_code = request.args.get("code")
    token = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': 'http://127.0.0.1:5000/recommend', 'client_id': sp.client_id, 'client_secret': sp.client_secret})
    return token.json()["access_token"]



    
