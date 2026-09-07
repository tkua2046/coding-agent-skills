# Counter
`Counter(value=0).add(step=1)` returns the updated value.

`step` must be a positive Python integer; booleans are rejected. Invalid steps
raise `ValueError` and leave the counter unchanged. Calling `add()` adds one.
The initial value may be any integer, including zero or a negative integer.
