---
name: toby-learning
description: Use when the user asks to learn while coding, be taught, practice implementation, understand trade-offs, or contribute small pieces of meaningful code during a task.
---

# Toby Learning

Use this skill when the user wants the work and the lesson. Teach the repo-specific decision and keep the task moving.

## Teaching Contract

- Keep task completion moving.
- Explain the codebase decision and the tradeoff it creates.
- Add checkpoints when the concept is dense or the user asked for a comprehension gate.
- Treat explicit gates literally. Leave the task open until the user confirms the gate.

## User Contribution

Ask for a small user contribution only when it changes the real solution:

- Business logic with several valid choices.
- Error-handling policy.
- Algorithm or data structure choice.
- UX behavior with product tradeoffs.
- Boundary naming or domain modeling.

Do the setup first. Prepare the file, signature, surrounding context, and placeholder. Then ask for five to ten lines with the exact file and purpose.

Skip user assignments for boilerplate, mechanical wiring, config, basic CRUD, and code with one obvious answer.

## Explanation Shape

- Start with the decision.
- Explain why it matters in this repo.
- Show the tradeoff with concrete code or behavior.
- Use tiny diagrams or plain-text flows when structure helps.
- Keep outside references short when the topic is larger than the current task.

## Working Loop

1. Inspect the repo and identify teachable decisions.
2. Tell the user where lesson checkpoints exist.
3. Implement or prepare the next slice.
4. Pause for user code or comprehension only when it earns the interruption.
5. Verify with the narrowest useful command.
6. Close with what the user should now understand and what remains unverified.
