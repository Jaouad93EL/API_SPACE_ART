from flask import Flask, request
from flask_cors import CORS
from . import config
from .models import db, bcrypt
from flask_mail import Mail, Message
from src.jsonResponse import custom_response
from .controllers.userController import user_api as user_blueprint
from .controllers.followController import follow_api as follow_blueprint
from .controllers.profileController import profile_api as profile_blueprint
from .controllers.audioController import audio_api as audio_blueprint
from .controllers.videoController import video_api as video_blueprint


def create_app():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'elhorm_j@etna-alternance.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'SpaceArt'
    app.config['MAIL_PASSWORD'] = 'SpaceArt'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    config.send_mail = Mail(app)
    CORS(app)
    app.config.from_object(config.app_config['development'])
    bcrypt.init_app(app)
    db.init_app(app)

    #------------------------------------route-----------------------------------#
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(follow_blueprint, url_prefix='/api/follow')
    app.register_blueprint(audio_blueprint, url_prefix='/api/audio')
    app.register_blueprint(video_blueprint, url_prefix='/api/video')
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    # -----------------------------------route-----------------------------------#

    @app.route('/', methods=['GET'])
    def ac():
        return custom_response("API SPACEART", 200)

    @app.route('/route', methods=['GET'])
    def route():
        methods, links, count = ['PUT', 'GET', 'POST', 'DELETE'], {}, 0
        for rule in app.url_map.iter_rules():
            temp = request.url_root
            new, url_root = list(rule.methods), temp.rsplit('/', 1)
            method = [x for x in new if x != 'OPTIONS' and x != 'HEAD']
            links[count], count = {"Method": method[0], "url": url_root[0]+str(rule)}, count + 1
        return custom_response(links, 200)
    return app
