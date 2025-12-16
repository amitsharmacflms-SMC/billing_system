from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import db
from models.products import Product

product_bp = Blueprint("products", __name__, url_prefix="/products")

# ---------------------------
# GET ALL PRODUCTS
# ---------------------------
@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.order_by(Product.id).all()
    return jsonify([{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "hsn": p.hsn,
        "mrp": float(p.mrp or 0),
        "rate": float(p.rate or 0),
        "pack": p.pack
    } for p in products])

# ---------------------------
# ADD PRODUCT
# ---------------------------
@product_bp.route("/add", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()

    if not data.get("name"):
        return {"error": "Product name required"}, 400

    product = Product(
        sku=data.get("sku"),
        name=data["name"],
        hsn=data.get("hsn"),
        mrp=data.get("mrp"),
        rate=data.get("rate"),
        pack=data.get("pack")
    )
    db.session.add(product)
    db.session.commit()

    return {"message": "Product added"}, 201

# ---------------------------
# UPDATE PRODUCT  ✅ FIXED
# ---------------------------
@product_bp.route("/update/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.hsn = data.get("hsn", product.hsn)
    product.rate = data.get("rate", product.rate)
    product.pack = data.get("pack", product.pack)

    db.session.commit()
    return {"message": "Product updated"}, 200

# ---------------------------
# DELETE PRODUCT  ✅ FIXED
# ---------------------------
@product_bp.route("/delete/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product deleted"}, 200
