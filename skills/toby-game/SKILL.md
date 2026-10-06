---
name: toby-game
description: >-
  Collaborate with the user to build a single-file HTML simulation game or toy
  in Toby's style. Trigger only when the user explicitly invokes this skill by
  name or with the `/toby-game` slash command. Do not trigger on a general
  request to make a game, a sim, a toy, a visualizer, or a simulation.
disable-model-invocation: true
---

# Toby Game

Build one self-contained HTML game with the creator, who picks the genre, theme, and tone each run. Toby's voice rules apply to chat with the creator. The game's own copy, meaning its cards, ticker, upgrade names, and end screen, uses the wider register in `references/comedy-and-narrative.md`.

## Opening move

Do not ask "what genre?" First ask what system we are modeling, and what one surprising thing it should do when it runs. Then ask whether there is a target, meaning an institution, a ceremony, or a process. If there is, ask who the underdog subject to it is. A premise can have no target and be a pure toy, so do not force a bureaucracy onto that toy. When there is a target, pick the mechanism and copy its real details before writing a single joke.

## The dials

Place the game on a few axes, propose one combination with a reason, then let the creator change any of them.

- **fidelity** — real model through openly vibes-based
- **narrative density** — silent toy through full press corps
- **tone** — warm through bleak to the dread register
- **player relationship** — observer, funder, or twitch actor
- **session length** — endless toy through bounded run with a graded ending
- **render** — 2D canvas, 3D, or DOM

Earlier games covered a particle field, an orbit sandbox, a traffic sim, a DOM card-swipe satire, a penalty duel, and a heist idle.

## The build

Build the loop first, on placeholder art, before anything else. In that loop the sim ticks, something changes, and the player interferes in a way that matters. Confirm the one surprising thing shows. Then add the guidance from one reference at a time, and calibrate with bots. End each pass with a short status and the next dial to turn.

## Known failures

Each item is a note creators gave on earlier games. Build against all of them from the first pass, and read the reference each item gives before that part of the build.

- `references/gameplay.md`: tie outcomes to choices the player saw coming ("feels unfair"), make the win take structure ("it solved itself"), hit-test on drawn positions with real motion ("the physics looks wrong"), make the world tick and respond at once ("it doesn't feel like a game"), and teach one verb in one line ("the instructions are too long").
- `references/comedy-and-narrative.md`: use the game's wider register ("make it funnier"), serialize threads and draw content without replacement ("the jokes repeat"), build the run as an arc with callbacks ("there's no story"), and fire a feed line only on a real change ("the feed flashes").
- `references/architecture.md`: integrate so the sim cannot blow up, and assert that values stay finite ("the sim drifts").
- `references/cross-device.md`: keep live controls on screen on a phone ("it breaks on mobile").
- `references/visual-identity.md`: use paper, ink, one red, one light, and idle motion ("it looks generic").
- `references/calibration-and-testing.md`: run bot bands and invariant tests before calling the game done.
