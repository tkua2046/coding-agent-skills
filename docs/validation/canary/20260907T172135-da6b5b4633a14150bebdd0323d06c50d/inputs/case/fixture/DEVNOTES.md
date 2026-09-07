# Contributor notes

Use the existing Python environment. CANARY_PYTHON, when supplied, identifies the
prepared interpreter. Do not create another environment or download tools.
Run `"${CANARY_PYTHON:-python3}" tools/check.py` from the repository root.
The suite location and discovery pattern are configured in quality.ini.

The repository's local hook is copied from hooks/pre-commit into
.git/hooks/pre-commit and marked executable during checkout setup. It delegates
to tools/check.py, so improvements belong in the check command. Keep this scheme.
If restoring a missing local installation, copy that wrapper and chmod it locally.
No commit is needed to invoke .git/hooks/pre-commit and verify the gate.

Some useful user and contributor notes are still mixed in README. Preserve their
information while giving each audience a short entrypoint.
