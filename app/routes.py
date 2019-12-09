import os
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from app import app, FireBaseAuth
from app.forms import LoginForm
from flask_login import login_required
from flask import flash, render_template, redirect, url_for, request

config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": "menuapp-f3764.firebaseapp.com",
    "databaseURL": "https://menuapp-f3764.firebaseio.com",
    "projectId": "menuapp-f3764",
    "storageBucket": "menuapp-f3764.appspot.com",
    "messagingSenderId": "77920760117",
    "appId": "1:77920760117:web:67cf1a4799eb73e064dc7c",
    "serviceAccount": "app/firebase-private-key.json",
    "measurementId": "G-33NWQZKM7W"

}
#Firebase SDK ADC
#default_app = firebase_admin.initialize_app()

#pyrebase package
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

#firebase-admin SDK
cred = credentials.Certificate(app.config['GOOGLE_APPLICATION_CREDS'])
firebase_admin.initialize_app(cred)

db = firestore.client()
user_ref = db.collection(u'Restaurants')
docs=user_ref.stream()

@app.route("/")
#@login_required
def index():
	# get array of locationRef dl links for images and print on frontend
	# 

	return render_template('/index.html', gdocs=docs)

@app.route("/debugLogin", methods=["GET", "POST"])
def debugLoginPage():
	form = LoginForm()
	#if request.method=='POST':
	if request.method=="POST":
		# flash(request.form["email"])
		# flash(request["password"])
		# flash('one moment..')
		# validate user using firebase
		# login_user
		# next
		return redirect(url_for('index'))

	return render_template('/debugLogin.html', form=form)

@app.route("/login")
def loginMain():
	FB_API_KEY = app.config['FIREBASE_API_KEY']
	return render_template('/loginMain.html', FB_API_KEY=FB_API_KEY)

@app.route("/upload", methods=['GET', 'POST'])
def uploadMain():
	if request.method == 'POST':
		f = request.files.get('file')
		# f.save(os.path.join(os.getcwd()+'/app/uploads', f.filename))
		# db.child('')
		# get QRcode of image
		# upload images to firebase
		# upload locationRef of both QRCode and Image to firestore
	return render_template('/upload.html')

@app.route("/base")
def basePage():
	return render_template('/base.html')