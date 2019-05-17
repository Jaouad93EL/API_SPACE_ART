import json

from flask import request, Blueprint, g
from ..models.ProfileModel import ProfileModel, ProfileSchema
from ..models.UserModel import UserModel, UserSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
from ..Google_storage import google
import urllib.parse

profile_api = Blueprint('profile', __name__)
profile_schema = ProfileSchema()
user_schema = UserSchema()

@profile_api.route('/update', methods=['PUT'])
@Auth.auth_required
def update_profile():
    req_data = request.get_json()
    data_user, error_user = user_schema.load(req_data, partial=True)
    data_profile, error_profile = profile_schema.load(req_data, partial=True)
    if error_profile: return custom_response(error_profile, 400)
    if error_user: return custom_response(error_user, 400)
    profile = ProfileModel.get_one_profile(g.user.get('id'))
    user = UserModel.get_one_user(g.user.get('id'))
    profile.update(data_profile)
    user.update(data_user)
    ser_user = user_schema.dump(user).data
    ser_profile = profile_schema.dump(profile).data
    info_user = {
        'firstname': ser_user.get('firstname'),
        'lastname': ser_user.get('lastname'),
        'age': ser_profile.get('age'),
        'size': ser_profile.get('size'),
        'weight': ser_profile.get('weight'),
        'description': ser_profile.get('description'),
        'city': ser_profile.get('city'),
    }
    return custom_response({'successful': info_user}, 200)


@profile_api.route('/update_banner', methods=['PUT'])
@Auth.auth_required
def update_banner():
    banner_storage = request.files.get('banner')
    if not banner_storage or banner_storage.content_type != 'image/png' and banner_storage.content_type != 'image/jpeg':
        return custom_response({'error': 'Is not a img/png file.'}, 400)
    profile = ProfileModel.get_one_profile(g.user.get('id'))
    ser_profile = profile_schema.dump(profile).data
    if ser_profile.get('banner_url') != "empty":
        google.delete_in_google("banner_space_art", str(g.user.get('id')), ser_profile.get('banner_name_storage'))
    url = google.store_in_google("banner_space_art", str(g.user.get('id')), banner_storage)
    profile.banner_profile(url, banner_storage.filename)
    return custom_response({'successful': {'url': urllib.parse.unquote(profile.banner_url)}}, 200)


@profile_api.route('/update_picture', methods=['PUT'])
@Auth.auth_required
def update_picture():
    picture_storage = request.files.get('picture')
    if not picture_storage or picture_storage.content_type != 'image/png' and picture_storage.content_type != 'image/jpeg':
        return custom_response({'error': 'Is not a img/png file.'}, 400)
    profile = ProfileModel.get_one_profile(g.user.get('id'))
    ser_profile = profile_schema.dump(profile).data
    if ser_profile.get('picture_url') != "empty":
        google.delete_in_google("picture_space_art", str(g.user.get('id')), ser_profile.get('picture_name_storage'))
    url = google.store_in_google("picture_space_art", str(g.user.get('id')), picture_storage)
    profile.picture_profile(url, picture_storage.filename)
    return custom_response({'successful': {'url': urllib.parse.unquote(profile.picture_url)}}, 200)



@profile_api.route('/update_pic_ban', methods=['PUT'])
@Auth.auth_required
def update_pic_ban():
    picture_storage = request.files.get('picture')
    banner_storage = request.files.get('banner')
    picture_url = None
    banner_url = None
    if picture_storage: picture_storage = request.put(request.url_root + 'api/profil/update_picture', files={'picture': picture_storage}, headers=request.headers)
    if banner_storage: banner_storage = request.put(request.url_root + 'api/profil/update_banner', files={'banner': banner_storage}, headers=request.headers)
    if picture_storage.status_code == 200: picture_url = json.load(picture_storage.text)
    if banner_storage.status_code == 200: banner_url = json.load(banner_storage.text)
    url = {
        'picture_url': picture_url['succcessful']['url'],
        'banner_url': banner_url['succcessful']['url']
    }
    return custom_response({'link': {url}}, 200)


@profile_api.route('/get_my_profile', methods=['GET'])
@Auth.auth_required
def get_my_profile():
    profile = ProfileModel.get_one_profile(g.user.get('id'))
    if not profile: return custom_response({'error': 'Profile not found'}, 400)
    ser_profile = profile_schema.dump(profile).data
    return custom_response({'successful': ser_profile}, 200)


@profile_api.route('/get_profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = ProfileModel.get_one_profile(user_id)
    user = UserModel.get_one_user(user_id)
    if not profile or not user: return custom_response({'error': 'Profile not found'}, 400)
    ser_profile = profile_schema.dump(profile).data
    ser_user = user_schema.dump(user).data
    info_user = {
        'firstname': ser_user.get('firstname'),
        'lastname': ser_user.get('lastname'),
        'age': ser_profile.get('age'),
        'size': ser_profile.get('size'),
        'weight': ser_profile.get('weight'),
        'description': ser_profile.get('description'),
        'city': ser_profile.get('city'),
        'picture_name_storage': ser_profile.get('picture_name_storage'),
        'banner_name_storage': ser_profile.get('banner_name_storage'),
        'picture_url': ser_profile.get('picture_url'),
        'banner_url': ser_profile.get('banner_url')
    }
    return custom_response({'successful': info_user}, 200)