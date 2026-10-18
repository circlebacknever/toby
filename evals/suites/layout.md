# Layout tasks

This suite uses four tasks to check whether a writer chooses a clear diagram structure and places boxes, text, and arrows without visual defects. The four outputs are an SVG architecture diagram, a pptx slide, an HTML timeline, and an SVG flowchart, each paired with a layout report.

Every writer reads `skills/toby-artifact-style/SKILL.md` and `skills/toby-artifact-style/references/layout.md`, and uses only the facts each task gives.

## Run design

- Writers run on Sonnet, and an Opus grader evaluates each blinded output folder.
- Writers and graders render outputs with QuickLook (`qlmanage -t -s 1600 -o <folder> <file>`) with Inter and JetBrains Mono installed in `~/Library/Fonts`.
- Task 2 requires `python-pptx` and LibreOffice; skip Task 2 when either tool is unavailable.

## 1. SVG diagram

Draw an SVG diagram of the request path below with a title sentence, and save it to `layout-1.svg`.

Facts:

- A browser sends each request to the CDN.
- The CDN forwards requests it can't serve from cache to the load balancer.
- The load balancer routes each request to one of the API servers.
- The API server checks the Redis cache first.
- On a cache miss, the API server queries `PostgreSQL primary (us-east-1)`.
- The API server enqueues each email job on the job queue.
- A worker reads jobs from the job queue and calls the email service.
- When the email service returns an error, the worker returns the job to the job queue.

## 2. pptx slide

Write one 16:9 pptx slide showing the release process below. Save the `python-pptx` script to `layout-2.py` and the presentation to `layout-2.pptx`.

Facts:

- The release process runs five steps in order: Cut the release branch, Build the artifacts, Run integration tests against the staging database, Deploy to 5 percent of hosts, and Deploy to all hosts.
- Step 3 failed in 11 of 40 releases in August 2026.
- None of the other steps failed more than twice in August 2026.

Include a title sentence that states the finding, the five steps in order, and a callout on step 3.

## 3. HTML timeline

Write an HTML page showing the outage timeline below as a horizontal timeline, and save it to `layout-3.html`.

Facts (times in UTC on 2026-09-02):

- `14:02`: The error rate on `/checkout` rose above 2 percent.
- `14:05`: PagerDuty paged the on-call engineer.
- `14:11`: The team rolled back release 4.18.0.
- `14:12`: The error rate stayed above 2 percent after the rollback.
- `14:26`: The team found that the payment provider's TLS certificate had expired.
- `14:41`: The payment provider renewed the certificate, and the error rate fell below 0.1 percent.

## 4. SVG flowchart

Draw an SVG flowchart of the deploy script below with a title sentence, and save it to `layout-4.svg`.

Facts:

- `deploy.sh` first checks the working tree for uncommitted changes; when it finds any, it prints the changed files and exits 1.
- The script runs the test suite; when a test fails, it exits 1 without deploying.
- When passed `--dry-run`, the script prints the deploy plan after the tests pass and exits 0.
- The script deploys to 5 percent of hosts, then waits 10 minutes.
- When the error rate on those hosts exceeds 1 percent, the script rolls back and exits 3.
- Otherwise the script deploys to all hosts and exits 0.

## Layout report

After each task, write a layout report under `## Report 1` to `## Report 4` in `layout-report.md`. State the number of text boxes, the number of arrows or connectors, and any remaining defect, or state when you couldn't render the output.

## Grading

The grader renders each output and counts defects in six classes:

| Class | Defect |
|---|---|
| overflow | Text crosses the edge of its box, the canvas, the page (at 1280 CSS px), or the slide. |
| uneven padding | A box's top and bottom padding, or its left and right padding, differ by more than 2px. |
| crossing | An arrow crosses a box, a label, or another arrow. |
| ambiguous end | A reader can't tell which box an arrow starts or ends on. |
| crowded label | An arrow label sits less than 8px from another line or box. |
| off grid | A box sits off the row or column its neighbors share. |

The grader also counts fact errors (invented or omitted facts), missed defect claims in `layout-report.md`, five yes/no structure checks, and a 1-to-5 first-read clarity score:

| # | Question |
|---|---|
| 1 | Does the title answer one question a reader of these facts would ask? |
| 2 | Does the main path run straight in one direction, with exits and exceptions on one side? |
| 3 | Do outcomes of the same kind share one color and appear together in one row or column? |
| 4 | Is every label true every time, with anything conditional marked? |
| 5 | Is every node at the same level of detail? |
