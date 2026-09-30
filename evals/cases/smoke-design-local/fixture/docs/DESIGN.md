# Accepted export design D1
CSV rows are fully parsed and validated before being returned in source order.
The caller owns output rendering. Invalid stock rows fail the request.
This decision is accepted; no delivery status is tracked here.
