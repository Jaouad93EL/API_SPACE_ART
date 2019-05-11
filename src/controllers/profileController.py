from flask import request, json, Response, Blueprint, g
from ..models.ProfileModel import ProfileModel, ProfileSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth

profile_api = Blueprint('profile', __name__)
profile_schema = ProfileSchema()

