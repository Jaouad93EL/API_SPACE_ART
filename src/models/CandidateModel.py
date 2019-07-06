import datetime
from marshmallow import fields, Schema
from . import db

class CandidateModel(db.Model):
    __tablename__ = 'candidate'
    id = db.Column(db.Integer, primary_key=True)
    motivate = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cast_id = db.Column(db.Integer, db.ForeignKey('cast.id'), nullable=False)
    accepted = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, motivate, user_id, cast_id):
        self.motivate = motivate
        self.user_id = user_id
        self.cast_id = cast_id
        self.accepted = 0
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

    def update_accepted(self, val):
        setattr(self, 'accepted', val)
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_candidates_by_cast_id(cast_id):
        return CandidateModel.query.filter_by(cast_id=cast_id).all()

    @staticmethod
    def get_one_post(id):
        return CandidateModel.query.filter_by(id=id).first()

    @staticmethod
    def get_one_candidate_by_cast_id(cast_id, user_id):
        return CandidateModel.query.filter_by(cast_id=cast_id, user_id=user_id).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

    def get_accepted(self):
        return self.accepted

class CandidateSchema(Schema):
    id = fields.Int(dump_only=True)
    motivate = fields.Str(required=False)
    user_id = fields.Int(required=False)
    cast_id = fields.Int(required=False)
    accepted = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)