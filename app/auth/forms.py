from flask import flash, render_template
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_login import current_user
from wtforms.fields.simple import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models.user import User
from .. import  db
from . import auth_bp

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():  # Handles POST and validation
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please log in instead.", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                is_verified=False
            )
            db.session.add(new_user)
            db.session.commit()

    # Renders template with the form
    return render_template('auth/sign_up.html', form=form, user=current_user)

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
