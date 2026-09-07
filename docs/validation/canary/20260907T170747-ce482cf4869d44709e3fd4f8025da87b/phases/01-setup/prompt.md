Use skills/dev-workflow to adapt this existing project's local checks and document
audiences. Keep the application, CLI behavior, sample data and existing application
test suite unchanged. Retain unittest, qa/, the custom discovery configuration,
the existing hook delegation and the application-only branch coverage settings.
The installed local hook should run the full suite even for documentation changes
and fail if tests fail or discovery finds no tests.

Make the normal check command include coverage when the prepared interpreter
already provides it: show missing lines and write the machine-readable report to
the configured artifacts path. Keep the existing no-percentage-threshold policy.
If coverage is unavailable, retain a working stdlib gate and state that limitation.
Do not install packages, add dependencies or replace the environment/toolchain.

Keep README useful for a first-time user. Move contributor instructions and
historical development detail to suitable existing/conventional locations, keep
useful information and links, and avoid duplicating authoritative instructions.
Exercise the local gate and summarize what actually worked, document locations
and any remaining limits. Temporary checks must leave the workspace restored.
This is one authorized local setup task; no further approval round is needed.
No application feature work, commits, tags, pushes or external actions.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
