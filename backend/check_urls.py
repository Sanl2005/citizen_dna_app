import requests
import models
import database

# Initialize DB Session
db = database.SessionLocal()
schemes = db.query(models.Scheme).all()

print(f"Checking {len(schemes)} schemes...")

for s in schemes:
    url = s.apply_url
    if not url:
        print(f"[MISSING] {s.scheme_name}")
        continue
        
    try:
        # verify=False to avoid SSL errors on some gov sites which have bad certs
        resp = requests.get(url, timeout=5, verify=False)
        if resp.status_code >= 400:
             print(f"[FAIL {resp.status_code}] {s.scheme_name}: {url}")
        else:
             print(f"[OK] {s.scheme_name}")
    except Exception as e:
        print(f"[ERROR] {s.scheme_name}: {url} -> {str(e)}")

db.close()
