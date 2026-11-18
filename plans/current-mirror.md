# Plan: Current mirror

```json plan
{
  "id": "current-mirror",
  "title": "Current mirror",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["current-mirror", "diode-connected-transistor", "current-source-load", "channel-length-modulation"],
  "prerequisites": ["square-law", "mosfet-regions", "mos-small-signal-model"],
  "size": "M",
  "tool": "circuits/amplifiers/current-mirror.html",
  "checks": "plans/checks/current-mirror.py"
}
```

## Concept

A diode-connected transistor turns a reference current into a gate voltage: it settles at whatever V_GS makes it carry
I_REF. A second transistor given the same V_GS copies the current, scaled by the ratio n of their W/L. It is a current
source: flat while it stays in saturation, with a small slope set by r_o (channel-length modulation), and collapsing once
its drain voltage falls below V_OV. The copy is exact only when the two drains sit at the same voltage. Used as the load
of a common-source stage in place of R_D, it gives a gain of about g_m·r_o/2 whatever the current.

## Picture

The page has a `.bench`: the left column holds figure 1, the controls, and figure 3; the right column (`aside`) holds the
readouts. Figure 2 sits under the bench at the left of a `.pair`, with the "copy" panel on its right.

The device, as in the other EE 105 tools: μ_nC_ox = 200 µA/V², V_T = 0.5 V, M1 with W/L = 10 (k₁ = 2 mA/V²), M2 with
W/L = n × 10, both with the same λ; the square law with (1 + λV_DS) in triode and saturation.

**Figure 1, `circuit`, viewBox 640 by 300.** The mirror, wires in `--ink`, 1.6 px. A rail "V_DD" at y = 30 from x = 80 to
x = 260. The reference current source (a circle with a downward arrow) from the rail down to M1's drain at x = 160,
labelled "I_REF = 100 µA" in `--c1`. M1 at x = 160 (drain at y = 120, source at y = 200, to ground at y = 230), its
gate wired to its own drain (the diode connection, a wire from the drain left and down to the gate, with a junction dot),
labelled "M1, W/L = 10". The gates joined by a wire at y = 160 running right to M2's gate at x = 420, labelled
"V_GS = 0.804 V" in `--c3`. M2 at x = 450, source to ground, labelled "M2, W/L = 10 × n" with n written; its drain wired up
to y = 70 and right to a voltage source V_out (a circle with "+" and "−") at x = 600 down to ground, labelled "V_out"
and "1.50 V" under it, left of the wire above the source, in `--ink`; an `--c2` arrow down into M2's drain labelled "I_out = 106 µA". When M2 is in triode, the
words "M2 in triode" in `--accent` beside it.

**Figure 2, `iout`, viewBox 480 by 320.** I_out against V_out. Plot area from x = 60 to x = 460 (V_out from 0 to 3 V, grid
every 0.25 V, labels every 0.5 V) and y = 20 to y = 270 (I_out from 0 to 1.3 × n·I_REF, five grid lines labelled with
SI prefixes). Drawn: the stretch V_out < V_OV shaded `--grid` and labelled "triode"; a dashed `--c4` vertical line at
V_OV labelled "V_OV, the lowest V_out"; a dashed (6 4) `--c1` horizontal line at n·I_REF labelled "n·I_REF, the ideal copy";
a dotted `--c3` vertical line at V_out = V_GS labelled "V_out = V_GS: exact"; the curve `mirror(…).Iout` against V_out in
`--c2`, 2.4 px, 200 points; the operating point, a 6 px `--c2` dot with a 16 px focusable ring handle. Axis names
"V_out (V)" and "I_out".

**The copy panel, beside figure 2,** in `.read`: "copy error = +6.44 %" in `--c2`, large (`.big`); "= λ(V_out − V_GS)/(1 + λV_GS)
in saturation"; "r_o = (1 + λV_out)/(λI_out) = 108 kΩ"; "lowest V_out = V_OV = 0.304 V" in `--c4`; and, for the
diode-connected M1, "its resistance to a small signal: 1/g_m ∥ r_o = 1.50 kΩ, not V_GS/I_REF = 8.04 kΩ".

**Figure 3, `load`, viewBox 640 by 240.** The mirror as a load. Left (x from 20 to 300): a common-source stage, wires in
`--ink`: the rail V_DD = 3 V at y = 30; the load from the rail to the output node at (160, 110), drawn as a resistor
labelled "R_D = 15 kΩ" in the resistor view or as a current source (a circle with a downward arrow) labelled "mirror,
r_o = 100 kΩ" in the mirror view; the amplifying transistor from the output node to ground at y = 210, its gate driven by
"v_in" from the left; the output "v_out" at the right of the output node. Right (x from 340 to 620): two horizontal bars
for |A_v|, one per load, scaled so that 60 fills 260 px, the chosen one in `--c2` and the other in `--ink-3`, each labelled
with its value: "R_D load: A_v = −13.0" and "mirror load: A_v = −50.0". Under them, in `--ink-2`, on two lines: "same current
I_out;" and "amplifier V_OV = 0.2 V, λ = 0.10 /V". The current is the mirror's I_out; R_D = (3 V/2)/I_out, so the
resistor-loaded output also sits at mid-supply.

**Readouts, in the aside,** in `.read`: "I_REF = 100 µA" in `--c1`; "V_GS = 0.804 V" in `--c3`; "V_OV = 0.304 V" in `--c4`;
"n = 1"; "I_out = 106 µA" in `--c2`, large (`.big`); "ideal n·I_REF = 100 µA"; "M2: saturation" or "M2: triode, below
V_OV" (`--accent`); "V_out = 1.50 V".

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| reference current | I_REF | `--c1` |
| output current | I_out | `--c2` |
| the shared gate voltage | V_GS | `--c3` |
| overdrive, the lowest output voltage | V_OV | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| I_REF | slider, log | I_REF in A, slider value log₁₀ I_REF | 10 µA to 1 mA (−5 to −3) | 0.05 decade | 100 µA (−4) | arrows: one step |
| n | four buttons, "1", "2", "3", "4" | (W/L)₂/(W/L)₁ | 1 to 4 | 1 | 1 | Tab and Enter |
| λ | slider | λ in 1/V | 0 to 0.2 | 0.01 | 0.1 | arrows: one step |
| V_out | the operating-point handle in figure 2, or a press anywhere in its plot | V_out in V | 0 V to 3 V | 0.01 V | 1.50 V | ← → 0.01 V, Shift + ← → 0.1 V |
| load | two buttons, "R_D load" and "mirror load" | the load drawn in figure 3 | | | mirror load | Tab and Enter |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "I_REF = 100 µA", "λ = 0.10 /V".
- What moves when each control changes: I_REF, n and λ redraw every figure and readout; V_out moves the operating point,
  figure 1's labels, the copy panel and figure 3's numbers; the load buttons change figure 3's drawing and which bar is
  coloured.
- Reset: I_REF = 100 µA, n = 1, λ = 0.1 /V, V_out = 1.5 V, mirror load.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: the copy is exact only when M2's drain sits where M1's does; any difference shows as an
  error of about λΔV, and below V_OV the copy collapses.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. k in A/V², VT in V, lam in 1/V, currents
in A, voltages in V, resistances in Ω.

### `drainCurrent(k, VT, lam, VGS, VDS)`

- Returns: 0 if V_OV ≤ 0 or VDS ≤ 0; (k/2)V_OV²(1 + lam·VDS) if VDS ≥ V_OV; else k(V_OV·VDS − VDS²/2)(1 + lam·VDS).
- Approximation: the square law with channel-length modulation in both regions.

### `vgsForCurrent(k, VT, lam, I)`

- Returns: the V_GS of a diode-connected transistor (V_DS = V_GS) carrying I: 200 bisections on [VT, VT + 10], moving the
  lower end up while `drainCurrent(k, VT, lam, v, v)` < I, and the midpoint of the last interval.

### `outputResistance(lam, I, VDS)`

- Returns: (1 + lam·VDS)/(lam·I), the exact slope of the saturated law; Infinity when lam·I = 0.
- Approximation: the course's 1/(λI) drops the factor 1 + λV_DS; the copy panel shows the exact one.

### `mirror(k1, VT, lam, Iref, n, Vout)`

- Returns: `{ VGS, VOV, Iout, region, error, ro }`: V_GS = `vgsForCurrent(k1, VT, lam, Iref)`, V_OV = V_GS − VT,
  I_out = `drainCurrent(n·k1, VT, lam, V_GS, Vout)`, region "saturation" if Vout ≥ V_OV else "triode",
  error = I_out/(n·Iref) − 1 (a fraction), ro = `outputResistance(lam, I_out, Vout)` in saturation and null in triode.
- Formula: in saturation the error is λ(V_out − V_GS)/(1 + λV_GS), zero at V_out = V_GS.
- Approximation: M1 and M2 identical apart from W, at the same temperature, with no mismatch in V_T.

### `diodeResistance(k1, VT, lam, Iref)`

- Returns: 1/(g_m + 1/r_o) for M1 at its own bias: g_m = k1·V_OV·(1 + lam·V_GS), r_o = `outputResistance(lam, Iref, V_GS)`.

### `loadGain(kind, I, VOVamp, lam, VDD)`

- Returns: the common-source gain −g_m(r_o ∥ load), with g_m = 2I/VOVamp and r_o = 1/(lam·I) (infinite when lam = 0);
  the load is (VDD/2)/I for kind "resistor" and 1/(lam·I) for kind "mirror". −Infinity when both are infinite.
- Approximation: the amplifier's and the mirror's r_o both written 1/(λI), as in the course; body effect ignored.

The tool calls these with k1 = 2×10⁻³, VT = 0.5, VOVamp = 0.2 and VDD = 3, and with I = the mirror's I_out in `loadGain`.

## Check cases

Computed by `plans/checks/current-mirror.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "vgsForCurrent", "args": [0.002, 0.5, 0, 0.0001], "expect": 0.816227766016838, "tol": 1e-12, "units": "V", "tag": "typical", "note": "k = 2 mA/V², V_T = 0.5 V, no λ, I_REF = 100 µA: the diode settles at V_GS = 0.5 + √(2I/k) = 0.816 V"},
  {"fn": "vgsForCurrent", "args": [0.002, 0.5, 0.1, 0.0001], "expect": 0.8042307268054738, "tol": 1e-12, "units": "V", "tag": "typical", "note": "the same with λ = 0.1 /V: 0.804 V, a little lower, because its own V_DS = V_GS adds a few percent of current"},
  {"fn": "vgsForCurrent", "args": [0.002, 0.5, 0.1, 1e-09], "expect": 0.5009758547267427, "tol": 1e-12, "units": "V", "tag": "limit-zero", "note": "1 nA: V_GS is barely above V_T, 0.501 V; the square law's tail, where real transistors are subthreshold"},
  {"fn": "mirror", "args": [0.002, 0.5, 0.1, 0.0001, 1, 1.5], "expect": {"VGS": 0.8042307268054738, "VOV": 0.3042307268054738, "Iout": 0.00010643978540247486, "region": "saturation", "error": 0.06439785402474851, "ro": 108042.30726805476}, "tol": 1e-12, "units": "V, A", "tag": "typical", "note": "a 1:1 mirror, I_REF = 100 µA, λ = 0.1 /V, V_out = 1.5 V: I_out = 106 µA, 6.4 % high, because M2's drain sits 0.7 V above M1's"},
  {"fn": "mirror", "args": [0.002, 0.5, 0.1, 0.0001, 1, 0.804], "expect": {"VGS": 0.8042307268054738, "VOV": 0.3042307268054738, "Iout": 9.999786447724682e-05, "region": "saturation", "error": -2.135522753177188e-05, "ro": 108042.30726805476}, "tol": 1e-12, "units": "V, A", "tag": "typical", "note": "V_out = 0.804 V, almost exactly V_GS: the copy is within 0.003 %"},
  {"fn": "mirror", "args": [0.002, 0.5, 0.1, 0.0001, 3, 1.5], "expect": {"VGS": 0.8042307268054738, "VOV": 0.3042307268054738, "Iout": 0.0003193193562074246, "region": "saturation", "error": 0.06439785402474851, "ro": 36014.10242268492}, "tol": 1e-12, "units": "V, A", "tag": "typical", "note": "M2 three times as wide: I_out = 319 µA, three times the copy, with the same 6.4 % error"},
  {"fn": "mirror", "args": [0.002, 0.5, 0, 0.0001, 1, 3], "expect": {"VGS": 0.816227766016838, "VOV": 0.316227766016838, "Iout": 0.00010000000000000005, "region": "saturation", "error": 4.440892098500626e-16, "ro": "Infinity"}, "tol": 1e-12, "units": "V, A", "tag": "limit-infinity", "note": "λ = 0: the copy is exact at any V_out above V_OV, here 3 V, and r_o is infinite"},
  {"fn": "mirror", "args": [0.002, 0.5, 0.1, 0.0001, 1, 0.15], "expect": {"VGS": 0.8042307268054738, "VOV": 0.3042307268054738, "Iout": 6.980075631226676e-05, "region": "triode", "error": -0.30199243687733235, "ro": null}, "tol": 1e-12, "units": "V, A", "tag": "breaks", "note": "V_out = 0.15 V, below V_OV = 0.304 V: M2 is in triode and gives 69.8 µA, 30 % short; the mirror has stopped being a current source"},
  {"fn": "outputResistance", "args": [0.1, 0.0001, 1.5], "expect": 114999.99999999999, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "λ = 0.1 /V at 100 µA and V_DS = 1.5 V: r_o = (1 + λV_DS)/(λI) = 115 kΩ; 1/(λI) alone gives 100 kΩ"},
  {"fn": "outputResistance", "args": [0, 0.0001, 1.5], "expect": "Infinity", "tol": 1e-09, "units": "Ω", "tag": "limit-infinity", "note": "λ = 0: an ideal current source, infinite output resistance"},
  {"fn": "diodeResistance", "args": [0.002, 0.5, 0.1, 0.0001], "expect": 1500.0342904135102, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "the diode-connected M1 at 100 µA: 1/g_m ∥ r_o = 1.50 kΩ, close to 1/g_m; a small resistance, not the 8 kΩ of V_GS/I_REF"},
  {"fn": "loadGain", "args": ["resistor", 0.0001, 0.2, 0.1, 3], "expect": -13.043478260869565, "tol": 1e-09, "units": "", "tag": "typical", "note": "a common-source stage at 100 µA with V_OV = 0.2 V and R_D = 15 kΩ (the drain at mid-supply on 3 V): A_v = −13.0"},
  {"fn": "loadGain", "args": ["mirror", 0.0001, 0.2, 0.1, 3], "expect": -49.999999999999986, "tol": 1e-09, "units": "", "tag": "typical", "note": "the same stage with a mirror load of r_o = 100 kΩ: A_v = −g_m(r_o ∥ r_o) = −1/(λV_OV) = −50"},
  {"fn": "loadGain", "args": ["mirror", 0.001, 0.2, 0.1, 3], "expect": -50.0, "tol": 1e-09, "units": "", "tag": "sign", "note": "ten times the current with the mirror load: still −50. g_m grows with I and r_o falls with it; the gain does not care"},
  {"fn": "loadGain", "args": ["mirror", 0.0001, 0.2, 0, 3], "expect": "-Infinity", "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "λ = 0 with a mirror load: the gain would be infinite; in a real circuit the next stage's input or the transistors' r_o set it"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. With λ = 0.1 /V and V_out = 1.5 V, is I_out exactly 100 µA?
   Why: No, 106 µA, 6.4 % high. M2's drain sits 0.7 V above M1's, and with channel-length modulation each extra volt adds
   about λ of current.
2. Where should V_out sit for an exact copy?
   Why: At V_GS, 0.804 V: then both transistors have the same V_GS and the same V_DS, so they carry the same current per
   unit W/L.
3. Drag V_out below 0.3 V. What happens?
   Why: M2 leaves saturation (V_out < V_OV = 0.304 V) and the current collapses toward zero: a mirror needs at least V_OV
   across its output.
4. Set n = 3. Does the error change?
   Why: No: the copy triples, but the percentage error depends only on λ and the drain-voltage difference.
5. In figure 3, switch between the loads, then change I_REF. Which gain moves?
   Why: Neither. With R_D chosen to put the output at mid-supply, g_mR_D = V_DD/V_OV whatever the current; with the
   mirror, g_m r_o/2 = 1/(λV_OV). The mirror's gain is about four times higher because r_o is far larger than the
   resistor the supply allows.

## Misconceptions

- "A mirror copies the current whatever the output voltage." What the tool shows instead: figure 2 slopes with λ and
  collapses below V_OV; the copy is exact only at V_out = V_GS.
- "The diode-connected transistor is a resistor of V_GS/I_REF." What the tool shows instead: to a small signal it is
  1/g_m ∥ r_o = 1.50 kΩ, against 8.04 kΩ for V_GS/I_REF.
- "To double the current, double L of M1." What the tool shows instead: the ratio is set by W/L, and n counts whole unit
  devices side by side.
- "A bigger load resistor always gives a bigger gain." What the tool shows instead: a resistor big enough to beat r_o
  would need a supply far above 3 V; the mirror gives the large resistance without the voltage drop.

## Quiz hooks

- L2 looks like: computes I_out = n·I_REF, V_GS from I_REF with the square law, and the gain of a stage with a current-
  source load −g_m(r_o ∥ r_o).
- L3 looks like: explains why the diode connection sets V_GS (the transistor carries whatever current it is fed, and its
  gate follows); explains the copy error as λ times the drain-voltage difference; finds the lowest output voltage V_OV;
  explains why a current-source load gives far more gain than a resistor on the same supply.
- L4 looks like: designs a mirror for a given ratio with unit devices; knows V_T mismatch and the body effect spoil the
  copy; raises the output resistance with a cascode and knows what it costs in headroom.
- Missteps:
  - copies the current at any output voltage, even below V_OV
  - scales the current by changing L instead of W
  - takes the diode-connected transistor's small-signal resistance as V_GS/I_REF
  - forgets that r_o, not R_D, limits the gain with a current-source load
- Seeds, to be varied and never asked word for word:
  - predict: a 1:2 mirror with λ = 0.05 /V has its output drain 1 V above its input drain: what does it deliver?
  - explain: why the diode-connected transistor always stays in saturation.
  - limit: λ made very small: what does the mirror become, and what limits the gain of a stage it loads?
  - transfer: a bias network must deliver 20 µA, 40 µA and 100 µA from one 20 µA reference: draw the mirror and give the
    device ratios.

## Where this shows up

- `current-mirror`: the copy, its error λΔV and its lowest output voltage V_OV.
- `diode-connected-transistor`: M1, always saturated, setting V_GS for whatever it carries; 1/g_m to a small signal.
- `current-source-load`: the mirror in place of R_D, gain −g_m(r_o ∥ r_o).
- `channel-length-modulation`: the slope of the flat part, 1/r_o, which sets both the copy error and the load's resistance.
- `square-law`: V_GS from I_REF, and why the copy scales with W/L.
- `common-source`: the stage the mirror loads, compared with its resistor load.
- Later: EE 140: biasing, cascode mirrors, and active loads in every op-amp.

## Page text

- Header `Concept:` A diode-connected transistor turns I_REF into V_GS; a second transistor at the same V_GS copies the
  current times its W/L ratio, exactly only when its drain sits where the first's does, and not at all below V_OV.
- Header `Course:` EE 105 (current mirrors, diode-connected transistors, current-source loads)
- Header `Play with:` I_REF, the width ratio n, λ, the output voltage, and a resistor or a mirror as a common-source load
- Header `Should click:` The copy is exact only when the two drains sit at the same voltage; any difference costs about
  λΔV, and below V_OV the mirror stops being a current source.
- Title: Current mirror
- Lede: Feed a current into a transistor whose gate is tied to its drain, and it settles at the one V_GS that carries that
  current. Hand that V_GS to a second transistor and it carries the same current, scaled by how much wider it is. Drag
  its drain voltage and see how well the copy holds.
- Caption of `circuit`: M1 sets V_GS for I_REF; M2 copies it. The output voltage is whatever the circuit hung on M2's drain
  imposes.
- Caption of `iout`: The output current against the output voltage. Drag the dot, or focus it and use ← →.
- Caption of `load`: The same current through a resistor or a mirror: the mirror's large r_o gives the larger gain.
- What should click:
  - **The diode connection sets V_GS.** With gate tied to drain, M1 is always saturated and settles at the V_GS that
    carries I_REF: V_GS = V_T + √(2I_REF/k).
  - **Same V_GS, same current per width.** M2 sees the same V_GS, so it carries n times the current if it is n times as
    wide, as long as it is saturated and its drain sits where M1's does.
  - **The copy costs λΔV.** Channel-length modulation tilts M2's curve: each volt between the two drains adds about λ of
    error. A cascode is the cure.
  - **Below V_OV it stops.** M2 needs V_out ≥ V_OV to stay saturated. Below that it is a resistor, and the current falls.
  - **A mirror is a big resistor without the drop.** As a load it offers r_o to a signal while dropping only a few tenths
    of a volt of DC, so a common-source stage gains g_m r_o/2 instead of g_mR_D.

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
