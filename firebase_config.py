import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase key
cred = credentials.Certificate("firebase_key.json")

# Initialize app
firebase_admin.initialize_app(cred)

# Firestore DB
db = firestore.client()