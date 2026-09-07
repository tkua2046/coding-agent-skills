def adjust(stock, sku, quantity):
    if sku not in stock:
        raise KeyError(sku)
    if type(quantity) is not int or quantity < 0:
        raise ValueError("quantity must be a non-negative integer")
    updated = dict(stock)
    updated[sku] = quantity
    return updated
