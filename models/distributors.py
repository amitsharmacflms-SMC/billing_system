from core.database import db

class Distributor(db.Model):
    __tablename__ = "distributor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    gstin = db.Column(db.String(50))
    state_code = db.Column(db.String(5))
