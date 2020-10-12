import os,binascii
from flask import Flask, render_template, redirect, g, request, url_for, jsonify, Response
import urllib
import json
from flask_sqlalchemy import SQLAlchemy
#from flask_restful import Api, Resource
import pymysql

from flask_bcrypt import Bcrypt # For Encrypting password
bcrypt=Bcrypt()


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = binascii.hexlify(os.urandom(12))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://<user>:<password>@<dbname>:3606/intv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80) , unique=True, nullable=False)
    email = db.Column(db.String(120) , unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #entry = db.relationship('entries',backref='username',lazy=True)

    def __repr__(self):
        return f"users('{self.username}')"

class entries(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    what_to_do = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20),nullable=False)
    status= db.Column(db.String(20))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)


    def __repr__(self):
        return f"entries('{self.what_to_do}','{self.due_date}','{self.status}')"


@app.route("/")
def home():
    return "<h1>This is Flask API page</h1>" # API landing page vanilla

@app.route("/api/items/<user_id>")
def show_items(user_id):
    user_id= urllib.parse.unquote(user_id)
    try:
        entry=entries.query.filter_by(user_id=user_id).all()
        if entry:
            tdlist=[]
            for i in entry:
                tdlistn = dict(user_id=i.user_id,
                          what_to_do=i.what_to_do,
                          due_date=i.due_date,
                          status=i.status)
                tdlist.append(tdlistn)
            return json.dumps(tdlist),200
        print(tdlist)
        return jsonify(tdlist), 200
    except:
        return {'message':"No records"},404


@app.route("/api/items/<user_id>", methods=['GET','POST']) #,defaults ={'status':'processing'})
def add_item(user_id):
    what_to_do = urllib.parse.unquote(request.json['what_to_do'])
    due_date = urllib.parse.unquote(request.json['due_date'])
    status = urllib.parse.unquote(request.json['status'])
    user_id = urllib.parse.unquote(user_id)
    try:
        entry =entries( what_to_do=what_to_do,due_date=due_date,status=status,user_id=user_id)
        print(entry)
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": "record added"})
    except:
        return jsonify({"result": "failed to add"}),302

@app.route("/api/items/<user_id>/<item>", methods=['DELETE'])
def delete_item(user_id,item):
    user_id = urllib.parse.unquote(user_id)
    item = urllib.parse.unquote(item)
    #db = get_db()
    query=entries.query.filter_by(user_id=user_id,what_to_do=item).first()
    db.session.delete(query)
    db.session.commit()
    return jsonify({"result": True})


@app.route("/api/items/<user_id>/<item>/<status>", methods=['PUT'])
def update_item(user_id, item,status):
    item = urllib.parse.unquote(item)
    user_id = urllib.parse.unquote(user_id)
    status = urllib.parse.unquote(status)
    check_entry = entries.query.filter_by(user_id=user_id,status=status,what_to_do=item).first()
    if check_entry:
        check_entry.status='done'
        db.session.commit()
    return jsonify({"message": "nothing updated"})

@app.route("/api/users", methods=['POST'])
def create_user():
    username = urllib.parse.unquote(request.json['username'])
    email = urllib.parse.unquote(request.json['email'])
    password = urllib.parse.unquote(request.json['password'])
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        user= users(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "user created"})
    except:
        return jsonify({"message": "Unable to register at this time"}), 302


@app.route("/api/user",methods=['POST'])
def validate_user():
    username = urllib.parse.unquote(request.json['username'])
    password = urllib.parse.unquote(request.json['password'])
    if username and password:
        entry = users.query.filter_by(username=username).first()

        if username == entry.username and bcrypt.check_password_hash(entry.password, password):
            return jsonify({"username": entry.username, "user_id":entry.id}),200
        else:
            return jsonify({"message": "username not found ,please register"}),404


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True,host="0.0.0.0", port=5001)


