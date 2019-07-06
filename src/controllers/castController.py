from flask import request, Blueprint, g
from ..models.ProfileModel import ProfileModel,ProfileSchema
from ..models.UserModel import UserModel, UserSchema
from ..models.CastModel import CastModel, CastSchema
from ..models.CandidateModel import CandidateModel, CandidateSchema
from ..shared.Authentication import Auth
from src.jsonResponse import custom_response

cast_api = Blueprint('cast', __name__)
cast_schema = CastSchema()
candidate_schema = CandidateSchema()
profile_schema = ProfileSchema()
user_schema = UserSchema()

@cast_api.route('/create_cast', methods=['POST'])
@Auth.auth_required
def create_cast():
    req_data = request.get_json()
    data, error = cast_schema.dump(req_data)
    if error: return custom_response(error, 400)
    if CastModel.get_one_cast_by_title(data.get('title')):
        return custom_response({"error": "Cast already exist."}, 400)
    cast = CastModel(data, g.user.get('id'))
    cast.save()
    return custom_response({"success": "Cast created."}, 200)


@cast_api.route('/get_all_cast', methods=['GET'])
def get_all_cast():
    casts = CastModel.get_cast_all()
    if not casts: return custom_response({'error': 'Casts not found.'}, 400)
    casts_array = []
    for c in casts:
        ser_cast = cast_schema.dump(c).data
        user = UserModel.get_one_user(ser_cast.get('user_id'))
        profile = ProfileModel.get_one_profile(ser_cast.get('user_id'))
        ser_user = user_schema.dump(user).data
        ser_profile = profile_schema.dump(profile).data
        casts_array.append({
            'cast': ser_cast,
            'user': ser_user,
            'profile': ser_profile
        })
    return custom_response({"success": casts_array}, 200)


@cast_api.route('/get_one_cast/<int:cast_id>', methods=['GET'])
def get_one_cast(cast_id):
    cast = CastModel.get_one_cast_by_id(cast_id)
    if not cast: return custom_response({'error': 'Casts not found.'}, 400)
    ser_cast = cast_schema.dump(cast).data
    user = UserModel.get_one_user(ser_cast.get('user_id'))
    profile = ProfileModel.get_one_profile(ser_cast.get('user_id'))
    ser_user = user_schema.dump(user).data
    ser_profile = profile_schema.dump(profile).data
    info = {
        'cast': ser_cast,
        'user': ser_user,
        'profile': ser_profile
    }
    return custom_response({"success": info}, 200)

@cast_api.route('/candidate_cast/<int:cast_id>', methods=['POST'])
@Auth.auth_required
def candidate_cast(cast_id):
    req_data = request.get_json()
    data = candidate_schema.dump(req_data).data
    cast = CastModel.get_one_cast_by_id(cast_id)
    if not cast:
        return custom_response({"error": "Cast not found."}, 400)
    if cast.get_user_id() == g.user.get('id'):
        return custom_response({"error": "Its your cast."}, 400)
    if CandidateModel.get_one_candidate_by_cast_id(cast.get_id(), g.user.get('id')):
        return custom_response({"error": "You are already registering."}, 400)
    candidate = CandidateModel(data.get('motivate'), g.user.get('id'), cast_id)
    candidate.save()
    return custom_response({"success": "You are registering."}, 200)


@cast_api.route('/all_candidate_in_one_cast/<int:cast_id>', methods=['GET'])
def all_candidate_in_one_cast(cast_id):
    cast = CastModel.get_one_cast_by_id(cast_id)
    if not cast:
        return custom_response({"error": "Cast not found."}, 400)
    candidates = CandidateModel.get_all_candidates_by_cast_id(cast_id)
    if not candidates:
        return custom_response({"error": "Candidates not found."}, 400)
    candidates_array = []
    for c in candidates:
        ser_candidate = candidate_schema.dump(c).data
        user = UserModel.get_one_user(ser_candidate.get('user_id'))
        profile = ProfileModel.get_one_profile(ser_candidate.get('user_id'))
        ser_user = user_schema.dump(user).data
        ser_profile = profile_schema.dump(profile).data
        candidates_array.append({
            'candidate': ser_candidate,
            'user': ser_user,
            'profile': ser_profile
        })
    return custom_response({"success": candidates_array}, 200)


@cast_api.route('/accepted_candidate_or_not/<int:cast_id>/<int:candidate_id>', methods=['GET'])
@Auth.auth_required
def accepted_candidate_or_not(cast_id, candidate_id):
    my_cast = CastModel.get_my_cast(cast_id, g.user.get('id'))
    if not my_cast:
        return custom_response({"error": "Cast not found."}, 400)
    candidate = CandidateModel.get_one_candidate_by_cast_id(cast_id, candidate_id)
    if candidate.get_accepted() == 0:
        candidate.update_accepted(1)
    elif candidate.get_accepted() == 1:
        candidate.update_accepted(2)
    elif candidate.get_accepted() == 2:
        candidate.update_accepted(1)
    return custom_response({"success": candidate.get_accepted()}, 200)