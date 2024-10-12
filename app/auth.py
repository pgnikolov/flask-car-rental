from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from .models import User
from . import db, mail
import config

auth = Blueprint('auth', __name__)

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth.route('/sign_up', methods=['GET', 'POST'])
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
        elif len(password1) < 7:
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

            # Създаване на токен за потвърждение на имейла
            s = get_serializer()
            token = s.dumps(email, salt='email-confirm')
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            subject = "Please confirm your email"

            # Създаване на съобщението
            msg_body = f"Please confirm your email by clicking on the following link: {confirm_url}"

            # Изпращане на имейл за потвърждение
            send_email(
                current_app,
                email,
                subject,
                msg_body  # Използвай генерирания текст вместо шаблон
            )

            flash("A confirmation email has been sent to your email address.", category='success')
            return redirect(url_for('views.index'))

    return render_template('sign_up.html', user=current_user)

def send_email(app, to, subject, template, **kwargs):
    with app.app_context():
        msg_body = kwargs.get('msg_body', '')
        msg = Message(subject, recipients=[to], sender=current_app.config['MAIL_DEFAULT_SENDER'])
        msg.body = msg_body
        mail.send(msg)


@auth.route('/confirm/<token>')
def confirm_email(token):
    s = get_serializer()  # Initialize the serializer
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        flash("The confirmation link is invalid or has expired.", category='error')
        return redirect(url_for('views.index'))

    user = User.query.filter_by(email=email).first()
    if user.is_verified:
        flash("Email already confirmed. Please log in.", category='info')
    else:
        user.is_verified = True
        db.session.commit()
        flash("Email confirmed! You can now log in.", category='success')

    return redirect(url_for('views.index'))
