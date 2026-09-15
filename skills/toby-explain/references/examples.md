# Worked Examples

These examples are not for reuse, so copy the pattern and write new material for the current question.

---

## New concept with no material shown yet

The user asks what a function is in mathematics. No code or equation has been shown yet.

→ `f(x) = x²` sends 3 to 9, and −3 to 9 as well. Two different inputs may share an output. The entire rule is that one input may never have two outputs. Check `x² + y² = 1` at `x = 0`. y comes out to both 1 and −1, so one input produces two outputs and the circle fails the rule. The whole test is to pick an input and count the outputs it produces.

---

## Decision inside work already underway

Mid-refactor, you just moved a range check from the controller into the repository layer.

→ I moved the range check into the repository because the controller has three callers now and two of them skipped it. The check belongs in the layer that every call path goes through. Moving the check costs one extra argument on the repository method. The cost is worth it, since a fourth caller is already planned for next sprint.

---

## Interpretation question with no single right answer

The user asks why the narrator keeps mentioning the color of the water.

→ One reading is that the water changes with the narrator's mood. The water is flat right after the argument with her sister, and stormy again three pages later when she lies to her mother. This reading fails if the color ever shifts with no emotional beat nearby. Check the two mid-book mentions before you claim the reading holds all the way through.
