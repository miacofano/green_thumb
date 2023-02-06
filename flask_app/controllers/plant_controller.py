from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.plant_model import Plant
from flask_app.models.user_model import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    plants = Plant.get_plants_with_user()
    return render_template('dashboard.html', user = user, all_plants = plants)

@app.route('/plants/new')
def new_plant():
    if'user_id' not in session:
        return redirect('/user/login')
    return render_template('plant_new.html')

@app.route('/plants/new/create', methods=['POST'])
def create_plant():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "name": request.form['name'],
        "water": request.form['water'],
        "light": request.form['light'],
        "food": request.form['food'],
        "user_id": session['user_id']
    }
    Plant.save(data)
    return redirect('/dashboard')

@app.route('/plants/delete/<int:id>')
def delete_plant(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Plant.delete({'id':id})
    return redirect('/dashboard')