# Voice tasks

Four voice-bearing outputs. Each is scored by the banned-word, foil, and
sentence checks in `scripts/validate-skills.py`.

1. **Status update.** You spent the afternoon on a flaky test. It fails on CI
   about one run in nine and passes locally every time. You found the cause: the
   test asserts on a timestamp formatted in the machine's local timezone, and CI
   runs in UTC. You have not fixed it yet. Write the status update to the user.

2. **Pushback.** The user says: "let's just add a retry wrapper around the whole
   sync job, it fails maybe twice a week and I don't have time to chase it." The
   job is not idempotent: a partial run writes rows, and a retry writes them
   again. Write the reply.

3. **PR description.** You moved rate-limit checks out of four route handlers
   into one middleware, deleted the duplicated token-bucket code, and added a
   test for the 429 path that did not exist. One behavior changed: the limit is
   now per-account rather than per-route-per-account. Write the PR description.

4. **"I don't know".** The user asks why memory use climbed 40 percent after
   last Tuesday's deploy. You looked at the diff and nothing in it allocates.
   You have no profiler data. Write the reply.
