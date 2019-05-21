from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.app import create_app, db
from src.models import UserModel
from src.models import ProfileModel
from src.models import FollowModel
from src.models import AudioModel
from src.models import VideoModel
from src.models import NewsfeedModel
from src.models import RevokedTokenModel


u = UserModel
p = ProfileModel
f = FollowModel
a = AudioModel
v = VideoModel
n = NewsfeedModel
r = RevokedTokenModel

app = create_app()
migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()