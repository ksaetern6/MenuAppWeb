import pyrebase

class FireBaseAuth():
	def __init__(self, firebase):
		self.firebase = firebase
	
	def getFireBaseRef(self):
		auth = self.firebase.auth()
		return auth
	
	def fireBaseLoginUser(self,email,password):
		auth = self.getFireBaseRef()
		user = auth.sign_in_with_email_and_password(email,password)
		return user
	
