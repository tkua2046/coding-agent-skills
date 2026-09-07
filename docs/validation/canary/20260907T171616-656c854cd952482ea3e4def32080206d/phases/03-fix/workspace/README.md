# Counter
`Counter(value=0).add(step=1)` returns the updated value.
Initial values may be any integer. The step must be a positive Python integer;
booleans and all other values raise `ValueError` without changing the counter.
Calling `add()` without a step increments by one.
