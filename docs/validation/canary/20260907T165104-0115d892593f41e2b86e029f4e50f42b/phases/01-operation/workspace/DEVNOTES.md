Python standard library only; no package installation is needed.

Run the full check from the repository root before committing, including for
documentation changes:

```sh
python -m unittest discover -s tests -v
```

In the supplied fixture, use the prepared runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v
```

The environment variable prevents disposable bytecode files. The command must
exit successfully and report collected tests. The current suite contains one
test. Investigate failures or unexpected collection counts before committing.
Zero-test exit behavior can vary by Python runtime; do not accept an empty suite
based solely on an exit code.

This is a manual commit gate. No active hook is supplied or installed by this
setup inspection. No lint, format, coverage or CI gate is configured. Application
code is in `catalog.py`; tests are in `tests/`. Coverage is not measured, and no
coverage threshold is established.

See [RESULT.md](RESULT.md) for verification evidence and limitations. The supplied
[previous command record](previous-command.json) is retained unchanged.
