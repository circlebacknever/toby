# Visual identity

The base style stays the same in any genre, but the set of techniques changes with the render mode.

**The floor.** Use warm paper and near-black ink, and exactly one red that means consequence, such as a denial, a death, or the one dangerous button. If you use the red anywhere else, it stops meaning anything. Mood comes from one source, which is one light in 3D or one accent in 2D. Keep something moving at all times, but reduce the motion when the player asks for reduced motion. Use monospace with steady-width digits for data and a humanist sans for prose. Remove any label that adds no information.

The palette is paper `#fdfaf1`, ink `#1a1c1f`, the one red `#c44e3f`, and a dark field `#0e0f12` for canvas. Draw the rest from a muted set: teal `#2e6a78`, green `#4d7a30`, amber `#b07020`, deep rust `#7a2d22`. Name the tokens `--toby-*`. Build a different set for a different mood, but keep the single red and its rare use. The example games ship an older token prefix, so rename it when you copy.

**3D.** Build characters and props from non-uniformly scaled low-poly spheres. A car, a head, and a tail are the same primitive, which is what makes them look related. Keep everything matte and flat-shaded, but let a ball or an eye use smooth shading. Use one warm or cool light, low fill underneath, and warm dots for windows and fire. Make things bob and sway on a shared clock, with a different offset for each thing, so the crowd does not move in unison. Frame a diorama from above, or use a clamped orbit for a system you study. Cuteness is optional, so for an austere premise, replace the spheres with boxes, lines, and the palette. Current three.js uses physical lighting, so old intensity numbers render dim and need retuning.

**2D.** Use a dark field, additive blending so overlap glows, and a faint full-frame wash each frame so trails fade.

**DOM.** Use the palette to color a board of cards and panels. Use the red for the deny stamp. Show idle motion without a render loop, such as a slow pulse or a stamp fading in under the drag. Build a list the player scrolls once, and mutate it in place without re-rendering it under a moving thumb. Order the list by a stable base cost so rows do not reshuffle as scaled prices change. Toggle a panel with an explicit `block` or `flex`, because a bare `display=''` only falls back to a stylesheet `display:none`.

**Dread.** The red changes from meaning "you did this" to meaning "already here." The red appears, stays on screen, and shows without a label in places where the player did not act. The warm dots fade out, the idle motion stops, and the camera stays on one shot without cutting. The scare comes from a single red dot that was not there in the previous frame.

Use no imported assets, no rainbow, and no boxed toolbar over the scene.
