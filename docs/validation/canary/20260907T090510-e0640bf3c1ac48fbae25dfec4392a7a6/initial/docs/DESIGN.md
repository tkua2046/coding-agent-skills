# Accepted design D1
The JSON boundary validates shapes, positive quantities, unique IDs and item SKUs.
The engine trusts validated orders and copies stock once for batch-local mutation.
Sufficient inventory is currently the caller's responsibility. The function returns
one boolean acceptance result per order and does not mutate caller inputs.
