# Stage 1: validated counter step

State: accepted and committed locally in the synthetic fixture; PR.md is ready for review.
Open finding IDs: none. R1 is reviewer-verified resolved in [round 2](../../reviews/round-2.md).
Independent review and recheck: complete. Required fixture-user acceptance:
[accepted](../../reviews/user-acceptance.md). No later stage or publication is in scope.
Next action: none within this stage; any later stage or publication needs separate authorization.

## Local delivery

Stage commit: `8619b4540ff1a3d1fecd2dafdac71c1c8927aa79`.
The installed pre-commit hook ran normally and passed all six tests; the committed
tree matches the index frozen before the hook. See [commit output](completion/stage-commit.txt)
and [commit identity](completion/commit-result.json). Final staged whitespace,
working/index equality and historical-report preservation checks passed
([evidence](completion/staged-verification.json)). A documentation-only follow-up
records this resulting hash and hook evidence; it does not change the implementation.

## Candidate and checks

Base: `68c524138693fbda460cb5f3c97c6bd5f96688ae`.
Before completion edits, all 11 [candidate manifest](candidate-manifest.json)
entries matched working bytes and index blobs, and [candidate.patch](candidate.patch)
matched the staged five-file payload exactly. See [identity evidence](completion/incoming-identity.json).
Code, tests, requirements, usage, changelog, VERSION and gate remain unchanged
from independent round 2. PLAN now records acceptance; PR and this handoff now
reflect delivery. These status edits do not change the reviewed behavior.

Fresh commands using CANARY_PYTHON with PYTHONDONTWRITEBYTECODE=1:
- `"$CANARY_PYTHON" -m unittest discover -s tests -v`: exit 0, six tests pass ([output](completion/tests.txt)).
- `"$CANARY_PYTHON" hooks/pre-commit`: exit 0, six tests pass ([output](completion/gate.txt)).

The executable installed pre-commit hook matches the repository gate byte for byte.
Round 2 independently established 75 invalid-input cases, recovery, and baseline
regression sensitivity. Its verdict applies to the unchanged behavioral payload.
[PR.md](../../PR.md) contains the reviewable local title/body.

## Preserved history and limitations

The [incoming handoff](completion/prior-record.md), [prior plan](completion/prior-plan.md)
and [prior PR draft](completion/prior-PR.md) preserve the previously pending status.
[Round 1](../../reviews/round-1.md), [round 2](../../reviews/round-2.md),
[input R1](../../reviews/input-R1.md), and all previous raw evidence are unchanged.
Historical baseline tests failed on negative-step validation. The initial auxiliary
import failure and whitespace diagnostics remain preserved; successful checks
are separate records. Do not rerun author-recheck/verify.py: it overwrites history.

Checks cover only the supplied fixture and prepared runtime. Git emits sandbox
cache/config diagnostics while succeeding; no escalation was attempted.
No external CI or integration checks ran. VERSION remains 0.1.0. No push, tag,
release, version bump, external PR creation, or later stage is authorized.
