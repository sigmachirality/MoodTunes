from flask import Flask, request

app = Flask(__name__)


auth_code = ""


@app.route('/')
def welcome_message():
    global auth_code
    auth_code = request.args.get('code')
    return 'Welcome!'


@app.route('/get_auth_code')
def get_auth_code():
    return auth_code


    
