# Cross-device — one live game, two screens

A game that never pauses cannot park its controls in a menu. The layout and the controls differ between a wide screen and a phone while the game stays live on both.

**Read-state can collapse. Live controls cannot.** Scores, rates, the catalog you browse between actions can fold into a sheet. Any verb the player drives during play stays on screen and moves to where the hand is. A control behind a gesture the player has to stop and open is a paused-game control, and the game is not paused. Panels can overlap on screen, but one surface takes the live verb at a time, so a tap never lands in two places.

**Nothing the player needs under a busy thumb.** On a phone the live controls live in the two bottom corners, clear of the home indicator, and the must-see action renders in the band above them. A thumb holding a stick owns the pixels under it, so nothing critical goes there.

**Lay out per screen.** Portrait phone: controls in the bottom corners, the camera lifted so the action sits in the clear band. Phone held sideways: no bottom sheet, controls in the side gutters, the camera pulled back so the short dimension still frames the play. Wide desktop: the scene with mouse and keyboard, read-state beside it. Clamp an ultrawide so the playfield does not stretch. As the view narrows, widen the field of view or pull the camera back so a five-inch screen stays legible. Size gameplay-critical things to be seen and hit at arm's length. Measure the chrome. Read the non-transitioning panels into a CSS variable and re-measure on resize, or a hardcoded dock height parks a button on top of the controls. Clear the home indicator with `env(safe-area-inset-*)`, and cap a portrait bottom sheet near 40–46vh so it never swallows the play. Floor the type and the hit targets for a thumb (roughly a 12px body, 15px panel titles, 44px targets). Check three real sizes before shipping — 390×844 portrait, 768×1024 tablet, 1280×800 desktop — for overlapped controls, cropped panels, and buttons the thumb cannot reach.

**Each archetype re-lays-out.** A twitch game puts live controls under both thumbs with the scene clear between them; a manager sim pins the speed knob and the buy verbs and tabs the browsing away. A sandbox keeps its sliders thumb-reachable while it runs. The relationship picks the controls. The screen picks where they go.

**Performance is part of the layout.** Cap the pixel ratio, scale particle and shadow budgets down on a phone, and shed detail before frame rate when it is tight. A phone at 20fps is unplayable however good the layout looks. When pinch-zoom is off, give a live game its own way to see a board bigger than the screen.

Test it live on a phone, both orientations, with a touch player. A game tuned on a mouse can be unwinnable on a thumb.
