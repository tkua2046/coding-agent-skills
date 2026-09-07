# Migration delivery plan

Next implementation outcome: a caller can load active settings and safely migrate
the supplied v1 to v2, including retry after interruption. This is proposed work
for a later task, dependent on the pending design and plan reviews and authorization
to implement. Decisive acceptance: after a crash following output publication,
v1 still reads correctly; retry selects equivalent v2 with no lost/duplicated entries,
and original source bytes remain unchanged.

| Proposed outcome / scope | Dependency and boundary | Acceptance |
|---|---|---|
| One coherent implementation increment: v2/direct and active reading, migration publication/recovery, validation and crash tests, README usage and DEVNOTES recovery/support instructions | Pending reviews settle string-ID policy, commit-point interpretation and filesystem support boundary. Reader, writer and restart behavior belong together: a writer without validated reading and retry cannot deliver the required usable migration. This is one suggested future commit boundary, not an instruction to commit now. | Existing tests remain green; all [specification examples](SPEC.md#acceptance-examples) pass. Failure injection and subprocess interruption demonstrate both selector states and idempotent recovery. Documentation explains storage support, uncertain completion and conflicts. |

Within that increment, establish an early runnable path using temporary fixture
copies: read active v1, produce/validate v2 and load it through a v2 selector. Then
complete durable activation and failures before treating the increment as deliverable.
That checkpoint is not a separately safe release. Add only test seams needed to
interrupt real persistence boundaries; avoid merely checking helper call sequences.

Planned checks: `"$CANARY_PYTHON" -B -m unittest discover -s tests -v`, using the
prepared runtime and standard library. Extend the suite for the linked acceptance
examples. Inject I/O failures at writes, file sync, output publication, directory
sync and selector publication. Terminate subprocesses at deterministic checkpoints
to exercise restart without normal cleanup. Assert source bytes, selector integrity,
destination validity and final mapping on retry. Use isolated directories rather
than migrating tracked fixture data. Process-kill tests do not establish actual
power-loss guarantees.

README will own public reader/migration usage and return/error behavior. DEVNOTES
will own the test command, storage assumptions, inspect/retry instructions, conflict
resolution and scratch cleanup. SPEC owns behavior; DESIGN owns rationale. Usage
and operations docs are not changed now to advertise unimplemented capabilities.

Sources: [original requirement](ORIGINAL.md), [proposed design](DESIGN.md),
[proposed specification](SPEC.md). Execution policy: [AGENTS.md](../AGENTS.md),
[DEVNOTES.md](../DEVNOTES.md), and this task's limits: design/planning only, requested
design and plan reviews remain pending, no implementation, commits, installs or
external actions. No additional approval rounds or release work are introduced.
Future code-review expectations belong to the later implementation task's scope.

## Current delivery and evidence

- Historical completed outcome: v1 reading. Original plan preserved
  [verbatim](history/PLAN.before-migration.md). No prior review reports were present
  in the fixture; none were replaced.
- Drafted this phase: migration design, proposed behavior specification and this
  plan, grounded in reader/data/test inspection.
- Design review: **pending**. Plan review: **pending**. Author self-checks are not
  those reviews and do not approve the documents.
- Implementation: **not started**. Proposed migration tests have not been implemented
  or run. No reader, data or existing test changes.
- Actual checks: two existing tests passed; a disposable local probe exercised
  file fsync, atomic replacement and directory fsync. See [EVIDENCE.md](EVIDENCE.md)
  for observations and limits.
