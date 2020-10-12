from flask import Flask, render_template, redirect, g, request, url_for, jsonify, flash
import json, requests
import urllib.request
import os
from todolist import app
from todolist.forms import LoginForm, RegistrationForm,TodoForm
from todolist.newsreaders import News

API_URL='http://127.0.0.1:5001'
#API_URL='http://0.0.0.0:5001'

@app.route("/")  #dont override decorator, not a good idea
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    username= form.username.data
    password = form.username.data
    if username and password:
        try:
            resp= requests.post(url=API_URL + '/api/user', json={"username": username,"password": password })
            resp = resp.json()
            print(resp)
            if resp['username']:
                flash(f'Welcome to the todolist page: '+ username, 'success')
                return redirect(url_for('show_list',user_id=resp['user_id']))
            else:
                flash(f'No such user account exists, please register', 'danger')
                return redirect(url_for('register',user_id=resp['user_id']))
        except:
            flash(f'No such user , try again later', 'danger')
            return render_template('home.html')
    return render_template('login.html', form=form)

@app.route("/show_list/<user_id>", methods=['GET','POST'])
def show_list(user_id):
    user_id=urllib.parse.quote(user_id)
    try:
        response = requests.get(API_URL + "/api/items/" + user_id)
        print(response)
        entries = response.json()
        print(entries)
        if entries:
            redirect(url_for('add_entry', user_id=user_id))
            return render_template('index.html',user_id=user_id, entries=entries)
        else:
            return render_template('index.html', user_id=user_id, entries=entries)
    except:
        redirect(url_for('add_entry',user_id=user_id))
        return render_template('index.html',user_id=user_id, title='Add tasks')

@app.route("/register",methods=['GET','POST'])
def register():
    form= RegistrationForm()
    username = form.username.data
    password = form.password.data
    email = form.email.data
    try:
        validate=requests.post(url=API_URL + '/api/user',json={"username": username, "password": password})
        if validate.status_code ==200:
            print("user already exists, try to login")
            flash(f'You already have an acccount','info')
            return redirect(url_for('login'))
        result =requests.post(url=API_URL + '/api/users',json={"username": username, "password": password,'email':email})
        if result.status_code == 200:
            flash(f'You may now login : ' + request.form['username'], 'success')
            return redirect(url_for('login'))
        return render_template('register.html',form=form)
    except:
        flash(f'API is down, try again later!', 'danger')
        return render_template('home.html')

@app.route("/add/<user_id>", methods=['POST'])
def add_entry(user_id):
    user_id = urllib.parse.quote(user_id)
    try:
        entry=requests.post( url=API_URL+'/api/items/'+user_id,json={
                  "what_to_do": request.form['what_to_do'],
                   "due_date": request.form['due_date'],
                   "status" : request.form['status']
                  })

        if entry.status_code == 200:
            flash("item added successfully", 'success')
            return redirect(url_for('show_list', user_id=user_id))
        return render_template('index.html',user_id=user_id)
    except:
        return render_template('index.html',user_id=user_id )

@app.route('/logout', methods=['GET'])
def logout():
    flash('Logged out.','info')
    return redirect(url_for('home'))

@app.route("/delete/<user_id>/<item>")
def delete_entry(user_id,item):
    user_id = urllib.parse.quote(user_id)
    item = urllib.parse.quote(item)
    try:
        entry= requests.delete(url=API_URL+'/api/items/'+ user_id +'/' +item )
        print(entry, entry.status_code)
        #if entry.status_code == 200:
        flash("Item deleted",'success')
    except:
        flash("could not delete item",'danger')
    return redirect(url_for('show_list',user_id=user_id))

@app.route("/mark/<user_id>/<item>/<status>")
def mark_as_done(user_id,item,status):
    user_id = urllib.parse.quote(user_id)
    item = urllib.parse.quote(item)
    status =urllib.parse.quote(status)
    print(user_id, item, status)
    if user_id and item and status:
        try:
            requests.put(url=API_URL+'/api/items/'+ user_id +'/' + item + '/' +status)
            flash("updated " +item , 'success')
            return redirect(url_for('show_list',user_id=user_id))
        except:
            flash("Could not update " + item ,'danger' )
    else:
        flash('No items to update','info')
    return redirect(url_for('show_list',user_id=user_id))

# this route calls NEWS API 
@app.route("/news")
def news():
    headlines = News().getNews()
    return render_template('news.html',title='Breaking News', headlines=headlines)
