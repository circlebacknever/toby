# Backend APIs (Java, Go, TypeScript)

This file covers bulk calls to a backend API. Open it when a change makes many calls to one service.

## Bulk calls

Replace a loop that makes one call per row across a network with one batched call. 500 sequential 2 ms round trips add a second before any work runs. The bulk method splits large input into chunks. For each input, the bulk method returns either created or rejected with a reason, so the caller can act on a partial success. A loop that calls code inside the same process can stay row by row.
