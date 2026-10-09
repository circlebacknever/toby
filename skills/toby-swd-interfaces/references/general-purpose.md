# General-purpose interfaces

Use these questions to check that an interface serves more than one caller and adds nothing for a need nobody has named. Open this file when you compare designs.

Build the functionality for current needs, and make the interface serve more than one use. When a signature fits only one caller, whoever writes the next caller has to change the signature. Ask these four questions early:

- **What is the simplest interface that covers all your current needs?** Use fewer methods that each handle more cases, so the interface stays small as needs grow.
- **In how many situations will this method be used?** A method that has one call site and only forwards its arguments to another call is a candidate for inlining.
- **Is this API easy to use for the common case today?** A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Does it keep one purpose?** An interface that serves unrelated purposes has become too general.

Do not add parameters or extension points for needs nobody has named. Cover today's needs plus one or two specific changes that the request, a ticket, or the code states.

## One method per caller variation

When each combination of conditions gets its own find, handler, or query method, the number of methods keeps growing. Replace them with one method that takes a query object or parameter describing the conditions.

## One interface type per caller

To follow the interface segregation principle, each caller declares its own interface type that lists only the methods it calls. One class or module provides all of those methods, so that class or module satisfies every caller's type. `references/backend-apis.md` shows an example in Go under "Go consumer interface".

## Parameters

Each parameter is one more value that every caller has to choose. Before adding one, check whether the module can compute the value itself, and whether any caller could pick a better value. Even a parameter with a default makes the person writing the call read it to know what the call does. So prefer a value the module computes, or a separate operation that does less, over a setting the caller passes.
