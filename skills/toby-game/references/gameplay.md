# Gameplay

A pure sandbox toy doesn't have a win or loss outcome, so it needs responsive motion, emergent patterns from simple rules, and sliders worth tweaking. The rules below apply to every game with an outcome.

## Player agency and physics

- **Tie outcomes to visible choices.** Show any randomness or risk (aim wobble, a goalkeeper's lean, rising noise) on screen before the player commits, and lock the trajectory on release. Never decide an outcome with a hidden coin flip after the player acts.
- **Test collisions in rendered coordinates.** Step positions with real kinematics (velocity, gravity, drag) and run hit tests against the drawn positions on each frame so a glove catches the ball only where they visibly meet on screen.
- **Keep the world moving.** Advance the simulation continuously and respond to input immediately. When the player skips a turn in an idle or manager game, let a visibly imperfect AI take the turn so skilled play beats it.
- **Teach the control in one line.** State the core action in one short phrase (`"drag to aim, release to shoot"`), and make every button or upgrade change a real number in the simulation formula.

## Difficulty and progression

- **Shape difficulty with structure first.** In a multi-round run, per-round win probabilities multiply (`0.62^6 ≈ 6%`), so add checkpoints, best-of-N rounds, or story retries before tuning raw numbers.
- **Require skill to win.** Add obstacles, plateaus that require a deliberate tactical shift, and diminishing returns on repeated moves so a single obvious strategy or random clicking doesn't win automatically (`references/calibration-and-testing.md`).
- **Share the rules with the opponent.** Let an opponent read the same game state and buy from the same upgrade list on a predictable schedule.
