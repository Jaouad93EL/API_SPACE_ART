import datetime
from marshmallow import fields, Schema
from . import db

class LikeModel(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
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
    def get_like_all(user_id):
        return LikeModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_one_like(id):
        return LikeModel.query.filter_by(id=id).first()

    @staticmethod
    def get_one_like_by_user_id(like_id, user_id):
        return LikeModel.query.filter_by(id=like_id, user_id=user_id).first()

    @staticmethod
    def get_nb_like_post_id(post_id):
        return LikeModel.query.filter_by(post_id=post_id).first()

    @staticmethod
    def get_one_if_liked(post_id, user_id):
        return LikeModel.query.filter_by(post_id=post_id, user_id=user_id).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    post_id = fields.Int(required=True)
    user_id = fields.Int(required=False)
    news_id = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)