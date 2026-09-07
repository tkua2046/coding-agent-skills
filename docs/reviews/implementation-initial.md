# Initial implementation review

**Verdict: needs changes.** Three P2 findings remain pending: template-resource validation is skipped, some local Markdown link forms bypass validation, and rerunning the manual hook trial overwrites earlier evidence. The scoped baseline checks and this reviewer's hook trials passed; those results do not resolve these reproduced defects or approve unchecked work.

Reviewer: independent code/content reviewer using the stage-development review operation; not the implementation author. Date: 2026-09-06. Review policy: owner-authorized autonomous review and local self-tests; no human approval is claimed.

## Frozen baseline and finalization

This report is finalized against the owner-supplied frozen snapshot at `/Users/tk/Documents/coding-agent-skills/artifacts/implementation-review-baseline`, with the durable [baseline archive](implementation-baseline.tar.gz) and [manifest](implementation-baseline-manifest.json). All finding locations, dispositions and earlier check results refer to that baseline and the recorded candidate hashes, not the now-changing canonical product files. F1–F3 remain pending for this reviewed version; later fixes require their own follow-up disposition.

Compared the supplied manifest with the previously recorded fingerprints: all 47 shared entries match. The appendix retains original fingerprints for items not enumerated by the supplied manifest, including discovery links, root .gitignore and the source-workflow record. Archive SHA-256: `7045ad23cdb15d5ba3b891c651f8ffba4cbf186bb6b39cb4a620ac52dfea3038`. Manifest SHA-256: `c755e9951db0806fc260b5aff877cc1d53dedd800925a7a9f48810f0696ba413`.

Finalization only associated the existing evidence with the durable baseline and updated this report. No new product inspection or runtime test pass was performed; the archive contents were not separately re-extracted/revalidated. The incomplete and unreviewed areas listed below remain unchanged. No changing canonical product files were read or modified during finalization.

## Scope and candidate

Reviewed all four skill bundles (entrypoints, operation prompts, metadata, templates, Python samples and document-ownership reference), tools/check.py and its package initializer, tests/test_check.py, tests/manual/hook_trials.py, root hook/dependency configuration, four discovery symlinks, README, DEVNOTES, AGENTS and CHANGELOG. VERSION and .gitignore were supporting inputs. Grounded the review in SPEC, the reviewed DESIGN, IMPLEMENTATION_PLAN and source workflow.

The repository had no HEAD commit: this is an initial working-tree candidate, including staged additions and the untracked manual trial script. The appendix identifies 49 product files/symlinks; their hashes matched the then-live checkout at the last comparison, before canonical fixes began. Two ignored Ruff-cache metadata files were incidentally captured but were not reviewed product content. No product, test, design, index or hook files were changed in the live checkout; only this report was written there.

## Findings

### F1 — P2: Validate literal resource links inside templates

**Location:** tools/check.py:74–75; tests/test_check.py:25–30. **Basis:** SPEC R7/R8; DESIGN:39.

**Observed counterexample:** In a separate copy, appended `Read [required supporting rules](missing-support.md).` to skills/feature-design/assets/design.template.md without creating the target. validate_bundle returned an empty error list, the checker CLI exited 0, and all 17 existing pytest cases still passed. The condition excluding every Markdown file under an `assets` path prevents checking this real template dependency.

**Consequence:** A shipped template can refer to unavailable supporting material while both the packaging check and the independent-copy regression report success. This is a demonstrated checker defect, not a claim that the reviewed templates already contain that broken link.

**Minimal correction:** Validate literal resource links in asset Markdown too; exempt actual example/placeholder content narrowly instead of skipping the directory. Determine asset membership relative to the bundle, not arbitrary ancestor directory names.

**Verification:** Add regressions for a missing and an escaping template dependency, plus a valid template/example control. Both direct bundle validation and the repository CLI must reject the broken cases. **Disposition: pending.**

### F2 — P2: Route local Markdown link forms through boundary validation

**Location:** tools/check.py:21–25. **Basis:** SPEC R7; DESIGN:9 and 39.

**Observed counterexamples:** In separate copies, appended either `[required supporting rules](file:///nonexistent/skill-review-rules.md)` or a reference-style link, `[required supporting rules][rules]` with `[rules]: missing-support.md`, to skills/feature-design/prompts/draft-design.md. Both returned no bundle errors and checker exit 0. The scheme shortcut skips the local file URI, while the inline-link-only expression never discovers the reference target.

**Consequence:** Missing or machine-specific runtime dependencies can evade the same portability checks that reject equivalent ordinary relative links.

**Minimal correction:** Resolve reference-style local targets through the existing existence/boundary checks. Reject nonportable file URIs, or explicitly resolve and validate them; do not classify them as remote documentation merely because they have a scheme.

**Verification:** Each reproduced form must fail, while an existing in-bundle reference target and an ordinary HTTPS documentation link remain valid. **Disposition: pending.**

### F3 — P2: Preserve each manual trial's evidence on rerun

**Location:** tests/manual/hook_trials.py:14 and 160–162. **Basis:** SPEC R8; skills/dev-workflow/references/documents.md:27–29 explicitly requires retaining earlier failed evidence.

**Observed counterexample:** In an experimental copy only, removed the sample hook configuration and ran the script: it exited 1 at hook installation and wrote its failure report. Restored the exact configuration and reran: it exited 0 and replaced that report at the same fixed path. Only hook-trials.json remained in its report directory, and the first fixture was no longer referenced. This used this reviewer's own runs; no other trial outputs were read.

**Consequence:** The normal failure/fix/rerun loop destroys the script's earlier recorded failure unless someone separately archives it. A later successful record cannot explain the original defect and follow-up by itself.

**Minimal correction:** Write immutable per-run reports with unique identities and tested-input hashes; a separate latest-result pointer may be updated. Retain failure records even when setup or assertions abort a run.

**Verification:** A failed run followed by a successful rerun must leave both original reports retrievable and unchanged, with their respective inputs and outcomes. **Disposition: pending.**

## Checks actually run

All executing or file-changing experiments used temporary copies. Commands below ran from the scoped copy; its `.venv` referenced the existing installed tools. Python was 3.12.4; installed versions matched requirements-dev.txt. A separate pre-commit cache was used.

| Check | Observed result |
|---|---|
| `.venv/bin/python tools/check.py` | Exit 0 on the unmodified scoped candidate. |
| `.venv/bin/ruff check .` and `.venv/bin/ruff format --check .` | Both exited 0. |
| `.venv/bin/python -m pytest` | 17 passed; reported 100% line/branch coverage for tools. F1 demonstrates the limit of that coverage result. |
| `.venv/bin/pre-commit install --install-hooks`, then `run --all-files` after staging the copy | Both exited 0; every configured hook passed, including the test hook in its isolated environment. |
| `.venv/bin/python tests/manual/hook_trials.py` | Exit 0: real temporary commits covered passing baseline/control, unchanged failing test, documentation-only failure, zero tests, Ruff edits requiring restaging, and source branch/missing-line reporting. |
| Three resource-link counterexamples | Checker incorrectly exited 0 for all three; the template-link variant also passed all 17 existing tests. |
| Evidence-retention reproduction | First run exited 1; restored-input rerun exited 0 and overwrote the first report. |

To avoid reading other trial outputs, the scoped test copy included the four grounding documents but used empty stand-ins for the out-of-scope linked JUSTIFICATION and VALIDATION documents. Other evidence/review documents were omitted. Accordingly, this is a passing gate on the **scoped product copy**, not a claim that every documentation link or the entire live repository's final gate was verified.

Not reviewed/run: other agents' outputs; live validation records; CI workflow/execution; remote links or live editor discovery; fresh-agent behavioral scenarios for intake, human-review handling or delivery/release; remote PR/tag/release actions. Release and review prompts received content inspection only. Environment recreation with uv was not tested; existing pinned tools and fresh isolated hook environments were used. No ongoing checks remain. No further runtime checks were started after the stop request.

## Next action

Use F1–F3 as baseline findings in the fix/review loop; record fixes with focused regressions and a separate review of the changed candidate. Incorporate separately gathered behavioral findings through the owner's fix/review loop; this report supplies no conclusion about those unseen results. No commit, stage acceptance or release approval is claimed.

## Candidate fingerprints

SHA-256 of raw file bytes; symlink hashes cover the literal target string, not the referenced directory. The original captured 51-entry JSON inventory, including the two incidental cache files, had SHA-256 `c45af5398397a5f92cffc9811395c78c0fe7ddce5f37479a1cd746578d0566ca`. The 49 reviewed product entries follow.

<details>
<summary>Product file and discovery-link hashes</summary>

```text
4a521cc68fd3564b6bf779a38812e79b330ecd83bdeab8fffef426e4829c3e54  .agents/skills/dev-workflow -> ../../skills/dev-workflow
8c152e08b630643a04463cdab3e9eb6ea2113e4da6fcad02c2939416a8ac68b9  .agents/skills/feature-design -> ../../skills/feature-design
dad14c8d74ba6a689b35394b376d7d71269f15bc49006db2fd3555d92e3a242e  .agents/skills/implementation-plan -> ../../skills/implementation-plan
69e5b484cae1eb2d4c03c96c00e3607c3f2b7bb5787fb91fb36aab503b43f930  .agents/skills/stage-development -> ../../skills/stage-development
6c8055812ee82cebf0fdbfaa643e85518f9bc59544786a0661da4ad7f3e71738  .gitignore
dbdc45bdf9a1682098855d8ee881365c05526634abecbe42d3e8028aa7d16e2c  .pre-commit-config.yaml
5f208d20a5edb9489b38eaa967e47e475044ae676d26b32428ac06f6cfe06174  AGENTS.md
d33979422628a86d44b8e845947455d4e641cd6ec1f37f978e16d4499166dc22  CHANGELOG.md
073fe01c825302904d841e399d76f97dee553df2cefd25ae8895d584b30bbe75  DEVNOTES.md
105c02e93b7076a5e84f694944e110b20662bc181a2f3f9685a2a2e50020e181  README.md
e9dd8507f4bf0c6f42458e41aea833ad0bd3f6127272335eee9bf4d58541ed67  VERSION
bcf473a5e2f348ca97f8102762a428e197ad1f842c63e2d2162a441d2006057c  pyproject.toml
d70d2075e66397b2966e80c356ad33c8af50eee807f60243bddc15e07b0ac404  requirements-dev.txt
1ad6784270d94f61f889bb308a97eb4855316c4e62ee84c24fedd948920ee962  skills/dev-workflow/SKILL.md
d0ce96fe3def1a63baa63f17f78ffb50ef569342336c9836bdfb227e9170466a  skills/dev-workflow/agents/openai.yaml
f922029f25c1ada60f46caed9b4b5d461d9fe21004cb2d8bb8a3b1a4f2279b9e  skills/dev-workflow/assets/AGENTS.template.md
887f54671f5fc076d03973cf4a2cd6535bdefbd1fc35f1b3846f76f53a02c693  skills/dev-workflow/assets/CHANGELOG.template.md
1063ef489aa7352847704b797b5da30798d9bd3ac72af81cd8c740a7d1f4b106  skills/dev-workflow/assets/DEVNOTES.template.md
a1e270244164500531e1cdf417f08234eda99ed4b2db9ac046061d6b34698f0d  skills/dev-workflow/assets/README.template.md
25b5ff3cdb359415b551b62d0712ccd4a37ea4f722e71f1ee51358121ad7956b  skills/dev-workflow/assets/python/.gitignore
a1a625b38e9a5198a45dd988faa178da571de8bdd3ca924b0291651545ad7e5e  skills/dev-workflow/assets/python/.pre-commit-config.yaml
a94db893f5664417906783deb7fcfcf505c8870829cf1c42b0c4ffbfdb0170e9  skills/dev-workflow/assets/python/pyproject.toml
74d7432adab7fa9d24ce355860074e6bb4cf03efe4157515076c215cb6f36747  skills/dev-workflow/assets/python/requirements-dev.txt
f0d6378816325a5c899f387b54e345d7ef8263701adc7219fa3011c739299a77  skills/dev-workflow/prompts/prepare-pr.md
8dde75600df5d31df9aeebb9e065c761160c5cee0b513340b9ec4534aed7d0cd  skills/dev-workflow/prompts/release.md
b03ce35b5b693b4974249003f284fa19b12e24bc33ebdc213c5cde537f994e5f  skills/dev-workflow/prompts/setup-dev-workflow.md
f2557f82931406e67241957769cd0e7e3d63e3719ced9d862f7e30909e2b75e8  skills/dev-workflow/references/documents.md
50a18f13bc8eff518003360c587af01c1f186a3bdf712922b8c9f8e7a6acc6e0  skills/feature-design/SKILL.md
656474af7a2bbc3f0e5eaf07dd2ed64b48f51a4b16fb0ee23f97c5d85a8206d8  skills/feature-design/agents/openai.yaml
76edf19a1075de9709ff4d9dbbd8a2c4c6aa87d602a8c72a7470ca847980e633  skills/feature-design/assets/design.template.md
046adeb78bb104cd3d7d357619189fe68a4e78a04ace93b6c8dbdfe6d80582e7  skills/feature-design/assets/review.template.md
8dacf653bbef1753fdb00924b6c94a966db2264b21e52f9f1225718313da4a04  skills/feature-design/assets/spec-addendum.template.md
5dd5f1796792b450ae0ec3cae9dee14c4f0207ab89464b8149fbc5578f961bd9  skills/feature-design/prompts/draft-design.md
50bb1db115d8473218c4bad7acc125f0c7cb8b729dbd9b8f87a4b73474ddfcb8  skills/feature-design/prompts/intake-feature.md
2cbfa664c01d4963c516bd6f42de29f861277e1b409e9ba7f396e421457b24d8  skills/feature-design/prompts/review-design.md
80bfe6f7330791e5b74498256af140b02a3f1a8fb33bc8adc9fddee2e291deb1  skills/implementation-plan/SKILL.md
1bd92cd5f5bfae5654a0cfd39a79f6a45ffdb5b09b16ded896fd2918a279d495  skills/implementation-plan/agents/openai.yaml
85206c6d9915e5f46199b81d32f293b3d95dd2e679f5fc49892d6f7c7f76b39f  skills/implementation-plan/assets/implementation-plan.template.md
31c2e16fd6cf51d08b32d59adbf995988734db1be235bb090aa9836026156ac5  skills/implementation-plan/prompts/plan-implementation.md
3f16da430e37fd585571154cf94a997fc7d8c325b810c34e22bc8a76fd82f506  skills/implementation-plan/prompts/review-implementation.md
d6453bb770dcf31fa17f7c6a5c5ce5310dea1169d7f9a1554cde19bf9649a0fd  skills/stage-development/SKILL.md
6e7972bb39551305a96b06c4bf68b2eccca436ee2ecd92cad1912b3642549a21  skills/stage-development/agents/openai.yaml
50762c6b4fa46bb4f6655fba937ac3bb6bdbc7870ca17a46a222ab2b1f32b76d  skills/stage-development/assets/stage-record.template.md
1c95d847591b242c27e595a209abd60894f8db516d963f457dd2ade7f2e8e687  skills/stage-development/prompts/execute-stage.md
cd4a53a0ab7208708739221ebad5a657553ee79dfeffd6cbfa768c37bf891e21  skills/stage-development/prompts/review-stage.md
73225657eb1a6c087acf1a6c05a97568294f1487c3fb5d0de7f70f31f181e473  tests/manual/hook_trials.py
efd0ffa8f3d8fc986639b5a64de2835732da3970d65fc789de45d5415adef91d  tests/test_check.py
76f14fd7c8343652459119320cb53b7e919dac7435e7ba7bb66ef7d1c4f4426d  tools/__init__.py
d0fa54d90cd8d2b9ec9ce7dd41b79919467b70f73041a89a42dfe2e43fdd93ad  tools/check.py
```

</details>

Grounding inputs:

```text
c6ccfca7c06e6e23e59b9ce5426a98e7b37988345634e73c52317cbb7aafebf0  docs/SPEC.md
2572c3820c0cfa3bf6f6f5bd948db5d978f5cd0bb361e141e26bd38aaaee1da4  docs/DESIGN.md
3906d221080a07299ffc97eacd9e67214a61cc49b3aed61db2e93dc06319024a  docs/IMPLEMENTATION_PLAN.md
42ca833c2de59629480a06b8be256cde55885a9a0d0aabb33e3afffd8b48b47e  docs/sources/user-workflow.md
```

Reviewer-created raw logs and reproductions remain in the temporary review workspace `/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skills-stage-review-9wkwb_kn` (candidate-gate.log, manual-hook-trials.log, portability-probes.json, evidence-overwrite-probe.json and the retained failure backup). The findings and observed outcomes above do not depend on those temporary files remaining available.
