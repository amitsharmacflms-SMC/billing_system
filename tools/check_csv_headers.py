import csv

with open("masters/products.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("CSV Headers:", reader.fieldnames)
