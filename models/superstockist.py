from core.database import db

class SuperStockist(db.Model):
    __tablename__ = "super_stockist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    gstin = db.Column(db.String(50))
    state_code = db.Column(db.String(5))
    email = db.Column(db.String(100))
