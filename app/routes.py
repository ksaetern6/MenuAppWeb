import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
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

#firebase-admin SDK
cred = credentials.Certificate(app.config['GOOGLE_APPLICATION_CREDS'])
firebase_admin.initialize_app(cred)

db = firestore.client()
user_ref = db.collection(u'Restaurants')
docs=user_ref.stream()

@app.route("/", methods=['GET','POST'])
#@login_required
def index():
	FB_API_KEY = app.config['FIREBASE_API_KEY']
	# get array of locationRef dl links for images and print on frontend
	data={}
	if request.method == 'POST':
		data = request.get_json()
		print(data)
	return render_template('/index.html', FB_API_KEY=FB_API_KEY, gdocs=docs, data=data)

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

@app.route("/login", methods=["POST", "GET"])
def loginMain():
	FB_API_KEY = app.config['FIREBASE_API_KEY']
	f = "string"
	# get post data and add user to fb
	if request.method == 'POST':
		f = request.get_json()
		redirect(url_for('/upload'))

	return render_template('/loginMain.html', data=f, FB_API_KEY=FB_API_KEY)

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