# Reservation extension plan

Next outcome: whole-order rejection and continued processing through both existing
APIs, with regression tests and updated usage/current behavior documentation in one
coherent increment. Prerequisite: the independent reviewer assesses this design and
plan, and material findings are resolved before the implementer proceeds. Decisive
acceptance is the [design example](DESIGN.md): reject `a:2,b:2` against `a:4,b:1`,
then accept `a:4` and an empty order, leaving `a:0,b:1`.

| Pending outcome | Boundary and dependencies | Acceptance |
| --- | --- | --- |
| S1: implement whole-order rejection in the shared engine, add meaningful API regression coverage, update README usage and SPEC current behavior | After document review; one local increment because both APIs already share the engine and there is no independently deliverable prerequisite | All [design acceptance cases](DESIGN.md#decisive-acceptance), existing tests, nonempty test gate, and independent code review; no implementation is delivered by this planning phase |

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
permitted and must not be labeled human acceptance. This phase only plans. No
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
