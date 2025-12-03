import os
import csv
from core.database import db
from models.products import Product
from models.distributors import Distributor
from models.suppliers import Supplier
from models.invoice_settings import InvoiceSetting

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "masters")

def load_csv(filename, required_cols):
    """Load CSV and validate column headers."""
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        print(f"❌ CSV not found: {filename}")
        return []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not set(required_cols).issubset(reader.fieldnames):
            print(f"❌ Invalid columns in {filename}")
            print(f"Required: {required_cols}")
            print(f"Found: {reader.fieldnames}")
            return []

        return list(reader)


# -------------------------------------------
# 1️⃣ IMPORT PRODUCTS
# -------------------------------------------
def import_products():
    rows = load_csv("products.csv",
                    ["id", "name", "hsn", "mrp", "rate", "pack", "gst_percent", "category"])
    if not rows: return

    for row in rows:
        product = Product.query.get(row["id"])

        if product:
            # Update existing
            product.name = row["name"]
            product.hsn = row["hsn"]
            product.mrp = float(row["mrp"])
            product.rate = float(row["rate"])
            product.pack = row["pack"]
            product.gst_percent = float(row["gst_percent"])
            product.category = row["category"]
        else:
            # Insert new
            product = Product(
                id=row["id"],
                name=row["name"],
                hsn=row["hsn"],
                mrp=float(row["mrp"]),
                rate=float(row["rate"]),
                pack=row["pack"],
                gst_percent=float(row["gst_percent"]),
                category=row["category"]
            )
            db.session.add(product)

    db.session.commit()
    print("✅ Products Imported")


# -------------------------------------------
# 2️⃣ IMPORT DISTRIBUTORS
# -------------------------------------------
def import_distributors():
    rows = load_csv("distributors.csv",
                    ["id", "name", "address", "city", "state", "pincode",
                     "gstin", "contact_person", "phone", "email"])

    if not rows: return

    for row in rows:
        dist = Distributor.query.get(row["id"])

        if dist:
            dist.name = row["name"]
            dist.address = row["address"]
            dist.city = row["city"]
            dist.state = row["state"]
            dist.pincode = row["pincode"]
            dist.gstin = row["gstin"]
            dist.contact_person = row["contact_person"]
            dist.phone = row["phone"]
            dist.email = row["email"]
        else:
            dist = Distributor(
                id=row["id"],
                name=row["name"],
                address=row["address"],
                city=row["city"],
                state=row["state"],
                pincode=row["pincode"],
                gstin=row["gstin"],
                contact_person=row["contact_person"],
                phone=row["phone"],
                email=row["email"]
            )
            db.session.add(dist)

    db.session.commit()
    print("✅ Distributors Imported")


# -------------------------------------------
# 3️⃣ IMPORT SUPPLIERS
# -------------------------------------------
def import_suppliers():
    rows = load_csv("suppliers.csv",
                    ["id", "name", "address", "city", "state", "pincode",
                     "gstin", "contact_person", "phone", "email"])

    if not rows: return

    for row in rows:
        sup = Supplier.query.get(row["id"])

        if sup:
            sup.name = row["name"]
            sup.address = row["address"]
            sup.city = row["city"]
            sup.state = row["state"]
            sup.pincode = row["pincode"]
            sup.gstin = row["gstin"]
            sup.contact_person = row["contact_person"]
            sup.phone = row["phone"]
            sup.email = row["email"]
        else:
            sup = Supplier(
                id=row["id"],
                name=row["name"],
                address=row["address"],
                city=row["city"],
                state=row["state"],
                pincode=row["pincode"],
                gstin=row["gstin"],
                contact_person=row["contact_person"],
                phone=row["phone"],
                email=row["email"]
            )
            db.session.add(sup)

    db.session.commit()
    print("✅ Suppliers Imported")


# -------------------------------------------
# 4️⃣ IMPORT INVOICE SETTINGS
# -------------------------------------------
def import_invoice_settings():
    rows = load_csv("invoice_settings.csv", ["key", "value"])
    if not rows: return

    for row in rows:
        setting = InvoiceSetting.query.filter_by(key=row["key"]).first()

        if setting:
            setting.value = row["value"]
        else:
            setting = InvoiceSetting(key=row["key"], value=row["value"])
            db.session.add(setting)

    db.session.commit()
    print("✅ Invoice Settings Imported")


# -------------------------------------------
# RUN ALL IMPORTERS
# -------------------------------------------
def import_all():
    print("🚀 Starting CSV Import...")
    import_products()
    import_distributors()
    import_suppliers()
    import_invoice_settings()
    print("🎉 Import Finished!")


if __name__ == "__main__":
    from app import create_app
    app = create_app()

    with app.app_context():
        import_all()
