# Order report request

Support staff report that large order batches take too long. We need a next step
for improving the existing report without changing its results. A teammate has
suggested moving to a database, shared cache and background job queue. No profile,
representative production trace, agreed latency target or measured bottleneck has
been supplied, and no infrastructure choice has been approved.

The catalog is fixed within a report batch; it may change between separate calls.
Users require integer-cent subtotals in order sequence through the current API.
The supplied source and tests describe the current implementation. Advise what work
should happen next and what would justify going further.
