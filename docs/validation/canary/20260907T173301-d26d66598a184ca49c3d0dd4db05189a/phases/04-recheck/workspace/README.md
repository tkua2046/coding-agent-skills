# Counter
`Counter(value=0).add(step=1)` returns the updated value.

`step` must be a positive Python integer; booleans are excluded. Invalid
steps raise `ValueError` without changing the counter. Omitting `step` adds one.
The initial value may be any integer, including zero and negative integers.
