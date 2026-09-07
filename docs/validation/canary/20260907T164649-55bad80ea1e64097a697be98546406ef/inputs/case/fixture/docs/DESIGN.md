# Export format transition D2 — agreed
Clients currently read unversioned CSV. Client A can be updated this week; Client B follows next month and must continue working meanwhile. The exporter will support an explicit JSON option alongside unchanged default CSV. Both clients must opt in explicitly. Remove CSV only after both client owners confirm migration; removal is outside the current assignment.
For acceptance, JSON preserves SKU strings and integer quantities including zero, and existing CSV consumers see byte-compatible output for the same input.
