# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask
#API_URL= os.environ['API_URL']


app = Flask(__name__)
app.config['SECRET_KEY']='saroj'
API_URL='http://127.0.0.1:5001'
from todolist import routes
