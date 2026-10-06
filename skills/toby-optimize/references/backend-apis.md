# Backend APIs (Java, Go, TypeScript)

This file covers bulk calls to a backend API. Open it when a change makes many calls to one service.

## Bulk calls

A loop that makes one call per row across a network turns into one batched call. 500 sequential 2 ms round trips add a second before any work runs. The bulk method chunks large input. It returns created or rejected-with-reason for each input, so the caller can act on a partial success. Code inside the process can keep its row-by-row loop.
