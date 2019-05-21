from flask import request, Blueprint, g
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
from ..Google_storage import google
import urllib.parse
from ..models.AudioModel import AudioModel, AudioSchema

audio_api = Blueprint('audio', __name__)
audio_schema = AudioSchema()

@audio_api.route('/upload_audio', methods=['POST'])
@Auth.auth_required
def upload_audio():
    audio_storage = request.files.get('audio')
    if not audio_storage or audio_storage.content_type != 'audio/mp3' and audio_storage.content_type != 'audio/mpeg':
        return custom_response({'error': 'Is not a mp3 file.'}, 400)
    req_data = request.form.to_dict()
    data, error = audio_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    audio_in_db = AudioModel.get_audio_by_name_and_user(audio_storage.filename, g.user.get('id'))
    if audio_in_db:
        return custom_response({'error': 'Audio already exist.'}, 400)
    audio_in_db = AudioModel.get_audio_by_titre(data.get('titre'))
    if audio_in_db:
        return custom_response({'error': 'Titre already exist.'}, 400)
    url = google.store_in_google("audio_space_art", str(g.user.get('id')), audio_storage)
    audio = AudioModel(data, g.user.get('id'), audio_storage.filename, url)
    audio.save()
    audio_data = {
        'id': audio.id,
        'titre': audio.titre,
        'description': audio.description,
        'url': urllib.parse.unquote(audio.url)
    }
    return custom_response({'successful': audio_data}, 200)


@audio_api.route('/get_audio_by_id_audio/<int:id_audio>', methods=['GET'])
@Auth.auth_required
def get_audio_by_id_audio(id_audio):
    audio_in_db = AudioModel.get_audio_by_id(id_audio)
    if audio_in_db:
        ser_audio = audio_schema.dump(audio_in_db).data
        url = ser_audio.get('url')
        result = urllib.parse.unquote(url)
        return custom_response({'successful': {'url': result}}, 200)
    return custom_response({'error': 'Audio not exist.'}, 400)


@audio_api.route('/get_all_audio/<int:id_user>', methods=['GET'])
def get_audio_all_audio(id_user):
    audio_in_db = AudioModel.get_audio_all(id_user)
    if audio_in_db:
        list_audio = []
        [list_audio.append(audio_schema.dump(a).data) for a in audio_in_db]
        return custom_response({'successful': list_audio}, 200)
    return custom_response({'error': 'Audio not exist.'}, 400)


@audio_api.route('/update_audio_by_id/<int:id_audio>', methods=['PUT'])
@Auth.auth_required
def update_audio_by_id(id_audio):
    req_data = request.get_json()
    data, error = audio_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    audio = AudioModel.get_audio_by_id(id_audio)
    audio.update(data)
    audio_data = {
        'id': audio.id,
        'titre': audio.titre,
        'description': audio.description,
        'url': urllib.parse.unquote(audio.url)
    }
    return custom_response({'successful': audio_data}, 200)


@audio_api.route('/update_audio_storage_by_id/<int:id_audio>', methods=['PUT'])
@Auth.auth_required
def update_audio_storage_by_id(id_audio):
    audio_storage = request.files.get('audio')
    if not audio_storage or audio_storage.content_type != 'audio/mp3' and audio_storage.content_type != 'audio/mpeg':
        return custom_response({'error': 'Is not a mp3 file.'}, 400)
    audio = AudioModel.get_audio_by_id(id_audio)
    google.delete_in_google("audio_space_art", str(g.user.get('id')), audio.audio_name_storage)
    url = google.store_in_google("audio_space_art", str(g.user.get('id')), audio_storage)
    audio.update_url(url, audio_storage.filename)
    return custom_response({'successful': {'url': urllib.parse.unquote(audio.url)}}, 200)


@audio_api.route('/delete_audio/<int:id_audio>', methods=['DELETE'])
@Auth.auth_required
def delete_audio(id_audio):
    audio = AudioModel.get_audio_by_id(id_audio)
    if not audio:
        return custom_response({'error': 'Audio not exist.'}, 400)
    if audio.user_id == g.user.get('id'):
        google.delete_in_google("audio_space_art", str(g.user.get('id')), audio.audio_name_storage)
        audio.delete()
        return custom_response({'successful': 'Audio delete'}, 200)
    return custom_response({'error': 'Is not your Audio.'}, 400)


