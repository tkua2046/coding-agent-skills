# Development
Python standard library only. Run `python3 -m unittest discover -s tests -v`.
Report actual checks separately from proposed checks. No remote actions.

In the prepared fixture environment, use
`"$CANARY_PYTHON" -m unittest discover -s tests -v`.
The [migration baseline evidence](docs/evidence/migration-baseline.md) records the
actual checks. Migration and recovery remain planned; operational instructions
will accompany implementation after the pending design and plan reviews.
