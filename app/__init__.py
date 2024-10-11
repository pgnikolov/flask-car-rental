from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.track_modifications import models_committed

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # location of db
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2:sha256'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .cars import cars_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(cars_bp, url_prefix='/')

    from .models import User, Car, RentalHistory
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    # redirect if not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
