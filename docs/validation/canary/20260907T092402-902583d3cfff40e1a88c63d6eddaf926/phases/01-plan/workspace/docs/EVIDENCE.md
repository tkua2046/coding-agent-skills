# Reservation planning evidence

Observed during this planning pass, 2026-09-07. Only fixture files and the prepared local Python runtime were used. Existing application, tests, configuration, and source documents were not edited. These notes and scratch transcripts are new artifacts.

## Baseline

Command: `PYTHONDONTWRITEBYTECODE=1 "${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v`

Exit status: **0**. Result: **6 tests ran, OK**. Raw combined stdout/stderr: [reservation-baseline.txt](../scratch/reservation-baseline.txt). Bytecode writing was disabled to preserve project files.

## Behavioral probe

Ran the prepared Python runtime with `PYTHONDONTWRITEBYTECODE=1`, importing `inventory.reserve`, `batch.execute`, and standard-library `json`. Passed exactly the mixed stock/orders in [the design acceptance table](DESIGN.md#decisive-acceptance-examples) to `reserve(stock, orders)` and `execute(stock, json.dumps(orders))`, then printed the original inputs.

Exit status: **0**. Both calls returned `{'a': -2, 'b': -3}` with all four acceptance flags `True`. Original stock and orders printed unchanged. Raw stdout: [reservation-probe.txt](../scratch/reservation-probe.txt). This is an observation of existing behavior, not a passing feature test; the expected final stock after implementation is `{'a': 0, 'b': 0}` with flags `[True, False, True, True]`.

## Inspection limits

Read `AGENTS.md`, original request, README, DEVNOTES, both supplied skills and relevant prompts/templates, all three application modules, and the existing test module. No earlier reports were present in the fixture file listing.

An attempted `git status --short` emitted sandbox warnings about xcrun cache creation and reading the user's Git ignore file, with no status entries. It is not treated as clean-tree evidence. No installed hook, external service, or CI was invoked, and no production change was attempted.
