# Plan: Common source, common gate and common drain

```json plan
{
  "id": "single-stage-amplifiers",
  "title": "Common source, common gate and common drain",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["common-source", "common-gate", "source-follower", "output-swing", "intrinsic-gain"],
  "prerequisites": ["square-law", "mosfet-regions", "channel-length-modulation", "small-signal-analysis", "mos-small-signal-model"],
  "size": "L",
  "tool": "circuits/amplifiers/single-stage-amplifiers.html",
  "checks": "plans/checks/single-stage-amplifiers.py"
}
```

## Concept

One transistor has three terminals. Ground one of them (for the signal), put the input on another and take the output
from the third, and you get the three single-transistor stages. Common source is an inverting voltage amplifier, common
gate a current buffer with a low input resistance, and common drain (the source follower) a voltage buffer with a gain
just under 1. In each, the small-signal gain is the slope of the large-signal curve at the bias point, and it holds only
while the transistor stays in saturation, which is what limits the output swing.

This plan replaces the earlier `common-source` stub: its transfer curve, swing and intrinsic gain are the common-source
mode of this tool.

## Picture

The page has a `.bench`: the left column holds figure 1, the controls, figure 2 and figure 3, in that order; the right
column (`aside`) holds the readouts and the comparison table.

The device and supply are fixed: an NMOS with μ_nC_ox = 200 µA/V², V_T = 0.5 V (the threshold), its body tied to its
source (no body effect), so k = 200 µA/V² × W/L; V_DD = 3 V. The three stages:
- **Common source (cs):** v_IN on the gate, the source grounded, R (called R_D) from V_DD to the drain; output at the
  drain.
- **Common gate (cg):** the gate held at V_B = 1.2 V, v_IN (an ideal voltage source) on the source, R (R_D) from V_DD to
  the drain; output at the drain.
- **Common drain (cd), the source follower:** v_IN on the gate, the drain on V_DD, R (called R_S) from the source to
  ground; output at the source.

Capitals are bias values, lower case with lower-case subscripts are signals, lower case with capital subscripts are
totals.

**Figure 1, `transfer`, viewBox 640 by 360.** v_OUT against v_IN. Plot area from x = 64 to x = 604 (v_IN from 0 to 3 V,
180 px per volt) and from y = 20 to y = 320 (v_OUT from 0 to 3 V, 100 px per volt). Grid lines and labels every 0.5 V
on both axes, "v_IN (V)" at the right end under the axis and "v_OUT (V)" at the top left.
1. Regions: each stretch of v_IN where the transistor is in cut-off or in triode is shaded full height with
   `--grid`, and labelled "cut-off", "triode" or "saturation" at the top of its stretch in `--ink-3`.
2. The swing limits: dashed (6 4) `--c4` horizontal lines at the v_OUT of each end of `satRange`'s input stretch,
   labelled at their right ends by what ends the stretch there, with the value: "edge of cut-off, 3.00 V" or "edge of
   triode, 0.49 V" (the region found by `bias` 1 mV beyond that end), or "end of the v_IN axis, 2.07 V" when the end is
   at 0 V or 3 V.
3. The curve: `solveOut` at 300 points from 0 V to 3 V, `--c2`, 2.4 px.
4. The tangent at the bias point, `--c3`, 1.6 px, with the slope from `slope`, 120 px long each side.
5. Projection lines, dotted `--ink-3`, from (V_IN ± v̂) on the v_IN axis up to the curve and across to the v_OUT axis.
6. A `--c1` bracket under the v_IN axis from V_IN − v̂ to V_IN + v̂.
7. The bias point: a 6 px `--ink` dot on the curve at (V_IN, V_OUT), with a 16 px focusable ring as its handle.

**Figure 2, `wave`, viewBox 640 by 220.** The signals, about their bias values, over two periods. Time across from
x = 64 to x = 604; centre line at y = 122. The vertical scale makes the largest of v̂, the output's excursion each way
and |A_v|·v̂ fill 84 px. Drawn: v_in = v̂·sin(ωt) in `--c1`, 1.6 px; v_out = `solveOut`(V_IN + v̂·sin ωt) − V_OUT in
`--c2`, 2.4 px, 240 points; the linear prediction A_v·v̂·sin(ωt) dashed (5 4) in `--c3`. Labels on one line at the top left, in this order: "v_in
50.0 mV" (`--c1`), "v_out +309 mV / −345 mV" (`--c2`, the largest rise and fall), "A_v·v̂ = 328 mV" (`--c3`).

**Figure 3, `smallsig`, viewBox 640 by 240.** The stage's small-signal circuit, wires in `--ink`, 1.6 px. The drain node
D at (330, 50) and the source node S at (330, 150); the controlled source, a circle of radius 14 at (330, 100) with a
downward arrow, labelled "g_m·v_gs" in `--c3`; r_o at x = 410 from D to S (wired across at y = 50 and y = 150),
labelled with its value; the gate node G at (220, 100), with no wire to S, labelled "G" below and to its left. The
gate, the controlled source and r_o sit inside a dashed `--ink-3` box from (196, 36) to (458, 160) labelled "transistor
model" just above its top-left corner, and the controlling voltage is marked "+" beside G, "−" beside S and "v_gs"
between them. Every node where three wires meet has a 2.6 px dot.
- cs: a sine source "v_in" (`--c1`) at x = 110 from G to ground; S wired down to ground at y = 210; R_D from D (wire
  right to x = 500) down to ground; the output terminal "v_out" (`--c2`) at (590, 50).
- cg: G wired straight down to ground; the sine source "v_in" at (370, 190) driving S through a wire from S down to
  y = 166 and right to x = 370, so no wire crosses another; R_in labelled under an arrow pointing at that wire; the sine source "v_in" at x = 110 driving S (wire from S left to x = 110); R_D from D
  down to ground at x = 500; "v_out" at (590, 50).
- cd: D wired up to a ground symbol at y = 22, labelled "V_DD → ground"; the sine source "v_in" at x = 110 from G to
  ground; R_S from S (wire right to x = 500) down to ground; "v_out" at (590, 150).
- Arrows in `--ink-2` with the values: "R_in →" pointing into the input node, labelled with R_in, and "← R_out"
  pointing into the output node, labelled with R_out.

**Readouts, in the aside,** in `.read`:
- The stage's name and its role: "voltage amplifier, inverting" (cs), "current buffer: low R_in, high R_out" (cg),
  "voltage buffer: high R_in, low R_out, gain just under 1" (cd).
- Bias: "V_IN = 0.80 V" in `--c1`; "V_OUT = 1.93 V" in `--c2`; "I_D = 107 µA"; "V_GS = 0.80 V, V_OV = 0.30 V,
  V_DS = 1.93 V"; the region, and in `--accent` when it is not saturation: "triode: the small-signal model does not
  apply" or "cut-off: no current". For cg, also "V_B = 1.2 V".
- Small signal: "g_m = 716 µS"; "r_o = 111 kΩ (1/(λI_D) = 93.2 kΩ)"; "A_v = −6.57" in `--c3`, large (`.big`), with the
  formula of the stage beside it; "slope of the curve = −6.57" in `--c3`; "R_in = ∞" and "R_out = 9.17 kΩ". Outside
  saturation the A_v, R_in and R_out lines read "not from this model outside saturation".
- Swing, in `--c4`: "room below = 1.44 V, room above = 1.07 V" from `room`.
- cs only: "intrinsic gain g_m·r_o = 79.5; |A_v| is 8.3 % of it".
- Every number has three significant figures and an SI prefix (µ, m, k).

**The comparison table, under the readouts,** headed "The three stages": columns Stage, A_v, R_in, R_out; rows
- common source: −g_m (r_o ∥ R_D); ∞; r_o ∥ R_D
- common gate: (1 + g_m r_o) R_D/(R_D + r_o) ≈ g_m R_D; (r_o + R_D)/(1 + g_m r_o) ≈ 1/g_m; r_o ∥ R_D
- common drain: g_m (r_o ∥ R_S)/(1 + g_m (r_o ∥ R_S)); ∞; 1/g_m ∥ r_o ∥ R_S

The current stage's row is in `--ink` and bold, the others in `--ink-2`.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| input voltage, bias and signal | V_IN, v_in, v̂ | `--c1` |
| output voltage, bias and signal | V_OUT, v_out | `--c2` |
| gain: the slope, the tangent, the controlled source | A_v, g_m | `--c3` |
| the limits of the swing | room below, room above | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| stage | three buttons, "common source", "common gate", "common drain (follower)" | the stage | cs, cg, cd | | cs | Tab and Enter |
| bias point | draggable handle on the curve (dragging anywhere in figure 1's plot moves it to the pointer's v_IN) | V_IN in V | 0 V to 3 V | 0.01 V | 0.80 V (cs), 0.30 V (cg), 1.50 V (cd) | ← → 0.01 V, Shift + ← → 0.1 V |
| R | slider, log, labelled R_D (cs, cg) or R_S (cd) | R in Ω, slider value log₁₀ R | 1 kΩ to 100 kΩ (3 to 5) | 0.05 decade | 10 kΩ (4) | arrows: one step |
| W/L | slider, log | W/L, slider value log₁₀(W/L) | 1 to 100 (0 to 2) | 0.05 decade | 10 (1) | arrows: one step |
| λ | slider | λ in 1/V | 0 to 0.2 | 0.01 | 0.1 | arrows: one step |
| amplitude | slider | v̂ in V | 0 V to 0.5 V | 0.005 V | 0.05 V | arrows: one step |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "R_D = 10.0 kΩ", "λ = 0.10 /V", "v̂ = 50.0 mV".
- Choosing a stage moves V_IN to that stage's start and R to 10 kΩ; W/L, λ and v̂ are kept.
- What moves when each control changes: everything is redrawn from `solveOut`, `bias`, `gm`, `ro`, `smallSignal`,
  `slope`, `satRange` and `room`.
- Reset: common source, V_IN = 0.80 V, R = 10 kΩ, W/L = 10, λ = 0.1 /V, v̂ = 0.05 V.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: the small-signal gain is the slope of the stage's own curve at the bias point; the
  three stages are one transistor with the input and output on different terminals; and the slope holds only on the
  saturated stretch, whose ends are the limits of the swing.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. `stage` is "cs", "cg" or "cd". `p` is
`{ k, VT, lam, VDD, R, VB }`: k in A/V², VT, VDD and VB in V, lam in 1/V, R in Ω. Voltages are in V, currents in A,
resistances in Ω; `"Infinity"` in a check case is an infinite value.

### `drainCurrent(k, VT, lam, VGS, VDS)`

- Returns: I_D in A: 0 if V_OV = VGS − VT ≤ 0 or VDS ≤ 0; (k/2)·V_OV²·(1 + lam·VDS) if VDS ≥ V_OV; otherwise
  k·(V_OV·VDS − VDS²/2)·(1 + lam·VDS).
- Approximation: the square law with channel-length modulation applied in both regions.

### `solveOut(stage, p, vin)`

- Returns: v_OUT in V for a DC input vin.
- Formula: with V_GS and V_DS written from v_OUT (cs: V_GS = vin, V_DS = v_OUT; cg: V_GS = VB − vin,
  V_DS = v_OUT − vin; cd: V_GS = vin − v_OUT, V_DS = VDD − v_OUT), the mismatch is (VDD − v_OUT)/R − I_D for cs and cg
  and I_D − v_OUT/R for cd. It falls as v_OUT rises. Bisect 100 times on v_OUT between lo and VDD (lo = vin for cg, 0
  otherwise), moving lo up when the mismatch is positive, and return the midpoint of the last interval.

### `bias(stage, p, vin)`

- Returns: `{ vout, ID, VGS, VDS, VOV, region }`, region "cut-off" (V_OV ≤ 0), "saturation" (V_DS ≥ V_OV) or "triode".

### `gm(k, VT, lam, VGS, VDS)`

- Returns: ∂I_D/∂V_GS in S: 0 in cut-off; k·V_OV·(1 + lam·VDS) in saturation; k·VDS·(1 + lam·VDS) in triode.

### `ro(lam, ID, VDS)`

- Returns: (1 + lam·VDS)/(lam·ID) in Ω, the exact slope of the saturated law; Infinity when lam·ID = 0.
- Approximation: the usual 1/(λI_D) drops the factor 1 + λV_DS; the tool shows it beside the exact value.

### `smallSignal(stage, gm, ro, R)`

- Returns: `{ Av, Rin, Rout }`, with ro or R possibly Infinity, and a ∥ b = ab/(a + b) (the other one when either is
  infinite):
  - cs: Av = −gm·(ro ∥ R), Rin = Infinity, Rout = ro ∥ R.
  - cg: Av = (1 + gm·ro)·R/(R + ro), Rin = (ro + R)/(1 + gm·ro), Rout = ro ∥ R; with ro infinite, Av = gm·R and
    Rin = 1/gm. Derived from KCL at the drain with the source driven by v_in and the gate grounded.
  - cd: with rr = ro ∥ R: Av = gm·rr/(1 + gm·rr) (1 when rr is infinite), Rin = Infinity, Rout = (1/gm) ∥ rr. Derived
    from KCL at the source with the drain grounded.
- Sign convention: Av is v_out/v_in; negative inverts.
- Approximation: the saturated small-signal model, with no body effect and an ideal input source (no source
  resistance).

### `slope(stage, p, vin)`

- Returns: (`solveOut`(vin + h) − `solveOut`(vin − h))/(2h) with h = 10⁻⁴ V: the slope of the curve itself.

### `satRange(stage, p)`

- Returns: `{ inLo, inHi, outLo, outHi }`: the stretch of v_IN over which the transistor is saturated, and the lowest
  and highest v_OUT on that stretch. Null if it is never saturated.
- Formula: classify `bias(…).region` at 601 evenly spaced v_IN from 0 to VDD; take the first and last saturated
  samples; refine each end by 60 bisections between that sample and its unsaturated neighbour (an end at 0 or VDD is
  kept); outLo and outHi are the smaller and larger of `solveOut` at the two ends.

### `room(stage, p, vin)`

- Returns: `{ down, up }` in V: `solveOut`(vin) − outLo and outHi − `solveOut`(vin). A negative value means the bias is
  already outside saturation on that side.

### `intrinsicGain(gm, ro)`

- Returns: gm·ro, a pure number: the gain of a common-source stage with R → ∞.

The tool calls these with p = { k: 200 µA/V² × W/L, VT: 0.5, lam: λ, VDD: 3, R, VB: 1.2 }, and `gm` and `ro` at the
`bias` it finds.

## Check cases

Computed by `plans/checks/single-stage-amplifiers.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "solveOut", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.8], "expect": 1.926605504587156, "tol": 1e-12, "units": "V", "tag": "typical", "note": "common source, W/L = 10 (k = 2 mA/V²), λ = 0.1 /V, R_D = 10 kΩ, V_DD = 3 V, v_IN = 0.8 V: the drain sits at 1.93 V"},
  {"fn": "bias", "args": ["cg", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.3], "expect": {"vout": 1.248275862068966, "ID": 0.00017517241379310337, "VGS": 0.8999999999999999, "VDS": 0.948275862068966, "VOV": 0.3999999999999999, "region": "saturation"}, "tol": 1e-12, "units": "V, A", "tag": "typical", "note": "common gate, gate at 1.2 V, source driven to 0.3 V: V_GS = 0.9 V, I_D = 175 µA, the drain at 1.25 V, saturated"},
  {"fn": "bias", "args": ["cd", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 1.5], "expect": {"vout": 0.7521823602060467, "ID": 7.521823602060468e-05, "VGS": 0.7478176397939533, "VDS": 2.2478176397939533, "VOV": 0.24781763979395333, "region": "saturation"}, "tol": 1e-12, "units": "V, A", "tag": "typical", "note": "source follower, R_S = 10 kΩ, gate at 1.5 V: the source sits at 0.752 V, one V_GS = 0.748 V below the gate, with 75.2 µA"},
  {"fn": "gm", "args": [0.002, 0.5, 0.1, 0.8, 1.926605504587156], "expect": 0.0007155963302752293, "tol": 1e-12, "units": "S", "tag": "typical", "note": "the common-source bias: g_m = k·V_OV·(1 + λV_DS) = 0.716 mS"},
  {"fn": "ro", "args": [0.1, 0.00010733944954128442, 1.926605504587156], "expect": 111111.1111111111, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "the common-source bias: r_o = (1 + λV_DS)/(λI_D) = 111 kΩ; the usual 1/(λI_D) gives 93.2 kΩ"},
  {"fn": "smallSignal", "args": ["cs", 0.0007155963302752293, 111111.1111111111, 10000], "expect": {"Av": -6.565103947479168, "Rin": "Infinity", "Rout": 9174.311926605504}, "tol": 1e-09, "units": "", "tag": "typical", "note": "common source: A_v = −g_m (r_o ∥ R_D) = −6.57, R_in infinite, R_out = r_o ∥ R_D = 9.17 kΩ"},
  {"fn": "slope", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.8], "expect": -6.565103846909448, "tol": 1e-07, "units": "", "tag": "typical", "note": "the slope of the large-signal curve at the same bias: −6.57, the small-signal gain"},
  {"fn": "smallSignal", "args": ["cg", 0.000875862068965517, 62500.00000000003, 10000], "expect": {"Av": 7.688466111771699, "Rin": 1300.649551500155, "Rout": 8620.689655172413}, "tol": 1e-09, "units": "", "tag": "sign", "note": "common gate at its bias (g_m = 0.876 mS, r_o = 62.5 kΩ): A_v = +7.69, no inversion; R_in = 1.30 kΩ, near 1/g_m = 1.14 kΩ; R_out = 8.62 kΩ"},
  {"fn": "slope", "args": ["cg", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.3], "expect": 7.688466020832063, "tol": 1e-07, "units": "", "tag": "sign", "note": "the slope of the common-gate curve: positive, +7.69. Raising the source lowers V_GS, so less current and a higher drain"},
  {"fn": "smallSignal", "args": ["cd", 0.0006070450520240971, 162830.42899914435, 10000], "expect": {"Av": 0.8511730499503954, "Rin": "Infinity", "Rout": 1402.1579569955995}, "tol": 1e-09, "units": "", "tag": "typical", "note": "source follower at its bias (g_m = 0.607 mS, r_o = 163 kΩ): A_v = 0.851, under 1; R_out = 1/g_m ∥ r_o ∥ R_S = 1.40 kΩ, near 1/g_m = 1.65 kΩ"},
  {"fn": "intrinsicGain", "args": [0.0007155963302752293, 111111.1111111111], "expect": 79.51070336391436, "tol": 1e-09, "units": "", "tag": "typical", "note": "common-source bias: g_m·r_o = 79.5, the ceiling on this transistor's gain at this bias, whatever R_D"},
  {"fn": "solveOut", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.4], "expect": 3.0, "tol": 1e-12, "units": "V", "tag": "limit-zero", "note": "common source with v_IN = 0.4 V, below V_T = 0.5 V: no current, the drain sits at V_DD = 3 V"},
  {"fn": "smallSignal", "args": ["cg", 0.001, "Infinity", 10000], "expect": {"Av": 10.0, "Rin": 1000.0, "Rout": 10000.0}, "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "common gate with r_o infinite, g_m = 1 mS, R_D = 10 kΩ: R_in = 1/g_m = 1 kΩ exactly, A_v = g_m·R_D = 10"},
  {"fn": "smallSignal", "args": ["cd", 0.001, "Infinity", "Infinity"], "expect": {"Av": 1.0, "Rin": "Infinity", "Rout": 1000.0}, "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "follower with r_o and R_S both infinite: A_v = 1 exactly and R_out = 1/g_m = 1 kΩ"},
  {"fn": "smallSignal", "args": ["cs", 0.001, 100000, "Infinity"], "expect": {"Av": -100.0, "Rin": "Infinity", "Rout": 100000.0}, "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "common source with R_D → ∞ (an ideal current-source load), g_m = 1 mS, r_o = 100 kΩ: the gain is the intrinsic gain, −100"},
  {"fn": "solveOut", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 1.1], "expect": 0.2892770587007364, "tol": 1e-12, "units": "V", "tag": "breaks", "note": "common source pushed 0.3 V above its 0.8 V bias: the tangent predicts 1.93 − 6.57·0.3 = −0.04 V, below ground; the curve says 0.289 V, in triode"},
  {"fn": "satRange", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}], "expect": {"inLo": 0.5, "inHi": 0.9892486763152886, "outLo": 0.48924867631528923, "outHi": 3.0}, "tol": 1e-09, "units": "V", "tag": "typical", "note": "common source: saturated for v_IN from 0.5 V to 0.989 V, where v_OUT = v_IN − V_T = 0.489 V; the output can sit anywhere from 0.489 V to 3 V"},
  {"fn": "satRange", "args": ["cd", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}], "expect": {"inLo": 0.5, "inHi": 3.0, "outLo": 1.1832913578315177e-30, "outHi": 2.0653902924432295}, "tol": 1e-09, "units": "V", "tag": "typical", "note": "follower: saturated over the whole input range above V_T, so its output runs from 0 V to 2.07 V at v_IN = 3 V"},
  {"fn": "satRange", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 100000, "VB": 1.2}], "expect": {"inLo": 0.5, "inHi": 0.6669297564687011, "outLo": 0.16692975646870178, "outHi": 3.0}, "tol": 1e-09, "units": "V", "tag": "other", "note": "common source with R_D = 100 kΩ: the saturated input window shrinks from 0.489 V wide to 0.167 V wide; the steeper curve crosses the same output range in a narrower input range"},
  {"fn": "room", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}, 0.8], "expect": {"down": 1.4373568282718667, "up": 1.073394495412844}, "tol": 1e-09, "units": "V", "tag": "typical", "note": "common source at v_IN = 0.8 V: the output can fall 1.44 V before triode and rise 1.07 V before it reaches V_DD, so a symmetric swing is at most 1.07 V"},
  {"fn": "room", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 20000, "VB": 1.2}, 0.8], "expect": {"down": 0.659760889107428, "up": 1.9830508474576276}, "tol": 1e-09, "units": "V", "tag": "typical", "note": "the same bias with R_D = 20 kΩ: the gain grows from −6.57 to −11.2, but the drain drops to 1.02 V and the room below shrinks from 1.44 V to 0.66 V"},
  {"fn": "room", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 40000, "VB": 1.2}, 0.8], "expect": {"down": -0.10013300396453068, "up": 2.8416545425002475}, "tol": 1e-09, "units": "V", "tag": "breaks", "note": "R_D = 40 kΩ at the same bias: the drain falls to 0.158 V, below the edge of saturation (the room below is negative): the transistor is in triode"},
  {"fn": "slope", "args": ["cs", {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 40000, "VB": 1.2}, 0.8], "expect": -1.0059958667529845, "tol": 1e-07, "units": "", "tag": "breaks", "note": "there the curve's slope is only −1.01: more R_D bought less gain, because the transistor left saturation"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Common source at its start. Double R_D. Does the gain double?
   Why: Nearly: it goes from −6.57 to −11.2, short of double because r_o is in parallel. But the drain drops from 1.93 V
   to 1.02 V, and the room below shrinks from 1.44 V to 0.66 V.
2. Now make R_D 40 kΩ. What happens to the gain?
   Why: It collapses to about −1. The same current would drop more than V_DD, so the drain falls into triode, where the
   transistor is no longer a current source. Gain from R_D only works while the stage stays saturated.
3. Switch to common gate. Which way does the output move when the input rises?
   Why: Up. Raising the source lowers V_GS, so less current flows and R_D drops less: the gain is positive, about +7.7.
4. In common gate, what does the input source see?
   Why: About 1/g_m, here 1.30 kΩ: the source moves the whole V_GS, so a small input voltage changes the current a lot.
   That low input resistance is why the stage is a current buffer.
5. Switch to the follower. Why is the gain below 1?
   Why: The output is the source, which has to stay one V_GS below the gate; for v_GS to change at all, the source must
   lag the gate a little. A_v = g_m R/(1 + g_m R), here 0.85.
6. Set λ = 0 in common source. What sets the ceiling on the gain now?
   Why: Nothing in the transistor: r_o is infinite and A_v = −g_m R_D. With λ back, the ceiling is the intrinsic gain
   g_m·r_o, reached only as R_D → ∞, where the swing is gone.

## Misconceptions

- "The common-source gain is −g_m·R_D, always." What the tool shows instead: the readout carries r_o ∥ R_D, and at
  R_D = 40 kΩ the curve's slope is −1.01 because the transistor is in triode.
- "A bigger R_D gives a bigger swing." What the tool shows instead: at a fixed bias the room below falls from 1.44 V to
  0.66 V when R_D doubles, and goes negative at 40 kΩ.
- "The minus sign means something is wrong." What the tool shows instead: the common-source curve falls from left to
  right, and the output wave in figure 2 is upside down against the input.
- "A follower's gain is 1." What the tool shows instead: the readout is 0.85 at R_S = 10 kΩ, and it nears 1 only as
  g_m·R_S grows.
- "The input resistance of a common-gate stage is infinite, like a gate." What the tool shows instead: the input is the
  source, and R_in reads about 1/g_m.

## Quiz hooks

- L2 looks like: writes A_v, R_in and R_out of each stage from the small-signal model with given g_m, r_o and R; finds
  the bias of a common-source stage and checks saturation.
- L3 looks like: explains each stage from the picture: which terminal is held still, why the common-gate input is
  1/g_m and the follower's output 1/g_m, why the follower's gain is below 1; reads the gain as the slope of the transfer
  curve; finds the limits of the swing from the edges of saturation; predicts what R, W/L and λ do to gain and swing.
- L4 looks like: picks a stage for a job (gain, buffering a voltage, buffering a current); trades gain against swing
  and headroom; knows the intrinsic gain g_m·r_o caps a single stage; knows the body effect lowers the follower's gain
  and a source resistance changes the common-gate gain.
- Missteps:
  - uses −g_m R_D without r_o, or outside saturation
  - takes the common-gate input resistance as infinite
  - takes the follower's gain as exactly 1, or its output resistance as R_S
  - forgets that V_DD is a small-signal ground, so a resistor to V_DD is a resistor to ground
  - thinks a bigger R_D always means a bigger swing
- Seeds, to be varied and never asked word for word:
  - predict: a common-source stage at a given bias; R_D is raised by half. What happens to the gain, the DC output and
    the room for the signal below it?
  - explain: why the source follower's gain is less than 1, and what would have to be true for it to reach 1.
  - limit: R_D made very large at a fixed bias current (an ideal current-source load): what does the gain approach, and
    what does that need from the supply?
  - transfer: a photodiode current must be turned into a voltage without loading the photodiode's capacitance; which
    stage goes first, and why?

## Where this shows up

- `common-source`: the inverting voltage amplifier, gain −g_m (r_o ∥ R_D).
- `common-gate`: the input at the source, R_in ≈ 1/g_m: a current buffer.
- `source-follower`: the output at the source, gain just under 1 and R_out ≈ 1/g_m: a voltage buffer.
- `output-swing`: the swing ends where the transistor leaves saturation, at cut-off or at the edge of triode.
- `intrinsic-gain`: g_m·r_o, the most one transistor gives.
- `small-signal-analysis`: each stage's A_v, R_in and R_out come from the same model at the bias point.
- `resistance-looking-in`: the 1/g_m into a source and r_o ∥ R_D into a drain are the rules this tool shows at work.
- Later: EE 140: cascodes and multistage amplifiers are these three stages stacked and chained.

## Page text

- Header `Concept:` One transistor, three ways to connect it: the small-signal gain of each stage is the slope of its
  own large-signal curve at the bias point, and it lasts only while the transistor stays saturated.
- Header `Course:` EE 105 (common source, common gate and common drain stages; output swing; intrinsic gain)
- Header `Play with:` The stage, the bias point on its transfer curve, R_D or R_S, W/L, λ and the signal amplitude
- Header `Should click:` Common source inverts and amplifies, common gate takes its input at 1/g_m, the follower gives
  just under 1 from a low output resistance; each gain is a slope, and the swing ends where saturation ends.
- Title: Common source, common gate and common drain
- Lede: Ground one terminal of a transistor for the signal, drive a second and take the output from the third. Common
  source amplifies and inverts, common gate takes in a current at a low resistance, and the source follower copies a
  voltage. Drag the bias point along each stage's curve: the gain is its slope, and it lasts only while the transistor
  stays saturated.
- Caption of `transfer`: Drag the dot (or press anywhere in the plot); focused, ← → move it 0.01 V, with Shift 0.1 V. The
  shaded stretches are cut-off and triode; the dashed lines are the limits of the swing.
- Caption of `wave`: The input signal, the output from the curve itself, and the dashed output the tangent predicts.
- Caption of `smallsig`: The stage as the signal sees it, with what the source and the load look into.
- What should click:
  - **The gain is a slope.** For a small signal the curve is as good as its tangent at the bias point, and the tangent's
    slope is A_v. The small-signal formulas compute that slope without drawing the curve.
  - **One transistor, three jobs.** Input on the gate and output at the drain: an inverting voltage amplifier. Input on
    the source: the source moves all of V_GS, so the input looks like 1/g_m, a current buffer. Output at the source: it
    follows the gate one V_GS lower, a voltage buffer with a gain just under 1.
  - **Swing ends where saturation ends.** The output can move only while the transistor stays saturated. Cut-off on one
    side and triode on the other bound the swing; more R_D steepens the curve but moves the bias toward triode.
  - **The ceiling is g_m·r_o.** With λ > 0, even an infinite R_D gives only the intrinsic gain g_m·r_o.

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
