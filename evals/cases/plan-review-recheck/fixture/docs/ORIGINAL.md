# Original request
Client A needs an opt-in JSON inventory export this week. Client B deploys next month and must continue receiving byte-identical default CSV meanwhile. Exporter capability must be available before A enables JSON. Preserve SKU strings and integer quantities including zero. Malformed quantities must fail without emitting a partial export. CSV removal is outside this assignment.
