from flask import Flask
from .extensions.database import db
from .extensions.login_manager import login_manager
from app.models.car import Car
from app.models.user import User
from app.models.rental import RentalHistory


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    if not app.config.get('SECRET_KEY'):
        raise ValueError("No SECRET_KEY set for Flask application")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .cars import cars_bp
    from .rentals import rentals_bp
    from .views import views_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cars_bp, url_prefix='/cars')
    app.register_blueprint(rentals_bp, url_prefix='/rentals')
    app.register_blueprint(views_bp)

    return app