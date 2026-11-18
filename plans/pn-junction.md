# Plan: The pn junction: charge, field and potential

```json plan
{
  "id": "pn-junction",
  "title": "The pn junction: charge, field and potential",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["depletion-region", "pn-equilibrium", "depletion-width", "pn-reverse-bias", "depletion-capacitance", "built-in-potential", "diffusion-current", "einstein-relation"],
  "prerequisites": ["doping", "potential-vs-doping", "drift-current", "gauss-law", "poisson-equation"],
  "size": "L",
  "tool": "devices/pn-junction/pn-junction.html",
  "checks": "plans/checks/pn-junction.py"
}
```

## Concept

Join p-type and n-type silicon and holes diffuse into the n side while electrons diffuse into the p side, leaving bare
ions behind: negative acceptors on the p side, positive donors on the n side. Their field pushes carriers back, and
equilibrium comes when that drift cancels the diffusion exactly, which forces D/μ = kT/q. The ions are two boxes of
charge with equal area, N_A x_p = N_D x_n, so the depletion reaches deep into the lightly doped side. Integrate the
boxes once for a triangle of field and again for a potential step of φ_bi = (kT/q)·ln(N_A N_D/n_i²). Reverse bias
adds to the step; the boxes must widen as √(φ_bi − V_D), and since the charge sits at the edges of a widening gap the
junction is a capacitor C_j = ε_s/W that falls as the bias grows.

## Picture

The page has a `.bench`: the left column holds figure 1 and the controls under it; the right column (`aside`) holds the
readouts. Under the bench, a `.pair`: figure 2 on the left and figure 3 on the right, with the D_p/μ_p slider under
figure 3.

The device: an abrupt silicon junction, p side for x < 0 doped N_A, n side for x > 0 doped N_D, the junction at x = 0.
kT/q = 0.026 V, n_i = 10¹⁰ cm⁻³, ε_s = 11.7 ε₀ with ε₀ = 8.854×10⁻¹⁴ F/cm, q = 1.602×10⁻¹⁹ C. V_D is the voltage of the
p side minus the n side (positive is forward). Potentials are measured from the neutral p side. For the readouts in
farads the junction's area is A = 100 µm × 100 µm = 10⁻⁴ cm².

**The x axis, shared by figures 1 and 3.** It is fixed by the dopings, not by V_D, so the region visibly widens under
bias: with x_p, x_n and W taken at V_D = −5 V (the slider's end), it runs from −x_p − 0.25W to x_n + 0.25W, mapped onto
the plot's left and right edges. Ticks are at multiples of a step of 1, 2 or 5 × 10^k nm, the smallest such step that
gives at most 8 ticks; labels are in nm, or in µm when the step is 1000 nm or more. At the start the axis runs from
−98.7 nm to 336 nm with ticks every 50 nm.

**Figure 1, `junction`, viewBox 640 by 560.** Four stacked panels sharing the x axis, plotted from x = 70 to x = 610.
Through all of them: a dotted `--ink-3` vertical at x = 0 from y = 22 to y = 500, and dashed (3 3) `--c4` verticals, 1 px,
at −x_p and x_n from y = 80 to y = 500.
- The device strip, from y = 22 to y = 66. Above it, "p side, N_A = 1.00×10¹⁸ cm⁻³" at x = 70, y = 14, start-anchored,
  and "n side, N_D = 1.00×10¹⁷ cm⁻³" at x = 610, y = 14, end-anchored. The p side is a `--surface` rectangle with a
  `--line` border, the n side the same. The depletion region, from −x_p to x_n, is a rectangle filled `--c4` at opacity
  0.12. In it, "−" marks in `--c4` from −x_p to 0 and "+" marks in `--c4` from 0 to x_n, each in two rows at y = 38 and
  y = 52, one every 14 px starting 7 px in from the part's left edge; a part narrower than 14 px gets one mark at its
  centre. In the neutral p side, holes as `--c2` open circles of radius 3 (1.4 px stroke) on a grid every 22 px, rows at
  y = 36 and y = 54 with the second row offset 11 px, drawn only where x < −x_p − 4 px; in the neutral n side, electrons
  as `--c1` dots of radius 3 on the same grid, only where x > x_n + 4 px.
- The charge panel, from y = 90 to y = 210, zero line at y = 150 (`--line`). max(N_A, N_D) maps to 50 px. The p box
  from −x_p to 0 down to −N_A, the n box from 0 to x_n up to +N_D, each filled `--c4` at opacity 0.35 with a 1.4 px
  `--c4` outline; each box is at least 2 px tall, so a light side's box still shows. "−qN_A" in `--c4` under the p box,
  "+qN_D" in `--c4` over the n box, centred on each box (and 8 px to the outer side of a box narrower than 30 px). Panel name "ρ" at x = 62, y = 154, end-anchored.
- The field panel, from y = 230 to y = 350, zero line at y = 240. The field's scale is fixed by the dopings: |E_max| at
  V_D = −5 V maps to 100 px (to y = 340), and that value is the tick label at y = 340, x = 62, end-anchored, written
  "−4.07×10⁵". The field is drawn as the triangle from (−x_p, 0) to (0, E_max) to (x_n, 0), filled `--ink` at opacity
  0.10 with a 2.2 px `--ink` outline. "E_max = −1.59×10⁵ V/cm" in `--ink` 14 px under the apex, centred on x = 0. In
  the gap above the field panel, an `--ink-2` arrow pointing left from x = 604 to x = 566 at y = 228, with "E points
  from n to p" at x = 560, y = 232, end-anchored. Panel name "E (V/cm)" at
  x = 62, y = 244, end-anchored.
- The potential panel, from y = 370 to y = 490. The scale is fixed by the dopings: 0 V at y = 490 and φ_bi + 5 V at
  y = 380, with those two values as tick labels at x = 62, end-anchored. φ(x) in `--c3`, 2.4 px, from 300 points across
  the axis. When V_D ≠ 0 a dotted (2 3) `--c3` horizontal at φ_bi from x_n to the right edge, labelled "φ_bi = 0.898 V"
  2 px above its right end, end-anchored. "φ_bi − V_D = 0.898 V" in `--c3` 6 px above the right plateau at x = 604,
  end-anchored (it replaces the φ_bi label when V_D = 0). Panel name "φ (V)" at x = 62, y = 434, end-anchored.
- The x axis at y = 510 with the ticks and labels described above, and "x (nm), 0 at the junction" (or "x (µm), …")
  centred at y = 540.
- The breakdown note, shown only when |E_max| > 4×10⁵ V/cm: "|E_max| > 4×10⁵ V/cm: a real", "junction breaks down here
  by" and "avalanche; the model ignores it" on three lines in `--ink`, 12 px, end-anchored 8 px inside a `--surface`
  rectangle with a `--line` border, 234 by 50 px, from y = 158: under the charge panel's zero line, where only the p box
  can be. The rectangle starts at x = 374 when the junction is left of x = 340, and at x = 76 otherwise.

**Figure 2, `cj`, viewBox 480 by 300.** The capacitance against V_D. Plot area from x = 60 to x = 420 (V_D from −5 V to
+1.2 V, grid every 0.5 V, labels every 1 V) and y = 20 to y = 250.
- The left axis: C_j in nF/cm², from 0 to a top value of C_j at V_D = 0.4 V rounded up to 1, 2 or 5 × 10^k nF/cm²,
  with five grid lines and labels. C_j = ε_s/W in `--ink`, 2.2 px, from 300 points between −5 V and φ_bi − 0.02 V,
  clipped to the plot area.
- The right axis: 1/C_j² in (cm²/µF)², from 0 to 1.1 × its value at −5 V, five labels at x = 424, start-anchored.
  1/C_j² as a dashed (5 4) `--ink-2` line, 1.8 px, from −5 V up to φ_bi, where it meets zero: a straight line.
- A tick under the V_D axis at φ_bi, and the label "φ_bi" in `--c3` at 4 px to its right, 6 px above the axis.
- The region from V_D = 0.4 V to 1.2 V shaded `--grid`, with no label (the caption names it), because any label there
  crosses the C_j curve.
- "C_j" in `--ink` 8 px above the curve at −4.9 V, and "1/C_j²" in `--ink-2` 8 px above its line at −4.7 V.
- The cursor at V_D: a dashed `--ink-2` vertical, a 14 px triangle handle under the axis at y = 262, and a dot on each
  curve.
- Axis names "V_D (V)", "C_j (nF/cm²)" on the left and "1/C_j² (cm²/µF)²" on the right, each rotated.

**Figure 3, `balance`, viewBox 480 by 420.** The junction at equilibrium (V_D = 0) whatever the V_D slider says, titled
"at equilibrium, V_D = 0" at x = 60, y = 14. It uses figure 1's x axis mapped onto x = 60 to x = 460, with the
equilibrium depletion region from −x_p to x_n shaded `--c4` at opacity 0.08 in both panels.
- Top panel, from y = 30 to y = 190: the carrier densities on a log scale from 10⁰ to 10²⁰ cm⁻³, grid every 4 decades
  with labels. n(x) in `--c1` and p(x) in `--c2`, 2.2 px, 300 points, labelled "n" and "p" in their colours at x = 464,
  beside the right end of each curve (p moves 15 px under n when they are within 11 px). Panel title
  "carriers (cm⁻³)" at x = 456, y = 24, end-anchored, above the panel.
- Bottom panel, from y = 230 to y = 390: hole current density magnitudes on a log scale from 10⁰ to 10⁹ A/cm², grid
  every 3 decades with labels. |diffusion| as a `--c2` line 4 px wide at opacity 0.45; |drift| as a dashed (5 4) `--c2`
  line, 1.8 px, on top of it; |net| as an `--ink` line, 2 px, drawn only where it is at least 1 A/cm². Labels: "hole
  diffusion, toward n" (solid swatch) and "hole drift, toward p" (dashed swatch) in `--c2` at the panel's top left,
  "hole currents (A/cm²)" at its top right, and, at x = 452, y = 380, end-anchored, "net = 0" in `--ink` when the
  D_p/μ_p slider is at 26.0 mV, replaced by
  "net reaches 1.36×10⁵ A/cm²" otherwise, where the number is the largest |net| among the 300 plotted points
  (1.36×10⁵ A/cm² at 30 mV with the starting dopings). The x axis under it with figure 1's ticks.

**Readouts, in the aside,** in `.read`:
- "φ_bi = (kT/q)·ln(N_A N_D/n_i²) = 0.898 V" in `--c3`.
- "V_D = 0.00 V", then "φ_bi − V_D = 0.898 V across the depletion region" in `--c3`, large (`.big`).
- "x_p = 10.3 nm, x_n = 103 nm, W = 113 nm" in `--c4`, and "N_A x_p = N_D x_n: the light side holds 91 % of W".
- "|Q| = qN_A x_p = 165 nC/cm² on each side" in `--c4`.
- "E_max = −1.59×10⁵ V/cm, at the junction".
- "C_j = ε_s/W = 91.7 nF/cm², 9.17 pF for 100 µm × 100 µm".
- "μ_p = 143 cm²/(V·s); D_p = (D_p/μ_p)·μ_p = 3.72 cm²/s" under figure 3, beside its slider.
- Every number has three significant figures and an SI prefix; dopings and densities are written a.bc×10^k cm⁻³;
  fields are written a.bc×10^k V/cm.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| electrons | n | `--c1` |
| holes, and the hole currents | p, J_p | `--c2` |
| potential and the built-in step | φ, φ_bi, φ_bi − V_D | `--c3` |
| bare ions: the depletion charge, its depths and width | ρ, Q, x_p, x_n, W | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| acceptors | slider, log | N_A in cm⁻³, slider value log₁₀ N_A | 10¹⁴ to 10¹⁹ (14 to 19) | 0.1 decade | 10¹⁸ (18) | arrows: one step |
| donors | slider, log | N_D in cm⁻³, slider value log₁₀ N_D | 10¹⁴ to 10¹⁹ (14 to 19) | 0.1 decade | 10¹⁷ (17) | arrows: one step |
| bias | slider, and the triangle handle in figure 2 (drag it, or press anywhere in the plot) | V_D in V | −5 V to +0.4 V | 0.05 V | 0 V | slider arrows: 0.05 V; on the focused handle ← → 0.05 V, Shift + ← → 0.5 V |
| D_p/μ_p | slider, under figure 3 | the ratio in mV | 20 mV to 32 mV | 0.5 mV | 26.0 mV | arrows: one step |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "N_A = 1.00×10¹⁸ cm⁻³", "V_D = 0.00 V", "D_p/μ_p = 26.0 mV
  (kT/q)"; the "(kT/q)" is shown only at 26.0 mV.
- What moves when each control changes: N_A and N_D change everything, including the x axis and the fixed scales of
  figure 1. V_D redraws figure 1, the cursor in figure 2 and the readouts; figure 3 does not move with V_D. D_p/μ_p
  redraws only figure 3's bottom panel and its readout.
- Handle drags in figure 2 above +0.4 V stop at +0.4 V.
- Reset: N_A = 10¹⁸ cm⁻³, N_D = 10¹⁷ cm⁻³, V_D = 0 V, D_p/μ_p = 26.0 mV.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: the two boxes of bare ions must hold equal charge, so the depletion reaches into
  the light side; integrating them gives a triangle of field and a step of potential, and reverse bias makes the step
  bigger, which takes more charge, so the boxes widen as √(φ_bi − V_D) and the capacitance falls.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. NA and ND in cm⁻³; VD in V
(p side minus n side); x in cm from the junction, negative on the p side; fields in V/cm; charges in C/cm²;
capacitances in F/cm²; current densities in A/cm².

### `mobility(carrier, N)`

- Arguments: carrier "n" or "p"; N, the total doping in cm⁻³.
- Returns: μ in cm²/(V·s), the Caughey–Thomas fit with Arora's 300 K parameters, the same as the drift-and-mobility
  tool: μ_n = 88 + 1252/(1 + (N/1.26×10¹⁷)^0.88), μ_p = 54.3 + 407/(1 + (N/2.35×10¹⁷)^0.88).
- Approximation: a fit, good to about 10 %.

### `builtIn(NA, ND)`

- Returns: φ_bi in V.
- Formula: 0.026 × ln(NA·ND/n_i²), the n side's potential from intrinsic minus the p side's.
- Valid for: NA, ND ≫ n_i and below about 10¹⁹ cm⁻³ (Boltzmann statistics).

### `widths(NA, ND, VD)`

- Returns: `{ xp, xn, W }` in cm.
- Formula: with V = φ_bi − VD, W = √(2ε_s V (1/NA + 1/ND)/q), xp = W·ND/(NA + ND), xn = W·NA/(NA + ND). All three are
  0 when V ≤ 0.
- Approximation: the depletion approximation (sharp-edged boxes of ions, no carriers inside, no field outside); an
  abrupt junction; all of V_D across the depletion region (no current, so no drop in the neutral regions).

### `fieldAt(NA, ND, VD, x)` and `peakField(NA, ND, VD)`

- Returns: E in V/cm at x; peakField is fieldAt at x = 0.
- Formula: −q·NA·(x + xp)/ε_s for −xp < x ≤ 0; −q·ND·(xn − x)/ε_s for 0 < x < xn; 0 elsewhere. From Gauss's law,
  dE/dx = ρ/ε_s, with E = 0 at −xp.
- Sign convention: negative means pointing toward −x, from the n side to the p side.

### `potentialAt(NA, ND, VD, x)`

- Returns: φ in V, measured from the neutral p side.
- Formula: 0 for x ≤ −xp; q·NA·(x + xp)²/(2ε_s) for −xp < x ≤ 0; V − q·ND·(xn − x)²/(2ε_s) for 0 < x < xn; V for
  x ≥ xn, with V = max(φ_bi − VD, 0). φ = −∫E dx; the two parabolas meet at x = 0.

### `chargePerArea(NA, ND, VD)`

- Returns: |Q| = q·NA·xp in C/cm², the magnitude of the ion charge on each side.

### `junctionCap(NA, ND, VD)`

- Returns: C_j = ε_s/W in F/cm²; Infinity when W = 0.
- Formula: d|Q|/d(φ_bi − VD), which works out to ε_s/W: the charge that changes sits at the edges of the region, so it
  acts as a parallel-plate capacitor of spacing W. 1/C_j² = 2(φ_bi − VD)(1/NA + 1/ND)/(qε_s) is a straight line in VD
  that meets zero at VD = φ_bi.
- Approximation: the depletion approximation; it fails as VD approaches φ_bi, where the diffusion capacitance of the
  diode tool takes over.

### `carriersAt(NA, ND, x)`

- Returns: `{ n, p }` in cm⁻³ at equilibrium (VD = 0).
- Formula: p = NA·e^(−φ/(kT/q)), n = ND·e^(−(φ_bi − φ)/(kT/q)), with φ = potentialAt(NA, ND, 0, x). np = n_i² everywhere.
- Approximation: Boltzmann statistics in the depletion approximation's potential; it shows how empty the region
  really is, and where the sharp edges are wrong.

### `holeCurrents(NA, ND, x, ratio)`

- Arguments: ratio is D_p/μ_p in V.
- Returns: `{ drift, diffusion, net }` in A/cm² at equilibrium.
- Formula: μ_p = mobility("p", NA); p and E at x from carriersAt and fieldAt at VD = 0; drift = q·μ_p·p·E;
  diffusion = −q·D_p·dp/dx with D_p = ratio·μ_p and dp/dx = p·E/(kT/q), so diffusion = −q·ratio·μ_p·p·E/(kT/q);
  net = drift + diffusion, which is zero exactly when ratio = kT/q = 0.026 V.
- Sign convention: positive is toward +x (toward the n side). The drift is negative and the diffusion positive.
- Approximation: μ_p taken at N_A throughout; the balance holds whatever μ_p is, which is the point.

## Check cases

Computed by `plans/checks/pn-junction.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "builtIn", "args": [1e+18, 1e+17], "expect": 0.8980081862676778, "tol": 1e-09, "units": "V", "tag": "typical", "note": "N_A = 10¹⁸ and N_D = 10¹⁷ cm⁻³: φ_bi = (26 mV)·ln(10³⁵/10²⁰) = 0.898 V"},
  {"fn": "builtIn", "args": [1e+18, 1e+18], "expect": 0.9578753986855231, "tol": 1e-09, "units": "V", "tag": "typical", "note": "N_D raised tenfold to 10¹⁸ cm⁻³: φ_bi rises by one decade's 59.9 mV, to 0.958 V"},
  {"fn": "widths", "args": [1e+18, 1e+17, 0], "expect": {"xp": 1.0275198889181624e-06, "xn": 1.0275198889181622e-05, "W": 1.1302718778099785e-05}, "tol": 1e-09, "units": "cm", "tag": "typical", "note": "at equilibrium: x_p = 10.3 nm, x_n = 103 nm, W = 113 nm; ten times the doping, a tenth of the depth"},
  {"fn": "widths", "args": [1e+18, 1e+17, -3], "expect": {"xp": 2.1407771594285027e-06, "xn": 2.1407771594285027e-05, "W": 2.354854875371353e-05}, "tol": 1e-09, "units": "cm", "tag": "typical", "note": "3 V of reverse bias: the step grows from 0.898 V to 3.898 V, 4.34 times, so every width grows √4.34 = 2.08 times, to W = 235 nm"},
  {"fn": "widths", "args": [1e+18, 1e+17, 0.897], "expect": {"xp": 3.4428688387568306e-08, "xn": 3.4428688387568303e-07, "W": 3.7871557226325135e-07}, "tol": 1e-09, "units": "cm", "tag": "limit-zero", "note": "V_D = 0.897 V, 1 mV short of φ_bi: the depletion region has shrunk to 3.8 nm; the approximation has long since stopped meaning anything"},
  {"fn": "widths", "args": [1e+19, 1000000000000000.0, 0], "expect": {"xp": 1.0410779642816793e-08, "xn": 0.00010410779642816793, "W": 0.00010411820720781075}, "tol": 1e-09, "units": "cm", "tag": "limit-infinity", "note": "a one-sided junction, N_A = 10¹⁹ and N_D = 10¹⁵ cm⁻³: W = 1.04 µm, all but 0.1 nm of it on the lightly doped n side"},
  {"fn": "peakField", "args": [1e+18, 1e+17, 0], "expect": -158901.2703753479, "tol": 1e-09, "units": "V/cm", "tag": "sign", "note": "at equilibrium the field peaks at the junction at −1.59×10⁵ V/cm: negative, pointing from the n side to the p side"},
  {"fn": "peakField", "args": [1e+18, 1e+17, -20], "expect": -766548.554317289, "tol": 1e-09, "units": "V/cm", "tag": "breaks", "note": "20 V of reverse bias: the model gives −7.67×10⁵ V/cm, but silicon doped like this breaks down by avalanche near 4×10⁵ V/cm, and the model knows nothing of it"},
  {"fn": "fieldAt", "args": [1e+18, 1e+17, 0, 5e-06], "expect": -81578.54792048172, "tol": 1e-09, "units": "V/cm", "tag": "typical", "note": "50 nm into the n side, about halfway across it: the field has fallen linearly to −8.16×10⁴ V/cm"},
  {"fn": "potentialAt", "args": [1e+18, 1e+17, 0, 0], "expect": 0.08163710784251617, "tol": 1e-09, "units": "V", "tag": "typical", "note": "at the junction itself: only 0.0816 V of the 0.898 V step has happened; the lightly doped n side holds the rest, 91 %, in proportion to its depth"},
  {"fn": "chargePerArea", "args": [1e+18, 1e+17, 0], "expect": 1.6460868620468963e-07, "tol": 1e-09, "units": "C/cm²", "tag": "typical", "note": "at equilibrium each side holds |Q| = qN_A x_p = qN_D x_n = 165 nC/cm² of bare ions"},
  {"fn": "junctionCap", "args": [1e+18, 1e+17, 0], "expect": 9.165210781030851e-08, "tol": 1e-09, "units": "F/cm²", "tag": "typical", "note": "at equilibrium: C_j0 = ε_s/W = 91.7 nF/cm², 9.17 pF for a 100 µm × 100 µm junction"},
  {"fn": "junctionCap", "args": [1e+18, 1e+17, -3], "expect": 4.399073636487425e-08, "tol": 1e-09, "units": "F/cm²", "tag": "typical", "note": "3 V of reverse bias: the plates are 2.08 times further apart, so C_j falls to 44.0 nF/cm²"},
  {"fn": "carriersAt", "args": [1e+18, 1e+17, 0], "expect": {"n": 2310.1297000831682, "p": 4.328761281083058e+16}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "at the junction, in equilibrium: p = 4.33×10¹⁶ and n = 2.31×10³ cm⁻³; their product is still n_i²"},
  {"fn": "carriersAt", "args": [1e+18, 1e+17, 5.13e-06], "expect": {"n": 38090467249378.4, "p": 2625328.782272471}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "halfway into the n side's depletion: n = 3.81×10¹³ and p = 2.63×10⁶ cm⁻³, both far below the 10¹⁷ cm⁻³ of ions; the region really is nearly empty of carriers"},
  {"fn": "carriersAt", "args": [1e+18, 1e+17, -9.3e-07], "expect": {"n": 102.86864072686001, "p": 9.721135546597078e+17}, "tol": 1e-09, "units": "cm⁻³", "tag": "breaks", "note": "1 nm inside the p edge of the 'depleted' region: holes are still at 9.72×10¹⁷ cm⁻³, 97 % of N_A; the real edge is smeared over a few nm, not a sharp box"},
  {"fn": "mobility", "args": ["p", 1e+18], "expect": 143.23226205513964, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "typical", "note": "holes in p-type silicon at 10¹⁸ cm⁻³: μ_p = 143 cm²/(V·s), the drift tool's fit"},
  {"fn": "holeCurrents", "args": [1e+18, 1e+17, -3e-07, 0.026], "expect": {"drift": -534904.5058036719, "diffusion": 534904.5058036719, "net": 0.0}, "tol": 1e-09, "units": "A/cm²", "tag": "limit-zero", "note": "at equilibrium 3 nm into the p side's depletion, with D_p/μ_p = kT/q: hole diffusion of +5.35×10⁵ A/cm² toward n, drift of −5.35×10⁵ A/cm² back, net zero"},
  {"fn": "holeCurrents", "args": [1e+18, 1e+17, -3e-07, 0.03], "expect": {"drift": -534904.5058036719, "diffusion": 617197.5066965446, "net": 82293.00089287269}, "tol": 1e-09, "units": "A/cm²", "tag": "other", "note": "the same point with D_p/μ_p set to 30 mV instead of 26 mV: a net hole current of 8.23×10⁴ A/cm² would flow with nothing connected, so D/μ must equal kT/q"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. N_A is ten times N_D. Before looking, where does most of the depletion region lie?
   Why: On the n side, the lightly doped one: x_n = 103 nm against x_p = 10.3 nm. The two boxes must hold equal charge,
   so the side with a tenth of the ions per cm³ needs ten times the depth.
2. Where is the field strongest, and why there?
   Why: At the junction, x = 0. Coming in from the p side the field grows with every negative ion it passes, and from
   there on it shrinks with every positive ion, so it peaks where the two kinds of charge meet.
3. Apply 3 V of reverse bias. By how much does W grow, and what happens to C_j?
   Why: The step grows from 0.898 V to 3.898 V, 4.34 times, so W grows √4.34 = 2.08 times, to 235 nm, and C_j = ε_s/W
   falls by the same factor, to 44.0 nF/cm².
4. Raise N_D tenfold, to 10¹⁸ cm⁻³. How much does φ_bi rise?
   Why: By 59.9 mV, one decade: φ_bi is the n side's potential minus the p side's, and the n side's moved up one step on
   the doping ladder.
5. In figure 3 the hole diffusion current is 5×10⁵ A/cm², yet nothing flows. Now set D_p/μ_p to 30 mV. What would
   happen, and what does that tell you?
   Why: A net hole current of about 10⁵ A/cm² would flow in a junction with nothing connected, which is impossible in
   equilibrium. So D/μ must be exactly kT/q: the Einstein relation.

## Misconceptions

- "The depletion region is split evenly about the junction." What the tool shows instead: with N_A = 10 N_D, the n side
  holds 91 % of W; at N_A = 10¹⁹ and N_D = 10¹⁵ cm⁻³ the p side holds a tenth of a nanometre.
- "Equilibrium means no current is flowing anywhere inside." What the tool shows instead: figure 3's diffusion and
  drift are each 5×10⁵ A/cm², and only their sum is zero.
- "The built-in potential is a battery: connect a wire and current flows." What the tool shows instead: the balance in
  figure 3 is exact; the step is held up by the ions, and the contacts at the two ends add steps that cancel it.
- "Reverse bias doubles, so the width doubles." What the tool shows instead: W grows as √(φ_bi − V_D), so 3 V of reverse
  bias, 4.34 times the step, only doubles it.
- "C_j is a fixed capacitance." What the tool shows instead: figure 2's C_j falls as the reverse bias grows, and only
  1/C_j² is a straight line.

## Quiz hooks

- L2 looks like: computes φ_bi, x_n, x_p, W, E_max and C_j from given dopings and bias, with the units right.
- L3 looks like: sketches ρ, E and φ across a junction for unequal dopings and explains each from the one before it;
  says why the light side holds the width; explains equilibrium as drift cancelling diffusion for each carrier
  separately; predicts the √ growth of W and the fall of C_j with reverse bias; reads φ_bi and the light side's doping
  off a 1/C_j² plot.
- L4 looks like: knows where the depletion approximation fails (the smeared edges, forward bias near φ_bi, breakdown
  fields above about 4×10⁵ V/cm); derives the Einstein relation from the equilibrium balance; uses C_j as the source
  and drain junction capacitances of a MOSFET and the tuning element of a varactor.
- Missteps:
  - puts the wider depletion on the heavily doped side
  - uses φ_bi + V_D for reverse bias with V_D written as a positive reverse voltage, or the sign the other way round
  - makes W grow in proportion to the reverse voltage instead of its square root
  - draws the field peak at a depletion edge instead of at the junction
  - says no current flows inside a junction at equilibrium, instead of two currents cancelling
- Seeds, to be varied and never asked word for word:
  - predict: a one-sided junction's light side is doped four times more heavily; what happens to W and to C_j at the
    same bias?
  - explain: why the potential across a junction cannot be measured with a voltmeter.
  - limit: the reverse bias raised without bound; what grows, and what physical limit stops the model first?
  - transfer: 1/C_j² against V_D measured on an unknown diode is a line of known slope meeting zero at 0.8 V; find the
    light side's doping and say what the intercept means.

## Where this shows up

- `doping`: the dopings set both boxes of charge and both ends of the potential step.
- `potential-vs-doping`: φ_bi is the n side's potential from intrinsic minus the p side's.
- `mos-capacitor`: a MOS capacitor's body depletes exactly like the light side of a one-sided junction.
- `body-effect`: a MOSFET's body is a reverse-biased junction under its channel, and V_SB widens it.
- `mos-capacitances`: the drain and source of a MOSFET are pn junctions with a C_j of their own.
- `pn-forward-bias`: lowering the step lets diffusion win, which is where a diode's current comes from.
- Later: EE 130: graded junctions, breakdown and the exact solution of Poisson's equation.

## Page text

- Header `Concept:` Two boxes of bare ions with equal charge, a triangle of field and a step of potential
  φ_bi = (kT/q)·ln(N_A N_D/n_i²); reverse bias raises the step, so the boxes widen as √(φ_bi − V_D) and
  C_j = ε_s/W falls.
- Header `Course:` EE 105 (pn junction in equilibrium, depletion width, reverse bias, depletion capacitance, diffusion
  and the Einstein relation)
- Header `Play with:` The two dopings, the bias V_D, and D_p/μ_p
- Header `Should click:` The light side holds the width; ρ, E and φ are each the integral of the one before; reverse bias
  widens the region as a square root and lowers C_j; and equilibrium is two large currents cancelling, which needs
  D/μ = kT/q.
- Title: The pn junction: charge, field and potential
- Lede: Where p-type meets n-type silicon, carriers spread across and leave bare ions behind. Those ions make a field,
  and the field makes a step in potential that stops the spreading. Change the dopings and the bias and watch the
  charge, the field and the potential, each built from the one above it.
- Caption of `junction`: From the top: the device with its bare ions, the charge density, the field and the potential.
  The scales stay fixed while V_D changes, so you can see the region widen.
- Caption of `cj`: The junction capacitance against V_D, and 1/C_j², a straight line that meets zero at φ_bi. Drag the
  triangle or press anywhere in the plot; focused, ← → move it 0.05 V, with Shift 0.5 V. The shaded band is forward
  bias, which the diode tool covers.
- Caption of `balance`: At equilibrium. Top, the carriers on a log scale: the region is empty by many decades. Bottom,
  the two hole currents: huge, and equal and opposite while D_p/μ_p = kT/q.
- What should click:
  - **Equal charge, unequal depth.** The ions on the two sides must cancel, N_A x_p = N_D x_n, so the region reaches
    deep into the lightly doped side and barely into the heavy one.
  - **Charge, then field, then potential.** Gauss's law turns the boxes into a triangle of field that peaks at the
    junction, and integrating again gives a step of φ_bi − V_D, mostly on the light side.
  - **Reverse bias widens it as a square root.** A bigger step needs more charge, and the charge grows as the depth, but
    the step grows as the depth squared, so W ∝ √(φ_bi − V_D). The charge that moves sits at the edges, so the junction
    is a capacitor ε_s/W that shrinks as the bias grows.
  - **Equilibrium is a tug of war.** Holes diffuse toward the n side and the field drives them back, each at about
    10⁵ A/cm². They cancel only because D/μ = kT/q, and that is the Einstein relation.

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
