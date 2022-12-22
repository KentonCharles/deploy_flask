from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.truck_model import Truck

# route to add new recipe form
@app.route('/trucks/new')
def new_truck_form():
    logged_user = User.get_by_id({'id':session['user_id']})
    return render_template('trucks_new.html', logged_user=logged_user)

# action route for processing new recipe w/ redirect to main dashboard
@app.route('/trucks/create', methods=['POST'])
def create_truck():
    # check for user login
    if "user_id" not in session:
        return redirect('/')
    # check for validation
    if not Truck.validator(request.form):
        return redirect('/trucks/new')
    truck_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Truck.create(truck_data)
    return redirect('/dashboard')

# route for displaying details for single recipe
@app.route('/trucks/<int:id>/view')
def get_one_truck(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_truck = Truck.get_one(data)
    logged_user = User.get_by_id({'id':session['user_id']})
    return render_template('trucks_one.html', one_truck=one_truck, logged_user=logged_user)

# route for displaying edit form
@app.route('/trucks/<int:id>/edit')
def edit_truck_form(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_truck = Truck.get_one(data)
    logged_user = User.get_by_id({'id':session['user_id']})
    return render_template('trucks_edit.html', one_truck=one_truck, logged_user=logged_user)

# action route for processing recipe edits
@app.route('/trucks/<int:id>/update', methods =['POST'])
def update_truck(id):
    if "user_id" not in session:
        return redirect('/')
    if not Truck.validator(request.form):
        return redirect(f'/trucks/{id}/edit')
    update_data = {
        **request.form,
        'id':id
    }
    Truck.update(update_data)
    return redirect('/dashboard')

# route to delete recipe(get request)
@app.route('/trucks/<int:id>/delete')
def delete_truck(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Truck.delete(data)
    return redirect('/dashboard')