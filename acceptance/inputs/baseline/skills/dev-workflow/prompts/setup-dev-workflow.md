# Set up or adapt a development workflow

Read repository instructions, README/developer guide, runtime/dependency configuration, existing checks, CI and local Git state.

Before changing an existing check's code/configuration, establish its observed baseline. Reuse applicable evidence or run the cited gate separately, capturing and inspecting its own output/exit condition before editing. The last command in a compound invocation does not establish an earlier command's result; an enforced exit condition does not establish an unobserved test count. If evidence is missing, record the baseline as unverified and proceed with justified authorized repair. A failing baseline is not an all-green prerequisite, and later checks establish the later state only.

Adapt only a demonstrated gap or explicitly requested change; an existing effective gate does not need replacement to match the sample. For inspection, use relevant actual gate results and report gaps; probe an unchanged runner's failure behavior only for an unresolved propagation risk. For new or changed runners, wrappers, discovery or hooks, verify meaningful collection, passing/failing execution and relevant failure propagation through the affected path. A direct runner check does not prove an installed hook executed. Reuse established tools; Python samples are optional examples.

## Checks

- Provide a clear normal check entrypoint and commit gate. For Python, Ruff handles lint/format; pytest can run pytest or unittest tests with coverage.
- Configure actual application source/module paths, branch measurement, missing-line output and optional machine reports. Account for subprocess execution when relevant. Do not leave the example's `app` source selector in an unrelated repository.
- Coverage reports and coverage failure thresholds are distinct decisions. Preserve an existing threshold; otherwise do not invent a required percentage. Test assertions, failure behavior and independent expectations matter beyond coverage.
- Run Ruff fixes before formatting. Inspect generated changes and restage them. Exclude environments, caches and generated reports from version control.
- A full-suite hook uses `pass_filenames: false`; run it even for documentation commits when that is the chosen policy. It must propagate test failures and zero-test collection failures. Do not suppress failures to bootstrap an empty project.
- Match hook interpreter and dependencies to the application. The Python sample's isolated test environment includes test tools only; add required project/runtime dependencies or use the repository's established environment deliberately.
- Before installing hooks, verify the intended local repository/worktree. Preserve existing hooks and custom hook paths. Prewarm dependencies and exercise a passing and failing case in an isolated fixture. Merely writing YAML does not prove installation or execution.
- Separate fast commit/PR checks from expensive integration or agent behavior trials when the project needs both. Keep required hooks effective; schedule the heavy suite before release and label it pending on ordinary PRs. A new demonstrated defect needs a retained regression case. Do not rerun a full expensive suite for every small prompt/doc edit.
- If this project itself maintains agent behavior, preserve relevant versioned behavioral regressions and their real outcomes. Reuse its evaluation system; an ordinary application setup request does not require creating an agent-testing framework.

## Documents and completion

Apply the document ownership reference, using the owned root templates as needed. Preserve original files or version history when moving content, update links and metadata, and avoid two copies of the same authoritative instructions.

Finish with a compact result and next action, including applicable changes, verified commands, hook status, coverage policy, document mapping and limits. In an inspection, report demonstrated facts and relevant gaps; absent optional tools are not automatically defects. Support both capabilities and alleged gaps with observed output, actually enforced conditions or inspected applicable configuration/source. Remembered framework behavior is an assumption until supported for this environment. Intended checks and expected output are not evidence; missing evidence stays unverified until resolved by a focused check or disclosed as a limit. Wrapper success cannot establish unchecked child results. Keep detailed output outside README/CHANGELOG. If no application tests exist, say so and schedule meaningful tests with the first implementation stage.

After drafting that report, load [delivery checks](../references/delivery-checks.md). Correct supported issues; expose unresolved limitations. Otherwise the check is silent and adds no report or review round.
