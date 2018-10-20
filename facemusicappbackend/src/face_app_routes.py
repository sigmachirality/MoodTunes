from flask import Flask, request
import cognitive_face as cf 

app = Flask(__name__)

KEY = 'cd103fed3d9f4756b1b11bf6531e844d' 
cf.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
cf.BaseUrl.set(BASE_URL)

face_img = None

@app.route('/')
def welcome_message():
    send_face()
    return


"""
Gets the image of the face from post body.
Stores the image in face_img variable.
"""
@app.route('/', methods=['POST'])
def get_face_image():
    post_body = request.files
    global face_img
    name = ''
    face_img = post_body[name] # Where 'name' is the name attribute given
                               # through post request.
    

"""
Sends the face image to the face api and gets back a list of faces
"""
def send_face():
    img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    faces = cf.face.detect(img_url)
    return faces