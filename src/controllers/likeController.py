from flask import request, Blueprint, g
from ..shared.Authentication import Auth
from ..models.PostModel import PostModel, PostSchema
from ..models.LikeModel import LikeModel, LikeSchema
from ..models.NewsfeedModel import NewsfeedModel, NewsfeedSchema
from src.jsonResponse import custom_response
from ..models import socket
from .models.UserModel import UserModel, UserSchema
from flask_socketio import SocketIO

like_api = Blueprint('like', __name__)
post_schema = PostSchema()
like_schema = LikeSchema()
user_schema = UserSchema()
newsfeed_schema = NewsfeedSchema()


def messageRecived():
    print('message was received!!!')

@like_api.route('/like_post/<int:post_id>', methods=['GET'])
@Auth.auth_required
def like_post(post_id):
    post = PostModel.get_one_post(post_id)
    if not post: return custom_response({'error': 'Post not found.'}, 400)
    if g.user.get('id') == post.get_id(): return custom_response({'error': 'Is your post.'}, 400)
    if LikeModel.get_one_if_liked(post.get_id(), g.user.get('id')):
        like = LikeModel.get_one_if_liked(post.get_id(), g.user.get('id'))
        if not like: return custom_response({'error': 'You not liked this post.'}, 400)
        news = NewsfeedModel.get_one_news_by_user_id(like.get_id(), g.user.get('id'))
        if not news: return custom_response({'error': 'You not liked this news.'}, 400)
        like.delete()
        news.delete()
        return custom_response({'success': 0}, 200)
    like = LikeModel(post_id, g.user.get('id'))
    like.save()
    news = NewsfeedModel("like", like.id, g.user.get('id'))
    news.save()
    user = user_schema.dump(UserModel.get_one_user(g.user.get('id'))).data
    json = {
        'type': 'like',
        'firstname': user['firstname'],
        'lastname': user['lastname']
    }
    notif = 'notif' + str(post.get_user_id())
    socket.emit(notif, json, callback=messageRecived)
    return custom_response({'success': 1}, 200)