# Safe stop

This file lists the stopping point for each kind of program when an error reaches step 4 of `toby-swd-errors`.

- A pure computation aborts.
- A process driving something physical, costly, or external reaches a defined safe stop before it exits.
- A supervised, isolated unit stops, and its supervisor restarts it to a known-good state.
- A long-running loop stops only the smallest piece of work that failed, such as one request, and keeps running.

A violated invariant means the code has a bug.
