"""Validate the JSON adapter before invoking the allocation engine."""
import json

def decode(text, stock):
    orders = json.loads(text)
    if not isinstance(orders, list):
        raise ValueError("orders must be a list")
    ids = set()
    for order in orders:
        if not isinstance(order, dict) or set(order) != {"id", "items"}:
            raise ValueError("order requires id and items")
        if not isinstance(order["id"], str) or order["id"] in ids:
            raise ValueError("order ids must be unique strings")
        ids.add(order["id"])
        if not isinstance(order["items"], list):
            raise ValueError("items must be a list")
        skus = set()
        for item in order["items"]:
            if not isinstance(item, list) or len(item) != 2:
                raise ValueError("item requires sku and quantity")
            sku, quantity = item
            if not isinstance(sku, str) or sku not in stock or sku in skus:
                raise ValueError("items must name unique known SKUs")
            if type(quantity) is not int or quantity <= 0:
                raise ValueError("quantity must be a positive integer")
            skus.add(sku)
    return orders
