
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "OfUJnnclWc7iAWap1qsr"
socketio = SocketIO(app)

import api.service
import api.socket_service
