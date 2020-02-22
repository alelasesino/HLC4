
from flask import request, redirect, url_for, render_template
from api import app, socketio
from flask_socketio import send, rooms

@app.route('/test')
def pepe():
    return render_template('test.html')

@socketio.on('message', namespace='/lol')
def handleMessage(msg):
    print("Message is", msg)
    send(msg, broadcast = True)


@socketio.on('connect', namespace='/lol')
def connect():
    print("User connected:", rooms()[0])


@socketio.on('disconnect')
def disconnect():
    print("User disconnected:", rooms()[0])