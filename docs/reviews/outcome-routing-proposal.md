# Routing probes: proposed cases and author verification

**Authoring complete; independently reviewed ready for matched baseline/candidate evaluation.** The [primary case review](outcome-routing-review.md) has no material findings. The two planning-only probes reuse existing applications and ask what work should happen next. They do not specify investigation, a design document, stage count, review count or a classification label as the answer.

**Authoring incident:** exposing a partial new case interrupted the existing baseline wave's global preflight. Both directories are now complete, the actual global loader passes, and this author has frozen their contents. This was an orchestration failure, not a worker failure; the primary task owns reconciliation of unstarted cases. Details and original report are retained below.

The primary task independently reproduced the boundary controls for [local](../validation/outcome-assets/routing/primary-local.json) and [uncertain](../validation/outcome-assets/routing/primary-uncertain.json), matching expected results. Next action belongs to the primary task: matched evaluations on the frozen inputs. No further case-author work is pending until actual route outcomes warrant it. This contract review and the no-model controls do not establish skill improvement or owner acceptance.

Use the case fingerprints in the primary review as the evaluation handoff identities. I verified that its default-JSON fingerprints (`eb25f2a…` / `a89badfe…`) and the compact-JSON fingerprints retained below describe the same unchanged files; the differing serialization explains the differing digest values. No case input was modified during this closure.

| Case | Existing application reused | Decision being tested |
|---|---|---|
| [route-local](../../evals/cases/route-local/case.json) | Inventory reservation engine, JSON adapter, validator, tests and README copied byte-for-byte from `bounded-delivery` | Does the agent propose usable work for whole-order rejection with sufficient behavior/acceptance reasoning, without unnecessary prerequisites? |
| [route-uncertain](../../evals/cases/route-uncertain/case.json) | Catalog report, tests and README copied byte-for-byte from `bounded-investigation` | Does the agent distinguish source evidence from an unmeasured performance claim and choose a bounded next commitment that resolves the important uncertainty? |

Both are version 1 and use the existing runner schema: one `01-plan` worker phase, a restricted reader, and the existing semantic grader. They remain `tier: heavy` because they invoke models; “lightweight” describes their small planning workload, not eligibility for ordinary fast checks. Each synthetic task supplies a five-minute planning allowance, separate from reader/grader overhead.

## What the worker receives

The [local request](../../evals/cases/route-local/fixture/docs/REQUEST.md) states the required rejection, continuation, API and input-preservation behavior. The [uncertain request](../../evals/cases/route-uncertain/fixture/docs/REQUEST.md) supplies a reported slowdown, an unapproved infrastructure suggestion, catalog lifetime and result compatibility. Neither imports an accepted design, completed stage or previous review. New AGENTS/DEVNOTES accurately describe a starting snapshot and available test command, with no installed hook or passing result claimed.

Both use the same neutral [planning authorization](../../evals/cases/route-local/requests/01.md): use the supplied feature-design and implementation-plan skills; inspect the project; leave `docs/NEXT.md` for the next developer. Read-only commands and scratch exploration are allowed, while production implementation and external actions are not. Supporting notes may be linked when useful. The named handoff is an observation point for the reader, not a limit on document count or a requirement to fill a design/plan template.

Skill selection is explicit. These probes do not test automatic discovery. No reviewer is dispatched and no review sequence is prescribed inside the worker task. The existing migration case remains the separate high-consequence control; these two probes do not establish migration safety or end-to-end review convergence.

## Acceptance focuses on useful work

The [local rubric](../../evals/cases/route-local/rubric.json) and [uncertain rubric](../../evals/cases/route-uncertain/rubric.json) share four criterion IDs. Three criteria are identical; adequate-next-work has application-specific behavioral anchors so vague advice cannot pass.

| Criterion | Required evidence |
|---|---|
| `adequate-next-work` | A feasible next action, its relevant behavioral/uncertainty reasoning and a decisive condition for moving forward. |
| `proportionate-commitment` | Additional stages, documents, reviews or exploration earn their place through a real decision, dependency or consequence. No count or preferred workflow label is scored. |
| `evidence-and-scope` | Source claims match inspected code; execution claims match actual archived commands and results; proposals remain distinguishable from completed work; planning authorization is respected. |
| `usable-handoff` | The restricted reader can recover the next action, reason, limits and completion condition from the actual beginning of NEXT.md. Supporting text cannot repair an unsupported reader answer. |

For the local case, source inspection can suffice to proceed. A meaningful acceptance example distinguishes rejection before mutation and use of remaining stock from plausible wrong implementations. An extra check is acceptable if it resolves a real uncertainty; neither minimum nor maximum stage/review count is imposed.

For the uncertain case, **an executed benchmark is not compulsory**. A concrete proposed measurement can be sufficient. A limited change hypothesis may also be sufficient if source evidence justifies it and representative performance plus compatibility checks bound further commitment. Simply saying “investigate” is insufficient; so is claiming a production bottleneck or speedup from inspection alone. The grader evaluates the reasoning and next decision, not whether the agent chose an approved category or repeated “once per batch.”

Thus these differ from `bounded-investigation`, which explicitly requests and requires an executed experiment. Passing either route probe will establish planning quality at explicit skill selection, not automatic routing throughout a full development lifecycle. Benefit still requires comparing actual baseline/candidate work, not just two passes.

## Read-only boundary and evidence honesty

Each case has an independently usable [local oracle](../../evals/cases/route-local/oracle.py) or [uncertain oracle](../../evals/cases/route-uncertain/oracle.py). It only reads the final workspace. Fixed hashes protect all original fixture files, including application, tests and source documents. It rejects additional project files outside authorized notes/scratch locations and requires an existing UTF-8 handoff. Runner checks independently retain unchanged inputs, no commits and no tags. The worker never receives the oracle or rubric.

This establishes the **final file boundary**, not whether a proposal is good or a claimed measurement is truthful. The semantic criterion requires inspection of the actual phase transcript and outputs; an author-created log alone is not execution proof. A temporary production edit restored before the oracle runs must still fail semantic scope assessment when the transcript demonstrates it. Scratch exploration is allowed; delivering a production feature under a different filename is not.

The author controls explicitly include a fabricated benchmark/approval claim. The file-boundary oracle passes that artifact, as expected; `evidence-and-scope` must fail it. This is a recorded limitation and an expected semantic outcome, **not an executed LLM grading result**. No keyword-based oracle pretends to establish honesty.

## Author verification performed

Original records: [local controls, final run](../validation/outcome-assets/routing/route-local/20260907-round2.json), [uncertain controls, final run](../validation/outcome-assets/routing/route-uncertain/20260907-round2.json), and [runner-schema/source-copy/lint checks](../validation/outcome-assets/routing/route-local/asset-validation.json). These contain commands, standard output/error, exit status and file-preservation observations. Author verification runs on disposable fixture copies and leaves the source fixtures unchanged.

| Check/control, performed for both cases | Observed result |
|---|---|
| Existing fixture suite | Pass: six reservation tests and two report tests; fixture files unchanged. These are baseline application checks, not skill results. |
| Known starting behavior | Reservation still accepts a shortage and produces negative stock; report makes three loader calls for three orders and preserves exact ordered totals/empty-input behavior. No timing was inferred. |
| Handoff plus ordinary notes/scratch | Boundary oracle passes and writes nothing. |
| Changed application, deleted original test, new production module, absent handoff | Each is rejected; oracle execution leaves the trial unchanged. |
| Invented benchmark and human approval in a handoff | Boundary oracle passes; semantic failure is the declared expectation, not a completed grading claim. |
| Existing runner loads the two cases; copied bytes match source; new oracle/verification scripts lint and format | Pass. No live skill, runtime, global grader or other case file was changed. |

The first lint check found import ordering in the two author verification scripts. [Its original output](../validation/outcome-assets/routing/route-local/lint-round1.json), exact pre-fix scripts and first control attempts remain in the relocated routing evidence directories. Import order was corrected and the controls repeated as round 2; application fixtures and oracle behavior were unchanged. This mechanical correction is not a skill improvement.

Reproduction scripts are [local](../../evals/cases/route-local/author_verify.py) and [uncertain](../../evals/cases/route-uncertain/author_verify.py). Run either with the prepared Python and `--output` pointing to a new JSON path under `docs/validation/outcome-assets/routing/<case>/`, outside `evals/cases/`; it refuses to overwrite prior evidence. Re-running author controls must not change case identity. Copy provenance is retained in each case's `provenance.json`.

**Not run by this case author:** worker, restricted reader, semantic grader, matched baseline/candidate comparison, or global/release gates. This author report contains no skill-quality grades or demonstrated benefit results; subsequent actual trials belong to the primary task's result records. OGR-01's delivery correction and OGR-03's reviewer provenance remain owned by the primary task; this increment only addresses OGR-02's neutral planning coverage.

## Authoring incident and frozen state

I created `route-local/case.json` in the live case directory before writing its rubric. The shared runner's `cases(root)` validates every case, so this exposed an invalid intermediate state to the already-running baseline wave. The primary task reported the following original diagnosis:

> current run_case calls cases(root) validating EVERYcase, so while your route-local/case.json existed butrubricnotyetwritten, baselinewave preflight failedFileNotFoundError route-local/rubric.json. ParentPTY98020exited1; completedactualrecords retained.

Responsibility: this author introduced the partial directory. The incident does not establish a failed worker, defective skill or grading result. Completed original runs were not deleted, edited or reclassified by this author. The primary task's [interruption disposition](../validation/outcome-waves/20260907T083357Z-4e7a7d0afaf24542989af3ae6d400197/interruption.json) now identifies the five never-started cases and the resume-only-missing correction; subsequent execution status remains in its result records.

After receiving the incident report, I called the actual `tools.canary.cases()` global loader again. It successfully loaded both version-1 cases. The directories are frozen for independent review; subsequent edits in this task are confined to this report. Future complete case additions must be assembled outside the discovered case directory and moved into place atomically.

The first freeze below is historical: it included author-verification outputs. At the primary task's request, those directories were moved intact to `docs/validation/outcome-assets/routing/<case>/` before any route worker trial. All eight relocated evidence files retained identical bytes. Requests, rubrics, fixtures, oracles and reusable verification scripts were unchanged. The global loader passed again.

**Author's compact-serialization freeze, excluding generated verification evidence:**

| Case | Retained case files | SHA-256 |
|---|---:|---|
| route-local | 14 | `ceeb46e882679009245b2098ce81dae6010da36c14e6cafb03031dd1ff672e22` |
| route-uncertain | 12 | `8f83efbad36ac59f1dc64b9e06706a08f51a40142f811ec96c7e215db3278911` |

Historical initial freeze, superseded by the evidence relocation:

| Case | Retained files before relocation | SHA-256 |
|---|---:|---|
| route-local | 19 | `9f2717165d8862ae858626bfef6e9a0434c1eb49afc8f8588279302e3f8b20e3` |
| route-uncertain | 15 | `b636bb33ceff6ad54708d64f3ad5a8436fe891bcce57c89d968c0d8b085afbd6` |

Digest procedure: apply the existing runner's `files` and `hashes` functions to each case directory, serialize the path-to-SHA256 mapping as UTF-8 JSON with sorted keys and compact separators, then SHA-256 that serialization. These identify this review candidate, not a new runtime identity scheme.
