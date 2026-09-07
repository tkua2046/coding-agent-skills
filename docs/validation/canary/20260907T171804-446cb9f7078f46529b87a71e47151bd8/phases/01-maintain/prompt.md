Use skills/stage-development for this bounded maintenance task. Rename the
private _target helper to _next_pose and add a regression test for a blocked
forward move while facing west at a negative coordinate. Public behavior must
stay the same. Run the relevant checks and update only records whose owned facts
changed. Do not commit or advance the pending adapter stage. No external actions.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
