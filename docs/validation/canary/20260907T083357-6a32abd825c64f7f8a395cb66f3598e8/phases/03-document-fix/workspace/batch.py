"""JSON boundary for the inventory reservation utility."""
from command_codec import decode
from inventory import reserve

def execute(stock, text):
    return reserve(stock, decode(text, stock))
