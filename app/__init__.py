import os
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from app.auth.FBAuth import FireBaseAuth
#from dotenv import load_dotenv

app=Flask(__name__)


"""
Flask_Login
"""
login = LoginManager(app)
login.login_view='loginMain'

"""
config file from Config class
"""
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object(Config)
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

"""
Flask_Dropzone
"""
dropzone = Dropzone(app)

from app import routes
