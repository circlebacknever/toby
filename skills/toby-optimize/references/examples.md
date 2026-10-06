# Worked Example

This file has a worked case of design-time performance. Open it before the first measurement on a new design.

## Example — Frontend: prevent many small slowdowns at design time

A list view re-fetches the full dataset on every keystroke of a filter box. Also,
each row component re-derives a sorted copy of the list. No single line is
"slow", but together they make the view sluggish.

Make the design-time changes before any measurement. Typing into a filter is
known to be expensive when each keystroke makes a network request. Debounce the fetch and
filter client-side when the set is small. Both are as simple as the slow
version.

The per-row re-sort is redundant work on a
known-hot path. Lift the sorted derivation to the parent so it runs once. The
debounce and the lifted sort are naturally efficient and simple, and they come
before any profiler session.
