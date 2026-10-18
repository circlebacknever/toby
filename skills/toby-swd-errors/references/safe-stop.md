# Safe stop

This file lists the stopping point for each kind of program when an unrecoverable error reaches step 4 of `toby-swd-errors`.

- A pure computation or CLI command logs diagnostics and exits with a non-zero code.
- A process controlling physical hardware or external transfers brings the system to a defined safe state before exiting.
- A supervised worker stops and lets its supervisor restart it in a known-good state.
- A multi-request server aborts only the failed request or task, rolls back its transaction, and keeps serving other requests.
