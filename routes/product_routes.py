from flask import Blueprint, request, jsonify
from core.database import db
from models.products import Product

product_bp = Blueprint("products", __name__, url_prefix="/products")


# -----------------------------------------
# GET ALL PRODUCTS
# -----------------------------------------
@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "hsn": p.hsn,
            "mrp": p.mrp,
            "rate": p.rate,
            "pack": p.pack
        })

    return jsonify(data)


# -----------------------------------------
# ADD PRODUCT
# -----------------------------------------
@product_bp.route("/add", methods=["POST"])
def add_product():
    try:
        data = request.get_json()

        name = data.get("name")
        hsn = data.get("hsn")
        mrp = data.get("mrp")
        rate = data.get("rate")
        pack = data.get("pack")

        if not name:
            return jsonify({"error": "Product name required"}), 400

        product = Product(
            name=name,
            hsn=hsn,
            mrp=mrp,
            rate=rate,
            pack=pack
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product added", "id": product.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -----------------------------------------
# GET SINGLE PRODUCT
# -----------------------------------------
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_single_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "hsn": product.hsn,
        "mrp": product.mrp,
        "rate": product.rate,
        "pack": product.pack
    })


# -----------------------------------------
# UPDATE PRODUCT
# -----------------------------------------
@product_bp.route("/update/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.get_json()

        product.name  = data.get("name", product.name)
        product.hsn   = data.get("hsn", product.hsn)
        product.mrp   = data.get("mrp", product.mrp)
        product.rate  = data.get("rate", product.rate)
        product.pack  = data.get("pack", product.pack)

        db.session.commit()

        return jsonify({"message": "Product updated"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -----------------------------------------
# DELETE PRODUCT
# -----------------------------------------
@product_bp.route("/delete/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
