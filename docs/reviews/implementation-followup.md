# Targeted implementation follow-up: F1–F3

**Verdict: not ready (needs changes).** F1 and F3 are fixed within this targeted scope. F2 is partially fixed: a percent-encoded absolute local path still bypasses the portability rejection. One P2 correction remains; this report does not approve unrelated work.

Reviewer: same independent stage-development reviewer, not the implementation author. Date: 2026-09-06. Owner-authorized local review/tests; no human approval is claimed. The [initial review](implementation-initial.md), including its inline-code examples, is preserved.

## Scope and actual checks

Reviewed only the F1–F3 changes in tools/check.py, tools/evidence.py, their deterministic tests, manual harness/module entrypoints, and dependency/hook wiring. pyproject.toml and the tools initializer were supporting inputs. Applied the initial review's SPEC R7/R8 and reviewed-design portability/evidence contracts. Did not repeat the library content review, inspect other agents' results, or read the author's running/manual trial outputs.

Copied the 11 listed inputs into a temporary workspace and used the existing .venv. Ran 13 selected deterministic tests: **13 passed, 16 deselected**. Coverage was disabled for this focused invocation; neither the author's full 29-test result nor the 100% coverage claim was independently re-established. See the exact command and output in [targeted-pytest.log](../validation/implementation-review-followup/targeted-pytest.log).

The [reviewer probes](../validation/implementation-review-followup/probe-results.json) contain 14 observations: 13 matched expectations, one exposed the remaining F2 defect. They cover asset links beneath an ancestor named assets, missing/escaping/valid targets, references and images, local URI/absolute-path handling, inert code examples, the unchanged initial report, and two deliberately failing harness invocations. [Probe source](../validation/implementation-review-followup/probes.py.txt) is retained as raw evidence.

## Dispositions

### F1 — Fixed: asset resources are validated

**Location:** tools/check.py:87–93; tests/test_check.py:62–69, 88–114.

The blanket assets exclusion is removed. Missing and escaping asset dependencies now fail, while a valid relative target succeeds even under an ancestor named assets. The selected CLI regression also rejects a missing template dependency. Inline and fenced examples remain inert. No further F1 correction is required by these observations.

### F2 — Partially fixed; P2 remains: classify local paths after decoding

**Location:** tools/check.py:31–41.

The original missing reference and file-URI examples now fail. Reference images and linked images are checked; valid local references and HTTPS links pass. The original initial-report inline-code example is unchanged and produces no link error. Configuration pins markdown-it-py==4.0.0 in requirements-dev.txt and both local hook dependency lists; isolated hook environments were not reinstalled in this follow-up.

**Remaining counterexample:** Create an existing rules.md inside a bundle, then link to its absolute path with each slash encoded as `%2F`, for example `[rules](%2Ftmp%2Fexample-skill%2Frules.md)`. In the actual fixture, validate_bundle returned `[]`, although the equivalent unencoded absolute path was rejected. Exact fixture text and output are recorded under `encoded-absolute-in-bundle` in the probe results.

**Cause/consequence:** The absolute-path test examines parsed.path before URL decoding. The later unquote creates an absolute path; Path joining discards the relative parent, and the boundary check succeeds because the file currently resides inside the bundle. Standalone validation therefore approves a machine-specific dependency that cannot remain portable after copying. No claim is made that the full repository gate also misses it.

**Minimal correction:** Decode the local path once, reject an absolute decoded path before joining it, and use that same decoded value for resolution. Add a regression using an existing in-bundle target, with both plain and encoded absolute forms rejected and a valid percent-encoded relative filename retained as a passing control.

**Disposition:** pending for the encoded-path variant; original reference/file-URI cases fixed.

### F3 — Fixed: independent reports and exception evidence are retained

**Location:** tools/evidence.py:9–16; tests/manual/hook_trials.py:54–59 and 164–170; tests/test_evidence.py:9–31.

The writer uses a timestamp/UUID name and exclusive creation. Selected tests verified failed-then-passing writer payloads preserve both files, a forced name collision cannot replace earlier bytes, and an unserializable payload leaves no partial report.

Invoked `python -m tests.manual.hook_trials` twice in the scoped copy with its sample directory deliberately absent. Both exited 1 as expected and wrote separate JSON records with status failed and FileNotFoundError details. The second run retained the first record unchanged; a legacy flat JSON fixture also remained unchanged. See [first exception log](../validation/implementation-review-followup/harness-exception-1.log), [second exception log](../validation/implementation-review-followup/harness-exception-2.log), and the copied per-run records in the evidence directory.

These were exception-retention smoke checks, not successful full hook trials. The writer tests establish the passing-payload retention case; the author's real fail-then-pass trial was neither read nor assumed successful.

## Evidence exclusion finalization

Included the small archive-handling change in this targeted scope: root pyproject.toml now extends Ruff's exclusions for docs/validation and docs/reviews/inputs-initial, and both Ruff hooks exclude those same paths. Static configuration parsing and representative path matching confirmed that evidence paths are excluded while tools/check.py and tests/test_check.py remain eligible. The diffs contain only these exclusion additions; no checker, writer, harness, test or dependency changes accompanied them. See [final configuration evidence](../validation/implementation-review-followup/config-exclusion-finalization.json).

The earlier Ruff formatting/E402 incident concerns the raw probe archive, not a product regression. The raw probe is now probes.py.txt. This reviewer did not alter the archived script's bytes during this finalization or inspect the author's failed-gate record/restoration work. No all-files gate or further runtime trial was run for the exclusions.

The disposition remains **not ready solely because the F2 encoded absolute-path counterexample is still open**. F1/F3 results remain applicable to their unchanged inputs; the configuration exclusion introduces no additional finding in this bounded inspection.

## Limits and next action

No broad gate, fresh environment installation, full hook suite, CI, release action, or behavioral-agent trial was rerun. Prior review findings outside F1–F3 and separately developing fixes remain outside this verdict. Fix the decoded-path case and rerun the affected checks before marking this changed candidate ready. No product code was edited.

## Candidate identity

The nine nonconfiguration inputs remain byte-identical to the tested snapshot. Only .pre-commit-config.yaml and pyproject.toml changed afterward, for the statically reviewed evidence exclusions above. The final fingerprints below include those two revisions; earlier runtime results apply to the unchanged code and the original recorded configuration.

The initial report is byte-identical to the start of this follow-up.

The [original tested-candidate manifest](../validation/implementation-review-followup/candidate-manifest.json) preserves the runtime-tested inputs. The [configuration finalization record](../validation/implementation-review-followup/config-exclusion-finalization.json) identifies the final candidate and comparison. SHA-256 fingerprints:

```text
88c95f4194e5a301c95c497409d17b13513dffba4719f9c1b490e0fde3d7564c  tools/check.py
29111ed0bac631f51ef0259d40e51f8f66bb0599a58cd7a255b29296f8d3a922  tools/evidence.py
76f14fd7c8343652459119320cb53b7e919dac7435e7ba7bb66ef7d1c4f4426d  tools/__init__.py
d859df28dde3b21e22352ee5b6ceab3c1bc85ecca53c7e24598759b512dbb771  tests/test_check.py
5b2c6866ae0756220fab37408eaa0b0d4f0647a506bc8ceedfa51983f00783ad  tests/test_evidence.py
84f6bd051635bf9d86d2fdae323f232e29122513fe83fc0606dacc8b722b4587  tests/__init__.py
53a215565b3814db386918a71378071182602fe2ee11954344c78d9d2d195f97  tests/manual/__init__.py
e808b32861c5897eaae24bdec9096ef69545ea61c33797349fb95df4ae0badb0  tests/manual/hook_trials.py
22f55def3c9fe9d76bac03ba3d1fe2671179ec5897e1a8910091726b9d558697  requirements-dev.txt
622e38c4d82490d8d550755fa75e4e93752cbf6ba68685511e0f1de79917ab82  .pre-commit-config.yaml
92b529c59e1072bb1c3197f8a535bcd2ed3ea59bc6c537522fe233904bc28842  pyproject.toml
62305c1614626d2e763fc6525be9116c3e2ea5b4a85929031fe6b7f0476c289b  docs/reviews/implementation-initial.md (preserved input)
```
