import datetime
from marshmallow import fields, Schema
from . import db

class VideoModel(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    video_name_storage = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data, user_id, video_titre_storage, url):
        self.titre = data.get('titre')
        self.description = data.get('description')
        self.email = data.get('email')
        self.user_id = user_id
        self.url = url
        self.video_name_storage = video_titre_storage
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def update_url(self, url, file_name):
        setattr(self, 'url', url)
        setattr(self, 'video_name_storage', file_name)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_video_by_name_and_user(video_name, user_id):
        return VideoModel.query.filter_by(video_name_storage=video_name, user_id=user_id).first()

    @staticmethod
    def get_video_by_titre(titre):
        return VideoModel.query.filter_by(titre=titre).first()

    @staticmethod
    def get_video_by_id(id):
        return VideoModel.query.filter_by(id=id).first()

    @staticmethod
    def get_video_all(user_id):
        return VideoModel.query.filter_by(user_id=user_id).all()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

class VideoSchema(Schema):
    id = fields.Int(dump_only=True)
    titre = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=False)
    url = fields.Str(required=False)
    video_name_storage = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)