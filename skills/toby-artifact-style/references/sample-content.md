# Toby Artifact sample content vocabulary

Load this file when you need fake content, such as placeholder data, demo copy, slide examples, dummy KV values, or sample status messages.

Toby Artifact's visual system is designed for a specific voice. Generic "Q4 Revenue / Sales Pipeline / Customer Success" copy does not match the visuals, so draw from the mission-ops domain.

## Why mission-ops

The system was tuned for evidence-led reference work. Mission-ops content has natural uses for the components that Toby Artifact ships. Those components include status pills (stable / watch / consequence), worked examples (premise → derivation → result), and decision rows (approve / hold / reject). They also include stat grids with units (°C, ms, dBm). Use this vocabulary by default, and deviate only when the actual content is from a different domain.

---

## Operational state

`stable` · `watch` · `consequence` · `unknown` · `drift` · `residual` · `breach` · `threshold` · `sample` · `pass` · `two-sample rule` · `watch band` · `consequence band` · `named rollback owner` · `controlled release` · `defer` · `escalate` · `throttle`

---

## Mission / artifact identifiers

- `M-01` through `M-05` — practice modules.
- `v4.2`, `v3.9` — versions.
- `R-04.2` — reference deck identifier.
- `T+04:12 UTC`, `T+18`, `T+42` — mission elapsed time.
- `n=240` — sample count.
- Full session line: `SESSION T+04:12 · M-01 · v4.2`.

---

## Decision verbs

The system has three live decision verbs:

- **Approve** — proceed with the action.
- **Hold** — defer the action and gather more evidence.
- **Reject** — block the action.

The archival actions are `Defer`, `File`, `Review`, `Snapshot`, and `Block`.

Never use marketing verbs in Toby Artifact artifacts: `Submit`, `Get Started`, `Continue`, `Learn More`.

---

## Ownership phrases

- `Owner · Mission ops · Sayo`
- `Owner · GN&C · Sayo`
- `Confidence · High · CI 95%`
- `Confidence · Medium · CI 80%`
- `Cadence · two-sample rule`
- `Cadence · two-sample rule + named rollback`

Use `Sayo` as the placeholder name in every artifact, so the same name appears across artifacts.

---

## Evidence framing

These sample claims show the format for units and intervals:

- `drift posterior 0.73`
- `coverage 94%`
- `pass window 7 min`
- `retry rate 18%`
- `queue age 88 s`
- `RSSI −82 dBm`
- `BER 5e-8`
- `R² 0.88`
- `slope +0.005 °C / sample`
- `±0.08 (95% CI)`

---

## Domain clusters

Pick the cluster that fits the artifact's subject, then reuse its specific terms.

### Orbital mechanics (M-01)
altitude · inclination · period · perigee · apogee · vis-viva · Kepler · semi-major axis · eccentricity · μ = 3.986 × 10¹⁴ m³/s² · LEO debris band above 900 km · passive deorbit · J2 perturbation

### Thermal residuals (M-02)
sensor S-1 · sensor S-2 · panel temperature · solar angle · thermal residual · model v3.1 · R² = 0.88 · drift trend +0.005 °C / sample · first-order thermal model

### Comms windows (M-03)
DSN · ESTRACK · Goldstone · Madrid · Canberra · Cebreros · pass length · X-band · S-band · RSSI · BER · link quality · ground station · ascending node · elevation max 48° · fold-back to S-band

### Retry pressure (M-04)
retry rate · queue age · partner errors · throttle ingress · ingress 60% · two-sample rule · consequence-band entry

### Release readiness (M-05)
viability score · build pass rate · caveat freshness · rollback rehearsed · weighted lanes · viability 0.73 ± 0.08 · watch band 0.6–0.85

---

## Example placeholder sentences

Copy and adapt these sentences when you need a quick demo paragraph or callout body.

- "Drift posterior is trending high, so defer the decision until the two-sample rule passes."
- "Retry volume is 18% above baseline, but the two-sample rule has not tripped yet."
- "Crossing 900 km enters the LEO debris-flux watch band. Defer the next decision until the debris model is updated."
- "Approve controlled release with named rollback owner on record (Sayo · mission ops)."
- "Pass length is shrinking by 0.2 min per day."
- "The residual is no longer random, so extend the model with a non-linear panel-angle term."
- "Both meters are above their watch threshold for two consecutive samples (T+04:08, T+04:12)."

---

## Caveats to attach

These standard caveats follow Toby Artifact's "caveat next to the claim" rule:

- "assumes a circular orbit and excludes J2 perturbations"
- "debris flux is excluded above 900 km"
- "drag coefficient for this body shape is not measured here, so the estimate is ±25%"
- "the watch threshold was breached at sample 8, then the two-sample rule was satisfied at sample 9"
- "rollback was rehearsed 21 May 09:18, with the owner on record"

---

## When to deviate from mission-ops

When the artifact's actual subject is from another domain, use that domain's real vocabulary. Mission-ops is the default for fake or placeholder content. A deck on DNS doesn't need to be reframed as mission ops, but a placeholder dashboard with no real subject does benefit from it.
