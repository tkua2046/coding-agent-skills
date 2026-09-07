"""Reserve each order against a batch-local stock snapshot."""
def reserve(stock, orders):
    remaining = dict(stock)
    outcomes = []
    for order in orders:
        if any(quantity > remaining[sku] for sku, quantity in order["items"]):
            outcomes.append({"order_id": order["id"], "accepted": False})
            continue
        for sku, quantity in order["items"]:
            remaining[sku] -= quantity
        outcomes.append({"order_id": order["id"], "accepted": True})
    return remaining, outcomes
