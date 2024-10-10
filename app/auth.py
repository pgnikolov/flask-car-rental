from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html', boolean=True)

@auth.route('/logout', methods=['POST'])
def logout():
    return '<p>logout</p>'

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if len(email) < 4:
            flash("Email must be at least 4 characters long", category='error')
        elif len(firstName) < 2:
            flash("First name must be at least 2 characters long", category='error')
        elif len(lastName) < 2:
            flash("Last name must be at least 2 characters long", category='error')
        elif password1!= password2:
            flash("Passwords do not match", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters long", category='error')
        else:
            flash("Account created successfully", category='success')
    return render_template('sign_up.html')