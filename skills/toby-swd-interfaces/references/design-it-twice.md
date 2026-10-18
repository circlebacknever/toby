# Design it twice

Open this file when a first interface comment fails the comment test, or when a cross-module or public interface is new or changes what callers rely on.

## The loop

1. Write one candidate design as function signatures with interface comments and empty bodies.
2. Run the comment test on each signature.
3. When it fails, state what failed ("the comment had to describe the retry buffer") and write a second design that divides the work differently. A simple rename doesn't count.
4. Stop when one design passes for a local interface, when two designs pass for a cross-module or public interface, or after three designs.

When none of the three designs passes, show the user the best one and state which comment-test condition it fails.

## Choose between passing designs

For a local interface, take the first passing design. When two or more designs pass for a cross-module or public interface, rank them in this order:

1. How little work the common call asks of the caller.
2. How many uses the design covers.
3. How fast the design runs and how few resources it uses.
4. How much the design hides without hiding anything callers need.

If the user rejects all designs, treat their stated reason as a new flaw, write one more design that fixes it, and stop.

## Asking a reviewer

When a separate review subagent or tool is available, send it the passing signatures, their interface comments, the four comment-test conditions, and the ranking order above, without implementations or your preference. Ask which design it picks, one reason per ranking criterion, and whether any design hides something callers need. Fix any hidden caller need before writing the function body.
