from core.database import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, index=True, nullable=False)  # optional
    name = db.Column(db.String(255), nullable=False, index=True)
    hsn = db.Column(db.String(50))
    mrp = db.Column(db.Numeric(12,2))
    rate = db.Column(db.Numeric(12,2))
    pack = db.Column(db.String(50))  # e.g. '10 Cs'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
