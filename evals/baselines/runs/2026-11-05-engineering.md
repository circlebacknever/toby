# Engineering checks

This run checks the repaired instructions with isolated implementation tasks, independent reviews, and explanation checks against source facts.

## Results

| Case | Original instructions | Revised instructions |
| --- | --- | --- |
| Build behavior and emitted diagnostics | 9/9 checks passed. | 9/9 checks passed. |
| Bug-fix behavior and emitted diagnostics | 9/9 checks passed. | 9/9 checks passed. |
| Complete review findings | 6/12 findings matched. | 12/12 findings matched after a reporting correction. |
| Guarded-only change | This case wasn't run. | The reviewer reported zero findings. |

The first revised review earned eight complete matches. Four findings demonstrated real failures but left the current cause implicit in the proposed repair. The reviewer instructions then required that causal explanation in the finding itself. Another fresh session produced twelve complete findings. Separate readers judged each review against the reproduced failures and existing guards.

The review covered arithmetic, account authorization, consumer compatibility, concurrent writes, payment retries, persisted recovery, resource bounds, outbound deadlines, rendered diagnostics, startup configuration, route registration, and shared refund rules. Private probes passed on the original application and failed on every seeded regression. The ordinary smoke tests passed in both versions.

The guarded-only preparation preserved the twelve contracts. Its SQL allowlist, role check, account-scoped cache key, and compatible receipt metadata remained valid. A fresh reviewer checked those guards and reported an empty findings array.

## Diagnostics

The execution grader invoked the domain operation and both entry points with controlled provider responses. It checked state after failure, retry behavior, repeated requests, preserved exception causes, and actual emitted JSON. Removing emitted diagnostics failed the grader even when behavior checks passed. Editing candidate tests couldn't hide the broken operation from the independent checks.

Both instruction versions passed these execution cases. These cases didn't show a behavior difference between revisions.

## Explanations

The comprehension judge rejected the corporate sentence that the syntax scorer accepted. It accepted the final concrete explanation and its joke, with nothing missing from the source facts. Earlier probes exposed an omitted qualifier and an unexplained term. Those outputs were preserved with the final probe.

The examples were authored to test the judge. They don't measure how often a writer produces a clear explanation.

## Verification

These commands passed:

```sh
python3 -B tests/test-eval-reporting.py
python3 -B -m unittest evals/test_execution.py -v
python3 -B tests/test-review-cases.py
python3 -B evals/review_cases.py verify
python3 -B evals/run.py gates
python3 -B tests/test-gates.py
git diff --check
```

The rule inventory and gate baselines were refreshed after review. The seeded gate regressions still failed as intended, and the restored tree passed. The package retains its token ceilings. Its bug-fix budget now includes the applicable design and operational skills.

The standard skill-creator validator couldn't start because Python couldn't import PyYAML. The repository's metadata, reference, instruction-sync, and package checks passed. I didn't install dependencies or update skill copies in user directories.

## Limits

Each implementation workflow has one paired sample. The revised reviewer had two attempts with a general reporting correction between them. These observations don't establish general reliability or a statistical improvement. All services in the fixtures were local substitutes.

Local outputs, judgments, instruction hashes, and the static viewer are under `evals/results/2026-11-05-skill-repair/`. Preparation, independent grading, and fresh-session instructions are documented in `evals/suites/execution.md` and `evals/suites/review-execution.md`.
