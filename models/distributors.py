from core.database import db
from datetime import datetime

class Distributor(db.Model):
    __tablename__ = "distributors"

    id = db.Column(db.Integer, primary_key=True)

    # Auto-generated unique key (name + pincode)
    unique_key = db.Column(db.String(200), unique=True)

    name = db.Column(db.String(200))
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    gstin = db.Column(db.String(30))
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
