# Local release execution contract, v1

Run through the existing `tools.canary` runner. The fixture is a standard-library CSV inventory summary utility with default CSV, opt-in JSON, aggregation and all-or-nothing invalid-input rejection. Phase 01 releases the completed compatible option from 1.2.0 to 1.3.0: dated notes, one local commit, actual gate and self-review, exact tag, committed-source zip build, artifact execution and offline publication simulation.

Phase 02 uses the supplied adapter to seed separately addressable matching, conflicting and uncertain namespaces. Their real local tags use `retry-<scenario>/v1.3.0`; all remain visible in the runner's normal Git snapshots. Matching has the candidate and completed artifact checksum; conflicting points at the original fixture commit; uncertain has the candidate tag but unknown publication state. These namespaces simulate separate service environments without clones, external servers or production network access. Setup creates new refs once and does not replace the main release tag.

The adapter is fixture infrastructure, not work assigned to the worker. Its state/events model observed service responses and attempted calls. They do not establish genuine remote publication or independently prove execution chronology. The hidden oracle checks version/notes structure, exact Git/artifact/source associations, actual artifact behavior, retained simulated state and no forbidden retry attempts. The rubric and existing captured traces separately judge required gate/review/build order, truthful usable reports and justified effort. A passing oracle is insufficient for full acceptance; no arbitrary deadline applies.

`python3 -B -m unittest tests.test_new_case_controls -v` runs the authored positive/negative controls in automatically cleaned temporary storage. Ordinary pytest/fast-hook runs use the same default; cleanup also runs after setup or test failures. No new archived workspaces are retained in normal mode.

For a one-off evidence capture, run:

```sh
NEW_CASE_CONTROLS_EVIDENCE=1 python3 -B -m unittest tests.test_new_case_controls -v
```

This explicitly retains command JSON records (stdout/stderr/exit codes), authored Git workspaces, built artifacts and semantic expectations in a fresh timestamp/unique-ID directory under ignored `artifacts/eval-contract-adaptation/new-case-controls/`. The path is printed before fixture setup. Evidence-mode failures retain partial records/workspaces too; existing archives and links are never replaced or removed.

These are deterministic fixture/oracle controls, not worker runs, model-grader calibration, A/B tests, hosted publication or skill-quality evidence. Semantic-only negative reports deliberately pass structural checks and retain expected failed criterion IDs in evidence mode for main-agent calibration.
