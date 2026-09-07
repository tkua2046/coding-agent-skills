Prepared the local PR draft: [PR.md](/private/var/folders/7w/2jmyflc53t3fhsxzmf590wk80000gn/T/skill-acceptance-lgowuf32/PR.md).

The documented gate ran with `CANARY_PYTHON` and failed: 1 test, 1 failure. `serialize("  x  ")` returns `"x"` instead of preserving spaces. The draft records this blocker and explains why the previous candidate’s passing report is no longer applicable.

No product code, version, commits, or remote state were changed.