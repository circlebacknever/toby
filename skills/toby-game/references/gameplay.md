# Gameplay — how it feels to play

A pure toy or sim has no outcome, meaning no verdict, no win, and no opponent, so skip the rules about outcomes. A toy or sim needs real motion, patterns that visibly arise from simple rules, and a setting worth changing. The rest of this file applies to games that produce an outcome.

**Tie outcomes to player choices.** Every outcome the player cares about traces to a choice they made and saw coming. Show any randomness before the player decides, in things the player can see. Examples are aim wobble, a keeper's lean, and a risk of waking someone that rises as the game gets noisier. Never add a hidden coin flip on top of a decision. Show the gamble before the player takes it, as a number and a green/amber/red rating on the thing about to happen. Show the outcome forming as the player drags, and lock it on release. When the player can only change a hidden probability, testers say every time that the player has too little control.

**Physics determines the outcome on screen.** Animate real motion, and let the positions on screen determine the outcome at the moment the outcome is settled. The glove meets the ball where the player sees them meet. Never roll the outcome and then animate toward it. Otherwise the ball jumps back into the keeper's hands after it visibly passed them, and every tester calls the game random. Run the hit test in the coordinates you render, on this frame's drawn position, so the math checks the same position the player sees.

**Real motion.** Natural physics comes from real kinematics, such as velocity, gravity, a little drag, and weight in the follow-through. An animation that plays the same regardless of force reads as fake, so let a ball arc and a body settle.

**It has to feel alive.** The sim ticks on its own, the world responds to a touch at once, and interference visibly matters. A screen where nothing moves until the player acts looks like a form. (Idle motion is in `references/visual-identity.md`.)

**Teach one player action in one line.** Skip the long tutorial, and write one line in the game's own words ("drag to aim, release to shoot"). The player discovers the rest. When the instructions need to be long, the player cannot understand the control by looking at it.

**Every lever changes a number in a formula.** Each button, upgrade, or shenanigan moves a number the resolver reads, or the player sees it as decoration within minutes. In the penalty game, the streaker, the rain, and the bribe each stay, because each one changes aim wobble, keeper reach, or shot quality. An idle or manager game needs rates the player can read and an upgrade list that shows more items as the run goes on. Check that each player action can physically succeed before you ship it. For example, a button that sends a worker who cannot cross the street before the job expires does nothing useful.

**Idle play keeps moving, and the AI stays beatable.** When the game runs itself, an AI takes the turns the player skipped, so the world keeps moving. The AI's instinct has to stay visibly flawed, such as a lazy pass or a snatched shot, or skilled play has nothing to beat. Give every object behavior in every state, including the state where no character is using it. For example, a loose ball rolls and decays until a paw grabs it.

**Set difficulty with structure first.** When a run is six rounds and the player wins each round 62% of the time, only about 6% of runs finish. Tuning the numbers does not change that, because the odds multiply as p^n. Change the structure first with best-of-N rounds, a checkpoint, or a free retry that the story explains, and then tune. Tie difficulty to the player's behavior and clamp it. Pace the story by elapsed time.

**The win has to be earned.** When steady small improvements lead to an easy winning strategy, the game fails. The player or a test bot finds that strategy once and stops exploring. Make the player earn the best strategy through the game's design. Add an obstacle to get past, a stretch with no progress that ends only after a deliberate move, or a surprising game state that the player can reach but never gets for free. When the obvious strategy wins, add an obstacle it has to overcome. (`references/calibration-and-testing.md` describes how to measure it: random and skilled input must score differently.)

**Reward varied play.** Give more reward when the player varies their moves, and penalize the player for repeating the same move many times in a row.

**Two sides share one upgrade list.** An opponent sees the same game state as the player, buys from the same upgrade list, and grows stronger on a fixed schedule.
