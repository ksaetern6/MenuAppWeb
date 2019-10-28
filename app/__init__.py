import os
from flask import Flask
#from dotenv import load_dotenv

app=Flask(__name__)
#load_dotenv=("../.flaskenv")

from app import routes
