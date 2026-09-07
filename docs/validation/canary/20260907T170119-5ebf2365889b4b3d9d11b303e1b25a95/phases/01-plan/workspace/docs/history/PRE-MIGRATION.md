# Pre-migration planning documents

Captured verbatim from this fixture before the fresh-context design/plan revision
on 2026-09-07. These are historical statements, not evidence of a completed review.
No prior review reports were present in the fixture file inventory.

## docs/DESIGN.md

```markdown
# Current design
The caller reads data/active.json and loads the selected v1 file. Stable IDs are
unique; duplicate IDs are errors. No migration or recovery protocol exists yet.
```

## docs/PLAN.md

```markdown
# Current plan
Complete: v1 reading. Pending: design and review v2 migration before execution.
```
