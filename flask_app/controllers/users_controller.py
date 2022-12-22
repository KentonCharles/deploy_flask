from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.truck_model import Truck

bcrypt = Bcrypt(app)

# route for main registration/login page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# action route for processing user registration
@app.route('/users/register', methods=['POST'])
def register_user():
    # check for validation
    if not User.validator(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':hashed_pass,
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect ('/dashboard')

# action route for processing login
@app.route('/users/login', methods=['POST'])
def user_login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid credentails', 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid credentails', 'log')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# route for logout
@app.route('/users/logout')
def user_logout():
    session.clear()
    return redirect('/')


# route for main dashboard
@app.route('/dashboard')
def user_dash():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_trucks = Truck.get_all()
    return render_template('welcome.html', logged_user=logged_user, all_trucks=all_trucks)