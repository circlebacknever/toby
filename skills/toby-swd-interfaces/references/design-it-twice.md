# Design it twice

This file has the design-it-twice loop, tie resolution between passing candidates, and how to ask a critic. Open it when an interface is consequential or a routine interface's first comment fails.

## The loop

1. Write one candidate as signatures plus interface comments with empty bodies, and describe what each one does without describing how.
2. Run the comment test.
3. If it fails, state what failed ("the comment had to describe the retry buffer"). Use that flaw to build the next candidate, which is a structurally different decomposition that removes that problem. A rename does not count.
4. Stop as soon as one candidate passes for a routine interface, two pass for a consequential one, or you reach three candidates total. Never write more than three candidates.

If you reach three candidates and none passes, give the strongest candidate to the user and say what blocks it.

## Resolve a real tie

For a routine interface, take the first passing candidate. Rank two or more passing consequential candidates by common-case caller burden, then generality, then efficiency, then depth that hides nothing callers need. When an independent review tool is available, ask it first, the way "Asking a critic" below describes.

If the user rejects all candidates, treat their stated reason as one new flaw. Generate exactly one more candidate that fixes that flaw, then stop.

## Asking a critic

Send the critic the passing signatures and interface comments only, with no implementations and no hint of your preference. Send the four comment-test conditions and the ranking order too. Ask for one verdict, with the chosen candidate, a one-line reason per ranking item, and any risk that a candidate hides what callers need. Weigh the verdict as evidence, and fix any such risk before writing a body.
