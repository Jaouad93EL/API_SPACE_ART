import datetime
from marshmallow import fields, Schema
from . import db

class NewsfeedModel(db.Model):
    __tablename__ = 'newsfeed'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, type, parent_id, user_id):
        self.type = type
        self.parent_id = parent_id
        self.user_id = user_id
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

    @staticmethod
    def get_news_all(user_id):
        return NewsfeedModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_one_news_by_user_id(news_id, user_id):
        return NewsfeedModel.query.filter_by(parent_id=news_id, user_id=user_id).first()

    @staticmethod
    def get_one_news_by_user_id_and_parent_id(parent_id, user_id):
        return NewsfeedModel.query.filter_by(parent_id=parent_id, user_id=user_id).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

    def get_parent_id(self):
        return self.parent_id

class NewsfeedSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)
    parent_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)