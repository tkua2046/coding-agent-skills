# Validation

Status: packaging, real hook trials, fresh-agent follow-ups and independent implementation reviews passed. Initial commit `0ac5b7b` is pushed and its remote CI passed. This documentation update records that observed result; later commits have their own CI runs. Date: 2026-09-06.

## Observed results

| Check/trial | Actual result | Evidence |
|---|---|---|
| Bundled skill-creator validation | Four skill entrypoints valid | [Original validator outputs](validation/skill-format/20260907T045525345635Z-7bbb3abe57ef46edbc2efb7144672c86.json) |
| Repository regression suite | 32 tests pass; checker/evidence code line and branch coverage 100% | [Full local gate: original output and candidate hashes](validation/local-gates/20260907T050102905544Z-ef4ead676e86439bbef96354e941fa6c.json) |
| Initial GitHub delivery | Remote main matched `0ac5b7b`; Linux CI passed | [Remote result](validation/delivery/20260907T050238512030Z-f3470935aff4464d91833bbc44bd6f57.json), [CI run](https://github.com/tkua2046/coding-agent-skills/actions/runs/34085252696), [commit-time hook output](validation/bootstrap-commit.log.txt) |
| Independent copies | All four folders validate outside the source repository | test_standalone_copy_preserves_all_skill_resources |
| Python sample through real commits | Eight required outcomes pass | [Raw commands/results](validation/hook-trials.json), [reproducible trial](../tests/manual/hook_trials.py) |
| Codex CLI discovery | Repository-local feature-design and its resources found | [Actual final response](validation/cli-discovery.txt) |
| Existing-code intake | Detected a pre-existing failing test, preserved source, requested behavioral clarification | [Original intake](validation/outputs/existing-intake-initial/INTAKE.md.txt), [36-line follow-up](validation/outputs/existing-intake-followup/INTAKE.md.txt), [preservation checks](validation/intake-followup-observations.json) |
| Stage execution | Implemented the feature, 21 tests/hooks pass; no commit while required reviews pending | [Original result](validation/outputs/stage/TRIAL_RESULT.md.txt), [author checks](validation/author-observations.json) |
| Release with stale/pending evidence | Correctly judged not ready; did not tag or publish | [Original assessment](validation/outputs/delivery-initial/RELEASE_ASSESSMENT.md.txt) |
| Release with refreshed valid evidence | Identified the exact merged 0.2.0 candidate as ready for subsequent authorized tagging; dry run made no tag | [Follow-up](validation/outputs/delivery-followup/TRIAL_FOLLOWUP.md.txt) |

The eight hook outcomes include an unchanged failing test with a different passing test staged, documentation-only failure, zero tests, passing controls, automatic Ruff fixes/restaging, and configured source/branch/missing-code measurement. These use real local Git commits; expected failures are successful negative tests.

## Reviews and improvements

[Initial design/plan review](reviews/design-and-plan-initial.md) found three actionable planning gaps. [Follow-up](reviews/design-and-plan-followup.md) confirmed the changes. Original input bytes and hashes remain in the [archive manifest](reviews/inputs-initial/manifest.json).

The intake trial produced a 103-line note containing raw test output. Its behavioral judgment was useful, but its presentation missed the requested separation between a short working page and raw evidence. The trial request also explicitly named only two output files, making the intended evidence location ambiguous. The revised prompt routes raw output to separate evidence while respecting any user-imposed file limit; the follow-up task permits supporting evidence without prescribing layout or the desired behavioral conclusion. A fresh agent produced a 36-line intake with three material clarification questions and separate original execution evidence. Source and application files remained unchanged. This is an improvement in the observed case, not a guaranteed output length. The original output remains available above.

The [initial implementation review](reviews/implementation-initial.md) found three P2 defects: unchecked asset links, missed reference/file links, and overwritten trial reports. The checker now parses Markdown and validates asset dependencies; each trial now creates a unique report with exclusive file creation. Regression tests pass. [Original counterexamples](validation/implementation-review-initial/portability-probes.json.txt) and [overwrite evidence](validation/implementation-review-initial/evidence-overwrite-probe.json.txt) remain available. The [targeted follow-up](reviews/implementation-followup.md) confirmed F1/F3 and exposed an encoded absolute-path variant of F2. That variant is now fixed by decoding before classifying/resolving the local path; plain and encoded absolute paths fail, while encoded relative filenames pass. The [final delta review](reviews/implementation-final.md) independently confirmed the correction and raw-evidence exclusions. All material implementation findings are resolved within the recorded review scopes.

A controlled setup failure followed by a real successful hook run retained both records: [failed attempt](validation/hook-trials/20260907T045412053042Z-0c7ebba356554c4faed3852e90263043.json), [successful run](validation/hook-trials/20260907T045418303746Z-8aadb94e0730408b9f5087867f1d6dc5.json). The earlier historical report also remained unchanged.

Immutable source/output archives are excluded from whitespace and final-newline fixers so automatic checks cannot silently change recorded bytes. The [archive integrity check](validation/archive-integrity/20260907T045627092078Z-67995941041544b38246c3f2962c13f3.json) verified 79 retained records against their manifests. A gate also caught a newly created reviewer script being formatted before archival; both [original and formatted variants](validation/implementation-review-followup/archive-handling-note.json) are preserved, and Ruff now excludes raw evidence as well. Review artifacts are finalized before the final candidate is staged.

## Scope and limitations

[Trial manifest](validation/trial-manifest.json) records per-file hashes of the copied skill inputs. Original fixture inputs and outputs are retained under validation; `.txt` archives preserve their bytes without pretending their original relative links resolve here.

Coverage describes the deterministic checker and evidence writer, not prompt quality. Markdown validation covers links/images, not arbitrary prose paths, shell commands or raw HTML. Fresh-agent trials are examples, not a general guarantee. Stage review correctly remained pending when no independent-review tool was exposed to that worker. CLI discovery was exercised; VS Code's graphical picker has not been directly exercised. No global skill installation or live release was performed.
