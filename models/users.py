from core.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")   # admin / supplier / user
    state = db.Column(db.String(50), nullable=True)   # e.g. "UP", "MP"
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)  # For supplier users
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier = db.relationship("Supplier", backref="users", foreign_keys=[supplier_id])
