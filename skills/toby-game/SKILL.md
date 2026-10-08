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

Build one self-contained HTML game with the creator, who picks the genre, theme, and tone each run. Toby's voice rules apply to chat with the creator. The text inside the game, such as its cards, news ticker, upgrade names, and end screen, uses a looser joking style. That style is called the wider register, and `references/comedy-and-narrative.md` describes it.

## Opening move

Do not ask "what genre?" First ask what system we are modeling, and what one surprising thing it should do when it runs. Then ask whether there is a target, meaning an institution, a ceremony, or a process. If there is a target, ask who the underdog is, meaning the person who has to deal with that target. A premise can have no target and be a pure toy, so do not force a bureaucracy onto that toy. When there is a target, pick the specific procedure to mock, such as a claim form or an appeal step. Copy its real details before you write any joke.

## The dials

The dials are six settings that describe the game. Choose a setting for each dial, propose that combination with a reason, and let the creator change any setting.

- **fidelity**: how accurate the model is, from a real physical or statistical model to one that is openly made up.
- **narrative density**: how much text the game shows, from no text in a silent toy to a constant stream of news lines.
- **tone**: from warm, to bleak, to the darkest style, which `references/comedy-and-narrative.md` describes under "The dread register".
- **player relationship**: the player's role, which is watching the system, spending resources to steer it, or controlling it with fast reflexes.
- **session length**: from an endless toy to a run with a fixed end and a graded ending.
- **render**: 2D canvas, 3D, or DOM.

Earlier games covered a particle field, an orbit sandbox, and a traffic sim. Others were a satire where the player swipes DOM cards, a penalty-kick duel, and a heist-themed idle game. An idle game keeps playing while the player upgrades it.

## The build

Build the loop first, on placeholder art, before anything else. In that loop the simulation advances on its own, something changes, and the player can affect the result in a way that matters. Confirm the one surprising thing shows. Then apply one reference file at a time, and tune the difficulty with the test bots in `references/calibration-and-testing.md`. End each pass with a short status and the next dial you propose to change.

## Known failures

Each item is a note creators gave on earlier games. Design to avoid every one of them from the first pass, and read the reference each item gives before that part of the build.

- `references/gameplay.md`: tie outcomes to choices the player saw coming ("feels unfair"), make winning require getting past an obstacle in the game's design ("it solved itself"), check collisions against the positions drawn on screen and move objects with real physics ("the physics looks wrong"), make the world advance on its own and respond to the player at once ("it doesn't feel like a game"), and teach the player's one action in one line ("the instructions are too long").
- `references/comedy-and-narrative.md`: use the game's wider register ("make it funnier"), advance each storyline one step at a time and pick each line from the lines not yet shown ("the jokes repeat"), build the run as a story that brings early details back at the end ("there's no story"), and show a feed line only when something in the game changed ("the feed flashes").
- `references/architecture.md`: compute the physics so values cannot grow without limit, and assert that values stay finite ("the sim drifts").
- `references/cross-device.md`: keep live controls on screen on a phone ("it breaks on mobile").
- `references/visual-identity.md`: use a warm paper background, near-black ink, one red, one light source, and constant small motion ("it looks generic").
- `references/calibration-and-testing.md`: check that the random, human-level, and superhuman test bots each score in their target range, and run the invariant tests, before calling the game done.
