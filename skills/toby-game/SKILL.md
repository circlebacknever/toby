---
name: toby-game
description: "Collaborate to build a single-file HTML simulation game or toy in Toby's style: a real system with its shortcuts named out loud, deadpan comedy where there is a target, a paper-and-ink look across canvas, 3D, or DOM, and an ending that reads the run back when the game has one. Trigger only when the creator explicitly invokes this skill by name or with the /toby-game slash command. Do not trigger on general requests to make a game, a sim, a toy, a visualizer, or a simulation, and do not trigger when a game is only mentioned in passing. Genre, theme, and tone are the creator's to pick each run; the example games show the range the style already covers."
---

# Toby Game

You bring the idea, and this skill supplies the style. The style means a real system underneath, jokes tied to the mechanics, a paper-and-ink look, and a run that tells a story. The game is one self-contained HTML file. Genre, theme, and tone are yours each time.

## What this prevents

This skill prevents the notes you would otherwise give twice:

- "make it funnier" → Use the wider in-world register described in `references/comedy-and-narrative.md`.
- "the jokes repeat" → Serialize the threads, escalate the beats, and draw content without replacement, as `references/comedy-and-narrative.md` describes.
- "there's no story, it doesn't flow" → Build the run as an arc that plants details early and pays them off later, as `references/comedy-and-narrative.md` describes.
- "the feed flashes, a line every frame" → Fire a line only on a real change, and pace the lines, as `references/comedy-and-narrative.md` describes.
- "feels random, feels unfair" → Tie outcomes to the player's choices, and show the gamble before the player takes it, as `references/gameplay.md` describes.
- "it solved itself instantly, the answer is trivial" → Make the player earn the win through structure, as `references/gameplay.md` describes.
- "the physics looks wrong, the hit doesn't match the screen" → Test collisions on the drawn positions, and use real motion, as `references/gameplay.md` describes.
- "the sim blows up or drifts after a while" → Integrate so the sim cannot blow up, and assert that values stay finite, as `references/architecture.md` describes.
- "it doesn't feel like a game" → Make the world tick on its own and answer the player at once, as `references/gameplay.md` describes.
- "the instructions are too long" → Teach one verb in one line, as `references/gameplay.md` describes.
- "it breaks on mobile" → Move live controls on a phone, and never hide them, as `references/cross-device.md` describes.
- "it looks generic" → Use paper, ink, one red, one light, and idle motion that never fully stops, as `references/visual-identity.md` describes.

## Opening move

Do not ask "what genre?" First ask what system we are modeling, and what one surprising thing it should do when it runs. Then ask whether there is a target, meaning an institution, a ceremony, or a process, and who the underdog caught in it is. A premise can have no target and be a pure toy, so do not force a bureaucracy onto that toy. When there is a target, name the specific mechanism and copy its real details before writing a single joke.

## The dials

Place the game on a few axes, propose one combination with a reason, then let the creator change any of them.

- **fidelity** — real model through openly vibes-based
- **narrative density** — silent toy through full press corps
- **tone** — warm through bleak to the dread register
- **player relationship** — observer, funder, or twitch actor
- **session length** — endless toy through bounded run with a graded ending
- **render** — 2D canvas, 3D, or DOM

## The build

Build the loop first, on placeholder art, before anything else. In that loop the sim ticks, something changes, and the player interferes in a way that matters. Confirm the one surprising thing shows. Then add the guidance from one reference at a time, and calibrate with bots. End each pass with a short status and the next dial to turn.

## References

- `references/architecture.md` — the one-file skeleton and the core engineering decisions
- `references/gameplay.md` — how it feels to play
- `references/comedy-and-narrative.md` — the voice and the story
- `references/visual-identity.md` — the look
- `references/cross-device.md` — keeping the game live on desktop and phone
- `references/calibration-and-testing.md` — balance measurement and correctness tests

## The games behind it

Read these for the range the style already covers. The games are Flux (a particle field), nbody (an orbit sandbox), and gridlock (a traffic sim). The others are denial-of-service (a DOM card-swipe satire), spot-kicks (a penalty duel), and raccoon-syndicate (a heist idle). These games are not bundled with the skill. The job is to build the next game in that range, on whatever subject you pick.
