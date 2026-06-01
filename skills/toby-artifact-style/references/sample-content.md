# Toby Artifact sample content vocabulary

Load this file when you need fake content — placeholder data, demo copy, slide examples, dummy KV values, sample status messages.

Toby Artifact's visual system pairs with a specific voice. Generic "Q4 Revenue / Sales Pipeline / Customer Success" copy makes the visuals look like a misfit. Draw from the mission-ops domain instead.

## Why mission-ops

The system was tuned for evidence-led reference work. Mission ops gives natural reasons to use the components Toby Artifact ships: status pills (stable / watch / consequence), worked examples (premise → derivation → result), decision rows (approve / hold / reject), stat grids with units (°C, ms, dBm). Reach for this vocabulary by default; deviate only when the actual content is from a different domain.

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

Three live verbs in the system:

- **Approve** — proceed with the action.
- **Hold** — defer the action; gather more evidence.
- **Reject** — block the action.

Archival actions: `Defer`, `File`, `Review`, `Snapshot`, `Block`.

Never use marketing verbs in Toby Artifact artifacts: `Submit`, `Get Started`, `Continue`, `Learn More`.

---

## Ownership phrases

- `Owner · Mission ops · Sayo`
- `Owner · GN&C · Sayo`
- `Confidence · High · CI 95%`
- `Confidence · Medium · CI 80%`
- `Cadence · two-sample rule`
- `Cadence · two-sample rule + named rollback`

Placeholder name: `Sayo`. Use it across artifacts to maintain coherence.

---

## Evidence framing

Sample claim formats with units and intervals:

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

Pick the cluster that fits the artifact's subject; reuse its specific terms.

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

Copy and adapt these when you need a quick demo paragraph or callout body.

- "Drift posterior trending high; defer decision until two-sample rule passes."
- "Retry volume sits 18% above baseline. Two-sample rule not yet tripped."
- "Crossing 900 km enters the LEO debris-flux watch band. Defer the next decision until the debris model is updated."
- "Approve controlled release with named rollback owner on record (Sayo · mission ops)."
- "Pass length is shrinking by 0.2 min per day."
- "Residual is no longer random — extend the model with a non-linear panel-angle term."
- "Both meters above their watch threshold for two consecutive samples (T+04:08, T+04:12)."

---

## Caveats to attach

Standard caveats that fit Toby Artifact's "caveat next to the claim" rule:

- "assumes circular orbit; J2 perturbations not included"
- "debris flux excluded above 900 km"
- "drag coefficient for this body shape is not measured here; estimate ±25%"
- "watch threshold breached at sample 8; two-sample rule satisfied at sample 9"
- "rollback rehearsed 21 May 09:18; owner on record"

---

## When to deviate from mission-ops

When the artifact's actual subject is from another domain, use that domain's real vocabulary. Mission-ops is the default for fake or placeholder content, not a mandatory frame for every artifact. A deck on DNS doesn't need to be reframed as mission ops; a placeholder dashboard with no real subject does benefit from it.
