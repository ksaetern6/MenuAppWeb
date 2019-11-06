import os
from flask import Flask
from config import Config
from flask_login import LoginManager
from app.auth.FBAuth import FireBaseAuth
#from dotenv import load_dotenv

app=Flask(__name__)

"""
config file from Config class
"""
app.config.from_object(Config)

"""
Flask_Login
"""
login = LoginManager(app)
login.login_view='loginMain'

from app import routes
