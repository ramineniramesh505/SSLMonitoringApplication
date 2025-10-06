from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Certificate, Base
import os

app = Flask(__name__)

# Database setup
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/sslmanager")
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/")
def home():
    session_db = Session()
    certs = session_db.query(Certificate).all()

    # Calculate days left and status
    for cert in certs:
        if cert.expiry:
            cert.days_left = (cert.expiry - datetime.utcnow().date()).days
            # Determine status
            if cert.days_left < 0:
                cert.status = "Expired"
            elif cert.days_left <= 30:
                cert.status = "Expiring Soon"
            else:
                cert.status = "Active"
        else:
            cert.days_left = "N/A"
            cert.status = "Unknown"

    session_db.close()
    return render_template("index.html", certs=certs)

@app.route("/add", methods=["POST"])
def add_certificate():
    cn = request.form.get("cn")
    expiry_str = request.form.get("expiry")
    notes = request.form.get("notes")
    expiry = None
    if expiry_str:
        try:
            expiry = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        except ValueError:
            expiry = None

    session_db = Session()
    new_cert = Certificate(cn=cn, expiry=expiry, notes=notes)
    session_db.add(new_cert)
    session_db.commit()
    session_db.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:cert_id>", methods=["POST"])
def delete_certificate(cert_id):
    session_db = Session()
    cert = session_db.query(Certificate).filter_by(id=cert_id).first()
    if cert:
        session_db.delete(cert)
        session_db.commit()
    session_db.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
