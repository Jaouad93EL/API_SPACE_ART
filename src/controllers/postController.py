import operator
import dateutil.parser
from flask import request, Blueprint, g
from ..models.PostModel import PostModel, PostSchema
from ..models.ProfileModel import ProfileModel,ProfileSchema
from ..models.UserModel import UserModel, UserSchema
from ..models.FollowModel import FollowModel, FollowSchema
from ..models.NewsfeedModel import NewsfeedModel, NewsfeedSchema

from src.jsonResponse import custom_response
from ..shared.Authentication import Auth


post_api = Blueprint('post', __name__)
post_schema = PostSchema()
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
    info_post = {
        'id': post.id,
        'text': post.text,
        'user_id': post.user_id
    }
    return custom_response({'success': info_post}, 200)


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
    li_newsfeed = []
    for news in user.newsfeed:
        news_parent = newsfeed_schema.dump(news).data
        ser_user = user_schema.dump(user).data
        ser_profile = profile_schema.dump(ProfileModel.get_one_profile(ser_user.get('id'))).data
        dict_news = {}
        if news_parent.get('type') == 'post':
            ser_post = post_schema.dump(PostModel.get_one_post(news_parent.get('parent_id'))).data
            dict_news = {
                'date': dateutil.parser.parse(ser_post.get('modified_at')),
                'type': 'post',
                'news': {'id': ser_post.get('id'), 'text': ser_post.get('text')},
            }
        elif news_parent.get('type') == 'like':
            print('de type like A FAIRE')
        dict_news['user'] = {
            'id_user': ser_user.get('id'),
            'firstname': ser_user.get('firstname'),
            'lastname': ser_user.get('lastname'),
            'picture_url': ser_profile.get('picture_url')
        }
        li_newsfeed.append(dict_news)
    return li_newsfeed

def insert_post(ser_post):
    pass

def insert_like(ser_like):
    pass