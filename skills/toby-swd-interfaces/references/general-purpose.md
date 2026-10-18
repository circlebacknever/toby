# General-purpose interfaces

Open this file when comparing interface designs so the chosen signature serves multiple callers without adding speculative options.

Ask these four questions early:

- **What is the simplest interface that covers all current needs?** Use fewer methods that each handle more cases so the interface stays small.
- **How many callers will use this method?** Inline a method that has one call site and only forwards its arguments.
- **Is this API easy to call for the common case today?** A general `find(query)` beats thirty `findByXAndY` methods only when the common call stays short.
- **Does it keep one purpose?** Split an interface when it starts serving unrelated jobs.

Cover today's needs plus only the specific changes that the request, a ticket, or the code states.

## One method per caller variation

When each combination of conditions gets its own `find`, handler, or query method, replace them with one method that takes a query object describing the conditions.

## One interface type per caller

Let each caller declare a small interface listing only the methods it calls, and let one class or module implement all of them (`references/backend-apis.md` shows a Go example).

## Parameters

Compute a value inside the module whenever callers can't pick a better one, because even a defaulted parameter adds a choice callers must read.
