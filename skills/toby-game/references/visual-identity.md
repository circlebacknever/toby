# Visual identity — the look

The floor stays the same in any genre, but the kit of techniques changes with the render mode.

**The floor.** Use warm paper and near-black ink, and exactly one red that means consequence, such as a denial, a death, or the one dangerous button. If you use the red anywhere else, it stops meaning anything. Mood comes from one source, which is one light in 3D or one accent in 2D. Nothing is ever fully still. When the player asks for reduced motion, quiet the motion. Use monospace with steady-width digits for data and a humanist sans for prose. Every label adds information or it is cut.

The palette is paper `#fdfaf1`, ink `#1a1c1f`, the one red `#c44e3f`, and a dark field `#0e0f12` for canvas. Draw the rest from a muted set: teal `#2e6a78`, green `#4d7a30`, amber `#b07020`, deep rust `#7a2d22`. Name the tokens `--toby-*`. Build a different set for a different mood, and keep the single rationed red. The example games ship an older token prefix, so rename it when you copy.

**3D.** Build characters and props from non-uniformly scaled low-poly spheres. A car, a head, and a tail are the same primitive, which is what makes them look related. Keep everything matte and flat-shaded. Let a ball or an eye go smooth. Use one warm or cool light, low fill underneath, and warm dots for windows and fire. Bob and sway on a shared clock with a per-thing offset so the crowd does not pulse in unison. Frame a diorama from above, or a clamped orbit for a system you study. Cuteness is optional, so for an austere premise, replace the spheres with boxes, lines, and the palette. Current three.js uses physical lighting, so old intensity numbers render dim and need retuning.

**2D.** Use a dark field, additive blending so overlap glows, and a faint full-frame wash each frame so trails fade.

**DOM.** The palette colors a board of cards and panels, and the red is the deny stamp. Show idle motion without a render loop, such as a slow pulse or a stamp fading in under the drag. Build a list the player scrolls once, and mutate it in place without re-rendering it under a moving thumb. Order the list by a stable base cost so rows do not reshuffle as scaled prices change. Toggle a panel with an explicit `block` or `flex`. A bare `display=''` only falls back to a stylesheet `display:none`.

**Dread.** The red stops meaning "you did this" and starts meaning "already here." It arrives, stays, and shows up unlabeled where the player did not act. The warm dots fade out, the idle motion stops, the camera holds and will not cut. One red dot that was not there last frame is the whole scare.

Use no imported assets, no rainbow, and no boxed toolbar over the scene.
