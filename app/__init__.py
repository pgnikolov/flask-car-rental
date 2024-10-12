from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os

db = SQLAlchemy()
DB_NAME = 'database.db'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # location of db
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2:sha256'
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    mail.init_app(app)
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
