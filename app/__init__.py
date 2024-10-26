import os
from os import path
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'database.db'
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'ikmghjzds'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.views import views_bp
    from app.auth import auth_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')