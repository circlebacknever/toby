# Pass-through methods and variables

This file has the fixes for check 4 in `SKILL.md`. Open it when a method only forwards a call, or a value passes through code that does not use it.

- A **pass-through method** does almost nothing except forward arguments to another method with a near-identical signature. Fix it by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two methods.
- A **pass-through variable** is a value passed through a chain of methods that don't use it, such as prop drilling in frontend code. Fix it with an object that the first and last methods in the chain both reach directly. A context object also works if it stays small and preferably immutable.

A decorator that adds little is a shallow pass-through. Before adding one, ask whether the behavior goes in the underlying module.
