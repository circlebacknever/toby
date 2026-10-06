# Skill boundaries

One row per skill. The fourth column decides which skill wins a shared rule. The
fifth column lists what the description's skip clause has to state.

| Skill | Owns alone | Shares | Who wins the shared rule | Never fires on |
|---|---|---|---|---|
| `toby-swd-strategy` | the design pass before writing, tactical debt, near-future variants | refactors, API changes, special cases | strategy decides whether the design changes at all; modules and interfaces decide what it changes to | renames, formatting, read-only investigation, throwaway spikes, structure already fixed by surrounding code |
| `toby-swd-modules` | placement, ownership, split and merge, boundary lines | deep module, general-purpose bias, special cases | modules owns where code lives | designing a signature, a one-file edit inside an existing module |
| `toby-swd-interfaces` | the callable surface, the comment test, parameters, the accessors and shallow red flags | deep module, general-purpose bias, caching surface | interfaces owns the contract | where a file goes, adding a field beside an identical one |
| `toby-swd-errors` | error paths, retries, validation | special cases | errors decides whether the error path is earned; interfaces designs its surface | throwaway parameter loops, error paths the types already rule out |
| `toby-optimize` | measured performance, whether a cache or a batch is earned | caching, batching | optimize decides whether the cache is earned; interfaces designs its surface | throwaway parameter loops, new behavior that includes a cache |
| `toby-swd-clarity` | names, comments, docstrings, control flow a reader trips on | exported contracts | clarity owns the wording; interfaces owns the contract | module docs, contract design |
| `toby-swd-testing` | test files, assertions, snapshots, regression tests for a fix | tests that follow a code change | testing fires when behavior changed | a rename, a formatting pass, a throwaway spike |
| `toby-swd-docs` | `AGENTS.md` and `README.md` in the user's own modules | public API changes | docs fires when the module's documented surface moved | code comments and docstrings |
| `toby-swd-environment` | commands, processes, ports, installs, migrations, state outside the edit | nothing | environment always fires on a command | a pure code edit with nothing to run |
| `toby-swd-experiment` | spikes, parameter sweeps, throwaway debug surfaces, proof of concept | retries, timeouts, tests, design | the throwaway frame outranks every noun inside it | work the user intends to keep |
| `toby-build` | mode, acceptance criteria, slicing, the approved plan | features, endpoints, screens | build owns multi-file new behavior and opens the swd method skills | a one-file edit following a pattern already in that file |
| `toby-code-review` | findings on a diff the user asks about | "review my changes" | code-review fires on the word review | a request to change the code |
| `toby-refactor` | behavior-preserving cleanup the user asked for | "review my changes" | refactor fires only when the user asked to change the code | a request for findings |

## The arbitration rule

Two skills matching means one of them owns the decision being made and the other
owns a decision nobody asked for. Name the decision in one sentence, load the
skill that owns it, and leave the rest. The Skill Routing section of `base/toby.md`
tells the agent to load one entry skill per request, picked by its description.
Each skip clause names the skill that takes the request.
