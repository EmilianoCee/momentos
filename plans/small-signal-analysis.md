# Plan: Bias point and small-signal analysis

```json plan
{
  "id": "small-signal-analysis",
  "title": "Bias point and small-signal analysis",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["operating-point", "small-signal-analysis", "transconductance", "mos-small-signal-model"],
  "prerequisites": ["square-law", "mosfet-regions"],
  "size": "M",
  "tool": "circuits/amplifiers/small-signal-analysis.html",
  "checks": "plans/checks/small-signal-analysis.py"
}
```

## Concept

A transistor amplifier is a DC bias that picks a point on a curve, plus a small wiggle that sees only the slope there.
The transconductance g_m (siemens) is that slope, and the small-signal model is the tangent line redrawn as a circuit:
a current source g_m·v_gs, with r_o across it.

## Picture

The page has a `.bench`: the left column holds figure 1 with the controls under it, then figure 2; the right column
(`aside`) holds the readouts.

The device and the stage are fixed: an NMOS with μ_nC_ox = 200 µA/V², V_T = 0.5 V (the threshold; the thermal
voltage is not used here) and λ = 0.1 V⁻¹, so k = μ_nC_ox·W/L. The common-source stage has V_DD = 3 V, R_D = 10 kΩ
from V_DD to the drain, the source grounded and V_GS (plus the signal v_gs) on the gate. Capitals are bias values
(V_GS, I_D, V_DS), lower case with lower-case subscripts are signals (v_gs, i_d), and lower case with capital
subscripts are totals (v_GS = V_GS + v_gs, i_D = I_D + i_d).

**Figure 1, `curve`, viewBox 640 by 360.** The transistor's curve and the rotated-waveform picture.
- Main plot: v_GS from 0 V to 1.6 V across, from x = 220 to x = 620 (250 px per volt), grid line and label every
  0.2 V, "v_GS (V)" at the right end under the axis. i_D up, from 0 at y = 220 to i_max at y = 20, five grid lines,
  labelled with SI prefixes just inside the plot's left edge, "i_D" near the top left of the plot. i_max is the
  smallest value of the form s × 10ⁿ µA, with s one of 1, 1.5, 2, 3, 4, 5, 6, 8, that is at least 1.4 × `drainCurrent`
  at v_GS = V_GS + v̂, and at least 20 µA. Everything in the main plot is clipped to it.
- The curve: `drainCurrent` against v_GS at the bias V_DS, 200 points from 0 V to 1.6 V, `--c2`, 2.2 px.
- V_T: a tick on the v_GS axis labelled "V_T".
- The overdrive: a `--c4` bracket just under the v_GS axis from V_T to V_GS, labelled "V_OV = 0.30 V".
- The tangent: a `--c3` line, 1.6 px, through the bias point with slope g_m, across the whole plot.
- The bias point: a 6 px `--ink` dot on the curve at (V_GS, I_D), with a 16 px focusable ring as its handle.
- Projection lines, dotted, `--ink-3`: from (V_GS ± v̂, 0) up to the curve, and from those points of the curve
  left to x = 220.
- Below the main plot: v_GS(t) = V_GS + v̂·sin(ωt) in `--c1`, 2 px, with time running down from y = 236 to y = 352
  over two periods; x is the v_GS value on the main plot's scale. A dashed `--c1` vertical line at V_GS.
- Left of the main plot: i_D(t) = `drainCurrent`(V_GS + v̂·sin(ωt), V_DS) in `--c2`, 2 px, with time running left
  from x = 204 to x = 24 over two periods; y is the i_D value on the main plot's scale. A dashed `--c2` horizontal
  line at I_D. When "show the tangent's prediction" is on, the tangent's prediction I_D + g_m·v̂·sin(ωt) is drawn
  over it as a dashed (5 4) `--c3` line, so the gap between them is the error of the linear model.

**Figure 2, `circuits`, viewBox 640 by 240.** Two circuits side by side, wires in `--ink`, 1.6 px.
- Left, from x = 20 to x = 300, headed "the stage": the rail "V_DD = 3 V" at y = 30; R_D vertical from y = 40 to
  y = 100 at x = 200, labelled "R_D = 10 kΩ"; the drain node at (200, 110) labelled "V_DS = 1.93 V"; the NMOS with its
  drain at the top, its source to ground at y = 210 and its gate on the left at x = 160; a `--c2` arrow down beside R_D
  labelled "I_D = 107 µA". From the gate, a wire left to x = 60 and down through a DC source labelled
  "V_GS = 0.80 V" (`--c1`), drawn as a battery with its long plate (+) on top, and a sine source labelled "v_gs"
  (`--c1`) in series, to ground, with both labels to the right of their sources.
- Right, from x = 300 to x = 636, headed "the small-signal circuit": the sine source "v_gs" at x = 345 from the
  gate node (380, 110) to ground; the gate node labelled "gate" above it and "no current in" below and to its right; from the drain node to
  ground, a current source at x = 480 (a circle with a downward arrow) labelled "g_m·v_gs" and, lower left,
  "g_m = 716 µS" in `--c3`; r_o at x = 575 and R_D at x = 620 from the drain node (575, 50) to ground, their values
  "r_o = 93.2 kΩ" and "R_D = 10 kΩ" at the bottom right, with "V_DD → ground" under them; the drain node labelled
  "v_ds = A_v·v_gs". The gate node, the controlled source and r_o sit inside a dashed `--ink-3` box from (366, 60) to
  (590, 176) labelled "transistor model" at its top left; the drain wire leaves through its top and the source (ground)
  wires through its bottom, and the T-junctions on the ground rail have dots.
- When "small-signal circuit alone" is ticked, the left circuit's DC sources (the V_DD rail and the V_GS source) are
  drawn at opacity 0.25 and the note "DC sources hold still: zero signal" appears under the left circuit.

**Readouts, in the aside,** in `.read`:
- "V_GS = 0.80 V" in `--c1`; "V_OV = V_GS − V_T = 0.30 V" in `--c4`; "I_D = 107 µA" in `--c2`; "V_DS = 1.93 V,
  saturation" in `--ink` (or "triode", or "cut-off").
- "g_m = 2I_D/V_OV = 0.716 mS" in `--c3`, large (`.big`); "r_o = 1/(λI_D) = 93.2 kΩ"; "A_v = −g_m (r_o ∥ R_D) = −6.46".
- "v̂ = 50.0 mV" in `--c1`; "i_d fundamental = 35.8 µA" in `--c2`; "second harmonic = 4.17 % of it (rule:
  v̂/4V_OV = 4.17 %)".
- In triode: "triode: V_DS < V_OV, the saturation model does not apply" in `--accent`. In cut-off: "cut-off: no
  current, g_m = 0" in `--accent`. Outside saturation the A_v line reads "A_v: not from this model outside
  saturation", and the rule in brackets is left out of the second-harmonic line.
- A second harmonic below 10⁻⁶ of the fundamental is written "0 %" (in triode at fixed V_DS the curve is a
  straight line in v_GS, so its second harmonic is zero to rounding).
- Every number has three significant figures and an SI prefix (µ, m, k).

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| gate voltage, bias and signal | V_GS, v_gs, v̂ | `--c1` |
| drain current, bias and signal | I_D, i_d, i_D | `--c2` |
| transconductance: the tangent and the controlled source | g_m | `--c3` |
| overdrive | V_OV | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| bias point | draggable handle on the curve (dragging anywhere in the main plot moves it to the pointer's v_GS) | V_GS in V | 0.40 V to 1.50 V | 0.01 V | 0.80 V | ← → 0.01 V, Shift + ← → 0.1 V |
| amplitude | slider | v̂ in V | 0 V to 0.5 V | 0.005 V | 0.05 V | arrows: one step |
| W/L | slider, log | W/L, slider value log₁₀(W/L) | 1 to 100 (0 to 2) | 0.05 decade | 10 (1) | arrows: one step |
| tangent | checkbox, "show the tangent's prediction" | | on, off | | on | Space |
| alone | checkbox, "small-signal circuit alone" | | on, off | | off | Space |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "v̂ = 30.0 mV", "W/L = 10.0".
- What moves when each control changes: the bias point and W/L change the bias, so `biasPoint` is solved again and
  everything is redrawn. The amplitude moves the waveforms, the projection lines, i_max and the signal readouts.
  The checkboxes only show or hide what they name.
- Reset: V_GS = 0.80 V, v̂ = 0.05 V, W/L = 10, tangent on, alone off.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: g_m is not a property of the transistor alone; it is the slope at the bias point.
  Move the dot and the slope changes. Raise the amplitude and the output stops looking like the input, which is what
  "small" means.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. k is μ_nC_ox·W/L in A/V², VT and
the voltages in V, lam (λ) in 1/V, currents in A, resistances in Ω.

### `drainCurrent(k, VT, lam, VGS, VDS)`

- Returns: I_D in A.
- Formula: with V_OV = VGS − VT: 0 if V_OV ≤ 0 (cut-off); (k/2)·V_OV²·(1 + lam·VDS) if VDS ≥ V_OV (saturation);
  k·(V_OV·VDS − VDS²/2)·(1 + lam·VDS) otherwise (triode).
- Valid for: VDS ≥ 0.
- Approximation: the square law, which ignores velocity saturation and subthreshold current; the factor
  (1 + λ·V_DS) is applied in triode too, so the two regions meet without a step.

### `biasPoint(k, VT, lam, VGS, VDD, RD)`

- Returns: `{ ID, VDS, VOV, region }`, region one of "cut-off", "saturation", "triode".
- Formula: cut-off if V_OV ≤ 0, with ID = 0 and VDS = VDD. Otherwise, with a = k·V_OV²/2, try saturation:
  ID = a·(1 + lam·VDD)/(1 + a·lam·RD), from ID = a·(1 + lam·(VDD − ID·RD)), and VDS = VDD − ID·RD; it holds if
  VDS ≥ V_OV. Otherwise triode: bisect 200 times on VDS between 0 and V_OV for the zero of
  (VDD − VDS)/RD − `drainCurrent`(…, VDS) (positive means VDS is too low), take the midpoint of the last interval,
  and ID = (VDD − VDS)/RD.
- Approximation: as `drainCurrent`.

### `gm(k, VT, lam, VGS, VDS)`

- Returns: ∂I_D/∂V_GS at fixed VDS, in S.
- Formula: 0 in cut-off; k·V_OV·(1 + lam·VDS) in saturation, which equals 2·I_D/V_OV; k·VDS·(1 + lam·VDS) in triode.
- Approximation: as `drainCurrent`.

### `ro(lam, ID)`

- Returns: 1/(lam·ID) in Ω, and Infinity when lam·ID = 0.
- Approximation: the exact slope gives (1 + λV_DS)/(λI_D); 1/(λI_D) is the usual form and is within λV_DS of it.

### `gain(gm, ro, RD)`

- Returns: the common-source voltage gain −gm·(ro ∥ RD), a pure number; RD alone when ro is Infinity.
- Sign convention: negative: the drain falls when the gate rises.
- Approximation: the small-signal model.

### `hd2Rule(VOV, vhat)`

- Returns: vhat/(4·VOV), the second harmonic of the drain current as a fraction of its fundamental.
- Formula: from (V_OV + v̂ sin θ)² = V_OV² + 2V_OV v̂ sin θ + v̂²/2 − (v̂²/2) cos 2θ: fundamental k·V_OV·v̂, second
  harmonic k·v̂²/4.
- Valid for: v̂ ≤ V_OV, in saturation. Beyond that the transistor cuts off for part of each cycle.

### `harmonics(k, VT, lam, VGS, VDS, vhat)`

- Returns: `{ a1, a2, ratio }`: the amplitudes in A of the fundamental and the second harmonic of
  `drainCurrent`(VGS + vhat·sin θ, VDS) − `drainCurrent`(VGS, VDS), and a2/a1 (0 when a1 = 0).
- Formula: a 256-point discrete Fourier sum: for n = 0 … 255, θ = 2πn/256; a_m = (2/256)·√((Σ i·sin mθ)² + (Σ i·cos mθ)²)
  for m = 1, 2.
- Approximation: V_DS is held at its bias value: this is the device curve, without the load.

### `swing(k, VT, lam, VGS, VDS, vhat)`

- Returns: `{ up, down }` in A: how far the drain current rises at v_gs = +vhat and falls at v_gs = −vhat, from the
  curve itself, at fixed VDS.
- Sign convention: both are positive for a rise and a fall.

The tool calls `biasPoint` with k = 200 µA/V²·W/L, VT = 0.5, lam = 0.1, VDD = 3, RD = 10 000, and every other function
at the resulting VDS. The tangent's prediction in figure 1 is I_D + g_m·v̂·sin(ωt), and the main script takes g_m from
`gm`.

## Check cases

Computed by `plans/checks/small-signal-analysis.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "drainCurrent", "args": [0.002, 0.5, 0, 0.8, 2], "expect": 9.000000000000002e-05, "tol": 1e-12, "units": "A", "tag": "typical", "note": "k = 2 mA/V², V_T = 0.5 V, no λ, V_GS = 0.8 V (V_OV = 0.3 V), saturated: I_D = ½·2 mA/V²·(0.3 V)² = 90 µA"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 0.1, 0.8, 2], "expect": 0.00010800000000000002, "tol": 1e-12, "units": "A", "tag": "typical", "note": "the same with λ = 0.1 /V at V_DS = 2 V: 90 µA × 1.2 = 108 µA"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 0, 1.0, 0.1], "expect": 8.999999999999999e-05, "tol": 1e-12, "units": "A", "tag": "typical", "note": "triode: V_OV = 0.5 V but V_DS = 0.1 V: I_D = 2 mA/V²·(0.5·0.1 − 0.005) V² = 90 µA"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 0.1, 0.4, 2], "expect": 0.0, "tol": 1e-12, "units": "A", "tag": "limit-zero", "note": "V_GS = 0.4 V is below V_T = 0.5 V: cut off, no current"},
  {"fn": "biasPoint", "args": [0.002, 0.5, 0.1, 0.8, 3, 10000], "expect": {"ID": 0.00010733944954128442, "VDS": 1.9266055045871557, "VOV": 0.30000000000000004, "region": "saturation"}, "tol": 1e-12, "units": "A, V", "tag": "typical", "note": "W/L = 10 (k = 2 mA/V²), V_GS = 0.8 V, V_DD = 3 V, R_D = 10 kΩ, λ = 0.1 /V: I_D = 107 µA, V_DS = 1.93 V, saturated"},
  {"fn": "biasPoint", "args": [0.002, 0.5, 0.1, 1.1, 3, 10000], "expect": {"ID": 0.00027107229412992633, "VDS": 0.2892770587007364, "VOV": 0.6000000000000001, "region": "triode"}, "tol": 1e-12, "units": "A, V", "tag": "breaks", "note": "the same stage with V_GS = 1.1 V: the drain falls to 0.289 V, below V_OV = 0.6 V. The transistor is in triode and the saturation model no longer holds"},
  {"fn": "gm", "args": [0.002, 0.5, 0, 0.8, 2], "expect": 0.0006000000000000001, "tol": 1e-12, "units": "S", "tag": "typical", "note": "k = 2 mA/V² at V_OV = 0.3 V, no λ: g_m = k·V_OV = 0.6 mS, which is also 2·90 µA/0.3 V"},
  {"fn": "gm", "args": [0.002, 0.5, 0, 1.1, 2], "expect": 0.0012000000000000001, "tol": 1e-12, "units": "S", "tag": "typical", "note": "the same transistor at V_OV = 0.6 V: g_m doubles to 1.2 mS. g_m belongs to the bias point, not to the transistor"},
  {"fn": "gm", "args": [0.002, 0.5, 0.1, 0.8, 1.9267], "expect": 0.0007156020000000002, "tol": 1e-12, "units": "S", "tag": "typical", "note": "with λ = 0.1 /V at the stage's V_DS = 1.93 V: g_m = 0.6 mS × 1.193 = 0.716 mS"},
  {"fn": "gm", "args": [0.002, 0.5, 0.1, 0.45, 2], "expect": 0.0, "tol": 1e-12, "units": "S", "tag": "limit-zero", "note": "V_GS below V_T: no current and no slope, g_m = 0"},
  {"fn": "ro", "args": [0.1, 0.0001], "expect": 99999.99999999999, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "λ = 0.1 /V at I_D = 100 µA: r_o = 1/(λ·I_D) = 100 kΩ"},
  {"fn": "ro", "args": [0, 0.0001], "expect": "Infinity", "tol": 1e-09, "units": "Ω", "tag": "limit-infinity", "note": "with λ = 0 the drain current ignores V_DS: r_o is infinite, an ideal current source"},
  {"fn": "gain", "args": [0.0006, "Infinity", 10000], "expect": -5.999999999999999, "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "g_m = 0.6 mS into R_D = 10 kΩ with r_o infinite: A_v = −g_m·R_D = −6"},
  {"fn": "gain", "args": [0.0007156, 93170, 10000], "expect": -6.462387515750704, "tol": 1e-09, "units": "", "tag": "typical", "note": "g_m = 0.716 mS, r_o = 93.2 kΩ, R_D = 10 kΩ: A_v = −g_m (r_o ∥ R_D) = −6.46"},
  {"fn": "hd2Rule", "args": [0.3, 0.03], "expect": 0.025, "tol": 1e-09, "units": "", "tag": "typical", "note": "v̂ = 30 mV on V_OV = 0.3 V: the second harmonic is v̂/(4·V_OV) = 2.5% of the fundamental"},
  {"fn": "harmonics", "args": [0.002, 0.5, 0, 0.8, 2, 0.03], "expect": {"a1": 1.7999999999999997e-05, "a2": 4.5000000000000157e-07, "ratio": 0.02500000000000009}, "tol": 1e-12, "units": "A, A, ratio", "tag": "typical", "note": "the same, from the curve itself: a fundamental of g_m·v̂ = 18 µA and a second harmonic of 0.45 µA, 2.5%"},
  {"fn": "harmonics", "args": [0.002, 0.5, 0, 0.8, 2, 0.001], "expect": {"a1": 5.999999999999957e-07, "a2": 4.999999999996353e-10, "ratio": 0.0008333333333327315}, "tol": 1e-12, "units": "A, A, ratio", "tag": "limit-zero", "note": "v̂ = 1 mV on V_OV = 0.3 V: the second harmonic is 0.083% of the fundamental. Small means small next to V_OV"},
  {"fn": "harmonics", "args": [0.002, 0.5, 0, 0.8, 2, 0.5], "expect": {"a1": 0.00031161135475780207, "a2": 0.00011535142851547335, "ratio": 0.37017723120240437}, "tol": 1e-12, "units": "A, A, ratio", "tag": "breaks", "note": "v̂ = 0.5 V on V_OV = 0.3 V: the transistor cuts off for part of every cycle and the second harmonic is 37% of the fundamental; the rule v̂/(4V_OV) would say 42%"},
  {"fn": "swing", "args": [0.002, 0.5, 0, 0.8, 2, 0.3], "expect": {"up": 0.00027000000000000006, "down": 9.000000000000002e-05}, "tol": 1e-12, "units": "A", "tag": "breaks", "note": "v̂ = V_OV = 0.3 V: the current rises 270 µA and falls 90 µA, while the tangent g_m·v̂ = 180 µA predicts the same both ways"},
  {"fn": "swing", "args": [0.002, 0.5, 0, 0.8, 2, 0.01], "expect": {"up": 6.100000000000013e-06, "down": 5.899999999999994e-06}, "tol": 1e-12, "units": "A", "tag": "sign", "note": "v̂ = 10 mV: up 6.1 µA and down 5.9 µA, within 2% of g_m·v̂ = 6 µA. The rise is always the larger: the curve bends up"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Move the bias from V_GS = 0.8 V to 1.1 V. Does g_m stay the same?
   Why: No. The slope of the curve grows with the overdrive: g_m = k·V_OV, so doubling V_OV from 0.3 V to 0.6 V doubles
   g_m. g_m belongs to the bias point, not to the transistor.
2. With the bias at 1.1 V, what happens to the gain?
   Why: It collapses. 270 µA through 10 kΩ pulls the drain down to 0.29 V, below V_OV = 0.6 V, so the transistor is in
   triode and is no longer a current source. Find the region before using the small-signal model.
3. Raise v̂ until the second harmonic reaches 10 %. How big is v̂ next to V_OV?
   Why: About 0.4 V_OV: the rule is v̂/(4V_OV). "Small" is measured against the overdrive, not against V_DD.
4. Put v̂ = V_OV. Does the drain current rise and fall by the same amount?
   Why: No: it rises three times as far as it falls (270 µA up, 90 µA down at V_OV = 0.3 V). The curve bends up, and
   the tangent misses both.
5. In the small-signal circuit, where did V_DD go?
   Why: To ground. A DC source holds its voltage whatever the signal does, so it adds no signal: for the signal it is a
   short to ground.

## Misconceptions

- "The small-signal model is a different transistor." What the tool shows instead: the tangent touches the same curve
  at the bias point, and the controlled source g_m·v_gs in figure 2 takes its g_m from that slope.
- "DC sources are zero volts in the real circuit." What the tool shows instead: the left circuit keeps V_DD = 3 V; only
  in the small-signal circuit, which counts changes, does it become ground.
- "g_m is a fixed number, like R." What the tool shows instead: dragging the bias point changes the g_m readout and the
  tangent's slope while W/L is untouched.
- "Small means small next to the supply." What the tool shows instead: the second-harmonic readout depends on v̂/V_OV,
  and at V_OV = 0.3 V a 0.1 V signal already gives 8 %.

## Quiz hooks

- L2 looks like: computes I_D, g_m = 2I_D/V_OV and r_o = 1/(λI_D) from given values, draws the small-signal model and
  writes A_v = −g_m(r_o ∥ R_D).
- L3 looks like: explains g_m as the slope of i_D against v_GS at the bias point; says why a DC source becomes ground;
  checks the region before linearising; predicts how g_m and the gain move when the bias or W/L changes; says what
  "small" is measured against.
- L4 looks like: chooses a bias for gain and swing together (low V_OV for gain, but enough V_DS headroom and a signal
  small next to V_OV); estimates distortion from v̂/(4V_OV); knows the square law fails at short channels and in weak
  inversion, and that g_m = 2I_D/V_OV changes with it.
- Missteps:
  - uses the small-signal model without checking that the transistor is in saturation
  - treats g_m as a constant of the transistor instead of a function of the bias
  - leaves a DC source in the small-signal circuit, or turns a DC current source into a short
  - adds a resistor between gate and source in the MOSFET model
  - measures "small" against V_DD instead of V_OV
- Seeds, to be varied and never asked word for word:
  - predict: a stage biased at some V_OV and I_D; W/L is doubled with V_GS held. What happens to I_D, g_m and the
    gain, and is the transistor still saturated?
  - explain: why the DC supply is a ground in the small-signal circuit.
  - limit: the signal amplitude raised toward V_OV: which way does the output wave distort, and why?
  - transfer: a BJT stage at a given I_C: write its g_m, and say what plays the role of V_OV in deciding what "small"
    means.

## Where this shows up

- `operating-point`: the bias is found first, with signals off, and it fixes every small-signal number.
- `transconductance`: g_m is the slope at the bias point, 2I_D/V_OV for a MOSFET.
- `mos-small-signal-model`: the tangent redrawn as a circuit: g_m·v_gs with r_o across it and no gate current.
- `square-law`: the curve the bias point sits on.
- `mosfet-regions`: the model holds only in saturation; the readout says when the bias leaves it.
- `common-source`: the stage in figure 2, with gain −g_m(r_o ∥ R_D).
- Later: EE 140: every analog design starts from a bias point and its g_m/I_D. EE 105's later units: the same steps
  for the BJT, with kT/q in place of V_OV.

## Page text

- Header `Concept:` A transistor amplifier is a bias point on a curve plus a small wiggle that sees only the slope
  there; g_m is that slope, and the small-signal model is the tangent redrawn as a circuit.
- Header `Course:` EE 105 (operating point, MOS small-signal model, transconductance)
- Header `Play with:` The bias point on the i_D–v_GS curve, the signal amplitude, W/L; the tangent's prediction; the
  small-signal circuit alone
- Header `Should click:` g_m belongs to the bias point, not to the transistor: move the point and the slope changes.
  "Small" means small next to the overdrive.
- Title: Bias point and small-signal analysis
- Lede: An amplifier holds a transistor at one point on its curve and adds a small wiggle. The wiggle sees only the
  slope at that point, g_m, so the curve can be replaced by its tangent and the transistor by a current source. Drag
  the point and the slope changes; make the wiggle big and the tangent stops telling the truth.
- Caption of `curve`: Drag the dot along the curve (or press anywhere in the plot); focused, ← → move it 0.01 V,
  with Shift 0.1 V. The gate voltage swings below, the drain current comes out on the left.
- Caption of `circuits`: The stage with its DC sources, and the same stage as the signal sees it.
- What should click:
  - **The signal sees a slope.** For a small v_gs the curve is as good as its tangent, so i_d = g_m·v_gs. That one
    number, the slope at the bias point, is all the transistor contributes to the gain.
  - **g_m belongs to the bias.** g_m = k·V_OV = 2I_D/V_OV. More current or more overdrive, a steeper slope. The same
    transistor at another bias is a different amplifier.
  - **Small means small next to V_OV.** The second harmonic is v̂/(4V_OV) of the fundamental. With V_OV = 0.3 V, 30 mV
    is already 2.5 %.
  - **DC sources hold still.** In the small-signal circuit V_DD and V_GS are grounds: they do not change, so they add
    no signal. The bias decides g_m and r_o, and then leaves the picture.

## Acceptance checklist

- [x] One `.html` file at the plan's `tool` path, started from `templates/tool-template.html`, with no dependencies, no `fetch` and no modules.
- [x] The house-style block is unchanged, and the tool's own CSS comes after its end marker.
- [x] The header comment has `Concept`, `Course`, `Play with`, `Should click` and `Plan`. `Checked` is written last, and only for what was checked.
- [x] `MATHS` has every function in the Maths section, with those names and arguments, and nothing in the maths block touches the page.
- [x] The check-cases block is the plan's, unchanged, and `node scripts/test-tools.js` passes for this tool.
- [x] Every control in the Interaction table exists, with its range, step and start value, and works from the keyboard.
- [x] Each quantity has its colour from the table, the same in the figure, the numbers and the prose. Controls are neutral.
- [x] Every number on the page has its unit. `j` is the imaginary unit.
- [x] The page has a `← map` link to its topic, a light/dark button, "What should click", "Predict, then try" with the prompts above, and "Where this shows up" with links to the map.
- [x] It respects `prefers-reduced-motion` and does not redraw when nothing is moving.
- [x] The tool's path is in the `tools` of each of the plan's topics in `map/`, and the plan's status is `built`.
- [x] `python3 scripts/build.py` and `python3 scripts/check.py` pass, and the page was looked at in a browser in light and dark.
