# Reservation extension plan

Current outcome: S1 is implemented and locally verified; independent code review
and human review remain pending. The independent document review passed before
implementation, with no material findings. Decisive
acceptance is the [design example](DESIGN.md): reject `a:2,b:2` against `a:4,b:1`,
then accept `a:4` and an empty order, leaving `a:0,b:1`.

| Outcome awaiting review | Boundary and dependencies | Acceptance |
| --- | --- | --- |
| S1: whole-order rejection in the shared engine, API regression coverage, README usage and SPEC current behavior | Document review passed; implementation and required checks complete | All [design acceptance cases](DESIGN.md#decisive-acceptance) and existing tests pass; independent code review and subsequent human review pending |

Update SPEC to describe the new behavior while preserving ORIGINAL and REQUEST as
source requirements. README should explain shortage results and subsequent-order
processing. Keep DEVNOTES as the operations owner; its existing checks remain valid.
Keep completed history and prior review reports; record new review findings and
verified dispositions without overwriting historical reports.

## Execution and review policy

Follow [REQUEST](REQUEST.md), fixture [AGENTS](../AGENTS.md), and
[DEVNOTES](../DEVNOTES.md). One combined independent document review is appropriate
for this small local change; the following implementer runs the checks and obtains
an independent code review before handoff for human review. Agent review is
permitted and must not be labeled human acceptance. No
commit, push, version change, release, dependency installation, or external service
is requested. The 15-minute allowance covers the whole task including necessary
reviews; it is not a separate budget per phase or a target to consume.

Use the prepared runtime from the project root:

```sh
"$CANARY_PYTHON" -m unittest discover -s tests -v
"$CANARY_PYTHON" .git/hooks/pre-commit
```

The installed hook rejects empty discovery and runs the suite. Run it explicitly
without committing. If checks or review reveal defects, fix them and rerun the
affected verification before reporting readiness; retain unresolved findings in
the handoff. Human review follows the agent work.

## Current delivery and evidence

Implementation handoff, 2026-09-07: S1 checks pass; independent code review is
pending with the separate reviewer requested by the user. Human review remains
pending. No code-review verdict is asserted and no commit was made. Next action:
independently review the captured candidate, record findings and dispositions,
then obtain human review after any necessary fixes and rechecks.

The prior [document review](../reviews/design-current.json) is preserved unchanged:
verdict ready, no open finding IDs. Before editing, all 15 recorded file hashes
matched, including the design, plan, requirements, code, tests and installed gate.
Its baseline evidence therefore applies to the starting content. D2's algorithm
and scope are unchanged; its status now links the passed document review.

The engine checks availability before any deduction. New tests use explicit
expected stock and ordered results through both APIs, covering shortages in either
item position, continuation after acceptance/rejection, exact depletion, zero
stock, empty orders/batches, nested input preservation and exact result types.
JSON regressions verify malformed or invalid later input cannot invoke the engine.
README owns usage and SPEC now describes current behavior. Original requirements,
completed history, existing tests, adapter, codec and gate are preserved.

Candidate: [S1 snapshot](../reviews/s1-candidate.json), containing base revision,
relevant changed-file diff, and full content/hashes of the code, tests, requirements,
documentation and check configuration. This is implementation evidence, not an
independent review. The reviewer should compare the current content to that snapshot.

Exact checks from the project root, using prepared Python 3.12.4 at
`/Users/tk/Documents/coding-agent-skills/.venv/bin/python`:

| Command | Result and retained output |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" -m unittest discover -s tests -v` | Exit 0; 12 tests passed ([output](../reviews/s1-unittest.txt)) |
| `PYTHONDONTWRITEBYTECODE=1 "$CANARY_PYTHON" .git/hooks/pre-commit` | Exit 0; 12 tests passed, nonempty collection ([output](../reviews/s1-gate.txt)) |

The installed gate makes no file edits. No dependency installation, external
service, version advancement, push or release was performed. All intended files
are staged for inspection without committing. The independent reviewer must still
assess correctness and test sufficiency; passing local checks is not acceptance.

## Preserved planning evidence

Planning inspection, 2026-09-07: S0 remains complete; S1 is proposed and unimplemented.
Independent document review, implementation, code review, and human review are
pending. No prior review report was present among the fixture files; the completed
record is preserved at [history/completed.md](history/completed.md).

Inspected the engine, JSON adapter/codec, all existing tests, README, DEVNOTES, and
the supplied and installed hook scripts. Baseline commands using `CANARY_PYTHON`:

- `-m unittest discover -s tests -v`: passed all 6 tests.
- `hooks/pre-commit`: passed all 6 tests; its contents match the installed hook.
- `.git/hooks/pre-commit`: also passed all 6 tests when invoked explicitly.
- A read-only in-memory probe of the opening design example through both APIs
  returned stock `{"a":-2,"b":-1}` and `[True, True, True]`, confirming the existing
  shortage defect. Inputs remained unchanged. This is baseline evidence, not
  acceptance of the requested feature.

Existing tests cover successful deduction, empty batches, adapter success, and
selected invalid inputs; they do not establish whole-order rejection, continuation,
empty-order acceptance, or nested order immutability. Planned acceptance closes
those gaps. Keep subsequent execution results and live delivery status here, with
links to independent review records when produced.

## Preserved original plan

> # Plan
> S0 complete: in-memory reservation and JSON validation are delivered.
> No pending work before the current change request.
