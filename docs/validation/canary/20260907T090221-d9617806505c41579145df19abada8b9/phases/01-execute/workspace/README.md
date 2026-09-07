# Counter
`Counter(value=0).add(step=1)` returns the updated value.

Omitting `step` adds one. Pass a positive Python integer to add another amount;
booleans and all other invalid steps raise `ValueError` without changing the
counter. The initial value may be any integer.
