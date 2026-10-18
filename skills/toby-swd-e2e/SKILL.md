---
name: toby-swd-e2e
description: >-
  Contains Toby's rules for end-to-end tests through a real entry point. Use it
  when writing a test that drives a route, a CLI command, a screen, or a job
  the way a user does. Skip it for unit tests, which toby-swd-testing covers.
---

# Toby SWD End-to-End Tests

Prove each slice with a test that drives the feature through its real entry point and wiring.

## Find the harness

Find the repo's end-to-end setup and add the test in its style. Open `references/harnesses.md` for the files and markers used in each stack.

When the repo doesn't have an end-to-end harness, use the framework's in-process test client when one exists. Otherwise propose a minimal harness only when the user asked for an e2e test or the work is strategic under `toby-build`. In other work, run the entry point manually, quote the output, and list the missing harness as a follow-up. Ask before installing a tool or starting a server or container (`toby-swd-environment`).

## Drive the entry point

| Entry point | The test |
| --- | --- |
| HTTP or RPC | sends a request through the test client or running app and asserts the response |
| Inbound webhook | posts a payload signed with the provider's test secret and reads the stored result |
| CLI | runs the command as a subprocess and asserts stdout, stderr, and exit code |
| Web screen | opens the page in a browser, selects elements by accessible role or visible label, and clicks what the user clicks |
| Mobile screen | opens the app on a simulator or emulator and taps what the user taps |
| Library function | imports the public API as callers do (from the installed package when packaging or exports change) and calls it |
| Queue consumer | publishes a message to the test broker and reads the stored result |
| Scheduled job | runs the job's entry command and asserts what it wrote |

For a queue consumer, ask before starting a container (`toby-swd-environment`) and run the broker with testcontainers or the repo's test compose file. Assert what the caller observes: the response body, rendered screen text, or state read back through the API.

## Real and fake

Keep everything inside the service boundary real: database, migrations, config loading, routing, and auth middleware. Point the test at an isolated test database, and make custom harnesses refuse any connection URL that isn't a test database.

Fake only third-party services at the network edge by stubbing the HTTP call in the provider module, using a local stub server, or using the framework's test mail backend (`:test` in Rails, `locmem` in Django). A test that mocks an internal module is a unit test.

## Test data

Create test data through the public API or seed helpers with unique ids, and clean up in a transaction rollback or teardown hook so a failed assertion mid-test doesn't leave rows behind. Wait for an observable condition (a row saved or a selector visible) and never sleep for a fixed duration.

## How many

- Write one e2e test per slice for its primary behavior plus one per failure criterion, and keep combinatoric edge cases in unit tests.
- When a feature spans two or more slices, add one whole-feature test in the final slice that walks through every slice in order (such as invite, accept, then sign in).

## Run it

Run the test before and after the change in the format `toby-swd-testing` gives (failing before and passing after for new behavior), and state the CI command that runs it. When a test requires credentials or hardware you don't have, write the test, mark the criterion `unverified`, and give the user the command to run.
