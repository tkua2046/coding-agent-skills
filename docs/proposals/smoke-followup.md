# Correct two observed smoke failures

The first paired smoke run passed ten of twelve cases on both versions. It does not yet demonstrate an improvement. Preserve all original attempts; correct a missing review prerequisite and an unsupported setup claim before accepting the candidate.

## Review input

The ready-review fixture calls an API and gate “existing” but supplies neither. Both reviewers identified that real gap. Supply a small existing batch-reservation API, its baseline compatibility tests and a developer guide with the actual gate/review policy. Link the guide from P1. Keep the proposed atomicity change unimplemented so this remains a design/plan review, not implementation assurance. Version the case and preserve the additional inputs. Readiness must follow actual sufficient context, not a prompt telling the reviewer to approve. The original missing-context output remains separately adjudicated; no skill relaxation follows from it.

## Setup scope and evidence

The baseline changed DEVNOTES. The evaluator's exact immutable-file list was not disclosed; the visible preservation instruction and report request left DEVNOTES ownership ambiguous. Make all existing-file preservation explicit and put recommendations in RESULT. This clarifies scope prospectively without changing the original failed guard or retroactively settling the ambiguity.

The candidate correctly ran the normal gate, then claimed specific failed/empty-suite probe results from a command whose captured output was empty. Intent and expected output do not establish execution. Replace setup's unconditional completion language with two cases: inspect an established gate using relevant actual results; when changing/configuring hooks or runners, verify their relevant failure propagation. Probe an unchanged framework only for a demonstrated unresolved propagation risk. This reduces unnecessary work while preserving the existing complete setup case's real hook/failure requirements.

Align the setup report and silent delivery check: claims must be supported by observed output or an actually enforced assertion. Missing expected output is unverified; resolve it with a focused check or disclose the limit. A wrapper's exit code alone cannot establish unchecked child results. Do not add a new report, validator, mandatory retry or generic framework.

## Verification

Review these corrections before applying them. Fresh paired runs use the corrected ready/setup inputs and unchanged grader. Exercise the neighboring PR smoke after the shared delivery check changes, then complete workflow-setup and execution-handoff trials to ensure real gate proof and required acceptance remain intact. The first three skill bundles stay frozen while their affected complete comparisons run. Record actual effort and unnecessary operations separately from pass/fail; no timing quota or document-length target determines correctness.
