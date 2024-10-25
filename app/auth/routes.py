from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from .forms import LoginForm
from app.models.user import User
from . import auth_bp
from werkzeug.security import check_password_hash
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))
