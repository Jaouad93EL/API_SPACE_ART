import operator
import dateutil.parser
from flask import request, Blueprint, g
from ..models.PostModel import PostModel, PostSchema
from ..models.LikeModel import LikeModel, LikeSchema
from ..models.ProfileModel import ProfileModel,ProfileSchema
from ..models.UserModel import UserModel, UserSchema
from ..models.FollowModel import FollowModel, FollowSchema
from ..models.NewsfeedModel import NewsfeedModel, NewsfeedSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth

post_api = Blueprint('post', __name__)
post_schema = PostSchema()
like_schema = LikeSchema()
follow_schema = FollowSchema()
profile_schema = ProfileSchema()
user_schema = UserSchema()
newsfeed_schema = NewsfeedSchema()

@post_api.route('/create_post', methods=['POST'])
@Auth.auth_required
def create_post():
    req_data = request.get_json()
    data, error = post_schema.dump(req_data)
    if error: return custom_response(error, 400)
    post = PostModel(data.get('text'), g.user.get('id'))
    post.save()
    news = NewsfeedModel("post", post.id, g.user.get('id'))
    news.save()
    ser_user = user_schema.dump(UserModel.get_one_user(g.user.get('id'))).data
    ser_profile = profile_schema.dump(ProfileModel.get_one_profile(ser_user.get('id'))).data
    dict_news = insert_post(post_schema.dump(post).data)
    dict_news['user'] = insert_user(ser_user, ser_profile)
    return custom_response({'success': dict_news}, 200)


@post_api.route('/delete_post/<int:post_id>', methods=['DELETE'])
@Auth.auth_required
def delete_post(post_id):
    post = PostModel.get_one_post_by_user_id(post_id, g.user.get('id'))
    if not post: return custom_response({'error': 'Not your Post'}, 400)
    news = NewsfeedModel.get_one_news_by_user_id(post.get_id(), g.user.get('id'))
    if not news: return custom_response({'error': 'Not your News'}, 400)
    post.delete()
    news.delete()
    return custom_response({'success': 'Post delete'}, 200)


@post_api.route('/all_post/<int:user_id>', methods=['GET'])
def all_post(user_id):
    following_in_db = FollowModel.get_all_following(user_id)
    li_newsfeed = []
    if following_in_db:
        for f in following_in_db:
            user = UserModel.get_one_user(follow_schema.dump(f).data.get('follow_id'))
            li_newsfeed += insert_news(user)
    me_user = UserModel.get_one_user(user_id)
    li_newsfeed += insert_news(me_user)
    return custom_response({'success': sorted(li_newsfeed, key=operator.itemgetter('date'), reverse=True)}, 200)

def insert_news(user):
    li_news = []
    for news in user.newsfeed:
        news_parent = newsfeed_schema.dump(news).data
        ser_user = user_schema.dump(user).data
        ser_profile = profile_schema.dump(ProfileModel.get_one_profile(ser_user.get('id'))).data
        dict_news = {}
        if news_parent.get('type') == 'post':
            dict_news = insert_post(post_schema.dump(PostModel.get_one_post(news_parent.get('parent_id'))).data)
        elif news_parent.get('type') == 'like':
            dict_news = insert_like(like_schema.dump(LikeModel.get_one_like(news_parent.get('parent_id'))).data)
        dict_news['user'] = insert_user(ser_user, ser_profile)
        li_news.append(dict_news)
    return li_news

def insert_post(ser_post):
    return {
        'date': dateutil.parser.parse(ser_post.get('modified_at')),
        'type': 'post',
        'news': {
            'id': ser_post.get('id'),
            'text': ser_post.get('text')
        }
    }

def insert_like(ser_like):
    ser_post = post_schema.dump(PostModel.get_one_post(ser_like.get('post_id'))).data
    ser_user = user_schema.dump(UserModel.get_one_user(ser_post.get('user_id'))).data
    ser_profile = profile_schema.dump(ProfileModel.get_one_profile(ser_user.get('id'))).data
    return {
        'date': dateutil.parser.parse(ser_like.get('modified_at')),
        'type': 'like',
        'like_id': ser_like.get('id'),
        'info_post_liked': insert_post(ser_post),
        'info_user_liked': insert_user(ser_user, ser_profile)
    }

def insert_user(ser_user, ser_profile):
    return {
        'id_user': ser_user.get('id'),
        'firstname': ser_user.get('firstname'),
        'lastname': ser_user.get('lastname'),
        'picture_url': ser_profile.get('picture_url')
    }


@post_api.route('/get_my_all_post/<int:user_id>', methods=['GET'])
def get_my_all_post(user_id):
    li_newsfeed = []
    me_user = UserModel.get_one_user(user_id)
    li_newsfeed += insert_news(me_user)
    return custom_response({'success': sorted(li_newsfeed, key=operator.itemgetter('date'), reverse=True)}, 200)