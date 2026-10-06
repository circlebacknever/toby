## toby-artifact-style

Apply Toby's artifact design system to a visual artifact. A visual artifact is an HTML, React, or SVG page or widget, a diagram, image, chart, dashboard, slide deck, mockup, printable reference card, or the copy inside one. Use it when the user asks for a visual or asks you to draw or show something, including a visual that teaches or explains. Skip it for a text answer in chat when no visual was asked for, which `toby-explain` handles, and for a game.

## toby-code-review

Report the real risks in a change the user asked about, and make no edits to the code. Use it for code review, PR review, diff review, commit review, working-tree review, or findings on changed code: bugs, regressions, missing tests, security issues, and repo-rule breaks. Skip it when the user asked for the code to be changed, which `toby-simplify-code` is for.

## toby-explain

Answer a question in plain words and stop. Use it when the user asks why something works the way it does, what the difference is, or how a thing works. Use it too for a walkthrough, a rationale, a trade-off, or plain English on any subject. Use it whenever the user asks for a clear, concise, short, simple, or direct explanation, in those words. Skip it for naming and comments inside code, which `toby-swd-clarity` is for, and for being taught a subject step by step, which `toby-learning` is for.

## toby-feature-dev

Turns a feature request into the smallest change that satisfies it, with evidence it works. Use it when the user asks to build, add, implement, wire up, or finish a behavior spanning more than one file or one call site. That covers a ticket, a product ask, a half-built feature, an endpoint, screen, job, or flag, or a bug fix whose repair is new behavior. Use it when the request does not define "done" and coding has to start anyway. Skip it for a one-file edit following a pattern already in that file, a review or cleanup pass over existing code, or read-only investigation or explanation. Skip it for a spike, proof of concept, or throwaway, which `toby-swd-experiment` is for.

## toby-game

Collaborate with the user to build a single-file HTML simulation game or toy in Toby's style. Trigger only when the user explicitly invokes this skill by name or with the `/toby-game` slash command. Do not trigger on a general request to make a game, a sim, a toy, a visualizer, or a simulation.

## toby-learning

Teach a subject by working through it, with the learner at the keyboard. Trigger only when the user explicitly invokes this skill by name or with the `/toby-learning` slash command. Do not trigger on a question that asks for an answer: "why is this slow", "what's the difference between", "walk me through", "help me understand". Those get a straight explanation, which `toby-explain` handles.

## toby-simplify-code

Reduce complexity in recently changed code while preserving behavior and tests. Use it when the user asks to simplify, tidy, tighten, refactor, de-duplicate, or clarify code that already works. Skip it when the user asked for findings and no edit, which `toby-code-review` handles. Skip it for a refactor that moves code between modules or changes a signature, which `toby-swd-modules` and `toby-swd-interfaces` handle.

## toby-squall

Brainstorm by widening from a single example to the broader set it belongs to. Trigger only when the user explicitly invokes the skill by name or with the `/toby-squall` slash command. Do not trigger on general brainstorming language like "help me think through this," "let's explore," or "brainstorm with me."

## toby-swd-clarity

Make the code readable to whoever maintains it next. Use it for naming, comments, docstrings, conventions, and control flow that confuses a reader, inside the code being touched. Skip it when the user wants a clear or concise explanation in chat, which `toby-explain` is for. Skip it for module documentation files, which `toby-swd-docs` is for, and for contract design, which `toby-swd-interfaces` is for.

## toby-swd-complexity

Decides whether an error path, a retry, a cache, or an optimization is worth its cost. Use it when a task touches error handling, retries, validation, recovery paths, caching, concurrency, batching, or a measured performance problem. Skip it for a throwaway parameter loop, which `toby-swd-experiment` is for, and skip designing the cache's surface, which `toby-swd-interfaces` is for.

## toby-swd-docs

Keeps the two module documents accurate: AGENTS.md for agents writing code in a module, README.md for humans using it. Use it when a task changes module structure, a public API, a cross-module decision, an extension rule, or human-facing module usage. Skip it for code comments and docstrings, which `toby-swd-clarity` covers.

## toby-swd-environment

Decides whether a command or a state change can run now or needs the user's approval first. Use it on any task that runs a command, starts or stops a process, takes a port, installs a dependency, or runs a migration or seed script. Use it too when a task updates a snapshot, clears a cache, edits credentials or settings, or otherwise changes state outside the edit itself. Skip it for a pure code edit with nothing to run.

## toby-swd-experiment

Runs a discovery loop when the behavior is not decided yet. Use it for a spike, a proof of concept, a parameter sweep, a comparison of options, or a throwaway debug surface. Use it too for a manual test or an iteration driven by user feedback. The word throwaway anywhere in the request takes priority over every other noun in it. This skill then covers the retry, timeout, and test questions raised inside a spike. Skip it for work the user intends to keep.

## toby-swd-interfaces

Decide what a callable surface exposes before writing its implementation. Use it when a task adds or changes a function, method, class, component props, hook return type, composable, REST endpoint, gRPC service, repository, cache interface, or message contract. Skip it when the question is where the code should go, which `toby-swd-modules` covers. Skip it too when adding a field beside an identical one already in that file.

## toby-swd-modules

Decide which module code goes in and which module defines each piece of knowledge. Use it when a task creates, moves, splits, merges, or places code. Use it too when one piece of knowledge is spread across functions, classes, services, files, packages, components, hooks, store slices, repositories, controllers, native modules, screens, or data layers. Skip it when the question is what one signature exposes, which `toby-swd-interfaces` covers. Skip it too for an edit inside one existing module that adds no new boundary.

## toby-swd-strategy

Decide whether this change leaves the design better or worse before writing it. Use it for non-trivial work, such as a feature, a bug fix with behavioral risk, a refactor, or a public API or module-boundary change. Use it too for an edit where the quick patch adds a special case or a hidden dependency. Skip it for read-only investigation, a rename, a formatting pass, a throwaway spike, and any change whose structure the surrounding code already determines.

## toby-swd-testing

Keeps tests an executable specification of behavior. Use it when writing, changing, deleting, weakening, or snapshotting a test, or when a failing test could pass by a change to its assertion. Use it whenever a behavior change or a bug fix in production code needs a matching test. Skip it when the change leaves behavior unchanged: a rename, a formatting pass, a comment edit. Skip it for a throwaway spike, which `toby-swd-experiment` covers.

## toby-voice

Revise Toby's prose before it is sent: a substantive reply, review findings, a commit message, a PR description, a doc, a plan, or artifact copy. Load it before finalizing prose, and do not wait to be asked. Use it when the user says `voice`, `toby voice`, or `voice pass`, or asks for a rewrite, banned-phrasing help, tone repair, or wording help. Skip it for names and comments inside code, which `toby-swd-clarity` covers, and for an explanation, which `toby-explain` covers.
