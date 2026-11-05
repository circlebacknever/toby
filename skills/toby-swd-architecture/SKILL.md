---
name: toby-swd-architecture
description: >-
  Defines feature structure and checks design in a finished diff. Use it when
  a change affects responsibilities, rules, writes, dependencies, failure
  behavior, or startup wiring, including existing paths. Skip it
  for a question about how existing code works, which toby-explain covers.
---

# Toby SWD Architecture

This file defines where each part of a feature goes and what to check in the finished diff.

## Default structure

Use this structure when a change affects a rule, write, dependency, responsibility, or failure path, including behavior inside existing functions. UI code follows `toby-swd-modules`' `references/web.md`, and libraries accept clients as arguments from the calling app.

Check the nearest sibling feature against the applicable design questions before copying its entry point, rules, and data access. Reuse the parts that pass. A tactical change needs this check too.

- **Entry point.** A route, view, CLI command, queue consumer, or job runs these steps in order:
  1. Authenticate the caller, check route-level role guards, and parse input into a typed value.
  2. When the input identifies one record, load it by id scoped to the caller, as `get_object_or_404(Invoice, id=invoice_id, account=request.account)` does.
  3. Call one operation and format its return value as a response.
  4. Write the outcome log defined in `toby-swd-observability`, unless middleware already logs it.
- **Operation.** A function or model method named for the business action, such as `renew_loan()`. It enforces every business rule, price, limit, state transition, and record-level permission check.
- **Writes and API calls.** One module writes each table, and one module calls each third-party API and converts the provider's SDK types into the repo's domain types.
- **Startup wiring.** Startup code builds clients from typed config. Only the startup wiring and the config module read environment variables.
- **Dependencies.** Supply clients and clocks through the repo's ordinary composition mechanism according to responsibility, lifetime, and caller needs. Business rules depend on the behavior they need, with provider details converted at the boundary. Use a narrow consumer interface when it hides that dependency. Test convenience doesn't determine the production boundary.
- **Tests.** Control time and external effects through those boundaries or the repo's test tools. A fixed clock, fake client, or existing patch can each fit the chosen design.

| Framework | Operation | Startup wiring |
| --- | --- | --- |
| Django | a model method, or a function in `services.py` | `settings.py`, and module scope for clients |
| Rails | a model method, or a class in `app/services` if the repo has one | `config/initializers` |
| FastAPI, Flask, Express | a function in a domain module, such as `loans.py` | the file or factory that creates the app |
| Serverless | a function in a module the handler imports | module scope, so warm starts reuse clients |

In Django and Rails the model writes its own table, so add a repository only when the repo already uses repositories.

Compute each price, limit, status transition, or format in one function that every caller calls. Place that function beside existing rules of that kind and cite `path:line`. When existing rules are in an entry point, put the new rule in an operation and move the old ones there when `toby-swd-campfire` allows. A three-line rule doesn't need a service class, repository, or interface. Open `references/examples.md` for Rails and Express examples.

## Design check

Check the questions that apply to the finished diff, including changed behavior behind an unchanged signature. Fix each problem required for the requested change. Record a blocked correction with its effect and the check that remains unverified.

1. Does an entry point, or a serializer or form only it calls, compute a price, limit, status transition, or record-level permission? Move the rule into an operation (a caller-scoped lookup by id stays).
2. Does code write a table or call an external API that another module manages? Call a function in that module instead.
3. Does shared code branch on a specific caller or customer id (`if account.id == ACME_ID`)? Move that case to the caller or branch on a capability field.
4. Does a boolean or enum flag switch a function between two distinct jobs (`save(user, delete=True)`)? Split it into one function per job.
5. Does the diff compute a value that another function already computes? Call the existing function and cite both lines.
6. Does a new switch on a type, kind, or status repeat another switch on the same field? Make each switch exhaustive (`toby-swd-extensibility`).
7. Does an operation build a network client or read an environment variable? Move client construction to startup and env reads to the config module.
8. Does code outside a provider's module use the provider's SDK types? Convert them to domain types inside the provider module.
9. Does a write depend on a value read from its row when concurrent requests or jobs can race? Use a conditional write or row lock (`toby-swd-hardening`).
10. Does code hold a database transaction or row lock open across an outbound HTTP, RPC, or queue call? Commit or release the lock before the external call.
11. Does a loop run a database query or outbound API call once per item? Replace it with one batch read or bulk call before the loop.
12. Does the change expose a format, policy, or coordination step to multiple callers, or add an abstraction that hides nothing? Apply the depth and shared-knowledge checks in `toby-swd-modules`.
13. Can a caller bypass an invariant, depend on unrelated methods, or misread changed errors, side effects, ordering, or lifetime? Apply `toby-swd-interfaces` and update the contract and affected callers.
14. Can a changed operation fail without enough emitted context to identify what ran, its outcome, and its cause? Use `toby-swd-observability` and run its diagnostic check. Pure helpers don't need their own outcome logs.
15. Does the change affect process state, dependencies, config, concurrency, log output, or deploy behavior? Apply the relevant `toby-swd-twelve-factor` and `toby-swd-hardening` checks, even inside an existing process.
