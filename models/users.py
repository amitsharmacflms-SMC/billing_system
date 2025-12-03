from core.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(300))
    role = db.Column(db.String(50))

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify(self, pw):
        return check_password_hash(self.password_hash, pw)
