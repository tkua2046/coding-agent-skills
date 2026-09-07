# Migration requirement
Migrate v1 settings into v2: {"version":2,"settings":{"theme":"dark","timeout":30}}.
Keep each stable ID and value. Before successful completion, including on crash,
original v1 data must remain usable. Retry cannot duplicate or drop entries.
The caller switches to v2 only after successful validation. No multi-process
migration is required. Existing active.json selects the current file/format.
