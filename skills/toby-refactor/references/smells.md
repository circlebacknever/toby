# Local cleanups

Ask each question below of the changed code. Before you fix or report a match, read the sentence that says when the code is fine. When the proof needs code outside the diff, quote the search you ran. `references/cleanup.md` says which fixes this pass makes and which become follow-ups.

**Does a function return its result by changing an argument?** For example, `apply_discount(order)` sets `order.total` and returns nothing, so the caller has to read the body to find the write. The code is fine when the language returns a result and an error that way, as C#'s `TryParse(s, out n)` does. The same holds for a buffer the caller passes for speed, and for a method whose job is to change its own object. Fix: return the result and leave the argument unchanged.

**Does a bare number or string stand for a rule?** For example, `if attempts > 3` appears in two files, or a price gets multiplied by `0.0825`. The code is fine when the meaning is plain in a small scope, such as a loop's 0 or 1, or an HTTP status checked once. Fix: name the value once as a constant and use the name at each site.

**Does one function mix calls to helpers with low-level code written inline?** For example, `place_order()` calls `reserve_stock()` and `charge()`, then builds an SQL string for the receipt. The code is fine when the function is low-level all the way through, such as a parser or a numeric loop. Length alone is no reason to split a function. Fix: move that code into a function at the level of the calls around it.

**Does a comment next to changed code still describe the old code?** The comment is fine when it states something the diff did not change, such as a unit or an invariant that still holds. Fix: rewrite the comment to say what the code does now.

**Did the change make a comment elsewhere false?** Search the callers and the docs for the behavior the diff changed, such as a return type, an error, or an invariant. Report it only with the file:line, the quoted comment, and one sentence on how the diff makes it false. A comment you only suspect is out of date does not count. Fix: correct that comment.

**Does nothing call a function or class anymore?** Search for the name as a string before you decide. The code is fine when it is exported or public, or when something reaches it through reflection, dependency injection, dynamic dispatch, or a test harness. Fix: delete it.

**Does a boolean or enum argument pick which of two jobs a function does?** For example, `export(rows, as_pdf=True)` branches at the top into a PDF body and a CSV body that share no code. The argument is fine when it picks a value that the function's single job uses, such as `include_tax`. Fix: split it into one function per job, and give each a name that says what it does.

**Does a call need so many arguments that the caller checks the declaration for their order?** The same holds when two or three arguments are passed together through several signatures, such as `start` and `end`. The call is fine when each argument stands on its own and keyword arguments keep it readable. Fix: group the arguments that are passed together into one value type.

**Does a line call through three or more objects, as in `order.customer().address().city()`?** The caller then depends on every object in that chain. The line is fine for a builder or a pipeline such as `.filter().map()`, where each call returns the same kind of value. Fix: add a method on the first object that returns what the caller needs.

**Does a method mostly read another object's fields?** For example, `Invoice.shipping_label()` reads six fields of `Address` and none of its own. The method is fine when combining several objects is its job, as in a comparator or a mapper. Fix: move the method onto the object whose data it reads.

**Is a class only getters and setters, with no method named for what callers need?** The class is fine when it is a record kept as plain data on purpose, with its behavior in another module. Fix: replace the accessors with operations named for what callers need, and keep the fields private.

**Is a domain value, such as money, a phone number, or a date range, a bare string or number whose parsing repeats?** Report it only when the same parsing or validation already appears at two or more other call sites. Fix: add a small type that parses and checks the value once, and use it at each site.
