# Split or merge

This file has the details of check 7 in `SKILL.md`. Open it before you split, merge, extract, or inline code.

## Merge

Merge two pieces when check 1 puts them in one module, or when merging removes a duplicated rule. Also merge when the merged interface is simpler because it does automatically what callers used to coordinate. Keep blocks separate when they look alike and change for different reasons.

A cache uses a hash table, but hash tables serve unrelated callers, so check 1 does not put them in one module.

## Split

Split only when the resulting pieces are independently understandable and each interface is simpler than the original. Length alone is not a reason to split, so a long method that is one deep abstraction with a simple signature stays whole.

One valid split extracts a general-purpose subtask, so the parent keeps its interface and the child method works on its own. The other valid split divides a method doing unrelated things into separate caller-visible methods. Take the second split only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so do not make that split.

## Inline

Inline a shared helper back into its callers when it has gained a flag parameter or a branch for each caller. Then extract only the code that every caller still shares.

## Conjoined methods

Apply the conjoined-methods test. If you can't understand one method's implementation without reading another's, the two methods are conjoined. That pair is a red flag even when the methods share a file.
