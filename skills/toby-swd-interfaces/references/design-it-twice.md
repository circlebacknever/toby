# Design it twice

This file has the steps for writing and comparing two or three interface designs. The file also covers how to choose between designs that both pass the comment test, and how to ask a separate reviewer for a verdict. Open it when an interface is consequential or a routine interface's first comment fails.

## The loop

1. Write one possible design as function signatures with their interface comments and empty function bodies. Each comment says what the function does and leaves out how it does it.
2. Run the comment test.
3. If it fails, state what failed ("the comment had to describe the retry buffer"). Then write the next design so that it divides the work differently and no longer has that flaw. A rename does not count.
4. Stop when one design passes for a routine interface, when two designs pass for a consequential interface, or when you have written three designs. Never write more than three designs.

If none of the three designs passes, show the user the best one and say which comment-test condition it fails.

## Choose between passing designs

For a routine interface, take the first passing design. When two or more designs for a consequential interface pass, rank them by these four criteria in order:

1. How little work the common call asks of the caller.
2. How many uses the design covers.
3. How fast the design runs and how few resources it uses.
4. How much the design hides without hiding anything callers need.

When a separate review tool is available, ask it for a verdict before you rank the designs, as "Asking a reviewer" below describes.

If the user rejects all designs, treat their stated reason as one new flaw. Generate exactly one more design that fixes that flaw, then stop.

## Asking a reviewer

Send the reviewer the passing signatures and interface comments only, with no implementations and no hint of your preference. Send the four comment-test conditions and the ranking order too. Ask for one answer that states the chosen design and gives a one-line reason for each ranking criterion. Also ask the reviewer to list any design that might hide something callers need. Treat the reviewer's answer as one input to your choice. Before you write the function body, fix any case the reviewer found where a design hides something callers need.
