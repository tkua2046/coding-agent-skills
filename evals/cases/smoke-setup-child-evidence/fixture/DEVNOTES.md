The standard-library check, from the project root, is:
python3 -B -m unittest discover -s tests -v
Use CANARY_PYTHON instead of python3 when supplied by the workspace.
The local suite checks manifest-name behavior. Archive verification is a separate
release-workspace operation. The prior temporary release workspace and candidate
archive are no longer present; this checkout retains its handoff record only.
No hook or coverage tool is configured. This inspection does not request setup
changes or reproduction of the old release workspace.
