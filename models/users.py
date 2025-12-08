from core.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Matches your DB
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))

    role = db.Column(db.String(50), default="user")
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    supplier_id = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(50), nullable=True)

    # helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
