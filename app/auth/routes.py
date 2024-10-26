from flask import request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app.models import User
from app import db
from . import auth_bp


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

            return redirect(url_for('views.index'))

    return render_template('sign_up.html', user=current_user)
