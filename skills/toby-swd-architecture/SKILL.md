---
name: toby-swd-architecture
description: >-
  Contains Toby's default structure for feature code and the design check for a
  finished diff. Entry skills open this file by path. Do not trigger it from a
  user request alone.
disable-model-invocation: true
---

# Toby SWD Architecture

This file says where each part of a feature goes, and what to check in the finished diff.

## Default structure

Use this section for a change that adds or moves a rule, a write, or an outbound call. UI code follows `toby-swd-modules`' `references/web.md`. A library takes each client as an argument from the app that uses it, because the library has no startup code of its own.

Copy how the nearest similar feature divides its entry point, rules, and data access. Use the default below when the repo has no similar feature, or when that feature computes its rules in its entry point.

- **Entry point.** A route, view, CLI command, queue consumer, or job runs these steps in order:
  1. Authenticate the caller and parse input into a typed value.
  2. When the input identifies one record, load that record by id, scoped to the caller, as `get_object_or_404(Invoice, id=invoice_id, account=request.account)` does.
  3. Call one operation and turn its result into a response.
  4. Write the outcome log that `toby-swd-observability` defines, unless middleware already writes that line.
- **Operation.** An operation is a function or model method named for the business action, such as `renew_loan()`. The operation contains each rule that sets an outcome, such as a price, a limit, a status change, or whether this caller may act on this record.
- **Writes and API calls.** One module writes each table, and one module calls each third-party API. Other code calls a function in that module, such as `invoice.mark_paid()`. The module that calls a provider converts the provider's types into the repo's own.
- **Composition root.** The composition root builds clients from config when the process starts. Only the composition root and the repo's config module read environment variables.
- **Tests.** Pass a network client into an operation only when a test cannot patch it. Freeze time with the repo's tool, such as freezegun, `travel_to`, or fake timers, so operations need no clock parameter.

| Framework | Operation | Composition root |
| --- | --- | --- |
| Django | a model method, or a function in `services.py` | `settings.py`, and module scope for clients |
| Rails | a model method, or a class in `app/services` if the repo has one | `config/initializers` |
| FastAPI, Flask, Express | a function in a domain module, such as `loans.py` | the file or factory that creates the app |
| Serverless | a function in a module the handler imports | module scope, so warm starts reuse clients |

In Django and Rails the model writes its own table, so add a repository only when the repo already uses repositories.

Compute each price, limit, status change, or format in one function that every caller calls. Put a new rule beside the code that already computes that kind of value, and cite that code at path:line. When that code is in an entry point, or a serializer or form only it calls, put the new rule in an operation. Move the old code there too when `toby-swd-campfire` allows the refactor. A three-line rule needs no service class, repository, or interface.

When you cannot tell where a part goes, open `references/examples.md` for a Rails model and an Express webhook.

## Design check

Answer each question from lines in the finished diff, and fix each yes. A question with no line you can cite is a no.

1. Does an entry point, or a serializer or form that only it calls, compute a price, limit, status change, or permission on one record? Move the rule into an operation. A lookup by id scoped to the caller stays.
2. Does code write a table or call an API that a different module writes or calls? Call a function in that module.
3. Does shared code check which caller or customer it serves, such as `if account.id == ACME_ID`? Move that case into the caller, or make the general path handle it.
4. Does a `True` or `False` argument switch a function between two jobs, such as `save(user, delete=True)`? Write one function per job.
5. Does the diff compute a value that another function already computes? Call that function, and cite both lines.
6. Does a new switch on a type, kind, or status repeat another switch on the same field? Make each switch exhaustive, as `toby-swd-extensibility` describes.
7. Does an operation build a network client or read an environment variable? Build the client once at startup, and read the variable in the composition root or the config module.
8. Does code outside a provider's module use the provider's type, such as an SDK response object? Convert that type to the repo's own type inside the provider's module.
9. Does a write, such as a claim, counter, or status change allowed only from certain statuses, depend on a value read from its row? When two requests or job runs reach the row at once, lock it or make the write conditional, as "Concurrent writes" in `toby-swd-hardening` describes.
