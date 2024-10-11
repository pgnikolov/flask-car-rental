from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # user is logged in until other activities
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout_confirmation')
@login_required
def logout_confirmation():
    return render_template('logout.html', user=current_user)


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'), )


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # Check if the email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please log in instead.", category='error')

        elif len(email) < 4:
            flash("Email must be at least 4 characters long", category='error')
        elif len(first_name) < 2:
            flash("First name must be at least 2 characters long", category='error')
        elif len(last_name) < 2:
            flash("Last name must be at least 2 characters long", category='error')
        elif password1!= password2:
            flash("Passwords do not match", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters long", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created successfully", category='success')
            return redirect(url_for('views.index'))

    return render_template('sign_up.html', user=current_user)