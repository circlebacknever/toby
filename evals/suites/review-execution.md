# Review execution

This suite checks independent reviews against a runnable change with reachable defects and guarded changes.

Use the commands and matching rules in `evals/review_cases/README.md`. Materialize a new directory for each fresh reviewer session. Keep the gold, probe source, category inventory, and earlier reviews outside the reviewer inputs. Run the private before-and-after probes separately from the review.

For an instruction comparison, prepare both runs from the same fixture and use `--skills-source` for each instruction snapshot. Give reviewers the same task without the snapshot labels. A different reader judges each submitted report against the private gold. Record every missed cause and unsupported finding, plus precision and recall. A passing run requires every seeded cause and zero false positives. Record an input breach or access to gold as an invalid run.

Also run a fresh session on a guarded-only preparation using `--clean`. Its expected findings array is empty, but the task doesn't disclose that expectation. Check any reported issue against the real guards and unchanged contracts before grading it.
