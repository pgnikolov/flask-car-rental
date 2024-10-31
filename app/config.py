from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-email-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@example.com'
