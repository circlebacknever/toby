# Skill boundaries

This table lists one row per skill. The fourth column states which skill takes priority when two skills share a topic, and the fifth column lists what each description's skip clause covers.

| Skill | Exclusive scope | Shared topics | Priority rule | Skip clause covers |
|---|---|---|---|---|
| `toby-swd-strategy` | design before changing responsibilities, contracts, dependencies, or invariants | refactors, API changes, special cases | strategy compares designs after the applicable module and contract checks | prose and formatting with unchanged design properties |
| `toby-swd-modules` | placement, responsibilities, hidden knowledge, caller coordination | deep modules, general-purpose interfaces, special cases | modules checks the boundary even inside an existing function | implementation details with unchanged responsibilities and caller burden |
| `toby-swd-interfaces` | callable contracts, side effects, errors, ordering, and lifetime | deep modules, general-purpose interfaces, caching contracts | interfaces checks caller obligations, including unchanged signatures | field additions with unchanged caller obligations and guarantees |
| `toby-swd-errors` | error paths, retries, validation | special cases | errors decides whether an error path is needed, while interfaces designs its signature | throwaway parameter loops, error paths the types already rule out |
| `toby-optimize` | measured performance, whether a cache or batch is worth its cost | caching, batching | optimize decides whether the cache is worth adding, while interfaces designs its signature | throwaway parameter loops, new behavior that includes a cache |
| `toby-swd-clarity` | names, comments, docstrings, hard-to-follow control flow | exported contracts | clarity covers the wording, while interfaces covers the contract | module docs, contract design |
| `toby-swd-testing` | test files, assertions, snapshots, regression tests | tests that follow a code change | testing loads when tests or snapshots change | a rename, a formatting pass, a throwaway spike, or a change that also edits production code |
| `toby-swd-docs` | `AGENTS.md` and `README.md` in the user's modules | public API changes | docs loads when the module's documented structure or API changes | code comments and docstrings |
| `toby-swd-environment` | commands, processes, ports, installs, migrations | nothing | environment loads before any state-changing, runtime, or slow command | a code edit that runs only focused tests, formatters, linters, or type-checks, and a snapshot update |
| `toby-swd-experiment` | spikes, parameter sweeps, throwaway debug code, proof of concept | retries, timeouts, tests, design | the word `throwaway` takes priority over every other noun in the prompt | work the user intends to keep, starting or stopping a server alone |
| `toby-build` | sizing, criteria, design, implementation, and verified diagnostics | features, endpoints, screens | build handles changed behavior and opens the applicable method skills | wrong output, slow code, behavior-preserving refactors, throwaways, and one-file text or formatting edits |
| `toby-bug-fix` | reproduction, bounded investigation, causal repair, regression and diagnostic checks | failure paths, design, tests | bug-fix repairs the cause and required diagnostic gaps, including across files | explanation-only questions, flaky tests, and performance work |
| `toby-swd-observability` | emitted diagnostic context and operational signals | failures, writes, retries, external calls | observability verifies actual output for affected operational paths | temporary debug output alone |
| `toby-swd-twelve-factor` | dependencies, config, process state, service connections, deploys, and log destinations | existing processes, concurrency, startup, shutdown | apply each affected constraint to both new and existing behavior | changes that leave those constraints unchanged |
| `toby-code-review` | findings on a diff or plan | "review my changes" | code-review loads when the user asks for review findings without edits | a request to change the code, or a question about how code works |
| `toby-refactor` | behavior-preserving cleanup | "review my changes" | refactor loads only when the user asks to change code while keeping behavior the same | a request for findings without edits, or a behavior change |

## Routing priority

When two skills appear to match one request, identify the decision the user is asking for and load the skill that covers that decision. Each entry skill's skip clause names the adjacent skill that takes the other requests.
