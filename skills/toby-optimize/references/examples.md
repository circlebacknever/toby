# Worked Example

This file shows how to remove known performance bottlenecks at design time before running a profiler.

## Design-time frontend fix

A list view re-fetches the full dataset on every keystroke of a filter input, and each row component re-sorts a copy of the list. Neither line looks slow in isolation, yet together they stall typing.

Make both design-time fixes before profiling. Debounce the network fetch so it runs after typing pauses, or filter client-side when the dataset is small. Hoist the sort into the parent component so it runs once per list change.
