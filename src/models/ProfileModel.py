import datetime
from marshmallow import fields, Schema
from . import db

class ProfileModel(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    picture_name_storage = db.Column(db.String(255), nullable=True)
    banner_name_storage = db.Column(db.String(255), nullable=True)
    picture_url = db.Column(db.String(255), nullable=True)
    banner_url = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    size = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data, user_id):
        self.picture_url = "empty"
        self.banner_url = "empty"
        self.age = data.get('age')
        self.size = data.get('size')
        self.weight = data.get('weight')
        self.description = data.get('description')
        self.city = data.get('city')
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def picture_profile(self, url, file_name):
        setattr(self, 'picture_url', url)
        setattr(self, 'picture_name_storage', file_name)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def banner_profile(self, url, file_name):
        setattr(self, 'banner_url', url)
        setattr(self, 'banner_name_storage', file_name)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_one_profile(user_id):
        return ProfileModel.query.filter_by(user_id=user_id).first()

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    picture_name_storage = fields.Str(required=False)
    banner_name_storage = fields.Str(required=False)
    picture_url = fields.Str(required=False)
    banner_url = fields.Str(required=False)
    age = fields.Int(required=False)
    size = fields.Int(required=False)
    weight = fields.Int(required=False)
    description = fields.Str(required=False)
    user_id = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)