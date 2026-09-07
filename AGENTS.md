# Working in this repository

- This repository contains reusable skills, not interview answers or private project material.
- Skill entrypoints and engineering artifacts are English; original source quotations keep their language.
- Keep each `skills/<name>` directory independently usable. Resolve runtime references within that directory.
- Read the relevant skill operation when designing, planning, implementing or reviewing this repository.
- Reviewers report findings against identifiable content and do not modify the reviewed product files. Never claim human approval or independent review without evidence.
- Keep user instructions in README, contributor operations in DEVNOTES, significant changes in CHANGELOG, and design/plan/review details in docs.
- Preserve original requirements and prior review findings using immutable references. Keep raw execution archives outside the source branch; publish complete cited evidence separately and link it from docs/EVIDENCE.md. Never force-add ignored run outputs.
- Stage only intended files; run the gate documented in DEVNOTES and address material findings before delivery.
- Normal commits/PRs require fast checks; expensive canary runs are deferred until release. Before tagging/publication require the current `tools.canary release-gate` to pass. Preserve failed attempts and disposition evidence; do not call fast/control results proof of skill behavior.
- Global installation, tag/release and unrelated external actions require their own task scope; do not repeat questions for actions already authorized.
- At existing outcome boundaries, assess the whole result against the original goal and cost. Final acceptance includes the complete source diff and actual usability, not only passing checks.
