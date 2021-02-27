from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import DB, Credential


def create_app():
    """Create Flask Application"""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'asdf1234'
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    DB.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return Credential.query.get(int(userid))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app