import os
import qrcode
import io
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore, storage
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

# firebase-admin SDK
cred = credentials.Certificate(app.config['GOOGLE_APPLICATION_CREDS'])
firebase_admin.initialize_app(cred, {
	'storageBucket': app.config["STORAGE_BUCKET"]
})

db = firestore.client()

# google-cloud storage
bucket = storage.bucket()
#storage_client = storage.Client()



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
		# get uploaded file
		f = request.files.get('file')
		
		bucketName = app.config['STORAGE_BUCKET']
		restauId = getRestaurantId(session['uid'])



		# upload to bucket
		locRef = upload_blob(bucketName, f, f.filename,'file')
		# create intial document with image reference
		docUrl = createDocumentFirestore(restauId)
		addFieldToDocument('locationRef',locRef,restauId,docUrl)

		# create qrcode & upload to bucket
		qrCode = createQRCode(docUrl)
		qrCodeName = "QRCODE_" + f.filename
		qrCodePath = os.path.join(os.getcwd()+'/app/uploads', qrCodeName)
		qrCode.save(qrCodePath)
		qrCodeRef = upload_blob(bucketName,qrCodePath,qrCodeName,'qrcode')
		# delete the saved qrcode
		os.remove(qrCodePath)

		# add qrcode to firestore
		addFieldToDocument('QRCode',qrCodeRef,restauId,docUrl)

	return render_template('/upload.html', page="Upload")

@app.route("/base")
def basePage():
	return render_template('/base.html')


"""
<====================== METHODS ==========================>
"""
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

def createQRCode(data):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(f"/{data}")
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	return img

def upload_blob(bucket_name, file, 	dest_blob_name, filetype):
	# upload file to bucket
	blob = bucket.blob(dest_blob_name)

	if filetype is "file":
		blob.upload_from_file(file,content_type="image/jpeg")
	else:
		blob.upload_from_filename(file,content_type="image/jpeg")

	fileUrl = 'gs://' + bucket_name + f"/{dest_blob_name}"
	return fileUrl

def createDocumentFirestore(restauId):
	doc_ref = db.collection(u'Restaurants').document(restauId).collection('items').document()
	docUrl = 'Restaurants' + f"/{restauId}" + "/items" + f"/{doc_ref.id}"
	return docUrl

def addFieldToDocument(key, data, restauID, docUrl):
	data = {
		u'{}'.format(key): data
	}
	doc_ref = db.document(docUrl)
	doc_ref.set(data,merge=True)
	return 

def getRestaurantId(uid):
	# find the restaurant based on user's id
	resta_ref = db.collection(u'Restaurants')
	query_ref = resta_ref.where(u'uid', u'==', u'{}'.format(uid)).stream()

	resta_id=''
	for doc in query_ref:
		resta_id = doc.id

	return resta_id
