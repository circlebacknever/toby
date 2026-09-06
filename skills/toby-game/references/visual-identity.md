# Visual identity — the look

The floor is the same in any genre. The kit changes with the substrate.

**The floor.** Warm paper over near-black ink, and exactly one red that means consequence: a denial, a death, the one dangerous button. Spend it anywhere else and it stops meaning anything. Mood comes from one source: one light in 3D, one accent in 2D. Nothing is ever fully still (quiet the motion when the player asks for reduced motion). Monospace with steady-width digits for data, a humanist sans for prose. Every label earns its place or it is cut.

The palette is paper `#fdfaf1`, ink `#1a1c1f`, the one red `#c44e3f`, and a dark field `#0e0f12` for canvas. Draw the rest from a muted set: teal `#2e6a78`, green `#4d7a30`, amber `#b07020`, deep rust `#7a2d22`. Name the tokens `--toby-*`. Build a different set for a different mood, and keep the single rationed red. (The example games ship an older token prefix, so rename it on copy.)

**3D.** Build characters and props from non-uniformly scaled low-poly spheres. A car, a head, and a tail are the same primitive, which is what makes them read as a family. Keep everything matte and flat-shaded. Let a ball or an eye go smooth. One warm or cool light, low fill underneath, warm dots for windows and fire. Bob and sway on a shared clock with a per-thing offset so the crowd does not pulse in unison. Frame a diorama from above, or a clamped orbit for a system you study. Cuteness is a choice. An austere premise drops the spheres for boxes, lines, and the palette. (Current three.js lights physically, so old intensity numbers render dim. Retune them.)

**2D.** A dark field, additive blending so overlap glows, and a faint full-frame wash each frame so trails fade.

**DOM.** The palette carries a board of cards and panels, and the red is the deny stamp. Idle without a render loop: a slow pulse, a stamp fading in under the drag. A list the player scrolls is built once and mutated in place, never re-rendered under a moving thumb, and ordered by a stable base cost so rows do not reshuffle as scaled prices change. Toggle a panel with an explicit `block` or `flex`. A bare `display=''` only falls back to a stylesheet `display:none`.

**Dread.** The red stops meaning "you did this" and means "already here" — it arrives, stays, shows up where the player did not act, unlabeled. The warm dots drain, the idle motion stops, the camera holds and will not cut. One red dot that was not there last frame is the whole scare.

No imported assets, no rainbow, no boxed toolbar over the scene.
