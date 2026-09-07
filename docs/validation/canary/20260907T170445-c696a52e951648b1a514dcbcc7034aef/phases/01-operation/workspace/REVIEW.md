# Combined review of D1 / P1

Verdict: **ready**. Open material findings: none. Next action: when implementation is authorized, carry out P1, run the established gate, and resolve material findings from the required independent code review before committing. This review authorizes no implementation or commit.

## Actual scope

Reviewed the supplied [Design D1](docs/DESIGN.md) and [Plan P1](docs/PLAN.md) against [REQUEST.md](REQUEST.md), with [AGENTS.md](AGENTS.md) and [DEVNOTES.md](DEVNOTES.md) as repository constraints. Candidate snapshot: `9c4fb8f4c61198b58e26deea93b8e6f5b7d3bdcd`; the initial working-tree status reported no changes. Git emitted sandbox cache/config warnings, but returned the snapshot and tracked-file list.

This was an independent document review in the fresh context supplied for this phase, using both skills' review operations and shared contracts. Static inspection included [inventory.py](inventory.py) and [tests/test_inventory.py](tests/test_inventory.py) to assess feasibility and existing acceptance coverage. It was not the independent implementation code review required by DEVNOTES.md, nor human acceptance.

## Assessment

- D1's private stock copy and complete per-batch preflight before debit satisfy caller isolation and all-or-nothing reservation under the documented validated positive-integer SKU-map inputs. Each later batch checks the remaining stock independently; persistence and concurrency are correctly out of scope.
- The decisive example exposes the current defect: with stock `a=2,b=0`, rejecting `{a:1,b:1}` currently leaves `a=1`, so the following `{a:2}` also rejects. D1 requires the first rejection to preserve `a=2,b=0`, then the second batch to succeed, yielding `({a:0,b:0}, [False, True])`. This conclusion is from static tracing, not execution.
- P1's single API-compatible increment is sufficient for this local change with no separate delivery dependency. It includes the rejected-multi-item/valid-following-batch regression, caller-input preservation, and existing API checks. Existing tests cover single-SKU continuation, preservation of both inputs, and missing-SKU rejection; they do not contain the decisive multi-item regression.
- P1 links the actual repository gate and independent code-review requirement and explicitly remains proposed. The documented gate is `python -m unittest discover -s tests -v` from the root; the supplied unittest file has discoverable test methods by static inspection. The standard-library implementation approach needs no new dependency. No additional document or stage is necessary for readiness.

## Checks and limits

Only fixture files and supplied skills were inspected. No tests, application code, or implementation steps were run; no runtime pass or test-collection result is claimed. Reviewed artifacts and prior reports were preserved. This report is the only authored artifact. No material uncertainty remains for document readiness; implementation correctness and gate success remain unverified.
