import datetime
from marshmallow import fields, Schema
from . import db
from ..app import bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    right = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.right = 0
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(data.get('password'))
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def update_right(self, r):
        self.right = r
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def __generate_hash(password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.filter_by(id=id).first()

    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    right = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)