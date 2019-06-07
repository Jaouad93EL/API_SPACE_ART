import json
from ..models import db

from flask import request, Blueprint, g

from ..models.PostModel import PostModel, PostSchema
from ..models.NewsfeedModel import NewsfeedModel
from ..models.ProfileModel import ProfileModel, ProfileSchema
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
    if following_in_db:
        for f in following_in_db:
            id_user = follow_schema.dump(f).data.get('follow_id')
            user = UserModel.get_one_user(id_user)
            for news in user.newsfeed:
                news_parent = newsfeed_schema.dump(news).data
                if news_parent.get('type') == 'post':
                    post = post_schema.dump(PostModel.get_one_post(news_parent.get('parent_id'))).data
                    print(post)
                elif news_parent == 'like':
                    print('de type like')
        return custom_response({'success': 'okokookokookokookokookokookook.'}, 200)
    return custom_response({'success': 'nonoonononoononono.'}, 200)

# @post_api.route('/all_post/<int:user_id>', methods=['GET'])
# def all_post(user_id):
#     post_in_db = PostModel.get_post_all(user_id)
#     following_in_db = FollowModel.get_all_following(user_id)
#     if following_in_db:
#         li_following = []
#         for f in following_in_db:
#             id_user = follow_schema.dump(f)
#             mini_profile = profile_schema.dump(ProfileModel.get_one_profile(id_user.data.get('follow_id')))
#             mini_user = user_schema.dump(UserModel.get_one_user(id_user.data.get('follow_id')))
#             news_in_db = newsfeed_schema.dump(NewsfeedModel.get_news_all(id_user.data.get('follow_id')))
#             if news_in_db:
#                 news = {}
#                 if news_in_db.data.get('type') == 'post':
#                     pass
#             m = {
#                 'id_user': mini_user.data.get('id'),
#                 'firstname': mini_user.data.get('firstname'),
#                 'lastname': mini_user.data.get('lastname'),
#                 'picture_url': mini_profile.data.get('picture_url')
#             }
#             li_following.append(m)
#     if post_in_db:
#         list_post = []
#         [list_post.append(post_schema.dump(a).data) for a in post_in_db]
#         return custom_response({'successful': list_post}, 200)
#     return custom_response({'error': 'Post not exist.'}, 400)