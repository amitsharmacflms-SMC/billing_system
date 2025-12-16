from core.database import db
from datetime import datetime

class Distributor(db.Model):
    __tablename__ = "distributors"

    id = db.Column(db.Integer, primary_key=True)

    unique_key = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(150))

    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    gstin = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(255))

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))
    supplier = db.relationship("Supplier", backref="distributors")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
