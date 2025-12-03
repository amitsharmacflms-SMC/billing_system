from core.database import db

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200))
    hsn = db.Column(db.String(20))
    rate = db.Column(db.Numeric(12,2))
    gst_percent = db.Column(db.Numeric(5,2))
    pack_pcs = db.Column(db.Integer)
    pack_case = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
