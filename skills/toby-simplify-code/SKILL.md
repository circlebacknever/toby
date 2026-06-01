---
name: toby-simplify-code
description: Use when the user asks to simplify, tidy, tighten, refactor, de-duplicate, clarify, or reduce complexity in recently changed code while preserving behavior and tests.
---

# Toby Simplify Code

Use this skill to make changed code easier to read while preserving behavior. If behavior must change, switch to feature or bug-fix work.

## Rules

- Preserve behavior.
- Prefer local style over generic taste.
- Work on recently modified code by default. Broaden scope only when the user asks or touched code depends on nearby cleanup.
- Keep the diff small. Whole-file formatting is separate work.
- Preserve tests. If a test looks wrong, classify the behavior it protects first.
- Stay at readability. Restructuring modules or redesigning interfaces is feature-dev's job (toby-swd-strategy, toby-swd-modules). If a cleanup isn't small, local, and behavior-preserving, leave it and note it as a follow-up.

## Simplification Targets

Look for:

- Repeated setup or branches that can be named once.
- Parameter juggling that leaks a lower-level mechanism into callers.
- Long conditionals where early returns or named predicates expose intent.
- Shallow wrappers that only rename another call.
- Comments that narrate obvious code. (toby-swd-clarity)
- Clever one-liners, nested ternaries, or dense chains that make debugging worse.
- Names that expose history while hiding purpose. (toby-swd-clarity)

Keep:

- Helpful domain boundaries.
- Explicit error handling. (toby-swd-complexity)
- Slightly longer code that makes state changes visible.
- Tests that describe behavior through public interfaces. (toby-swd-testing)

## Process

1. Inspect the diff and nearby patterns.
2. Identify candidate simplifications and discard any that risk behavior drift.
3. Make one coherent cleanup pass.
4. Run the narrowest relevant verification.
5. Re-read the diff and check that the caller now reads closer to intent.

## Final Response

State what got simpler and what verification ran. If behavior could not be proven, say what remains unknown.
