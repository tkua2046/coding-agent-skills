Use skills/feature-design's intake/investigation guidance on this existing order
report. A teammate proposes replacing it with a database, cache service and job queue
because large batches are slow. We have not established the cause. Investigate with
a bounded local experiment and recommend what to do next, with actual evidence and
its limits. The catalog is fixed within each report batch. Preserve production code
and its tests; this task does not authorize the proposed rebuild or feature delivery.
Keep a short findings entry at docs/INVESTIGATION.md; original commands/results may
live separately. No dependencies, remote services or commit. Budget: five minutes.


Use only this fixture and the supplied skills/. Read fixture AGENTS.md if present. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.
