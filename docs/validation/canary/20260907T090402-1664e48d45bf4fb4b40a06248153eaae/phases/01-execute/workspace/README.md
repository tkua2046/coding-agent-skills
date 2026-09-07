# Counter
`Counter(value=0).add(step=1)` returns the updated value.

Calling `add()` adds one. An explicit step must be a positive Python integer;
booleans, zero, negative values and non-integers raise `ValueError` without
changing the counter. The initial value may be any integer.
