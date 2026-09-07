"""Generate a catalog-backed order subtotal report."""
import json
from pathlib import Path

def load_catalog(path):
    rows=json.loads(Path(path).read_text())
    return {row["sku"]:row for row in rows}

def summarize(orders, catalog_path):
    rows=[]
    for order in orders:
        catalog=load_catalog(catalog_path)
        item=catalog[order["sku"]]
        rows.append({"sku":order["sku"],"subtotal_cents":item["price_cents"]*order["quantity"]})
    return rows
