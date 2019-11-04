import os
from flask import Flask
from config import Config
#from dotenv import load_dotenv

app=Flask(__name__)
app.config.from_object(Config)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from app import routes
