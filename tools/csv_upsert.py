import os
import csv
from app import app
from core.database import db
from models.products import Product
from models.distributors import Distributor
from models.suppliers import Supplier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTERS_DIR = os.path.join(BASE_DIR, "..", "masters")


# ---------------------------------------------------------
# Auto-detect delimiter: comma, tab, or pipe
# ---------------------------------------------------------
def detect_delimiter(text):
    if "\t" in text:
        return "\t"
    if "|" in text:
        return "|"
    return ","


# ---------------------------------------------------------
# Normalize headers
# ---------------------------------------------------------
def normalize_headers(row):
    return {k.strip().lower(): (v.strip() if v else "") for k, v in row.items()}


# ---------------------------------------------------------
# IMPORT PRODUCTS
# ---------------------------------------------------------
def import_products():
    print("\n📦 Importing Products...")

    filepath = os.path.join(MASTERS_DIR, "products.csv")

    with app.app_context():
        with open(filepath, encoding="utf-8-sig") as f:
            sample = f.read(500)
            f.seek(0)

            delimiter = detect_delimiter(sample)
            reader = csv.DictReader(f, delimiter=delimiter)

            for raw in reader:
                row = normalize_headers(raw)

                sku = row.get("sku")
                name = row.get("name")

                if not sku or not name:
                    print("⚠ Skipped invalid product row:", row)
                    continue

                product = Product.query.filter_by(sku=sku).first()
                if not product:
                    product = Product(sku=sku)

                product.name = name
                product.hsn = row.get("hsn", "")
                product.mrp = float(row.get("mrp", 0) or 0)
                product.rate = float(row.get("rate", 0) or 0)
                product.pack_size = row.get("pack_size", "")
                product.gst = float(row.get("gst", 0) or 0)
                product.category = row.get("category", "")

                db.session.add(product)

        db.session.commit()
        print("✔ Products Imported Successfully")


# ---------------------------------------------------------
# IMPORT DISTRIBUTORS (Your uploaded file)
# ---------------------------------------------------------
def import_distributors():
    print("\n🏪 Importing Distributors...")

    filepath = os.path.join(MASTERS_DIR, "distributors.csv")

    with app.app_context():
        with open(filepath, encoding="utf-8-sig") as f:
            sample = f.read(500)
            f.seek(0)

            delimiter = detect_delimiter(sample)
            reader = csv.DictReader(f, delimiter=delimiter)

            for raw in reader:
                row = normalize_headers(raw)

                name = row.get("name")
                if not name:
                    print("⚠ Skipped row (no name):", row)
                    continue

                dist = Distributor.query.filter_by(name=name).first()
                if not dist:
                    dist = Distributor(name=name)

                dist.address = row.get("address", "")
                dist.city = row.get("city", "")
                dist.state = row.get("state", "")
                dist.pincode = row.get("pincode", "")
                dist.gstin = row.get("gstin", "")
                dist.contact_person = row.get("contact_person", "")
                dist.phone = row.get("phone", "")
                dist.email = row.get("email", "")

                db.session.add(dist)

        db.session.commit()
        print("✔ Distributors Imported Successfully")


# ---------------------------------------------------------
# IMPORT SUPPLIERS
# ---------------------------------------------------------
def import_suppliers():
    print("\n🏢 Importing Suppliers...")

    filepath = os.path.join(MASTERS_DIR, "suppliers.csv")

    with app.app_context():
        with open(filepath, encoding="utf-8-sig") as f:
            sample = f.read(500)
            f.seek(0)

            delimiter = detect_delimiter(sample)
            reader = csv.DictReader(f, delimiter=delimiter)

            for raw in reader:
                row = normalize_headers(raw)

                name = row.get("name")
                if not name:
                    print("⚠ Skipped supplier row:", row)
                    continue

                sup = Supplier.query.filter_by(name=name).first()
                if not sup:
                    sup = Supplier(name=name)

                sup.gstin = row.get("gstin", "")
                sup.address = row.get("address", "")
                sup.city = row.get("city", "")
                sup.state = row.get("state", "")
                sup.pincode = row.get("pincode", "")

                db.session.add(sup)

        db.session.commit()
        print("✔ Suppliers Imported Successfully")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 Starting CSV Import...")

    import_products()
    import_distributors()
    import_suppliers()

    print("\n✅ ALL CSV DATA IMPORTED SUCCESSFULLY\n")
