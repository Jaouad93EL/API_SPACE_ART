
class Development(object):
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = "SpaceArt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:j19991106@localhost:5432/SpaceArt?sslmode=disable"

class Production(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:j19991106@localhost:5433/SpaceArt?sslmode=disable"
    JWT_SECRET_KEY = "SpaceArt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


send_mail = None

app_config = {
    'development': Development,
    'production': Production,
}
