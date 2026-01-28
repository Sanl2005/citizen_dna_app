import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_user_by_mobile(mobile):
    doc = db.collection("digilocker_users").document(mobile).get()
    if doc.exists:
        return doc.to_dict()
    return None
