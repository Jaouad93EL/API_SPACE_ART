import datetime
from marshmallow import fields, Schema
from . import db

class FollowModel(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    follow_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, follow_id, user_id):
        self.follow_id = follow_id
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_follow(follow_id, user_id):
        return (FollowModel.query.filter_by(follow_id=follow_id, user_id=user_id)).first()

    @staticmethod
    def get_all_following(user_id):
        return (FollowModel.query.filter_by(user_id=user_id)).all()

    @staticmethod
    def get_all_followers(user_id):
        return (FollowModel.query.filter_by(follow_id=user_id)).all()

    def __repr(self):
        return '<id {}>'.format(self.id)


class FollowSchema(Schema):
    id = fields.Int(dump_only=True)
    follow_id = fields.Int(required=False)
    user_id = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

class MiniInfo:
    def __init__(self, id, firstname, lastname, picture_url):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.picture_url = picture_url