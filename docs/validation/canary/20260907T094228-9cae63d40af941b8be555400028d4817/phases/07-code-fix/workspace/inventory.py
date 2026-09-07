"""Reserve each order against a batch-local stock snapshot."""
def reserve(stock, orders):
    remaining = dict(stock)
    outcomes = []
    for order in orders:
        accepted = all(remaining[sku] >= quantity for sku, quantity in order["items"])
        if accepted:
            for sku, quantity in order["items"]:
                remaining[sku] -= quantity
        outcomes.append({"order_id": order["id"], "accepted": accepted})
    return remaining, outcomes
