# Contributor checks

Run the existing tests with the prepared runtime:

```sh
"${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
```

No installed hook or CI result is represented by this fixture. Existing test results
must be observed before being reported; this note is an available command, not a pass.
