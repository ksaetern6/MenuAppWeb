import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from app import app, FireBaseAuth
from app.forms import LoginForm
from flask_login import login_required
from flask import flash, render_template, redirect, url_for, request, session

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

@app.route("/", methods=['GET','POST'])
#@login_required
def index():
	FB_API_KEY = app.config['FIREBASE_API_KEY']
	# get array of locationRef dl links for images and print on frontend
	if request.method == 'POST':
		data = request.get_json()
		print("it doesnt load the page?")
		session['uid'] = data['uid']
		print(data['uid'])

	print(session['uid'])
	# get all items on the menu
	if session['uid']:
		items = getAllItems(session['uid'])
	else:
		items = {}

	return render_template('/index.html', page="Home", FB_API_KEY=FB_API_KEY, data=session['uid'], items=items)

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
	# get post data and add user to fb
	# if request.method == 'POST':
	# 	f = request.get_json()
	# 	redirect(url_for('/upload'))

	return render_template('/loginMain.html', page="Login", FB_API_KEY=FB_API_KEY)

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

def getAllItems(uid):
	# find the restaurant based on user's id
	resta_ref = db.collection(u'Restaurants')
	query_ref = resta_ref.where(u'uid', u'==', u'{}'.format(uid)).stream()

	resta_id=''
	for doc in query_ref:
		resta_id = doc.id

	# go through restaurant's items
	all_items = db.collection(u'Restaurants/{}/items'.format(resta_id)).stream()

	# get all location Refs
	items = {}
	
	for item in all_items:
		item_dict = item.to_dict()
		items[item_dict['locationRef']] = item_dict['QRCode']

	return items