# Plan revision recheck contract, v1

Run through the existing `tools.canary` runner. Two document-only phases adapt the design recheck pattern to B5/B6: P2 adds prerequisite wording but still orders the consumer first; P3 fixes ordering and retains full JSON/failure/old-client acceptance. Original P1, P2 and R1 remain in fixture history. The overlay supplies only P3; it cannot erase the worker's failed recheck report.

The rubric judges both review openings, whole-contract verification, revision-specific dispositions, scope and unnecessary process. Captured replies, traces and phase workspace/Git snapshots provide evidence. No deadline or worker-owned audit system is added. The hidden oracle checks untouched P3 and report presence only; runner checks preserve original history and prohibit commits/tags. Prose correctness is deliberately left to the existing semantic grader.

`python3 -B -m unittest tests.test_new_case_controls -v` runs the authored positive/negative controls in automatically cleaned temporary storage. Ordinary pytest/fast-hook runs use the same default; cleanup also runs after setup or test failures. No new archived workspaces are retained in normal mode.

For a one-off evidence capture, run:

```sh
NEW_CASE_CONTROLS_EVIDENCE=1 python3 -B -m unittest tests.test_new_case_controls -v
```

This explicitly retains command JSON records (stdout/stderr/exit codes), authored Git workspaces, built artifacts and semantic expectations in a fresh timestamp/unique-ID directory under ignored `artifacts/eval-contract-adaptation/new-case-controls/`. The path is printed before fixture setup. Evidence-mode failures retain partial records/workspaces too; existing archives and links are never replaced or removed.

These are deterministic fixture/oracle controls, not worker runs, model-grader calibration, A/B tests, hosted publication or skill-quality evidence. Semantic-only negative reports deliberately pass structural checks and retain expected failed criterion IDs in evidence mode for main-agent calibration.
