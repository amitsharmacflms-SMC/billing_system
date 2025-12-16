from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import db
from models.products import Product
from datetime import datetime

product_bp = Blueprint("products", __name__, url_prefix="/products")


# -----------------------------------------
# GET ALL PRODUCTS
# -----------------------------------------
@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify([
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "hsn": p.hsn,
            "mrp": float(p.mrp) if p.mrp else 0,
            "rate": float(p.rate) if p.rate else 0,
            "pack": p.pack
        }
        for p in products
    ])


# -----------------------------------------
# ADD PRODUCT  ✅ FIXED
# -----------------------------------------
@product_bp.route("/add", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()

    sku = data.get("sku")
    name = data.get("name")

    if not sku or not name:
        return {"error": "SKU and Product name required"}, 400

    # prevent duplicate SKU
    if Product.query.filter_by(sku=sku).first():
        return {"error": "SKU already exists"}, 409

    product = Product(
        sku=sku,
        name=name,
        hsn=data.get("hsn"),
        mrp=data.get("mrp", 0),
        rate=data.get("rate", 0),
        pack=data.get("pack")
    )

    db.session.add(product)
    db.session.commit()

    return {"message": "Product added successfully"}, 201
