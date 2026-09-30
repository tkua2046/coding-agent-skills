"""Reserve each order against a batch-local stock snapshot."""
def reserve(stock, orders):
    remaining = dict(stock)
    outcomes = []
    for order in orders:
        for sku, quantity in order["items"]:
            remaining[sku] -= quantity
        outcomes.append({"order_id": order["id"], "accepted": True})
    return remaining, outcomes
