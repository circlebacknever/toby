# Gameplay — how it feels to play

Each of these rules for how a game feels was learned from a rebuild. A pure toy or sim has no outcome, meaning no verdict, no win, and no opponent, so skip the outcome laws. A toy or sim needs real motion, watchable emergence, and a knob worth turning. The rest is for games that resolve something.

**Tie outcomes to player choices.** Every outcome the player cares about traces to a choice they made and saw coming. Put chance before the choice, in things the player can read. Examples are aim wobble, a keeper's lean, and a wake risk that climbs as the night gets loud. Never add a hidden coin flip on top of a decision. Show the gamble before the player takes it, as a number and a green/amber/red rating on the thing about to happen. Show the outcome forming as the player drags, and lock it on release. A sim that only nudges a hidden probability gets the same note every time, which is that the player has too little control.

**Physics determines the outcome on screen.** Animate real motion and let the geometry determine the outcome at the moment it is settled. The glove meets the ball where the player sees them meet. Never roll the outcome and then animate toward it. Otherwise the ball snaps into a save it visibly cleared, so every tester calls it random. Run the hit test in the coordinates you render, on this frame's drawn position, so the math checks the same position the player sees.

**Real motion.** Natural physics comes from real kinematics, such as velocity, gravity, a little drag, and weight in the follow-through. An animation that plays the same regardless of force reads as fake, so let a ball arc and a body settle.

**It has to feel alive.** The sim ticks on its own, the world responds to a touch at once, and interference visibly matters. A screen where nothing moves until the player acts looks like a form. (Idle motion is in `references/visual-identity.md`.)

**Teach one verb in one line.** Skip the long tutorial, and write one line in the game's own words ("drag to aim, release to shoot"). The player discovers the rest. Long instructions mean the control is not legible.

**Every lever changes a number in a formula.** Each button, upgrade, or shenanigan moves a number the resolver reads, or the player sees it as decoration within minutes. The streaker, the rain, and the bribe each change wobble, reach, or quality, which is why each one stays. An idle or manager game needs legible rates and a catalog that reveals more items as the run grows. Check a verb can physically succeed before you ship it. A dispatch that cannot cross the street in a job's time is a dead button.

**Idle play keeps moving, and the AI stays beatable.** A game that runs itself plays the skipped beats with an AI so the world keeps moving. The AI's instinct has to stay visibly flawed, such as a lazy pass or a snatched shot, or skilled play has nothing to beat. Give every entity behavior in every state, including the state where nobody wants it. For example, a loose ball rolls and decays until a paw grabs it.

**Set difficulty with structure first.** Six 62% rounds finish 5% of the time, no matter the tuning, because the odds multiply as p^n. Reshape the run with best-of-N, a checkpoint, or a story-flavored mulligan, and then tune. Tie difficulty to the player's behavior and clamp it. Pace the story by elapsed time.

**The win has to be earned.** A smooth ramp to a trivial answer makes the game fail, because the player or the optimizer finds it once and never looks again. Make the player earn the good line through structure. Use a barrier to clear, a plateau that ends only after a real move, or a surprising regime that is reachable and never free. When the obvious strategy wins, add an obstacle it has to overcome. (`references/calibration-and-testing.md` describes how to measure it: random and skilled input must score differently.)

**Don't let it repeat.** Draw content without replacement, reward varied play and punish the streak, and let the world's reactions escalate as the run goes.

**Two sides share one catalog.** An opponent reads the same state and buys from the same catalog the player does, and escalates on a schedule.

In the dread register the feel inverts, so anticipation replaces surprise. The approach is unstoppable and has no ceiling. See `references/comedy-and-narrative.md`.
