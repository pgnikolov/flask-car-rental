from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.track_modifications import models_committed

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # location of db
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .cars import cars_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(cars_bp, url_prefix='/cars')

    from .models import User, Car, RentalHistory
    with app.app_context():
        db.create_all()

    return app
