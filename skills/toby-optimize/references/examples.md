# Worked Example

This file has a worked case of avoiding slow code at design time, before any measurement. Open it before the first measurement on a new design.

## Example — Frontend: prevent many small slowdowns at design time

A list view re-fetches the full dataset on every keystroke of a filter box. Also,
each row component re-derives a sorted copy of the list. No single line is
"slow", but together they make the view sluggish.

Make the design-time changes before any measurement. Typing into a filter is
known to be expensive when each keystroke makes a network request. Debounce the fetch, so it waits until typing
pauses. When the set is small, filter it client-side. Both are as simple as the slow
version.

Sorting the list again in every row repeats work on a path known to run often.
Move the sort to the parent component so it runs once. The debounce and the
single sort are fast and simple, and they come before any profiler session.
