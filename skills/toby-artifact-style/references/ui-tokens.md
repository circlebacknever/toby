# UI tokens

Use these tokens when writing CSS for an HTML or React page.

## Spacing in multiples of 4

Prefer named tokens. When no token matches exactly, pick the closest one, and never use a one-off value.

```css
--space-xs:     4px;   /* gap between tightly-coupled siblings */
--space-sm:     8px;   /* inline gap, badge padding */
--space-md:    12px;   /* tight control padding */
--space-base:  16px;   /* row padding, card body gap */
--space-lg:    20px;   /* cell padding, dialog body gap */
--space-xl:    24px;   /* section padding */
--space-2xl:   32px;   /* dialog padding */
--space-3xl:   40px;   /* empty-state padding */
--space-4xl:   48px;   /* major separation */
--space-5xl:   64px;   /* section gap */
```

## Control heights, icon sizes, radius, border widths

```css
/* Pair control heights with --space-* paddings. */
--ctrl-h-xs:   20px;   /* badge, very compact pill */
--ctrl-h-sm:   28px;   /* btn--sm, toolbar btn, pagination cell */
--ctrl-h-md:   36px;   /* default btn, input, combobox */
--ctrl-h-lg:   44px;   /* touch target, OTP slot */
--ctrl-h-xl:   56px;   /* topbar */

/* Icons */
--icon-xs: 12px;  --icon-sm: 14px;  --icon-md: 16px;  --icon-lg: 20px;  --icon-xl: 24px;

/* Radius */
--radius-xs:    4px;   /* kbd, day cells */
--radius-sm:    8px;   /* compact controls, chips */
--radius-md:   10px;   /* buttons */
--radius-base: 12px;   /* inputs, cards, panels */
--radius-lg:   18px;   /* outer slide panel, dialog */
--radius-full: 999px;  /* pills, status dots */

/* Border widths */
--bw-hairline: 1px;    /* default rule */
--bw-accent:   2px;    /* focus ring, in-page accent */
--bw-emph:     3px;    /* section accent strip, active-tab underline, sidebar inset */
--bw-strip:    4px;    /* alert left edge, dialog--alert top */
```

## Elevation, z-index, motion timing

```css
/* For elevation, pick the lowest layer that solves the problem. */
--elev-hairline: 0 0 0 1px var(--border-hairline);
--elev-card:     0 1px 0 var(--border-hairline);
--elev-low:      0 1px 2px rgba(28,31,35,0.06);
--elev-mid:      0 2px 8px -2px rgba(28,31,35,0.10), 0 0 0 1px var(--border-hairline);
--elev-pop:      0 6px 24px -8px rgba(28,31,35,0.18), 0 0 0 1px var(--border-hairline);
--elev-high:     0 12px 32px -10px rgba(28,31,35,0.24), 0 0 0 1px var(--border-hairline);

/* Z-index values are strictly layered, so never invent a value between these. */
--z-base: 0;  --z-rail: 10;  --z-dropdown: 50;  --z-nav-panel: 60;
--z-popover: 70;  --z-tooltip: 80;  --z-sheet: 90;  --z-modal: 100;  --z-toast: 200;

/* Motion timing */
--ease-out:          cubic-bezier(0.2, 0, 0, 1);
--motion-fast:       100ms;  /* hover, focus, press */
--motion-quick:      120ms;  /* state changes */
--motion-disclosure: 180ms;  /* panel reveal */
--motion-overlay:    220ms;  /* sheet & dialog entrance */
```

## Interaction shades and code colors

```css
/* Interaction shades are derived from ink and accent. */
--surface-card:       #fffefa;  /* alias of paper-3 for card backgrounds */
--surface-pressed:    #d9d3bf;
--ink-hover:          #4a4e57;
--ink-pressed:        #000000;
--accent-hover:       #a04030;
--accent-pressed:     #7e3023;

/* Code blocks use lifted syntax colors on a dark background. */
--code-kw:            #8ec8d8;  /* keywords, lifted info teal */
--code-num:           #e8a48e;  /* numbers, warm coral */
--code-str:           #a8c98a;  /* strings, lifted green */
--code-com:           #7c7568;  /* comments, muted and italic */
```

## Interaction states

- **Hover (paper):** The background changes to `--toby-paper-2`, but the foreground stays the same.
- **Hover (dark):** The background lightens to `--ink-hover` (`#4a4e57`), but the text stays the same.
- **Active / press:** The background turns darker (`--surface-pressed` / `--ink-pressed` / `--accent-pressed`), but the border stays. The control does not shrink or move.
- **Focus:** Draw a 2px outside ring in `--toby-info` (teal) at a 2px offset. **Never use red.**
- **Selected / current in lists/trees/menus:** Use a `--toby-paper-2` background with a 3px `--toby-info` inset on the left. Paper-3 against paper-3 is invisible, so never use paper-3 as a selection state.

Hover and base must differ by ≥ 3:1 contrast (WCAG 1.4.11).

## Icons

- Use Lucide where available. Inline SVG is acceptable for static artifacts. Use the app's icon library for coded frontends when one exists. Draw icons at 16–20px with a 1.5px stroke, square caps, and monochromatic `currentColor`.
- Heroicons-outline, Tabler, and Phosphor-regular are acceptable fallback families. Material Icons and Carbon are too dense, so do not use them.
- Keep the system to about 12 glyphs. If you need a 13th, use a text label.
