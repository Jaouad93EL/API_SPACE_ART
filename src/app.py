from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from . import config
from .models import db, bcrypt, mail, mongo, socket, es
from .models.UserModel import UserModel, UserSchema
from .models.PrivateModel import PrivateModel
from .models.NotifModel import NotifModel
from flask_mail import Mail
from src.jsonResponse import custom_response
from src.useful.typeConverter import IntListConverter


from .controllers.userController import user_api as user_blueprint
from .controllers.followController import follow_api as follow_blueprint
from .controllers.profileController import profile_api as profile_blueprint
from .controllers.audioController import audio_api as audio_blueprint
from .controllers.videoController import video_api as video_blueprint
from .controllers.postController import post_api as post_blueprint
from .controllers.likeController import like_api as like_blueprint
from.controllers.messageController import message_api as message_blueprint
from.controllers.notifController import notif_api as notif_blueprint
from.controllers.castController import cast_api as cast_blueprint
from.controllers.searchController import search_api as search_blueprint

user_schema = UserSchema()

def create_app():
    app = Flask(__name__)
    #type
    app.url_map.converters['listInt'] = IntListConverter
    #
    app.config.from_object(config.app_config['development'])
    config.send_mail = Mail(app)
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    socket.init_app(app)
    CORS(app)


    #------------------------------------route-----------------------------------#
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(follow_blueprint, url_prefix='/api/follow')
    app.register_blueprint(audio_blueprint, url_prefix='/api/audio')
    app.register_blueprint(video_blueprint, url_prefix='/api/video')
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    app.register_blueprint(post_blueprint, url_prefix='/api/post')
    app.register_blueprint(like_blueprint, url_prefix='/api/like')
    app.register_blueprint(message_blueprint, url_prefix='/api/message')
    app.register_blueprint(notif_blueprint, url_prefix='/api/notif')
    app.register_blueprint(cast_blueprint, url_prefix='/api/cast')
    app.register_blueprint(search_blueprint, url_prefix='/api/search')
    # -----------------------------------route-----------------------------------#


    @app.route('/', methods=['GET'])
    def ac():
        return custom_response("API SPACEART", 200)

    @socket.on('my event')
    def handle_my_custom_event(json):
        user_sender_info = user_schema.dump(UserModel.get_one_user(json['sender'])).data
        user_sender_data = {
            'id': user_sender_info['id'],
            'firstname': user_sender_info['firstname'],
            'lastname': user_sender_info['lastname'],
            'message': json['message'],
            'type': 'message'
        }
        for user in json['users']:
            # socket.emit('re' + str(user), user_sender_data)
            socket.emit('my response', user_sender_data)

            if user != json['sender']:
                # socket.emit('notif' + str(user), user_sender_data)
                socket.emit('my response', user_sender_data)
                NotifModel.save_notif_by_id_user(user, user_sender_data)
        private = list(PrivateModel.get_one_private_conversation_by_li_user(json['users']))
        if private:
            PrivateModel.add_one_private_message_in_conversation(str(private[0]['_id']), user_sender_data)
        else:
            PrivateModel.new_private_conversation(json['users'], user_sender_data)


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

