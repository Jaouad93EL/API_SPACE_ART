import json

from flask import Blueprint, g
from ..models.FollowModel import FollowModel, FollowSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
follow_api = Blueprint('follow', __name__)
follow_schema = FollowSchema()

@follow_api.route('/newfollowing/<int:follow_id>', methods=['POST'])
@Auth.auth_required
def newfollowing(follow_id):
    follow = FollowModel.get_follow(follow_id, g.user.get('id'))
    if follow or g.user.get('id') == follow_id:
        return custom_response({'error': 'Follow failed.'}, 400)
    else:
        follow = FollowModel(follow_id, g.user.get('id'))
        follow.save()
        return custom_response({'success': 'New Follow.'}, 200)


@follow_api.route('/unfollowing/<int:follow_id>', methods=['DELETE'])
@Auth.auth_required
def unfollowing(follow_id):
    if g.user.get('id') == follow_id:
        return custom_response({'error': 'Unfollow failed.'}, 400)
    else:
        follow = FollowModel.get_follow(follow_id, g.user.get('id'))
        if not follow:
            return custom_response({'error': 'User for unfollow not found.'}, 400)
        follow.delete()
        return custom_response({'success': 'unFollow'}, 200)


@follow_api.route('/all_following', methods=['GET'])
@Auth.auth_required
def all_following():
    following_in_db = FollowModel.get_all_following(g.user.get('id'))
    if following_in_db:
        li = []
        [li.append(follow_schema.dump(f).data.get('follow_id')) for f in following_in_db]
        return custom_response({'success': {'following': li}}, 200)
    else:
        return custom_response({'error': 'Empty.'}, 400)


@follow_api.route('/all_followers', methods=['GET'])
@Auth.auth_required
def all_followers():
    followers_in_db = FollowModel.get_all_followers(g.user.get('id'))
    if followers_in_db:
        li = []
        [li.append(follow_schema.dump(f).data.get('follow_id')) for f in followers_in_db]
        return custom_response({'success': {'followers': li}}, 200)
    else:
        return custom_response({'error': 'Empty.'}, 400)


@follow_api.route('/all_following_user/<int:user_id>', methods=['GET'])
def all_following_user(user_id):
    following_in_db = FollowModel.get_all_following(user_id)
    if following_in_db:
        li = []
        for f in following_in_db:
            mini_user = follow_schema.dump(f)
            m = {
                'id_user': mini_user.data.get('follow_id'),
                'firstname': mini_user.data.get('firstname'),
                'lastname': mini_user.data.get('lastname'),
                'picture_url': mini_user.data.get('picture_url')
            }
            li.append(m)
        #[li.append(follow_schema.dump(f).data.get('follow_id')) for f in following_in_db]
        return custom_response({'success': {'following': li}}, 200)
    return custom_response({'error': 'Empty.'}, 400)


@follow_api.route('/all_followers_user/<int:user_id>', methods=['GET'])
def all_followers_user(user_id):
    followers_in_db = FollowModel.get_all_followers(user_id)
    if followers_in_db:
        li = []
        for f in followers_in_db:
            mini_user = follow_schema.dump(f)
            m = {
                'id_user': mini_user.data.get('follow_id'),
                'firstname': mini_user.data.get('firstname'),
                'lastname': mini_user.data.get('lastname'),
                'picture_url': mini_user.data.get('picture_url')
            }
            li.append(m)
        #[li.append(follow_schema.dump(f).data.get('follow_id')) for f in followers_in_db]
        return custom_response({'success': {'followers': li}}, 200)
    return custom_response({'error': 'Empty.'}, 400)