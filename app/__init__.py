from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import os

db = SQLAlchemy()
DB_NAME = 'database.db'
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # location of db
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2:sha256'
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Default to Gmail if not set
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default to 587 if not set
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Convert to boolean
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'flask.rent.a.car')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'ikmghjzds')
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

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
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
