import csv
import io

def export_rows(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    for row in rows:
        if not row.get("sku") or int(row["quantity"]) < 0:
            raise ValueError("invalid stock row")
    return rows
