import os
import pyrebase
from app import app
from app.forms import LoginForm
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
firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route("/")
def index():
    #form = LoginForm
	testObj = db.child("TestName").get()
	return render_template('/index.html', testObj=testObj)
	#output = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

@app.route("/login", methods=["GET", "POST"])
def loginMain():
	form = LoginForm()
	if request.method=='POST':
	#if form.validate_on_submit():
		flash('one moment..')
		return redirect(url_for('index'))
	return render_template('/loginMain.html', form=form)
