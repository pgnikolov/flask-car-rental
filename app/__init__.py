from flask import Flask
from flask_login import LoginManager
from .extensions.database import db
from app.models.car import Car
from app.models.user import User
from app.models.rental import RentalHistory


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    if not app.config.get('SECRET_KEY'):
        raise ValueError("No SECRET_KEY set for Flask application")

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.auth import auth_bp
    from app.cars import cars_bp
    from app.rentals import rentals_bp
    from app.views import views_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cars_bp, url_prefix='/cars')
    app.register_blueprint(rentals_bp, url_prefix='/rentals')
    app.register_blueprint(views_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app