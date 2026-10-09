---
name: toby-swd-e2e
description: >-
  Contains Toby's rules for end-to-end tests through a real entry point. Entry
  skills open this file by path. Do not trigger it from a user request alone.
disable-model-invocation: true
---

# Toby SWD End-to-End Tests

Prove each slice with a test that uses the feature the way its user does, through the real entry point and the real wiring.

## Find the harness

Find the repo's end-to-end setup, and add the new test to it in its style. Open `references/harnesses.md` for the files, folders, and markers to search for in each stack.

When the repo has none, use the framework's in-process test client if it has one. Otherwise, propose a harness only when the user asked for an end-to-end test or the work is strategic under `toby-build`. Propose the smallest one, such as a test that starts the app and sends it HTTP requests. In other work, run the entry point by hand, quote the output, and list the missing harness as a follow-up. Ask before installing a tool or starting a server, as `toby-swd-environment` says.

## Drive the entry point

| Entry point | The test |
| --- | --- |
| HTTP or RPC | sends a request through the test client or to the running app, and reads the response |
| Inbound webhook | posts a payload signed with the provider's test secret and reads the stored result |
| CLI | runs the command as a subprocess and reads its output and exit code |
| Web screen whose changed behavior runs in browser JavaScript | opens the page in a browser and clicks what the user clicks |
| Mobile screen | opens the app on a simulator or emulator and taps what the user taps |
| Library function | imports the public API as callers do and calls it. When the change adds a module or data file or edits packaging config, it imports the installed package from outside the source tree |
| Queue consumer | publishes a message to the broker and reads the result the consumer stores |
| Scheduled job | runs the job's command and reads what it wrote |

For a queue consumer, run the broker in a container, as Dev/prod parity in `toby-swd-twelve-factor` says, with testcontainers or the repo's compose file. Start the consumer inside the test.

Assert what the caller sees, such as the response body, the text on the screen, or a row read back through the API.

## Real and fake

Keep everything inside the system real, including the database, migrations, config loading, routing, and auth middleware. Point the test at a database made for the run, such as a testcontainers Postgres or the `test_` database Django's test runner creates. When the harness reads the database URL itself, as a compose file or a start script does, make it refuse any other database. A framework runner that creates its own test database, such as Django's, needs no such check.

Fake only third parties outside the system, at the network edge. Patch the HTTP call in the provider's module, or use a stub server or the provider's sandbox. For outbound email, use the framework's test mail backend, such as Rails' `:test` delivery or Django's `locmem` backend. A test that mocks the module under change is a unit test.

## Test data

Create the data each test needs through the public API or a seed function, with unique ids. Leave no rows another test reads, so tests pass in any order. Wait for a condition, such as a row appearing or a selector rendering, and never sleep a fixed time.

## How many

- Write one test per slice for the behavior its criteria describe, plus one for each failure a criterion names. Edge cases belong in unit tests.
- When a feature has two or more slices, add one test with its last slice. That test walks through every slice in order, such as invite, accept, then sign in.

## Run it

Run the test before and after the change, in the format from `toby-swd-testing`, and watch the first run fail. State the command that runs it in CI.

When the test needs a credential, a device, or a paid service you cannot get here, write it anyway. Mark the criterion unverified, and give the user the command to run.
