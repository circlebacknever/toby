# Placement note

A placement note tells the reader where new code goes and why. Write one when you answer a question about where code goes, or when a plan or a handoff states a placement.

- Put the file and the place inside it in the first sentence, such as "The retry helper goes in `http/client.ts`, inside `request()`."
- Give each reason as a fact from the code or the request, such as the files that call the code, a limit, a count, or how often a value changes.
- Give a rejected placement its own sentence with its cost, such as "A helper in `billing/sync.ts` would leave `orders/sync.ts` without retries."
- Say what the code or the request shows about each caller.
- Do not write that a module owns, knows, or decides, or that code lives, sits, or belongs somewhere.
- Terms in this skill, such as deep module, leakage, and pulling complexity down, are for your reasoning. The note states the fact behind the term.
