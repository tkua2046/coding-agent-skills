# Counter
`Counter(value=0).add(step=1)` returns the updated value.
The initial value may be any integer. Omit `step` to add one, or pass a positive
Python integer. Booleans and other invalid steps raise `ValueError` without
changing the counter.
