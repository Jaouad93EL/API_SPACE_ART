class Development(object):
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = "SpaceArt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:j19991106@localhost:5432/SpaceArt?sslmode=disable"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'elhorm_j@etna-alternance.net'
    MAIL_PASSWORD = 'j19991106'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MONGO_URI = "mongodb://localhost:27017/SpaceArt"

class Production(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:j19991106@localhost:5433/SpaceArt?sslmode=disable"
    JWT_SECRET_KEY = "SpaceArt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'elhorm_j@etna-alternance.net'
    MAIL_PASSWORD = 'j19991106'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MONGO_URI = "mongodb://localhost:27017/SpaceArt"


app_config = {
    'development': Development,
    'production': Production,
}
