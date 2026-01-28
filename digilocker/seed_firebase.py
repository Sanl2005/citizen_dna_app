import firebase_admin
from firebase_admin import credentials, firestore

# ---------- INIT FIREBASE ----------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- SAMPLE USERS ----------
users = {
    "9876543210": {
        "name": "Ravi Kumar",
        "documents": [
            {
                "name": "Aadhaar Card",
                "doctype": "ADHAR",
                "issuer": "UIDAI",
                "uri": "/static/docs/9876543210/aadhaar.pdf"
            },
            {
                "name": "Income Certificate",
                "doctype": "INCER",
                "issuer": "State Government",
                "uri": "/static/docs/9876543210/income_certificate.pdf"
            }
        ]
    },

    "9123456789": {
        "name": "Ananya Sharma",
        "documents": [
            {
                "name": "Aadhaar Card",
                "doctype": "ADHAR",
                "issuer": "UIDAI",
                "uri": "in.gov.uidai-aadhaar-ananya"
            },
            {
                "name": "Degree Marksheet",
                "doctype": "MARKS",
                "issuer": "Anna University",
                "uri": "in.edu.au-marks-ananya"
            }
        ]
    },

    "9012345678": {
        "name": "Karthik R",
        "documents": [
            {
                "name": "Driving License",
                "doctype": "DL",
                "issuer": "Transport Department",
                "uri": "in.gov.tn-dl-karthik"
            }
        ]
    },

    "9345678901": {
        "name": "Sneha Iyer",
        "documents": [
            {
                "name": "PAN Card",
                "doctype": "PAN",
                "issuer": "Income Tax Department",
                "uri": "in.gov.itd-pan-sneha"
            }
        ]
    },

    "9988776655": {
        "name": "Arjun Patel",
        "documents": [
            {
                "name": "Aadhaar Card",
                "doctype": "ADHAR",
                "issuer": "UIDAI",
                "uri": "in.gov.uidai-aadhaar-arjun"
            },
            {
                "name": "Voter ID",
                "doctype": "VOTER",
                "issuer": "Election Commission of India",
                "uri": "in.gov.eci-voter-arjun"
            }
        ]
    }
}

# ---------- SEED DATA ----------
collection_ref = db.collection("digilocker_users")

for mobile, data in users.items():
    collection_ref.document(mobile).set(data)
    print(f"Seeded DigiLocker data for {mobile}")

print("✅ Firebase seeding completed successfully.")
