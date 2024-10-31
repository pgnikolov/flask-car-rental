from flask import request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
from app.models import User
from app import db
from . import auth_bp
from app import mail


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if not user.is_verified:
                flash('Please confirm your email address first.', 'warning')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please log in instead.", category='error')
        elif len(email) < 4:
            flash("Email must be at least 4 characters long", category='error')
        elif len(first_name) < 2:
            flash("First name must be at least 2 characters long", category='error')
        elif len(last_name) < 2:
            flash("Last name must be at least 2 characters long", category='error')
        elif password1 != password2:
            flash("Passwords do not match", category='error')
        elif len(password1) < 4:
            flash("Password must be at least 7 characters long", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                is_verified=False
            )
            db.session.add(new_user)
            db.session.commit()

            send_verification_email(new_user.email)
            flash('A confirmation email has been sent to your email address.', 'info')

            return redirect(url_for('views.index'))

    return render_template('sign_up.html', user=current_user)


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email


def send_verification_email(user_email):
    token = generate_token(user_email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    msg = Message("Confirm Your Email", recipients=[user_email])
    msg.body = f"Click the link to confirm your email: {confirm_url}"
    mail.send(msg)


@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account already confirmed. Please log in.', 'success')
    else:
        user.is_verified = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')

    return render_template('confirm_email.html')
