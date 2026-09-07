# Reservation extension delivery

Next outcome: S1 delivers whole-order rejection through both existing APIs, with
tests and current behavior/usage documentation. It follows the independent review
of this design and plan and resolution of material findings. Decisive acceptance is
the [D2 mixed-order example](DESIGN.md#decisive-acceptance): rejection leaves all
items available for a later success, and later orders see that success's deductions.

| Outcome / scope | Dependency and boundary | Acceptance evidence |
|---|---|---|
| S1 (pending): implement D2 in the reservation engine; add meaningful regression coverage; update `docs/SPEC.md` to reflect the extension and `README.md` usage to remove the sufficient-stock caller requirement. Preserve original sources and S0 history. | Independent document review first. One local increment keeps behavior, tests, and documentation coherent; no separate infrastructure or adapter redesign is needed. | All [design acceptance examples](DESIGN.md#decisive-acceptance) pass through the appropriate APIs; existing tests and the local gate pass with nonempty discovery; necessary code review is completed and findings resolved before human handoff. |

Sources: [REQUEST.md](REQUEST.md), [ORIGINAL.md](ORIGINAL.md), and
[DESIGN.md](DESIGN.md). Execution/review policy: [DEVNOTES.md](../DEVNOTES.md) and
the request. Use the supplied runtime for the existing checks:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" hooks/pre-commit
```

The independent reviewer follows this planning phase, then the implementer.
Agent-only review is authorized; human review follows the completed feature.
This phase changes planning documents only. No commit, push, version advancement,
release, package installation, or external service is requested. Keep the whole
task, including necessary document/code reviews, within the original 15-minute
allowance; it is not a separate allowance for each phase.

## Current delivery and baseline evidence

- Planning prepared; independent document review, S1 implementation, new tests,
  code review, and human review remain pending. No implementation changes made.
- Inspected `inventory.py`, `batch.py`, `command_codec.py`,
  `tests/test_inventory.py`, and `hooks/pre-commit`. The engine copies stock once
  but deducts unconditionally. The adapter decodes the whole batch before calling
  it. Existing tests cover success, empty batch, adapter success, unknown SKU,
  duplicate SKU, and boolean quantity rejection, but no insufficient-stock case.
- Baseline on 2026-09-07: both commands above passed, each discovering 6 tests.
  The gate explicitly rejects empty discovery. These passes do not establish D2.
- A read-only engine probe of the design's four-order example returned
  `{"a":-3,"b":-2}` with all four flags `True`, confirming the requested gap.
  D2 instead requires `{"a":0,"b":0}` and `[False,True,False,True]`.
- The implementer should record final check results and delivery status here;
  preserve any reviewer reports and their findings/dispositions rather than
  replacing them with author self-check claims.

## Preserved progress

See [completed S0](history/completed.md). The original plan below is retained
verbatim as historical context, not the current pending-work status.

# Plan
S0 complete: in-memory reservation and JSON validation are delivered.
No pending work before the current change request.
