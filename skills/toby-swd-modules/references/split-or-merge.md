# Split or merge

This file gives the rules for splitting, merging, extracting, or inlining functions and modules.

## Merge

Merge two pieces when they share a design decision, when merging removes a duplicated rule, or when the merged interface lets callers skip manual coordination steps. Keep blocks separate when they look alike by coincidence and change for different reasons.

## Split

Split a function or module only when a reader can understand each piece on its own and each piece has a simpler interface than the original. Length alone isn't a reason to split, so keep a long function whole when its steps share local state behind one simple signature.

Two splits work well:

- Extract a self-contained helper function so the parent keeps its interface and the helper works on its own.
- Divide a function that does two unrelated jobs into two caller-visible functions, provided callers rarely need to call both halves in sequence.

## Inline

Inline a shared helper back into its callers when it has gained a boolean flag or a branch for each caller. Then extract only the code that every caller still shares.

## Conjoined methods

When you can't understand one function's body without reading another function's body side by side, the two functions are conjoined. Merge them back together or redraw the split so each function stands on its own.
