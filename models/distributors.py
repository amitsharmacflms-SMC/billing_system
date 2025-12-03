from core.database import db
from datetime import datetime

class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    gstin = db.Column(db.String(30))
    state = db.Column(db.String(100))
    state_code = db.Column(db.String(5))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
