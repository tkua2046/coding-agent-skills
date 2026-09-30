# Accepted ordering worksheet design D2
Validate the entire input with the existing loader, then filter quantity <= reorder_at.
Keep the default complete export, row shape/order, normalization and exit codes.
An invalid omitted row still fails before replacing destination bytes. Equality counts;
header-only/no matches succeeds with []. Reuse the atomic writer after full validation.
The local in-memory scope does not need a streaming architecture.
