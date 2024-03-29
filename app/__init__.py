from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import db
from app.admin.views import blueprint as admin_blueprint
from app.event.views import blueprint as event_blueprint
from app.user.models import User
from app.user.views import blueprint as user_blueprint




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(event_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    return app
