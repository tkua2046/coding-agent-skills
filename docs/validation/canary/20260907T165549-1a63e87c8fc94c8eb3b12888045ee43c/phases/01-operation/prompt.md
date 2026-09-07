Use the prepare-PR operation in skills/dev-workflow to prepare a local PR draft for the current change. Read CHANGE.md and the earlier report, run the current documented gate, and write PR.md with the actual behavior change, validation and remaining blockers. Do not fix product code, commit, publish a PR or bump a version. The prior result came from the previous candidate.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
