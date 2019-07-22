from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_socketio import SocketIO


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
mongo = PyMongo()
socket = SocketIO()