# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask
#API_URL= os.environ['API_URL']


app = Flask(__name__)
app.config['SECRET_KEY']='addanythingbetterthanthis'
API_URL='http://127.0.0.1:5001'  # use your API hosted IP address, port
from todolist import routes
