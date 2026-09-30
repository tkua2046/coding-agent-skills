# Checks

From the root, run `python3 -B tools/check.py`. Use the supplied CANARY_PYTHON
instead of python3 when present. The project uses standard-library unittest.
One application test currently fails because negative adjustments are ignored.
That separate defect is known and must remain visible during this setup repair.
There is no commit hook or coverage configuration in this small project.
