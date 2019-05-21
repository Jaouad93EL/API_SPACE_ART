from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import create_app, db
from src import UserModel
from src import ProfileModel
from src import FollowModel
from src import AudioModel
from src import VideoModel
from src import NewsfeedModel
from src import RevokedTokenModel


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