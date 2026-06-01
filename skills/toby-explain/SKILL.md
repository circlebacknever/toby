---
name: toby-explain
description: Use when the user asks for explanations, code walkthroughs, rationale, architecture notes, trade-off explanations, teaching, or educational commentary while work continues.
---

# Toby Explain

Use this skill when the user wants the work explained while it happens. Name the repo decision, explain the cost, then keep moving.

When the decision is one the swd-* skills govern, name the principle by its source so the explanation matches the rule being applied.

## Explain

- Why a file or module owns the behavior — deep modules, the knowledge each one owns. (toby-swd-modules)
- How data crosses the relevant boundary.
- Why one design has lower risk — invest or borrow against the system's future, and where complexity lives; the interface is the cost, the implementation is the benefit. (toby-swd-strategy, toby-swd-interfaces)
- What a test protects — behavior at the public interface, where callers notice it. (toby-swd-testing)
- What an error path or edge case means in practice — which rung of the error ladder it sits on and why. (toby-swd-complexity)
- What remains unknown after verification.

## Skip

- Generic framework tutorials unless the user asks.
- Line-by-line restatement.
- Decorative insight boxes.
- Long recaps after the user watched the work happen.

## Shape

- Use two or three sentences for most explanations.
- Put file references near the claim they support.
- Use cause and effect: `This belongs here because ...`
- Use a short plain-text flow when relationships matter.
- Keep final answers focused on result, verification, and risk.

## During Code Changes

Before editing, name the boundary being touched and why. After editing, explain the main decision and what verification actually proves.
