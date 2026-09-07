# Design D1
Work on a private copy of caller stock. Preflight all items in each batch before any debit, then debit the full accepted batch. This prevents a partial rejection without rollback state. Example: stock a=2,b=0; batch a=1,b=1 rejects and leaves a=2,b=0; following batch a=2 succeeds. No persistence/concurrency is required.
