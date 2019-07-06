import datetime
from marshmallow import fields, Schema
from . import db

class CastModel(db.Model):
    __tablename__ = 'cast'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(128), nullable=True)
    online = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data, user_id):
        self.title = data.get('title')
        self.description = data.get('description')
        self.address = data.get('address')
        self.online = data.get('online')
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
    def get_cast_all():
        return CastModel.query.all()

    @staticmethod
    def get_one_cast_by_title(title):
        return CastModel.query.filter_by(title=title).first()

    @staticmethod
    def get_one_cast_by_id(id):
        return CastModel.query.filter_by(id=id).first()

    @staticmethod
    def get_my_cast(cast_id, user_id):
        return CastModel.query.filter_by(id=cast_id, user_id=user_id).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

class CastSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    address = fields.Str(required=False)
    online = fields.Int(required=True)
    user_id = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)