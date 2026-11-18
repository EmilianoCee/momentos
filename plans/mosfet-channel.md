# Plan: The MOSFET channel: triode, pinch-off and the square law

```json plan
{
  "id": "mosfet-channel",
  "title": "The MOSFET channel: triode, pinch-off and the square law",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["mosfet-regions", "triode-region", "pinch-off", "square-law"],
  "prerequisites": ["drift-current", "threshold-voltage", "accumulation-depletion-inversion", "mosfet-structure"],
  "size": "L",
  "tool": "devices/mos/mosfet-channel.html",
  "checks": "plans/checks/mosfet-channel.py"
}
```

## Concept

Above threshold the gate holds a sheet of electrons under the oxide, C_ox(V_GS − V_T − V(x)) per area, where V(x) is the
channel's voltage at a point x along it. The drain pulls those electrons along by drift. Every slice of the channel must
carry the same current, I_D = W·Q(x)·μ·E(x), so where the sheet is thin the field must be strong. Near the source the
channel is thick and the voltage changes slowly; toward the drain it thins and the voltage rises faster. With a small
V_DS the channel is a resistor set by the gate (triode). When V_DS reaches V_OV the sheet's thickness at the drain falls
to zero (pinch-off), and any extra drain voltage drops across a short gap at the drain end: the current stops growing at
(1/2)μC_ox(W/L)V_OV², the square law.

## Picture

The page has a `.bench`: the left column holds figure 1, the controls, and figure 2; the right column (`aside`) holds the
readouts. Under the bench, a `.pair`: figure 3 on the left and figure 4 on the right.

The device: a long-channel NMOS with μ_n = 400 cm²/(V·s) in the channel, C_ox = 5×10⁻⁷ F/cm² (about 7 nm of oxide), so
μ_nC_ox = 200 µA/V²; V_T = 0.5 V; L = 1 µm and W = (W/L)·1 µm; no channel-length modulation. The source and body are at
0 V. x runs from 0 at the source to 1 at the drain, as a fraction of L.

**Figure 1, `channel`, viewBox 640 by 300.** The cross-section. The p-type body from y = 120 to y = 290 across the whole
width, labelled "p-type body (0 V)" at its bottom left. The source, an n+ box from x = 20 to x = 120, y = 120 to y = 190,
labelled "source n+, 0 V"; the drain, an n+ box from x = 520 to x = 620, labelled "drain n+, V_DS = 0.20 V" (the value
in `--c3`). The oxide from x = 110 to x = 530, y = 100 to y = 120; the gate above it from y = 70 to y = 100, labelled
"gate, V_GS = 1.00 V" (the value in `--c3`). Under the oxide, from x = 120 to x = 520 (400 px for 1 µm), the channel:
a band whose top is at y = 120 and whose thickness at x is 60 px × Q(x)/(C_ox × 1.5 V), filled `--c1` at opacity 0.25
with a `--c1` outline, and electrons as `--c1` dots of radius 2 px scattered inside it, their number per 20 px of length
proportional to Q there (one dot per 50 nC/cm²). In saturation the band reaches zero thickness at the drain edge,
marked with a `--c4` dot labelled "pinch-off" (the label inside the oxide, left of the dot), and a dashed `--c1` arrow
from there into the drain, with "the gap: high field, V_DS − V_OV dropped here" under the drain at the right. A small arrow under the channel labelled "electrons drift →" in `--c1`. The probe:
a dashed `--ink-2` vertical line through the channel at the probe's x, with a 7 px focusable ring handle at the channel's
top edge.

**Figure 2, `along`, viewBox 640 by 220.** Along the channel. Plot area from x = 60 to x = 600 (x from 0 to 1 µm, grid every
0.1 µm, labelled every 0.2 µm) and y = 20 to y = 190. Left axis: voltage from 0 to V_top, with V_top = 1.15 × the larger
of V_DS, V_OV and 0.5 V, rounded up to a multiple of 0.25 V, four grid lines with labels, name "V(x) (V)" in `--c3`;
right axis: charge from 0 to C_ox·V_top on the same grid lines (so the two curves share one scale, Q = C_ox(V_OV − V)),
labels in nC/cm², name "Q(x) (nC/cm²)" in `--c1`. Drawn: V(x) from
`channelV` in `--c3`, 2.2 px, 200 points; in saturation a dotted `--c3` vertical step at x = 1 µm from V_OV up to V_DS,
labelled "the gap"; Q(x) from `channelCharge` in `--c1`, 2.2 px; the probe as a dashed `--ink-2` vertical line with a dot
on each curve, and a focusable triangle handle under the axis.

**Figure 3, `output`, viewBox 480 by 320.** I_D against V_DS. Plot area from x = 60 to x = 460 (V_DS from 0 to 2 V, grid
every 0.25 V, labelled every 0.5 V) and y = 20 to y = 270 (I_D from 0 to I_max, five grid lines labelled with SI prefixes;
I_max is 1.4 × the larger of `drainCurrent` at the current V_GS and at V_GS = 1 V, both at V_DS = 2 V). Drawn: thin
`--ink-3` curves for those of V_GS = 0.7, 0.9, 1.1, 1.3, 1.5, 1.7 and 1.9 V whose saturated current fits under I_max,
each labelled "V_GS = 0.9" just above its right end; the current V_GS's curve in `--c2`, 2.6 px; the
edge of saturation, I = (k/2)·V_DS², dashed (6 4) `--c4`, labelled "V_DS = V_OV" just right of where it reaches 80 % of I_max; "triode" and "saturation" in
`--ink-3` on either side; the deep-triode line I = k·V_OV·V_DS, dotted `--c2`, from 0 to V_DS = V_OV/2, explained by the label
"dotted: resistor 1/(kV_OV)" at the plot's top left; the operating point, a 6 px `--c2` dot with a 16 px focusable ring handle. Axis names "V_DS (V)"
and "I_D".

**Figure 4, `transfer`, viewBox 480 by 320.** I_D against V_GS at the current V_DS. Plot area as figure 3, V_GS from 0 to
2 V. Drawn: `drainCurrent` against V_GS at the current V_DS in `--c2`, 2.6 px; the square law (k/2)(V_GS − V_T)² dashed
(6 4) `--c4`, labelled "saturated: (k/2)V_OV²" just left of where it reaches 80 % of I_max; a dashed `--ink-2` vertical line at V_T labelled "V_T"; the operating
point, a 6 px `--c2` dot with a 16 px focusable ring handle. Axis names "V_GS (V)" and "I_D".

**Readouts, in the aside,** in `.read`:
- The region in bold: "triode", "saturation" or "cut-off", with its rule: "V_DS < V_OV" or "V_DS ≥ V_OV" or "V_GS < V_T".
- "V_OV = V_GS − V_T = 0.50 V" and "V_DS,sat = V_OV = 0.50 V" in `--c4`.
- "I_D = 160 µA" in `--c2`, large (`.big`), with the formula of the region: "k(V_OV·V_DS − V_DS²/2)" or "(k/2)V_OV²" or "0".
- "k = μ_nC_ox·W/L = 2.00 mA/V²"; "with V_DS ≪ V_OV the channel is a resistor 1/(kV_OV) = 1.00 kΩ".
- At the probe: "x = 0.50 µm"; "V(x) = 0.088 V" in `--c3`; "Q(x) = 206 nC/cm²" in `--c1`; "E(x) = 1.94 kV/cm";
  "v = μE = 7.76×10⁵ cm/s"; "W·Q·μ·E = 160 µA = I_D". When v exceeds 10⁷ cm/s, in `--accent`: "faster than velocity
  saturation allows: the long-channel model fails here". At the pinch-off point, "E = ∞ in this model".
- Every number has three significant figures and an SI prefix, except the drift speed, written a×10ⁿ cm/s.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| channel electrons and their charge | Q(x) | `--c1` |
| drain current | I_D | `--c2` |
| voltages: gate, drain and along the channel | V_GS, V_DS, V(x) | `--c3` |
| overdrive and the edge of saturation | V_OV, V_DS,sat | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| V_GS | slider, and the operating-point handle in figure 4 | V_GS in V | 0 V to 2 V | 0.01 V | 1.00 V | arrows: 0.01 V; on the handle Shift + ← → 0.1 V |
| V_DS | slider, and the operating-point handle in figure 3 | V_DS in V | 0 V to 2 V | 0.01 V | 0.20 V | arrows: 0.01 V; on the handle Shift + ← → 0.1 V |
| W/L | slider, log | W/L, slider value log₁₀(W/L) | 1 to 100 (0 to 2) | 0.05 decade | 10 (1) | arrows: one step |
| probe | handle in figure 1 and in figure 2 | x as a fraction of L | 0 to 1 | 0.01 | 0.5 | ← → 0.01, Shift + ← → 0.1 |
| sweep | button, "sweep V_DS from 0 to 2 V" | | | | | Enter |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "V_GS = 1.00 V", "V_DS = 0.20 V", "W/L = 10.0".
- What moves when each control changes: V_GS, V_DS and W/L redraw every figure and readout; the probe moves its lines,
  dots and the "at the probe" readouts.
- "sweep V_DS" raises V_DS from 0 V to 2 V over 4 s and leaves it at 2 V; under prefers-reduced-motion it sets V_DS to
  2 V at once.
- Reset: V_GS = 1.00 V, V_DS = 0.20 V, W/L = 10, probe at 0.5, any sweep stopped.
- Motion: only the sweep animates; nothing is redrawn when no control changes.
- The one thing that should click: the current is the same in every slice, so a thinner sheet needs a stronger field;
  as V_DS rises the sheet at the drain thins to nothing, and past that point the extra voltage has nowhere to go but a
  short gap, so the current stops growing.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. Voltages in V; k = μ_nC_ox·W/L in A/V²;
Cox in F/cm²; mu in cm²/(V·s); W and L in cm; x a fraction of L from 0 (source) to 1 (drain). With V_OV = VGS − VT,
V_e = min(VDS, V_OV) and F = V_OV·V_e − V_e²/2:

### `region(VGS, VDS, VT)`

- Returns: "cut-off" if V_OV ≤ 0, "triode" if VDS < V_OV, else "saturation".

### `drainCurrent(k, VT, VGS, VDS)`

- Returns: I_D in A: 0 in cut-off, otherwise k·F: k(V_OV·VDS − VDS²/2) in triode and (k/2)V_OV² in saturation.
- Approximation: long channel (no velocity saturation), no channel-length modulation, threshold the same all along the
  channel (no body effect from V(x)).

### `channelV(VGS, VT, VDS, x)`

- Returns: V(x) = V_OV − √(V_OV² − 2xF), in V; 0 in cut-off.
- Formula: I_D = W μ C_ox (V_OV − V) dV/d(xL) is the same at every x; integrate from the source.
- Approximation: the gradual channel: the field along the channel is much weaker than the field across the oxide.

### `channelCharge(Cox, VGS, VT, VDS, x)`

- Returns: |Q(x)| = Cox·√(V_OV² − 2xF) = Cox(V_OV − V(x)), in C/cm²; 0 in cut-off.

### `channelField(VGS, VT, VDS, L, x)`

- Returns: E(x) = F/(L·√(V_OV² − 2xF)), in V/cm; Infinity where the square root reaches 0 (the pinch-off point); 0 in
  cut-off or with F = 0.
- Approximation: breaks near pinch-off, where the speed μE would pass velocity saturation.

### `speedAt(mu, VGS, VT, VDS, L, x)`

- Returns: μ·E(x), in cm/s.

### `currentAt(mu, Cox, W, L, VGS, VT, VDS, x)`

- Returns: W·|Q(x)|·μ·E(x), in A: the drift current through the slice at x; NaN where E is infinite.
- It equals `drainCurrent(mu·Cox·W/L, …)` at every x short of the pinch-off point.

### `onResistance(k, VGS, VT)`

- Returns: 1/(k·V_OV) in Ω, the slope of the triode curve at V_DS = 0; Infinity in cut-off.

The tool calls these with mu = 400, Cox = 5×10⁻⁷, L = 10⁻⁴ cm, W = (W/L)·10⁻⁴ cm, k = mu·Cox·W/L and VT = 0.5.

## Check cases

Computed by `plans/checks/mosfet-channel.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "region", "args": [1.0, 0.2, 0.5], "expect": "triode", "tol": 1e-09, "units": "", "tag": "typical", "note": "V_GS = 1 V, V_T = 0.5 V, V_DS = 0.2 V: V_DS < V_OV = 0.5 V, triode"},
  {"fn": "region", "args": [1.0, 0.8, 0.5], "expect": "saturation", "tol": 1e-09, "units": "", "tag": "typical", "note": "the same with V_DS = 0.8 V: V_DS ≥ V_OV, saturation"},
  {"fn": "region", "args": [0.4, 1.0, 0.5], "expect": "cut-off", "tol": 1e-09, "units": "", "tag": "typical", "note": "V_GS = 0.4 V below V_T = 0.5 V: cut-off, whatever V_DS"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 1.0, 0.2], "expect": 0.00016, "tol": 1e-15, "units": "A", "tag": "typical", "note": "k = μ_nC_ox·W/L = 2 mA/V², V_OV = 0.5 V, V_DS = 0.2 V: I_D = k(V_OV·V_DS − V_DS²/2) = 160 µA"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 1.0, 0.8], "expect": 0.00025, "tol": 1e-15, "units": "A", "tag": "typical", "note": "V_DS = 0.8 V, past V_OV: I_D = (k/2)·V_OV² = 250 µA, the square law"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 1.5, 2.0], "expect": 0.001, "tol": 1e-15, "units": "A", "tag": "typical", "note": "double the overdrive to 1 V (saturated): I_D = 1 mA, four times as much"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 1.0, 0.001], "expect": 9.99e-07, "tol": 1e-15, "units": "A", "tag": "limit-zero", "note": "V_DS = 1 mV: I_D = 0.999 µA, almost exactly k·V_OV·V_DS: the channel is a resistor of 1/(k·V_OV) = 1 kΩ"},
  {"fn": "onResistance", "args": [0.002, 1.0, 0.5], "expect": 1000.0, "tol": 1e-09, "units": "Ω", "tag": "limit-zero", "note": "that resistance: 1/(2 mA/V² × 0.5 V) = 1 kΩ, set by the gate"},
  {"fn": "drainCurrent", "args": [0.002, 0.5, 1.0, 5.0], "expect": 0.00025, "tol": 1e-15, "units": "A", "tag": "limit-infinity", "note": "V_DS = 5 V, far past pinch-off: still 250 µA. Without channel-length modulation the current ignores the drain"},
  {"fn": "channelCharge", "args": [5e-07, 1.0, 0.5, 0.2, 0], "expect": 2.5e-07, "tol": 1e-15, "units": "C/cm²", "tag": "typical", "note": "at the source, the channel charge is C_ox·V_OV = 5×10⁻⁷ F/cm² × 0.5 V = 250 nC/cm²"},
  {"fn": "channelCharge", "args": [5e-07, 1.0, 0.5, 0.2, 1], "expect": 1.5e-07, "tol": 1e-15, "units": "C/cm²", "tag": "typical", "note": "at the drain, with V_DS = 0.2 V: C_ox(V_OV − V_DS) = 150 nC/cm²; the sheet is thinner where the gate-to-channel voltage is smaller"},
  {"fn": "channelV", "args": [1.0, 0.5, 0.2, 0.5], "expect": 0.08768943743823399, "tol": 1e-09, "units": "V", "tag": "typical", "note": "halfway along that channel the voltage is 0.088 V, less than half of 0.2 V: the field is weaker near the source, where the sheet is thick"},
  {"fn": "channelField", "args": [1.0, 0.5, 0.2, 0.0001, 0.5], "expect": 1940.285000290664, "tol": 1e-09, "units": "V/cm", "tag": "typical", "note": "the field halfway along a 1 µm channel at V_DS = 0.2 V: 1.94 kV/cm"},
  {"fn": "speedAt", "args": [400, 1.0, 0.5, 0.2, 0.0001, 0.5], "expect": 776114.0001162656, "tol": 1e-09, "units": "cm/s", "tag": "typical", "note": "the electrons there drift at μE = 400 cm²/V·s × 1.94 kV/cm = 7.76×10⁵ cm/s"},
  {"fn": "currentAt", "args": [400, 5e-07, 0.001, 0.0001, 1.0, 0.5, 0.2, 0.5], "expect": 0.00016, "tol": 1e-15, "units": "A", "tag": "other", "note": "drift in that slice: W·Q·μ·E = 10 µm × 206 nC/cm² × 400 cm²/V·s × 1.94 kV/cm = 160 µA, the drain current"},
  {"fn": "currentAt", "args": [400, 5e-07, 0.001, 0.0001, 1.0, 0.5, 0.2, 0.9], "expect": 0.00015999999999999996, "tol": 1e-15, "units": "A", "tag": "other", "note": "near the drain the sheet is thinner and the field stronger, and the product is again 160 µA"},
  {"fn": "channelCharge", "args": [5e-07, 1.0, 0.5, 0.8, 1], "expect": 0.0, "tol": 1e-15, "units": "C/cm²", "tag": "typical", "note": "in saturation the charge at the drain end is zero: the channel has pinched off"},
  {"fn": "channelField", "args": [1.0, 0.5, 0.8, 0.0001, 1], "expect": "Infinity", "tol": 1e-09, "units": "V/cm", "tag": "breaks", "note": "at the pinch-off point the model's field is infinite, and μE would pass any speed; real electrons stop near 10⁷ cm/s and cross a short high-field gap"},
  {"fn": "channelField", "args": [1.0, 0.5, 0.8, 0.0001, 0.99], "expect": 24999.999999999985, "tol": 1e-09, "units": "V/cm", "tag": "breaks", "note": "just 10 nm before it the field is already 25 kV/cm: μE = 10⁷ cm/s, at velocity saturation"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. With V_DS = 0.2 V, is the voltage halfway along the channel 0.1 V?
   Why: No, 0.088 V. The sheet is thicker near the source, so the field there can be weaker and still carry the same
   current; more of the voltage drops near the drain.
2. Press "sweep V_DS". What happens to the channel at the drain end as V_DS passes V_OV = 0.5 V?
   Why: Its thickness reaches zero: the gate-to-channel voltage there has fallen to V_T. Past that, the extra drain
   voltage drops across a short gap and the current stays at 250 µA.
3. Double V_OV from 0.5 V to 1 V with the transistor saturated. By how much does I_D grow?
   Why: Four times. Twice the overdrive gives twice the charge per area and, at pinch-off, twice the voltage to drift
   through: (k/2)V_OV².
4. With a tiny V_DS, what is the transistor?
   Why: A resistor, 1/(kV_OV) = 1 kΩ here, whose value the gate sets: more V_GS, more electrons, less resistance.
5. Move the probe toward the drain in saturation. What happens to the electrons' speed?
   Why: It climbs without limit in this model. Real electrons stop near 10⁷ cm/s, so the field the long-channel
   picture predicts near pinch-off is not what happens; the current is still set by the rest of the channel.

## Misconceptions

- "Pinch-off means the current stops." What the tool shows instead: in saturation I_D stays at (k/2)V_OV²; the electrons
  cross the pinched gap pushed by its strong field.
- "The channel is uniform, so the voltage rises linearly." What the tool shows instead: figure 2's V(x) bends upward
  toward the drain while Q(x) falls.
- "Saturation means the transistor is fully on, like a closed switch." What the tool shows instead: the resistor-like
  region is triode, at small V_DS; saturation is where the current no longer depends on V_DS.
- "The current grows with V_DS forever." What the tool shows instead: past V_DS = V_OV the output curves are flat.

## Quiz hooks

- L2 looks like: decides the region from V_GS, V_DS and V_T and computes I_D with the triode or saturation formula.
- L3 looks like: explains the triode current as drift of the channel charge C_ox(V_OV − V(x)); explains why the sheet thins
  toward the drain and why that makes the current bend over; explains pinch-off and why the saturated current is set by
  V_OV alone; says the deep-triode transistor is a gate-controlled resistor 1/(kV_OV).
- L4 looks like: knows the long-channel picture fails near pinch-off (velocity saturation) and that channel-length
  modulation tilts the saturated curves; knows the threshold varies along the channel through the body effect.
- Missteps:
  - uses the saturation formula in triode, or the triode formula past V_DS = V_OV
  - takes "saturation" to mean the transistor is fully on
  - thinks pinch-off stops the current
  - compares V_DS with V_GS instead of with V_GS − V_T
- Seeds, to be varied and never asked word for word:
  - predict: a transistor in triode with V_DS = V_OV/2; V_GS is raised by 0.2 V. Which region is it in now, and what
    happens to I_D?
  - explain: why the channel's charge is smallest at the drain end, and what that does to the field there.
  - limit: V_DS made much smaller than V_OV: what does the transistor become, and what sets its value?
  - transfer: a transistor is to be used as a voltage-controlled resistor in an attenuator: which region, and how big can
    the signal across it be before the resistance stops being constant?

## Where this shows up

- `triode-region`: the channel as a gate-controlled resistor that bends over as it thins toward the drain.
- `pinch-off`: the drain end of the channel reaching zero charge at V_DS = V_OV.
- `square-law`: I_D = (1/2)μC_ox(W/L)V_OV² once the channel is pinched off.
- `mosfet-regions`: cut-off, triode and saturation, split by V_GS = V_T and V_DS = V_OV.
- `drift-current`: each slice carries W·Q·μ·E, the same current from source to drain.
- `threshold-voltage`: the channel charge is C_ox(V_GS − V_T) at the source, from the MOS capacitor.
- `channel-length-modulation`: the gap at the drain grows with V_DS and shortens the channel, which tilts the flat curves.
- Later: EE 105's amplifiers: g_m and the regions come from these curves; EE 130 and EE 140: short-channel effects and
  velocity saturation.

## Page text

- Header `Concept:` The channel is a sheet of electrons C_ox(V_OV − V(x)) drifting from source to drain; every slice carries
  the same W·Q·μ·E, so the sheet thins toward the drain, pinches off at V_DS = V_OV, and the current settles at (k/2)V_OV².
- Header `Course:` EE 105 (MOSFET regions, triode, pinch-off, square law)
- Header `Play with:` V_GS, V_DS and W/L; a probe along the channel; a sweep of V_DS through pinch-off
- Header `Should click:` The current is the same in every slice, so a thinner sheet needs a stronger field; at V_DS = V_OV
  the sheet at the drain vanishes, the extra voltage drops across a short gap, and the current stops growing.
- Title: The MOSFET channel: triode, pinch-off and the square law
- Lede: Above threshold the gate holds a sheet of electrons under the oxide, and the drain pulls them along. Every slice of
  that sheet must pass the same current, so where it is thin the electrons must move faster. Raise the drain voltage and
  watch the sheet thin toward the drain until it pinches off, and the current stop growing.
- Caption of `channel`: The blue band is the electron sheet, drawn as thick as its charge. Drag the probe, or focus it and
  use ← →, to read the charge, field and speed at any point.
- Caption of `along`: The voltage along the channel and the charge of the sheet. Where the charge is low the voltage climbs
  fast.
- Caption of `output`: Output curves for several V_GS. Drag the dot to change V_DS; the dashed curve is the edge of
  saturation.
- Caption of `transfer`: The current against V_GS at this V_DS. Drag the dot to change V_GS.
- What should click:
  - **A sheet of charge, drifting.** The gate holds C_ox(V_GS − V_T − V(x)) of electrons per area. The drain's field drags
    them along: I_D = W·Q(x)·μ·E(x), the drift current of a very thin layer.
  - **Same current everywhere.** Charge cannot pile up, so every slice carries the same I_D. Near the source the sheet is
    thick and a weak field will do; toward the drain it thins and the field must grow.
  - **Pinch-off.** When V_DS = V_OV the gate-to-channel voltage at the drain falls to V_T and the sheet there vanishes.
    More drain voltage drops across a short high-field gap; the rest of the channel, and so the current, hardly change.
  - **Triode is a resistor, saturation is a current source.** With small V_DS, I_D ≈ kV_OV·V_DS: a resistor set by the
    gate. Past pinch-off, I_D = (k/2)V_OV², set by the gate alone. That flat current is what amplifiers and current
    mirrors use.

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
