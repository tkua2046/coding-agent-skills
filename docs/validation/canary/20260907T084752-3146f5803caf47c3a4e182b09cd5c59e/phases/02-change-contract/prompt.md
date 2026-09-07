The fixture user has now confirmed a public behavior change: a blocked forward
move stops the command batch immediately. Return the unchanged pose and the
outcomes through that failed command; omit outcomes for commands not attempted.
The confirmation is preserved in docs/STOP_REQUEST.md. Use skills/feature-design
and skills/implementation-plan to revise the affected current contract, design,
acceptance and pending work. This phase is planning only: implementation follows
later. Preserve prior requests and completed-stage history. No commits or
external actions.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
