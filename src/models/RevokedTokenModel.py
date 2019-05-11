from . import db

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.Text())

    def __init__(self, jwt):
        self.jti = jwt

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        return RevokedTokenModel.query.filter_by(jti=jti).first()

