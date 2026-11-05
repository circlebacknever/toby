# Fresh reviews

This fixture checks whether an independent reviewer finds reachable regressions and rejects guarded changes.

## Run

1. Run `python3 -B evals/review_cases.py verify` to check every private probe against both application versions. Each contract passes before the change and fails after it. The ordinary tests pass in both versions.
2. Run `python3 -B evals/review_cases.py prepare /tmp/parcel-review-<run>` with a new directory for each run. Add `--skills-source /path/to/snapshot` to compare instruction versions against the same fixture.
3. Start a fresh reviewer session with only the instruction to read `/tmp/parcel-review-<run>/TASK.md` and perform its review. Don't disclose this fixture source, gold, expected categories, or earlier findings.
4. Run `python3 -B evals/review_cases.py judge-prompt /tmp/parcel-review-<run>`. Give that prompt to a different fresh reader after the review finishes.
5. Run `python3 -B evals/review_cases.py grade /tmp/parcel-review-<run>/review.json /tmp/parcel-review-<run>/judgment.json`.

Run `python3 -B tests/test-review-cases.py` to check grading and isolation of reviewer inputs.

Prepare a separate session with `prepare /tmp/parcel-review-<run> --clean` to test a change containing only guarded edits and optional metadata.
The task doesn't disclose that the change has zero seeded defects.
Judge its findings against the actual diff, and grade with `grade REVIEW JUDGMENT --clean`.
An empty report passes. Any finding still needs independent verification before counting as an unseeded defect or false alarm.

## Matching

The reviewer writes its own findings before another reader sees the gold. The reader matches the submitted words to the same trigger, mechanism, and consequence, then checks the proposed repair. A category, a suggested pattern, or a source citation alone doesn't match. A matched finding requires four distinct excerpts from its own prose as evidence. The grader rejects incomplete judgments and source lines outside the file. The independent reader supplies the semantic judgment, and the script checks its structure and arithmetic.

Each matched cause earns one point. Each unsupported or duplicate finding loses two points. Report precision, recall, and the missed causes. A passing run finds every seeded cause without a false positive. Verify any real defect outside the gold before accepting the score.

The match measures a complete justified finding. An incomplete causal explanation can fail matching even when the cited code has a real defect. Keep that reason visible, and distinguish it from an invented defect when reporting the results.

## Boundaries

The concurrency probe uses two SQLite connections and a barrier after each stock read. The barrier exposes the proposed race without a timing guess. The timeout probe checks the argument sent to the external client. It doesn't contact a provider or measure a network timeout. Payment and publication probes inject faults at the external boundary and inspect the resulting state.

The materialized review directory contains the two application versions, the diff, the task, and the current instruction files. It doesn't contain the gold or private probes. A fresh session still has filesystem access outside that directory, so the task forbids reading the authoring checkout or earlier reviews. Record any breach as an invalid run.
