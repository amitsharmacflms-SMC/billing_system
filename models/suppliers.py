from core.database import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)

    unique_key = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(150))

    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    state_code = db.Column(db.String(5))
    pincode = db.Column(db.String(10))

    gstin = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
