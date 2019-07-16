from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from . import config
from .models import db, bcrypt, mail, mongo
from flask_mail import Mail
from src.jsonResponse import custom_response


from .controllers.userController import user_api as user_blueprint
from .controllers.followController import follow_api as follow_blueprint
from .controllers.profileController import profile_api as profile_blueprint
from .controllers.audioController import audio_api as audio_blueprint
from .controllers.videoController import video_api as video_blueprint
from .controllers.postController import post_api as post_blueprint
from .controllers.likeController import like_api as like_blueprint
from.controllers.messageController import message_api as message_blueprint
from.controllers.castController import cast_api as cast_blueprint


def create_app():
    app = Flask(__name__)
    config.send_mail = Mail(app)
    CORS(app)
    app.config.from_object(config.app_config['development'])
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    socket = SocketIO(app)


    #------------------------------------route-----------------------------------#
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(follow_blueprint, url_prefix='/api/follow')
    app.register_blueprint(audio_blueprint, url_prefix='/api/audio')
    app.register_blueprint(video_blueprint, url_prefix='/api/video')
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    app.register_blueprint(post_blueprint, url_prefix='/api/post')
    app.register_blueprint(like_blueprint, url_prefix='/api/like')
    app.register_blueprint(message_blueprint, url_prefix='/api/message')
    app.register_blueprint(cast_blueprint, url_prefix='/api/cast')
    # -----------------------------------route-----------------------------------#


    @app.route('/', methods=['GET'])
    def ac():
        return custom_response("API SPACEART", 200)

    def messageRecived():
        print('message was received!!!')

    @socket.on('my event')
    def handle_my_custom_event(json):
        print('recived my event: ' + str(json))
        socket.emit('my response', json, callback=messageRecived)

    @app.route('/route', methods=['GET'])
    def route():
        methods, links, count = ['PUT', 'GET', 'POST', 'DELETE'], {}, 0
        for rule in app.url_map.iter_rules():
            temp = request.url_root
            new, url_root = list(rule.methods), temp.rsplit('/', 1)
            method = [x for x in new if x != 'OPTIONS' and x != 'HEAD']
            links[count], count = {"Method": method[0], "url": url_root[0] + str(rule)}, count + 1
        return custom_response(links, 200)
    return app