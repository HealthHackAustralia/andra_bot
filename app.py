from flask import Flask, request, make_response
from robot import say_with_emotion
from json import loads
from sys import stderr
import threading

app = Flask(__name__)

def async_say_with_emotion(*args):
    stderr.write('Started thread')
    thr = threading.Thread(target=say_with_emotion, args=args, kwargs={})
    stderr.write('Started thread')
    thr.start()
    return 'DONE'

def async_say_with_emotion_2(*args):
    pass

@app.route("/say")
def say():
    try:
        message, emotion = request.args['message'], request.args['emotion']
        return_msg = async_say_with_emotion(message, emotion)
        stderr.write(message)
        return return_msg
    except:
        try:
            message, emotion = request.form['message'], request.form['emotion']
            return_msg = async_say_with_emotion(message, emotion)
            stderr.write(message)
            return return_msg
        except Exception, e:
            return 'Failure: {0}'.format(str(e))
