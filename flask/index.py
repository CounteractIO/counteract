from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_cors import CORS, cross_origin
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
import json
from pprint import pprint
from tweepy.streaming import StreamListener


# These values are appropriately filled in the code
consumer_key_real = "rst5oIqIuOOVnRt3UWCycP6hx"
consumer_secret_real = "ttzgiQQWzEep0A7B6J92STiJiFNOdyCTuAsfDMEuwlwBYjFudV"
access_token_real = "765521612783378436-zLHd5Fgvh8egm9ro3DD842W9zxxZ0P2"
access_token_secret_real = "G8GgxmC1CKE4sXiNcJdjY7VTm0tXImOloSXofpIHQRA0P"

consumer_key_test = "JBboCjRWkNmTtd9Ja5VSND1Sy"
consumer_secret_test = "bGTmHrWjaDXYWPWqS4LqQ4cbid5OZ7jK2SarRrOxNpK7fn4bj9"
access_token_test = "765521612783378436-xz8vC8H7Rwp6Tkdvvy8YFJ3Modbnmsx"
access_token_secret_test = "LYO1sF6pzZD4EV9sbgrYMO1UYzwC2N4SX8Z5V2bapVKug"


app = Flask(__name__)
CORS(app)

# Convert image to vector
def image_vector(img_file):
    img_data = clarifai_api.tag_images(img_file)
    tags = img_data['results'][0]['result']['tag']['classes']

    vector = [0] * current_index

    for tag in tags:
        if tag in tag_indices:
            vector[tag_indices[tag]] = 1

    return vector

@app.route('/')
def home():
    return jsonify(result="Hello")

@app.route('/tweet')
@cross_origin()
def add_numbers():
    handle = request.args.get('handle')
    message = request.args.get('message')
    auth = OAuthHandler(consumer_key_real, consumer_secret_real)
    auth.secure = True
    auth.set_access_token(access_token_real, access_token_secret_real)

    api = API(auth)
    api.update_status('@'+handle+' '+message)
    return jsonify(result="Tweeted!")


if __name__ == '__main__':
    app.run(debug=True)


