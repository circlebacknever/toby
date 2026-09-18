# Layout tasks

The grader uses four tasks to check two things. The first is whether a writer picks a structure the reader can follow. The second is whether the writer places boxes, text, and arrows without defects. The tasks are an SVG architecture diagram, a pptx slide, an HTML timeline, and an SVG flowchart. Each task also asks the writer for a layout report, so the grader can compare the writer's claims with the render.

Every writer reads `skills/toby-artifact-style/SKILL.md` and `skills/toby-artifact-style/references/layout.md`. Use only the facts each task gives.

## Run design

The user adopted `layout.md` on 2026-09-18, after the runs in `evals/results/layout-2026-09-17/` and `evals/results/layout-2026-09-18/`. Later runs follow this design unless the user agrees a different one.

- Writers run on Sonnet. Haiku made 57 to 84 layout defects per 6 outputs in both arms, with or without `layout.md`, so this suite leaves it out.
- Each run has one arm, because the user dropped the control arm once `layout.md` was adopted. Compare a new run with the Sonnet test rows of the two earlier reports.
- One Opus grader grades each writer folder, and the graders do not know which writer made which folder.
- Writers and graders render with QuickLook: `qlmanage -t -s 1600 -o <folder> <file>`. The machine needs Inter and JetBrains Mono installed in `~/Library/Fonts`, or QuickLook draws every label in a fallback font.
- Task 2 needs `python-pptx` and LibreOffice. Leave it out of a run on a machine without them.

## 1. SVG diagram

Draw an SVG diagram of the request path below, with a title. Write it to `layout-1.svg`.

Facts:

- A browser sends each request to the CDN.
- The CDN sends requests it cannot serve to the load balancer.
- The load balancer sends each request to one of the API servers.
- The API server reads from the Redis cache first.
- On a cache miss, the API server reads from `PostgreSQL primary (us-east-1)`.
- The API server writes each email job to the job queue.
- A worker reads jobs from the job queue and calls the email service.
- When the email service returns an error, the worker writes the job back to the job queue.

## 2. pptx slide

Write one 16:9 pptx slide that shows the release process below. Write the python-pptx code to `layout-2.py`, and write the slide to `layout-2.pptx`.

Facts:

- The release process has five steps, in this order: Cut the release branch. Build the artifacts. Run integration tests against the staging database. Deploy to 5 percent of hosts. Deploy to all hosts.
- Step 3 failed in 11 of 40 releases in August 2026.
- No other step failed more than twice in August 2026.

The slide shows a title sentence that states the finding, the five steps, and a callout on step 3.

## 3. HTML timeline

Write an HTML page that shows the outage timeline below as a horizontal timeline. Write it to `layout-3.html`.

Facts, times in UTC on 2026-09-02:

- 14:02 The error rate on `/checkout` rose above 2 percent.
- 14:05 The on-call engineer was paged.
- 14:11 The team rolled back release 4.18.0.
- 14:12 The error rate stayed above 2 percent after the rollback.
- 14:26 The team found that the payment provider's certificate had expired.
- 14:41 The payment provider renewed the certificate, and the error rate fell below 0.1 percent.

## 4. SVG flowchart

Draw an SVG flowchart of the deploy script below, with a title. Write it to `layout-4.svg`.

Facts:

- `deploy.sh` first checks the working tree for uncommitted changes. When it finds any, the script prints the changed files and exits 1.
- The script runs the test suite. When a test fails, the script exits 1 and deploys nothing.
- With `--dry-run`, the script prints the deploy plan after the tests pass, and exits 0.
- The script deploys to 5 percent of hosts, then waits 10 minutes.
- When the error rate on those hosts is above 1 percent, the script rolls back and exits 3.
- Otherwise the script deploys to all hosts and exits 0.

## Layout report

After each task, write a layout report under `## Report 1` to `## Report 4` in `layout-report.md`. Each report states the number of text boxes and the number of arrows or connectors. It lists every defect the writer found and did not fix. A writer that did not render the output says so in its report.

## Grading

Task 1 has 9 nodes, one arrow that points against the flow, and a 30-character label. Task 3 has event labels from 31 to 88 characters long, so one fixed card width does not fit all six. Task 4 has 3 decisions and 5 exits, with two failure exits that share `exit 1`.

The grader renders the SVG and the HTML page with QuickLook at full size, and converts the pptx slide to PNG with LibreOffice. QuickLook renders HTML at a page width of about 1024 CSS px. A page cut off at that width counts as overflow only when it would also be cut off at 1280 CSS px.

The grader counts defects in each class below, for each output.

| Class | Defect |
|---|---|
| overflow | Text crosses the edge of its box, the canvas, the page, or the slide. |
| uneven padding | A box's top and bottom padding, or its left and right padding, differ by more than 2px. |
| crossing | An arrow crosses a box, a label, or another arrow. |
| ambiguous end | A reader cannot tell which box an arrow starts or ends on. |
| crowded label | An arrow label sits less than 8px from another line or box. |
| off grid | A box sits off the row or column its neighbors share. |

The grader also counts fact errors. A fact error is a node, arrow, or label that states something the task facts do not say. A missing fact that the diagram needs is also a fact error.

The grader also answers each structure question below with yes or no, for each output. The grader writes n/a for a question when the output has nothing it asks about, such as outcome colors on a timeline.

| # | Question |
|---|---|
| 1 | Does the title answer one question a reader of these facts would ask? |
| 2 | Does the main path run straight in one direction, with exits and exceptions on one side? |
| 3 | Do outcomes of the same kind share one color and appear together in one row or column? A report-only exit, such as a dry run that prints a plan, is its own kind. |
| 4 | Is every label true every time, with anything conditional marked? |
| 5 | Is every node at the same level of detail? |

The grader also counts missed claims, which are defects in the render that the writer's report does not list. A report that states "no defects" for an output with 3 defects scores 3 missed claims.

The grader gives each output a score from 1 to 5 for how easily a reader understands it on first look. A score of 5 means a reader follows it at once.

The grader records the defect counts, the fact errors, the structure answers, and the score for each output. The run reports the distribution across samples, because single samples of the voice suite scored from 1 to 11 on identical inputs.
