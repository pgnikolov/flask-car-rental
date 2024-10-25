import os
import secrets


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_NAME = 'database.db'

    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
