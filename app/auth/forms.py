from flask import flash, render_template
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_login import current_user
from wtforms.fields.simple import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User
from .. import  db
from . import auth_bp
