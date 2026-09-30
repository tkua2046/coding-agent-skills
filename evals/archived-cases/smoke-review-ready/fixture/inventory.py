def reserve_batches(stock, batches):
    remaining = dict(stock)
    accepted = []
    for batch in batches:
        ok = True
        for sku, quantity in batch.items():
            if remaining.get(sku, 0) < quantity:
                ok = False
                break
            remaining[sku] -= quantity
        accepted.append(ok)
    return remaining, accepted
