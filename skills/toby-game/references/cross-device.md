# Cross-device

Keep a real-time game playable on both desktop and mobile without hiding live action controls inside a pause menu.

## Live controls and thumb zones

- **Keep action verbs on screen.** Fold read-only tables, catalogs, and stats into a collapsible sheet, while keeping every control the player uses during live play visible and single-target so a tap never triggers two overlapping elements.
- **Clear the thumb zone.** On a portrait phone, place live controls in the bottom corners clear of `env(safe-area-inset-*)` and lift the camera so the action renders in the unobstructed band above the player's thumbs.
- **Adapt to orientation and viewport.** In landscape mobile, move controls to the side gutters and drop the bottom sheet. On desktop, pair mouse/keyboard controls with side panels and clamp ultrawide aspect ratios.

## Sizing and frame budget

- Measure docked panel heights into CSS variables on load and `resize`, cap portrait bottom sheets at `40–46vh`, and keep body text at `>= 12px`, panel titles at `>= 15px`, and touch targets at `>= 44px`.
- Check layout and reachability at `390×844` (portrait phone), `768×1024` (tablet), and `1280×800` (desktop), and test touch input in both orientations.
- Cap `devicePixelRatio` and scale down particle and shadow counts on mobile so frame rate stays near 60 fps.
