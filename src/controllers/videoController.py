from flask import request, Blueprint, g
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
from ..Google_storage import google
import urllib.parse
from ..models.VideoModel import VideoModel, VideoSchema

video_api = Blueprint('video', __name__)
video_schema = VideoSchema()

@video_api.route('/upload_video', methods=['POST'])
@Auth.auth_required
def upload_video():
    video_storage = request.files.get('video')
    if not video_storage or video_storage.content_type != 'video/mp4':
        return custom_response({'error': 'Is not a mp4 file.'}, 400)
    req_data = request.form.to_dict()
    data, error = video_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    video_in_db = VideoModel.get_video_by_name_and_user(video_storage.filename, g.user.get('id'))
    if video_in_db:
        return custom_response({'error': 'Video already exist.'}, 400)
    video_in_db = VideoModel.get_video_by_titre(data.get('titre'))
    if video_in_db:
        return custom_response({'error': 'Titre already exist.'}, 400)
    url = google.store_in_google("video_space_art", str(g.user.get('id')), video_storage)
    video = VideoModel(data, g.user.get('id'), video_storage.filename, url)
    video.save()
    video_data = {
        'id': video.id,
        'titre': video.titre,
        'description': video.description,
        'url': urllib.parse.unquote(video.url)
    }
    return custom_response({'successful': video_data}, 200)


@video_api.route('/get_video_by_id_video/<int:id_video>', methods=['GET'])
@Auth.auth_required
def get_video_by_id_video(id_video):
    video_in_db = VideoModel.get_video_by_id(id_video)
    if video_in_db:
        ser_video = video_schema.dump(video_in_db).data
        url = ser_video.get('url')
        result = urllib.parse.unquote(url)
        return custom_response({'successful': {'url': result}}, 200)
    return custom_response({'error': 'Video not exist.'}, 400)


@video_api.route('/get_all_video/<int:id_user>', methods=['GET'])
def get_video_all_video(id_user):
    video_in_db = VideoModel.get_video_all(id_user)
    if video_in_db:
        list_video = []
        [list_video.append(video_schema.dump(a).data) for a in video_in_db]
        return custom_response({'successful': list_video}, 200)
    return custom_response({'error': 'Video not exist.'}, 400)


@video_api.route('/update_video_by_id/<int:id_video>', methods=['PUT'])
@Auth.auth_required
def update_video_by_id(id_video):
    req_data = request.get_json()
    data, error = video_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    video = VideoModel.get_video_by_id(id_video)
    video.update(data)
    video_data = {
        'id': video.id,
        'titre': video.titre,
        'description': video.description,
        'url': urllib.parse.unquote(video.url)
    }
    return custom_response({'successful': video_data}, 200)


@video_api.route('/update_video_storage_by_id/<int:id_video>', methods=['PUT'])
@Auth.auth_required
def update_video_storage_by_id(id_video):
    video_storage = request.files.get('video')
    if not video_storage or video_storage.content_type != 'video/mp4':
        return custom_response({'error': 'Is not a mp4 file.'}, 400)
    video = VideoModel.get_video_by_id(id_video)
    google.delete_in_google("video_space_art", str(g.user.get('id')), video.video_name_storage)
    url = google.store_in_google("video_space_art", str(g.user.get('id')), video_storage)
    video.update_url(url, video_storage.filename)
    return custom_response({'successful': {'url': urllib.parse.unquote(video.url)}}, 200)


@video_api.route('/delete_video/<int:id_video>', methods=['DELETE'])
@Auth.auth_required
def delete_video(id_video):
    video = VideoModel.get_video_by_id(id_video)
    if video.user_id == g.user.get('id'):
        google.delete_in_google("video_space_art", str(g.user.get('id')), video.video_name_storage)
        video.delete()
        return custom_response({'successful': 'Video delete'}, 200)
    return custom_response({'error': 'Is not your Video.'}, 400)


