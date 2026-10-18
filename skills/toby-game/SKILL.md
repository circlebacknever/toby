---
name: toby-game
description: >-
  Collaborate with the user to build a single-file HTML simulation game or toy
  in Toby's style. Trigger only when the user explicitly invokes this skill by
  name or with the `/toby-game` slash command. Don't trigger on a general
  request to make a game, a sim, a toy, a visualizer, or a simulation.
disable-model-invocation: true
---

# Toby Game

Build one self-contained HTML simulation game or toy with the creator. Follow Toby's voice rules in chat, and use the wider joking register from `references/comedy-and-narrative.md` for in-game text (cards, news ticker, upgrade names, and end screens).

## Opening move

Ask what system we are modeling and what one surprising behavior it should show when it runs. Then ask whether the premise mocks a target institution or bureaucratic process (and who the underdog is), or whether it is a pure simulation toy. When there is a target, copy the real details of its forms and procedures before writing any jokes.

## The dials

Propose a starting setting and reason for each of the six dials below, and let the creator adjust any of them:

- **Fidelity:** how closely the simulation models real physics or statistics versus playful rules.
- **Narrative density:** how much text appears, from a silent toy to a live wire-service ticker.
- **Tone:** from warm comedy to bleak satire to the dread register (`references/comedy-and-narrative.md`).
- **Player relationship:** watching the system, steering it by spending resources, or controlling it with direct reflexes.
- **Session length:** an endless sandbox toy or a timed run with a graded ending.
- **Render:** 2D canvas, 3D (Three.js), or DOM cards.

## The build

Build the playable core loop on placeholder art first: the simulation advances on its own, state changes visibly, the player's action alters the outcome, and the one surprising behavior appears. Then apply the reference files below one pass at a time, calibrate with the test bots, and end each pass with a short status and the next dial to tune.

## References

Read each reference before building or tuning that part of the game:

- `references/gameplay.md` covers player agency, screen-space hit testing, real kinematics, one-line instructions, and structural difficulty.
- `references/comedy-and-narrative.md` covers the wider comedy register, escalating story threads, non-repeating flavor queues, and the dread register.
- `references/architecture.md` covers the single-file HTML structure, pure tick resolution, seeded RNG, clamped frame deltas, and finite-value invariants.
- `references/cross-device.md` covers thumb-friendly mobile layouts, fold-away reference sheets, and frame-rate budgets.
- `references/visual-identity.md` covers the paper/ink/red palette, low-poly 3D and 2D/DOM styling, and constant subtle motion.
- `references/calibration-and-testing.md` covers `scripts/check-single-html.mjs`, invariant checks, and the random, human-grade, and superhuman bot bands.
