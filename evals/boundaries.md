# Skill boundaries

This table lists one row per skill. The fourth column states which skill takes priority when two skills share a topic, and the fifth column lists what each description's skip clause covers.

| Skill | Exclusive scope | Shared topics | Priority rule | Skip clause covers |
|---|---|---|---|---|
| `toby-swd-strategy` | design pass before writing, deadline shortcuts, near-future variants | refactors, API changes, special cases | strategy decides whether the design changes, while modules and interfaces decide the target structure | renames, formatting, read-only investigation, throwaway spikes, structure already fixed by surrounding code |
| `toby-swd-modules` | placement, split and merge, module boundaries | deep modules, general-purpose interfaces, special cases | modules decides where code goes | designing a signature, a one-file edit inside an existing module |
| `toby-swd-interfaces` | function and API signatures, the comment test, parameters | deep modules, general-purpose interfaces, caching contracts | interfaces designs the signature and comment | where a file goes, adding a field beside an identical one |
| `toby-swd-errors` | error paths, retries, validation | special cases | errors decides whether an error path is needed, while interfaces designs its signature | throwaway parameter loops, error paths the types already rule out |
| `toby-optimize` | measured performance, whether a cache or batch is worth its cost | caching, batching | optimize decides whether the cache is worth adding, while interfaces designs its signature | throwaway parameter loops, new behavior that includes a cache |
| `toby-swd-clarity` | names, comments, docstrings, hard-to-follow control flow | exported contracts | clarity covers the wording, while interfaces covers the contract | module docs, contract design |
| `toby-swd-testing` | test files, assertions, snapshots, regression tests | tests that follow a code change | testing loads when tests or snapshots change | a rename, a formatting pass, a throwaway spike, or a change that also edits production code |
| `toby-swd-docs` | `AGENTS.md` and `README.md` in the user's modules | public API changes | docs loads when the module's documented structure or API changes | code comments and docstrings |
| `toby-swd-environment` | commands, processes, ports, installs, migrations | nothing | environment loads before any state-changing, runtime, or slow command | a code edit that runs only focused tests, formatters, linters, or type-checks, and a snapshot update |
| `toby-swd-experiment` | spikes, parameter sweeps, throwaway debug code, proof of concept | retries, timeouts, tests, design | the word `throwaway` takes priority over every other noun in the prompt | work the user intends to keep, starting or stopping a server alone |
| `toby-build` | sizing, acceptance criteria, slicing, the approved plan | features, endpoints, screens | build handles new or changed behavior and opens the `toby-swd-*` method skills | wrong output, slow code, behavior-preserving refactors, throwaways, and one-file edits copying a local pattern |
| `toby-code-review` | findings on a diff or plan | "review my changes" | code-review loads when the user asks for review findings without edits | a request to change the code, or a question about how code works |
| `toby-refactor` | behavior-preserving cleanup | "review my changes" | refactor loads only when the user asks to change code while keeping behavior the same | a request for findings without edits, or a behavior change |

## Routing priority

When two skills appear to match one request, identify the decision the user is asking for and load the skill that covers that decision. Each entry skill's skip clause names the adjacent skill that takes the other requests.
