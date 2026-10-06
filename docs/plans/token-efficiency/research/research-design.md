# Design research proposals

This file proposes edits to five Toby design skills from the design research findings. It edits no repo file. Each token count is the change in characters divided by 4, measured against the current files with `design_tokens.py` in this scratchpad folder. If the implementer applies every proposal, the five skills shrink by about 446 tokens.

The file holds 3 gaps, 3 conflicts, 8 rewrites, and 9 cuts. Only the gaps add tokens. A proposal with no Risk line weakens no rule that I found in AGENTS.md or the five target skills.

## Gaps

### G1. Separate refactor step

- Target: `skills/toby-swd-strategy/SKILL.md` line 54, in "The test for modifying existing code".
- Current: "Then refactor first and add the change on top with no workaround."
- Proposed: "Then refactor first with behavior unchanged, run the tests, and add the change on top as a separate step with no workaround. When the user asks for commits, the refactor gets its own commit."
- Evidence: Beck's March 2022 post starts from reviewers who say pull requests that mix refactoring and behavior changes are too long. His April 2022 post gives separate commits or pull requests as one fix. Fowler defines a refactoring as a change that keeps observable behavior the same.
- Reason a model fails: the skill tells the model to refactor first and gives no rule about keeping the refactor apart from the behavior change, so one mixed diff follows the skill. Model behavior here is unmeasured, so E6 proposes a measurement.
- Source: `https://newsletter.kentbeck.com/p/management-separate-tidying`, `https://newsletter.kentbeck.com/p/getting-untangled`, `https://martinfowler.com/bliki/DefinitionOfRefactoring.html`
- Tokens: +31.
- Risk: the AGENTS.md Work Loop says "act in one coherent diff". One diff can still hold two commits, so the user should confirm that reading.

### G2. Fields valid only in some combinations

- Target: `skills/toby-swd-interfaces/SKILL.md` Red flags, as a new entry after "One method per caller variation" on line 130.
- Current: no entry.
- Proposed: "- **Fields valid only in some combinations**: a comment has to list which combinations of optional fields, such as `data`, `error`, and `loading`, can occur. Where the language has union or sealed types, replace the fields with one variant per state."
- Evidence: Minsky's connection record had optional fields that allowed a session ID while disconnected. He replaced it with a type that has one record per connection state. Wlaschin models a contact that needs an email or a postal address as a union of the three valid cases. `skills/toby-swd-interfaces/references/web.md` Example 1 already uses a union for `useProduct`, but that file loads only for web code.
- Reason a model fails: `skills/toby-swd-clarity/references/examples.md` Example 4 returns three nullable fields and lists their valid combinations in comments, so the skills as written give the model the failure as an example. C3 changes that example.
- Source: `https://blog.janestreet.com/effective-ml-revisited/`, `https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/`
- Tokens: +63.
- Risk: in a language without sum types, a model may build a class hierarchy to imitate a union. The condition "Where the language has union or sealed types" limits the entry to languages with the feature.

### G3. Inline a helper that grew a flag per caller

- Target: `skills/toby-swd-modules/SKILL.md` check 7, "Split or merge", as a new paragraph after the Split paragraph on line 81.
- Current: no paragraph.
- Proposed: "**Inline** a shared helper back into its callers when it has gained a flag parameter or a branch for each caller. Then extract only the code that every caller still shares."
- Evidence: Metz describes a helper that gains a parameter and a conditional each time a new caller almost fits, until the code is hard to change. Her fix is to inline the helper, delete what each caller does not use, and extract again. Stevens, Myers, and Constantine wrote in 1974 that a module built by pooling duplicate code is often coincidentally bound, so a change for one caller can break the others. Metz cites experience and no study.
- Reason a model fails: the cheapest edit for a caller that almost fits is one more parameter. The interfaces red flag "One method per caller variation" replaces a set of methods with one method and a parameter, which is the same edit. That red flag fits methods that apply one rule to different values. G3 fits a helper whose branches apply different rules, so both entries stay.
- Source: `https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction`, `https://scrapbox.io/files/607d58d8fb61eb001eee7175.pdf`
- Tokens: +44.
- Risk: the simplify-code Out of scope section forbids moving code between modules, so simplify-code reports this case as a flag for `toby-swd-modules` to fix.

### Practices left out

- Functional core, imperative shell has one source, a 2012 screencast that states a rationale and compares no designs.
- Connascence gives names to kinds of coupling. Modules check 2 already gives the action, which is to count the modules one change touches.
- The rule of three as a fixed count comes from page 58 of Refactoring, which the research did not read. Jeffries on the c2 wiki removes duplication at the first copy. C2 merges copies only when they encode one rule, which needs no count.
- The interfaces Brownfield section and the simplify-code Behavior drift section already cover Hyrum's law, as listed under Aligned.
- CUPID lists five properties and cites no study. Each property overlaps a rule the skills already state, such as the simplify-code Idiom section for idiomatic code.
- TDD against bundling is a testing question for `toby-swd-testing`, which is outside these targets.

## Conflicts

### C1. Inferred near-future variants

- Target: `skills/toby-swd-strategy/SKILL.md` line 26, in "Before writing". The proposal also edits `skills/toby-swd-strategy/references/examples.md` Example 4, lines 109 and 127 to 128.
- Current: "State the change in one sentence, including the obvious near-future variants ("today there is one provider, but tomorrow there will be three")." Example 4 says "The word "today" in the first sentence implies the near-future variant."
- Proposed: line 26 becomes "State the change in one sentence, with each near-future variant that the request, a ticket, or the code states. Leave out a variant you inferred." In Example 4, line 109 becomes "The channels are email and SMS. The ticket adds push and Slack." Lines 127 to 128 become "The ticket states two more channels, each with its own client, so build the dispatch now:".
- The two sides: Ousterhout says to make a new interface somewhat general-purpose now. Fowler's YAGNI says to build no capability until it is needed. Early work costs the build, delays other work, adds complexity, and needs repair when understanding changes. Ousterhout's own lecture notes also say not to build specific features before they are needed. Example 4 builds a `Channel` interface and two classes because the task said "today". The modules ladder asks for "a case set that visibly grows" before option 4, so Example 4 also breaks a rule in `toby-swd-modules`.
- Recommendation: follow YAGNI for the cases and the dispatch code the model builds. Follow Ousterhout for the interface signature, which `toby-swd-interfaces` already limits to "near-future variants you can name".
- Source: `https://martinfowler.com/bliki/Yagni.html`, `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign`, `https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf`
- Tokens: -2.
- Risk: the design pass gets narrower. When a user implies growth without stating it, the model asks or lists the variant as an unknown, which the Source test in AGENTS.md already requires.

### C2. Copied code and a repeated rule

- Target: `skills/toby-swd-modules/SKILL.md` Red flags line 134 and check 7 line 79. The proposal also edits `skills/toby-simplify-code/SKILL.md` line 25, in "What to look for".
- Current: "**Repetition**: nontrivial code is repeated, so factor it to one place." Simplify-code says "Repeated setup or branches with two or more real occurrences, where defining them once removes lines."
- Proposed: the modules red flag becomes "- **Repeated rule**: one rule is written in two places, so a change to one must change both." In check 7, "or when it removes duplicated nontrivial code" becomes "or when it removes a copy of one rule". The simplify-code bullet becomes "- Repeated setup or branches that encode one rule, where defining them once removes lines."
- The two sides: the current rules count copies of code. Thomas says DRY means one representation of each piece of knowledge. In 2019 he said the "avoid copy and paste" reading was never its meaning. Stevens, Myers, and Constantine warned that a module built by pooling duplicate code is often coincidentally bound. Metz prefers duplication over the wrong abstraction. On the other side, Jeffries on the c2 wiki removes duplication at the first copy. Beck ranks no duplication third of his four rules. `toby-swd-clarity` Consistency already merges code only when the copies share knowledge, so two Toby skills give opposite rules.
- Recommendation: merge copies only when they encode one rule, because Thomas, Stevens, Metz, and the clarity skill agree on that rule. When two different teams ask for changes to the two copies, the copies encode two rules under R1's definition of a reason to change.
- Source: `https://www.artima.com/articles/orthogonality-and-the-dry-principle`, `https://changelog.com/podcast/352`, `https://scrapbox.io/files/607d58d8fb61eb001eee7175.pdf`, `https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction`, `https://c2.com/wiki/remodel/pages/ThreeStrikesAndYouRefactor`
- Tokens: 0.
- Risk: simplify-code finds fewer copies to merge. When a model cannot tell whether two copies share a rule, it leaves them, which the Disposition rule of precision over recall already prefers.

### C3. Types before comments

- Target: `skills/toby-swd-clarity/SKILL.md` line 17, the paragraph under the title. The proposal also edits `skills/toby-swd-clarity/references/examples.md` Example 4, lines 87 to 101.
- Current: ""Good code is self-documenting" is false. Correct that belief before you start. Only signatures can be expressed in code." Example 4 says "The types cannot say that a 404 leaves `error` null, or that `user` is null while loading."
- Proposed: line 17 becomes "Names and types state part of a contract. Put a unit, a null meaning, or a rule about which states can occur in a type when the language allows it. Comments state the rest, which is behavior, side effects, invariants the type cannot hold, and reasons. Non-trivial code with no interface comment is unfinished, however good its names are." Lines 87 to 101 become the text below.

  ````
  Return a union with one variant per state, and comment what the type cannot show:

  ```ts
  type UserQuery =
    | { status: "loading" }
    | { status: "ready"; user: User }
    | { status: "missing" }                  // The server returned 404.
    | { status: "failed"; error: ApiError }; // The request failed or returned 5xx.
  ```

  The union rules out a user and an error at the same time, so no comment has to
  list the valid combinations. The comments map each state to a server response,
  which the type cannot show.
  ````

- The two sides: the clarity skill says code can express only signatures, so units and invariants need comments. Minsky and Wlaschin show types that make invalid combinations impossible to build. King shows a parsed type that removes later checks. Ousterhout says comments state what the code cannot state, so a type that states more leaves less for the comment. The current Example 4 also contradicts `skills/toby-swd-interfaces/references/web.md` Example 1, which uses a union for the same loading, error, and data case.
- Recommendation: state a rule in the type where the language supports it, and state everything else in comments. The clarity skill keeps Ousterhout's side of his comment dispute with Martin.
- Source: `https://blog.janestreet.com/effective-ml-revisited/`, `https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/`, `https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/`, `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=comments`
- Tokens: -66.
- Risk: a model may wrap every primitive in a new type. King's 2020 post says such a wrapper guarantees less than a type that cannot hold a bad value. The code-review entry "Primitive obsession" fires only when the same parsing appears at two sites, which limits the wrapping.

## Rewrites

### R1. Check 1 wording

- Target: `skills/toby-swd-modules/SKILL.md` lines 30 and 32, in check 1. The proposal also edits `skills/toby-swd-modules/references/solid.md` line 5.
- Current: "State the one design decision or piece of knowledge each module encapsulates." Line 32 says ""One reason to change" and "one body of knowledge" are the same test."
- Proposed: line 30 becomes "Give each module one design decision to hide, starting with those most likely to change, such as a file format or a pricing rule. A split described as a sequence, such as "first read, then parse, then write", is temporal decomposition, which spreads one decision across shallow stages. Divide the code again so each module hides one whole decision." Line 32 starts "This check is the single-responsibility principle. A reason to change is a person or team that asks for changes, so put code that two teams change in two modules." and keeps its last sentence. In solid.md, "A module holds one body of knowledge, which gives it one reason to change." becomes "One person or team asks for changes to each module."
- Why: "piece of knowledge" fits any grouping. Parnas starts from the decisions most likely to change, so his criterion gives the model a list to start from. Martin defines a reason to change as the person or business function that asks for changes. His Employee class has pay, hours, and save methods that the CFO, the COO, and the CTO each ask to change. A model can read from the task who asks for each change.
- Source: `https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf`, `https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html`
- Tokens: -10.
- Risk: a model may split by team too often. Check 7 still rejects a split that leaves two shallow modules.

### R2. Interface segregation

- Target: `skills/toby-swd-interfaces/SKILL.md` line 43, in "Bias toward somewhat general-purpose". The proposal also edits `skills/toby-swd-modules/references/solid.md` line 8.
- Current: "A consumer that needs one method gets an interface with one method."
- Proposed: line 43 becomes "Under interface segregation, a consumer that calls one method declares a one-method type. One deep provider implements every such type. `references/backend-apis.md` shows this for a backend service." In solid.md, the second sentence becomes "A consumer declares a type with only the methods it calls, and one deep provider implements it."
- Why: line 43 comes after the advice "Use fewer methods, each with broader semantics", so a model can read the two as opposite rules for the provider. Martin prefers many client-specific interfaces, while Ousterhout says many small classes make shallow modules. The rewrite applies Martin's rule to the consumer's type and Ousterhout's rule to the provider. `references/backend-apis.md` Example 3 already declares the interface at the consumer.
- Source: `http://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf`, `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign`
- Tokens: -20.

### R3. Parse outside input

- Target: `skills/toby-swd-interfaces/SKILL.md` line 108, in step 7.
- Current: "The module that defines the contract validates that input at the boundary."
- Proposed: the last two sentences of the paragraph become "The module that defines a contract for outside input, such as a request, a message, or a deserialized payload, parses it into a typed value. Later code takes that type and repeats no check."
- Why: a validator checks the input and passes the raw value on, so later code checks it again. King calls these scattered checks shotgun parsing. With shotgun parsing, a program can half-process invalid input before an error appears. A parser keeps what it learned in the type. `references/runtime-config.md` already parses config this way at startup.
- Source: `https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/`
- Tokens: -5.
- Risk: the term "trust boundary" leaves the skill. R4 uses "input from outside the program", which keeps the meaning.

### R4. Guard for an impossible condition

- Target: `skills/toby-simplify-code/SKILL.md` line 31, in "What to look for".
- Current: "A try/catch, guard, or branch that defends against a condition that can't occur. toby-swd-complexity's error ladder already defines that condition out of existence."
- Proposed: "- A try/catch, guard, or branch for a condition that cannot occur, where you can quote the type or caller that rules it out. A check on input from outside the program stays."
- Why: Ousterhout's "define errors out of existence" changes what an operation means, which the simplify-code Out of scope section forbids. The current bullet uses the phrase for deleting dead code. Ousterhout's notes also say input from less-trusted sources must always be checked, but the current bullet does not keep that check.
- Source: `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=exceptions`
- Tokens: -13.
- Risk: the bullet drops the sentence about one fewer branch, which the Disposition section already asks for.

### R5. Strategy "While writing" section

- Target: `skills/toby-swd-strategy/SKILL.md` lines 36 and 38, in "While writing".
- Current: "Aim for deep modules. Small functions help that goal only when they make a module deeper."
- Proposed: "Do not expose a mechanic, a config knob, or a special case because it is the quickest edit, since every caller then has to manage it. Compute a value inside the module when the caller cannot pick a better one. Split a function only when each piece can be understood without the other, and keep a deep function whole."
- Why: lines 36 and 38 use seven sentences to repeat `toby-swd-modules` checks 3 and 7. The strategy skill loads alone when it is the only match, so each rule keeps one sentence here. The split rule follows Ousterhout's test that the pieces can be understood apart.
- Source: `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign`, `https://github.com/johnousterhout/aposd-vs-clean-code`
- Tokens: -74.

### R6. Big-bang redesign

- Target: `skills/toby-swd-strategy/SKILL.md` line 91, in "Anti-patterns".
- Current: "Trying to fix the whole architecture in one pass repeats the waterfall failure mode. Build the design up from many small correct decisions."
- Proposed: "Fix the architecture one small refactor at a time, inside the code this change touches, and run the tests after each one."
- Why: "the waterfall failure mode" states no failure a model can check for. Beck makes small structural changes before a behavior change. The new text also states the scope rule from line 46, which K3 deletes.
- Source: `https://newsletter.kentbeck.com/p/tidy-first-example`, `https://martinfowler.com/bliki/DefinitionOfRefactoring.html`
- Tokens: -4.

### R7. Sentence cap in the comment test

- Target: `skills/toby-swd-interfaces/SKILL.md` lines 66 and 71, in step 3.
- Current: "Four sentences or fewer for the whole entry point." Line 71 says "You can check these conditions by reading the comment."
- Proposed: line 66 becomes "- Four sentences or fewer, plus one per argument whose units, bounds, or empty case the type cannot state." Delete line 71.
- Why: `skills/toby-swd-clarity/references/examples.md` Example 1 gives a six-sentence comment as the example to copy, but that comment fails the four-sentence cap. Ousterhout's interface comment covers the arguments as well as the behavior. The four-sentence cap has no outside source. Line 71 says the conditions can be checked, which the list already shows.
- Source: `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=comments`
- Tokens: -23.
- Risk: a model may pad a comment with argument sentences. The other three conditions still apply.

### R8. Shallow-module sentence in clarity

- Target: `skills/toby-swd-clarity/SKILL.md` line 46, in "Comments".
- Current: "If it has to describe internals to be complete, the module is shallow. A shallow module is a signal to redesign it."
- Proposed: "If it has to describe internals to be complete, the module is shallow, so change the design."
- Why: three sentences state one rule from Ousterhout's comments lecture.
- Source: `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=comments`
- Tokens: -24.

## Cuts

Each cut deletes the quoted text and adds nothing.

### K1. Effort percentage

- Target: `skills/toby-swd-strategy/references/examples.md` lines 154 to 157, and "or goes well past that effort range" on lines 164 to 165.
- Current: "The target is roughly 10–20% more effort than the tactical path, spent continuously through the change."
- Why: Ousterhout marks the 10 to 20 percent figure and its payback period with question marks. He cites no study. A model cannot measure its own effort as a percentage. SKILL.md already sets a bound it can count, which is one design fix per change.
- Source: `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=working`
- Tokens: -74.
- Risk: the skill loses its only statement of how much extra work to expect.

### K2. Tactical tornado bullet

- Target: `skills/toby-swd-strategy/SKILL.md` line 90, in "Anti-patterns".
- Current: "**Tactical tornado.** A tactical tornado is a large volume of working code, written fast, where each piece adds a special case or dependency."
- Why: the paragraph at line 18 says the same thing. Ousterhout compared AI coding tools to tactical tornadoes in April 2025, so the line 18 paragraph stays.
- Source: `skills/toby-swd-strategy/SKILL.md` line 18, `https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design`
- Tokens: -56.
- Risk: Ousterhout's term "tactical tornado" leaves the skill, while line 18 still describes the behavior.

### K3. Repeated scope rule

- Target: `skills/toby-swd-strategy/SKILL.md` line 46, in "After writing".
- Current: "Keep cleanups scoped to code you're already in. Do not extend a refactor across the codebase."
- Why: line 45 ends with the same rule. R6 also states it for a big-bang redesign.
- Source: `skills/toby-swd-strategy/SKILL.md` line 45.
- Tokens: -24.

### K4. Language list in check 5

- Target: `skills/toby-swd-modules/SKILL.md` line 71, in check 5.
- Current: "This check matters most in class-heavy Java, Kotlin, C#, Swift, Python, and TypeScript code."
- Why: a capable model knows which languages have implementation inheritance. Line 61 already covers languages without it.
- Source: `skills/toby-swd-modules/SKILL.md` line 61.
- Tokens: -24.

### K5. Repeated sentences in simplify-code

- Target: `skills/toby-simplify-code/SKILL.md` line 12, and line 18 in "Disposition".
- Current: "Never ship a diff to look productive, because this skill is meant to prevent that churn." Line 18 says "You must prove the edit is safe, so the default is to leave the code alone."
- Why: Disposition bullets 1 and 4 state both rules.
- Source: `skills/toby-simplify-code/SKILL.md` lines 16 and 19.
- Tokens: -41.

### K6. Second statement of comment-first design

- Target: `skills/toby-swd-interfaces/SKILL.md` line 75, at the end of step 3.
- Current: "The comment is a design tool, and it is the cheapest way to find out the abstraction is wrong."
- Why: line 17 states the same rule, which comes from Ousterhout's comments lecture.
- Source: `skills/toby-swd-interfaces/SKILL.md` line 17, `https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=comments`
- Tokens: -64.

### K7. Frequency claim about splits

- Target: `skills/toby-swd-modules/SKILL.md` line 81, in check 7.
- Current: "Over-splitting is the more common error."
- Why: Ousterhout and Martin disagree on how far to decompose. Neither cites a study, so the frequency claim has no data behind it. The sentences around it give the split test.
- Source: `https://github.com/johnousterhout/aposd-vs-clean-code`
- Tokens: -10.

### K8. Vague split threshold

- Target: `skills/toby-swd-modules/SKILL.md` line 18, under the title.
- Current: "Split a module only when the reason is stronger than a first instinct."
- Why: "stronger than a first instinct" sets no test, but check 7 gives one.
- Source: `skills/toby-swd-modules/SKILL.md` line 81.
- Tokens: -18.

### K9. Repeated one-line exemption

- Target: `skills/toby-swd-strategy/SKILL.md` line 30, in "Before writing".
- Current: "A change that is only one line doesn't need an architecture review, because the design pass scales to the size of the decision."
- Why: line 24 states the one-line exemption.
- Source: `skills/toby-swd-strategy/SKILL.md` line 24.
- Tokens: -32.

## Aligned

Leave each of these rules as written.

- Modules title paragraph, deep module and interface as cost, matches Ousterhout's CS190 notes.
- Modules check 1, temporal decomposition, matches Parnas 1972 and Ousterhout's notes.
- Modules check 2, information leakage and its exception for shared signatures, matches Ousterhout's notes and Parnas.
- Modules check 3, pulling complexity down, matches Ousterhout's notes.
- Modules check 4, pass-through methods and variables, matches Ousterhout's red flag for a layer with no new abstraction.
- Modules check 5, composition by default with interface inheritance allowed, matches Gamma's 2005 interview.
- Modules check 6, removing the special case, matches Ousterhout's text-class example in APOSD chapter 6 and his advice to define errors out of existence.
- Modules check 7, the split test and the conjoined-methods test, matches Ousterhout. Martin agreed his PrimeGenerator split was a problem.
- Modules check 8, the interface comment as a depth test, matches Ousterhout's comments lecture.
- Modules red flag for classitis matches Ousterhout's notes.
- "Replace the growing conditional" and `references/replace-the-conditional.md` match Martin's open-closed principle and Fowler's Replace Conditional with Polymorphism. The exception for a switch that has not changed in a year limits the extra code North says OCP adds.
- `references/solid.md` bullets for open-closed, Liskov, and dependency inversion match Martin 2000. The dependency-inversion bullet requires no interface per class, which fits North's complaint that DIP leads to costly abstraction.
- Interfaces title section, the interface as cost and comment-first design, matches Ousterhout's comments lecture.
- Interfaces "Bias toward somewhat general-purpose", with its questions and its limit to named variants, matches APOSD chapter 6 and YAGNI.
- Interfaces Brownfield, which lists each caller and the behavior it relies on, matches Hyrum's law.
- Interfaces red flags for accessors and for one method per caller variation match APOSD chapter 6.
- Interfaces `references/examples.md`, the rate limiter, the UserCard, and the upload, matches Ousterhout's notes.
- Clarity comments table and the rule to comment at a different level from the code match Ousterhout. Ousterhout and Martin agree that implementation code needs comments only where it is not obvious.
- Clarity Consistency, which merges code only when the copies share knowledge, matches Thomas on DRY and Stevens 1974.
- Clarity "Declared type differing from the real one" matches Martin's Liskov substitution principle.
- Simplify-code Behavior drift matches Fowler's definition of refactoring and Hyrum's law.
- Simplify-code precision over recall matches Fowler's statement that some code that smells is fine.
- Simplify-code `references/smells.md` "Smells left off this list on purpose" takes Ousterhout's side on length and comments and Thomas's side on duplication. Martin opposes the length and comment positions. Jeffries opposes the duplication position. No source on either side cites a study.
- Strategy title section and "After writing" match Ousterhout's notes on strategic programming.
- Strategy "When the quick fix is the correct choice" matches Beck's case-by-case trade-off between tidying first and shipping sooner.

## Eval ideas

Each eval runs two arms on the same prompt, the current skill text and the proposed text. The user agrees each design before any run.

- E1 tests C1. The prompt asks for SMS beside an existing email `send()` and states no other channels. A run passes when it adds no interface, class, or registry for a channel nobody stated.
- E2 tests G2 and C3. The prompt asks for a TypeScript hook that fetches a user and reports loading, error, and data. A run passes when the return type is a union with one variant per state.
- E3 tests C2. The prompt asks simplify-code to tidy two rounding blocks that look alike, where one rounds tax by regulation and one rounds a display price. A run fails when it merges the two blocks into one helper.
- E4 tests G3. The prompt gives a `formatAddress` helper with two flag parameters and asks for a third caller's variant. A run passes when it inlines or splits the helper, and fails when it adds a third flag.
- E5 tests R3. The prompt asks for an endpoint that takes a JSON body with an email and an age and calls `createUser`. A run passes when `createUser` takes a parsed type and no check repeats after the handler.
- E6 tests G1. The prompt gives a brownfield change that needs a refactor and asks for commits. A run passes when the refactor commit changes no test expectation and comes before the behavior commit.
- E7 tests R4. The prompt asks simplify-code to tidy a handler that checks a field of a parsed JSON body for None. A run fails when it deletes that check.
- E8 tests R2. The prompt gives a six-method service and a new consumer that calls one method. A run passes when the consumer declares a one-method type and the service stays one class.
