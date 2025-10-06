import os
import json
from datetime import datetime
import requests
from requests_kerberos import HTTPKerberosAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Certificate, Base

# ------------------------------
# Database setup
# ------------------------------
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/sslmanager")
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# ------------------------------
# Kerberos / FreeIPA setup
# ------------------------------
# Make sure your keytab is set in environment
# Example: export KRB5_CLIENT_KTNAME=/tmp/ramesh.keytab
IPA_API = "https://ramesh5.core42idm.local/ipa/cert-find"
auth = HTTPKerberosAuth(mutual_authentication=False)

# ------------------------------
# Fetch certificates from FreeIPA
# ------------------------------
def fetch_certificates_from_ipa():
    try:
        response = requests.get(IPA_API, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()
        # FreeIPA returns results in "result" -> "result"
        certs = data.get("result", {}).get("result", [])
        print(f"Fetched {len(certs)} certificates from IPA")
        return certs
    except Exception as e:
        print("Error connecting to IPA:", e)
        return []

# ------------------------------
# Sync to PostgreSQL
# ------------------------------
def sync_certs_to_db():
    certs = fetch_certificates_from_ipa()
    if not certs:
        print("No certificates to sync.")
        return

    session_db = Session()
    for cert in certs:
        cn = cert.get("subject_cn") or cert.get("cn")
        expiry_str = cert.get("not_after")
        expiry = None
        if expiry_str:
            try:
                expiry = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S").date()
            except Exception:
                expiry = None
        notes = cert.get("description", "")

        # check if CN exists
        existing = session_db.query(Certificate).filter_by(cn=cn).first()
        if existing:
            existing.expiry = expiry
            existing.notes = notes
        else:
            new_cert = Certificate(cn=cn, expiry=expiry, notes=notes)
            session_db.add(new_cert)

    session_db.commit()
    session_db.close()
    print(f"Synced {len(certs)} certificates into database.")

# ------------------------------
# Run sync
# ------------------------------
if __name__ == "__main__":
    sync_certs_to_db()

