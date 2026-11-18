# Plan: The diode: injection, diffusion and the exponential

```json plan
{
  "id": "diode-current",
  "title": "The diode: injection, diffusion and the exponential",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["diode-iv", "diode-small-signal", "pn-forward-bias", "minority-carrier-diffusion", "diffusion-capacitance", "recombination-and-lifetime"],
  "prerequisites": ["pn-equilibrium", "diffusion-current", "einstein-relation", "mass-action-law", "boltzmann-factor"],
  "size": "L",
  "tool": "devices/pn-junction/diode-current.html",
  "checks": "plans/checks/diode-current.py"
}
```

## Concept

Forward bias lowers the junction's barrier by V_D, so e^(V_D/(kT/q)) times as many majority carriers get over it and
arrive on the far side as minority carriers: the minority density at each depletion edge rises by that factor. With no
field in the neutral regions, those carriers can only diffuse toward the contacts, recombining on the way, and the
current is the diffusion at the edge, qD times the slope of the profile. The slope scales with the edge density, so
I = I_S(e^(V_D/(kT/q)) − 1): ten times the current for every 59.9 mV. I_S is set by n_i²/N, so the lightly doped side
supplies most of it, and by how far the carriers get, W in a short region and L = √(Dτ) in a long one. The tangent of
the exponential at the bias point is a resistance r_d = (kT/q)/I_D, and the minority charge waiting in the neutral
regions grows with the current, which looks like a capacitance C_d = dQ_s/dV_D.

## Picture

The page has a `.bench`: the left column holds figure 1 and the controls under it; the right column (`aside`) holds the
readouts. Under the bench, a `.pair`: figure 2 on the left and figure 3 on the right.

The diode: silicon, p side N_A = 10¹⁸ cm⁻³, n side N_D = 10¹⁷ cm⁻³ (the pn-junction tool's starting dopings), each
neutral region W long from its depletion edge to an ohmic contact, the same lifetime τ for both minority carriers, area
A = 100 µm × 100 µm = 10⁻⁴ cm². kT/q = 0.026 V, n_i = 10¹⁰ cm⁻³. D_n = (kT/q)·μ_n(N_A) = 6.82 cm²/s and
D_p = (kT/q)·μ_p(N_D) = 8.60 cm²/s, from the Einstein relation and the drift tool's mobility fit. V_D is the p side
minus the n side.

**Figure 1, `profiles`, viewBox 640 by 340.** The excess minority carriers in the two neutral regions.
- Regions: the p side's neutral region from x = 60 (its contact) to x = 290 (its depletion edge), the depletion region
  from x = 290 to x = 330 as a `--surface` rectangle labelled "depletion, not to scale" at x = 310, y = 37, 10 px,
  `--ink-3`, centred, and the n side's neutral region from x = 330 (its depletion edge) to x = 560 (its contact). Each
  neutral region is W long, mapped onto its 230 px. The contacts are `--ink-2` bars 4 px wide at x = 56 and x = 564
  from y = 40 to y = 260, each labelled "contact" at y = 276, centred. Region titles on two lines at y = 14 and
  y = 27, 11 px, centred: "p side, N_A = 10¹⁸ cm⁻³:" over "electrons are the minority" at x = 175, and "n side,
  N_D = 10¹⁷ cm⁻³:" over "holes are the minority" at x = 445.
- The vertical axis, linear, rescaled to the current V_D: when V_D ≥ 0, 0 at y = 260 and 1.1 × max(Δn(0), Δp(0)) at
  y = 40; when V_D < 0, 0 at y = 60 and −1.1 × max(|Δn(0)|, |Δp(0)|) at y = 260. The zero line in `--line`, the top or
  bottom value as a tick label at x = 64, start-anchored, at y = 52 (or y = 256 under reverse bias), and "0" at the
  zero line at x = 52, end-anchored. Axis name "excess minority density
  (cm⁻³)" rotated at x = 18.
- Δn(x) on the p side in `--c1`, 2.4 px, and Δp(x) on the n side in `--c2`, 2.4 px, each from 150 points between its
  depletion edge and its contact, x measured from the edge toward the contact. The area between each curve and the zero
  line is filled in its colour at opacity 0.15: the stored charge.
- The edge slopes: from each depletion edge a dashed (4 3) line in that carrier's colour, 1.4 px, with the curve's slope
  at the edge, drawn until it reaches the zero line or the contact. These are what set the current.
- The edge values: "Δp(0) = 7.20×10¹³ cm⁻³" in `--c2` at x = 336, 8 px above the curve's edge point, start-anchored;
  "Δn(0) = 7.20×10¹² cm⁻³" in `--c1` at x = 284, 8 px above its edge point, end-anchored.
- The diffusion lengths, only when L < W: a `--c2` tick 8 px tall on the zero line at L_p from the n edge, labelled
  "L_p" in `--c2` 26 px under the zero line (18 px above it under reverse bias); a `--c1` tick at L_n from the p edge,
  labelled "L_n" the same way.
- Under the zero line, "0" at each edge and "W = 1.00 µm" centred under each neutral region, in `--ink-2`, 10 px.
- At V_D = 0 (within 0.0025 V) both profiles are flat on zero and "V_D = 0: no excess" is written centred at x = 310,
  y = 150.
- The injection warning, shown only when `injectionRatio` exceeds 0.1: "The injected holes are more than a tenth of
  N_D: low-level injection" over "is failing, and the real current grows more slowly than this", two lines in `--ink`,
  12 px, centred at x = 320, on a `--surface` rectangle with a `--line` border from (70, 300), 500 by 34 px. With the starting W and τ it appears from
  V_D = 0.779 V.

**Figure 2, `iv`, viewBox 480 by 300.** The I–V curve, linear. Plot area from x = 60 to x = 460 (V_D from −0.3 V to
0.8 V, grid every 0.1 V, labels every 0.2 V) and y = 20 to y = 250 (I_D from −1 mA to 10 mA, grid every 1 mA, labels
every 2 mA). I_D in `--ink`, 2.2 px, from 400 points, clipped to the plot area. The tangent at the cursor in `--c3`,
1.8 px, from V_D − 0.1 V to V_D + 0.1 V and clipped, drawn only when I_D > 10 µA. The cursor at V_D: a dashed `--ink-2`
vertical with a 14 px triangle handle under the axis at y = 262 and a dot on the curve. Axis names "V_D (V)" and
"I_D (mA)".

**Figure 3, `log`, viewBox 480 by 300.** The same curve on a log scale. The same V_D axis; y from 10⁻¹⁶ A at y = 250 to
10⁻¹ A at y = 20, grid every decade, labels every 3 decades. |I_D| in `--ink`, 2.2 px, drawn first; its hole part
|I_p| = I_Sp·|e^(V_D/(kT/q)) − 1| in `--c2`, 1.4 px, and its electron part |I_n| in `--c1`, 1.4 px, drawn over it, each
from 400 points and clipped. "holes" in `--c2` at (64, 34) and "electrons" in `--c1` at (64, 48) name the two parts. A dotted `--ink-3` horizontal at I_S labelled "I_S" at x = 64, 4 px above it, start-anchored. A slope triangle
in `--ink-3` at the cursor, 59.9 mV across and one decade up, labelled "59.9 mV" under it and "×10" to its right, drawn
only when 0.1 V ≤ V_D ≤ 0.72 V. The same cursor and handle as figure 2; both handles set V_D. Axis names "V_D (V)" and
"|I_D| (A), log scale".

**Readouts, in the aside,** in `.read`:
- "W = 1.00 µm; L_n = √(D_nτ) = 26.1 µm, L_p = √(D_pτ) = 29.3 µm", then the regime from W/L_p: "short: W ≪ L, a straight
  line" when W/L_p < 0.2, "long: W ≫ L, an exponential decay" when W/L_p > 3, and "neither: both W and L matter"
  otherwise.
- "D_n = 6.82 cm²/s, D_p = 8.60 cm²/s".
- "I_S = 1.49 fA: holes 93 %, electrons 7 %", the shares from `saturationCurrent`'s Ip and In.
- "V_D = 0.650 V", then "I_D = 107 µA", large (`.big`).
- "Δp(0) = p_n0·(e^(V_D/(kT/q)) − 1) = 7.20×10¹³ cm⁻³" in `--c2`; "Δn(0) = n_p0·(e^(V_D/(kT/q)) − 1) = 7.20×10¹² cm⁻³" in
  `--c1`.
- "r_d = (kT/q)/(I_D + I_S) = 243 Ω" in `--c3`.
- "Q_s = 63.4 fC, C_d = dQ_s/dV_D = 2.44 pF, Q_s/I_D = 592 ps" in `--c4`.
- Every number has three significant figures and an SI prefix; densities are written a.bc×10^k cm⁻³.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| minority electrons on the p side, and their current | Δn, I_n, L_n | `--c1` |
| minority holes on the n side, and their current | Δp, I_p, L_p | `--c2` |
| the small-signal tangent | r_d, g_d | `--c3` |
| the stored minority charge and its capacitance | Q_s, C_d | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| bias | slider, and the triangle handles in figures 2 and 3 (drag either, or press anywhere in either plot) | V_D in V | −0.3 V to 0.8 V | 0.005 V | 0.65 V | slider arrows: 5 mV; on a focused handle ← → 5 mV, Shift + ← → 50 mV |
| width | slider, log | W in µm, slider value log₁₀(W/1 µm) | 1 µm to 100 µm (0 to 2) | 0.05 | 1 µm (0) | arrows: one step |
| lifetime | slider, log | τ in s, slider value log₁₀ τ | 1 ns to 10 µs (−9 to −5) | 0.1 | 1 µs (−6) | arrows: one step |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "V_D = 0.650 V", "W = 1.00 µm", "τ = 1.00 µs".
- What moves when each control changes: V_D redraws figure 1, the cursors and tangent in figures 2 and 3, and the
  readouts. W and τ change I_S, so they redraw every figure and readout.
- Reset: V_D = 0.65 V, W = 1 µm, τ = 1 µs.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: the barrier sets the minority density at the edges, e^(V_D/(kT/q)) times its
  equilibrium value, and the current is just diffusion down the slope from there, so the current is exponential in V_D;
  the slope's length scale, W or L, and the light side's n_i²/N set how big it is.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. NA and ND in cm⁻³; W, L and x in
cm; tau in s; A in cm²; VD in V; currents in A; charge in C; capacitance in F. kT/q = 0.026 V, n_i = 10¹⁰ cm⁻³,
q = 1.602×10⁻¹⁹ C.

### `mobility(carrier, N)` and `diffusivity(carrier, N)`

- Returns: μ in cm²/(V·s), the Caughey–Thomas fit with Arora's 300 K parameters (μ_n = 88 + 1252/(1 + (N/1.26×10¹⁷)^0.88),
  μ_p = 54.3 + 407/(1 + (N/2.35×10¹⁷)^0.88)); and D = 0.026 × μ in cm²/s, the Einstein relation.
- Use: D_n = diffusivity("n", NA), because the minority electrons move through the p side; D_p = diffusivity("p", ND).

### `diffusionLength(D, tau)`

- Returns: L = √(D·tau) in cm.

### `excessAt(N, VD, L, W, x)`

- Arguments: N, the doping of the side the minority carrier is in; x, the distance from that side's depletion edge.
- Returns: the excess minority density in cm⁻³; 0 for x < 0 or x ≥ W.
- Formula: d0 = (n_i²/N)·(e^(VD/0.026) − 1), computed with expm1; then
  d0·(e^(−x/L) − e^(−(2W − x)/L))/(1 − e^(−2W/L)), which is d0·sinh((W − x)/L)/sinh(W/L) written so that it cannot
  overflow. It solves D·d″ = d/τ with d(0) = d0 and d(W) = 0 at the contact.
- Sign convention: negative under reverse bias, a deficit below equilibrium.
- Approximation: low-level injection (d0 ≪ N); no recombination in the depletion region; an ideal ohmic contact.

### `saturationCurrent(NA, ND, W, tau, A)`

- Returns: `{ IS, In, Ip }` in A.
- Formula: In = q·A·n_i²·D_n·coth(W/L_n)/(NA·L_n), Ip = q·A·n_i²·D_p·coth(W/L_p)/(ND·L_p), IS = In + Ip, with
  L_n = diffusionLength(D_n, tau) and L_p = diffusionLength(D_p, tau). Short (W ≪ L): coth(W/L)/L → 1/W. Long
  (W ≫ L): coth → 1, and W drops out.

### `diodeCurrent(IS, VD)`

- Returns: I_D = IS·(e^(VD/0.026) − 1) in A, computed with expm1.
- Sign convention: positive from the p side to the n side.

### `conductance(IS, VD)`

- Returns: `{ gd, rd }`: g_d = dI_D/dV_D = IS·e^(VD/0.026)/0.026 in S, which is (I_D + IS)/(kT/q), and r_d = 1/g_d
  in Ω.
- Approximation: the tangent holds for signals much smaller than kT/q = 26 mV.

### `storedCharge(NA, ND, W, tau, A, VD)`

- Returns: Q_s in C, the excess minority charge in both neutral regions.
- Formula: q·A·n_i²·(e^(VD/0.026) − 1)·(L_n·tanh(W/(2L_n))/NA + L_p·tanh(W/(2L_p))/ND), the integral of each profile.

### `diffusionCap(NA, ND, W, tau, A, VD)`

- Returns: C_d = dQ_s/dV_D in F: q·A·n_i²·e^(VD/0.026)/0.026·(L_n·tanh(W/(2L_n))/NA + L_p·tanh(W/(2L_p))/ND).

### `transitTime(NA, ND, W, tau, A, VD)`

- Returns: Q_s/I_D in s, using saturationCurrent and diodeCurrent. Short diode: about W²/(2D); long diode: about τ.
- Valid for: VD ≠ 0 (at VD = 0 both are zero); the page shows it only for V_D ≥ 0.1 V.

### `injectionRatio(NA, ND, VD)`

- Returns: the larger of d0/N on the two sides, a pure number. Low-level injection needs it well under 0.1.

## Check cases

Computed by `plans/checks/diode-current.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "diffusivity", "args": ["p", 1e+17], "expect": 8.60321501882698, "tol": 1e-09, "units": "cm²/s", "tag": "typical", "note": "holes crossing n-type silicon at 10¹⁷ cm⁻³: D_p = (kT/q)·μ_p = 26 mV × 331 = 8.60 cm²/s"},
  {"fn": "diffusivity", "args": ["n", 1e+18], "expect": 6.815549305046079, "tol": 1e-09, "units": "cm²/s", "tag": "typical", "note": "electrons crossing p-type silicon at 10¹⁸ cm⁻³: D_n = 26 mV × 262 = 6.81 cm²/s"},
  {"fn": "diffusionLength", "args": [8.6, 1e-06], "expect": 0.002932575659723036, "tol": 1e-09, "units": "cm", "tag": "typical", "note": "D = 8.6 cm²/s and τ = 1 µs: L = √(Dτ) = 29.3 µm, how far a hole gets before it recombines"},
  {"fn": "excessAt", "args": [1e+17, 0.6, 0.00293, 0.0001, 5e-05], "expect": 5261228012197.281, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "n side at 10¹⁷ cm⁻³, V_D = 0.6 V, L = 29.3 µm, W = 1 µm, halfway to the contact: 5.26×10¹² cm⁻³, about half the edge's 1.05×10¹³; a short region gives a straight line"},
  {"fn": "excessAt", "args": [1e+17, 0.6, 9.3e-05, 0.01, 9.3e-05], "expect": 3871558889977.646, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "the same edge with L = 0.93 µm and W = 100 µm, one diffusion length in: 3.87×10¹² cm⁻³, the edge value over e"},
  {"fn": "excessAt", "args": [1e+17, -0.3, 0.00293, 0.0001, 0], "expect": -999.9902521278564, "tol": 1e-09, "units": "cm⁻³", "tag": "sign", "note": "reverse bias, V_D = −0.3 V, at the edge: −1.00×10³ cm⁻³, a deficit; the edge is emptied of its few minority holes, p_n0 = n_i²/N_D"},
  {"fn": "saturationCurrent", "args": [1e+18, 1e+17, 0.0001, 1e-06, 0.0001], "expect": {"IS": 1.4880074992850007e-15, "In": 1.0923849464421788e-16, "Ip": 1.3787690046407828e-15}, "tol": 1e-09, "units": "A", "tag": "typical", "note": "N_A = 10¹⁸, N_D = 10¹⁷ cm⁻³, W = 1 µm, τ = 1 µs, A = 100 µm × 100 µm: I_S = 1.49×10⁻¹⁵ A, 93 % of it holes injected into the lightly doped n side"},
  {"fn": "saturationCurrent", "args": [1e+18, 1e+17, 0.01, 1e-09, 0.0001], "expect": {"IS": 1.6181666082105367e-15, "In": 1.322552569793257e-16, "Ip": 1.485911351231211e-15}, "tol": 1e-09, "units": "A", "tag": "limit-infinity", "note": "W = 100 µm with τ = 1 ns (L_p = 0.93 µm): a long diode; I_S = 1.62×10⁻¹⁵ A, set by L instead of W, and making W longer still changes nothing"},
  {"fn": "diodeCurrent", "args": [1.4880074992850007e-15, 0.65], "expect": 0.00010714383019780413, "tol": 1e-09, "units": "A", "tag": "typical", "note": "I_S = 1.49 fA at V_D = 0.65 V: I_D = 107 µA"},
  {"fn": "diodeCurrent", "args": [1.4880074992850007e-15, 0.7099], "expect": 0.0010727903031882433, "tol": 1e-09, "units": "A", "tag": "typical", "note": "59.9 mV more, V_D = 0.7099 V: I_D = 1.07 mA, ten times as much"},
  {"fn": "diodeCurrent", "args": [1.4880074992850007e-15, 0], "expect": 0.0, "tol": 1e-09, "units": "A", "tag": "limit-zero", "note": "V_D = 0: no current; diffusion over the barrier and drift down it cancel"},
  {"fn": "diodeCurrent", "args": [1.4880074992850007e-15, -0.3], "expect": -1.487992994378149e-15, "tol": 1e-09, "units": "A", "tag": "sign", "note": "V_D = −0.3 V: I_D = −1.49×10⁻¹⁵ A, essentially −I_S; more reverse voltage changes nothing"},
  {"fn": "conductance", "args": [1.4880074992850007e-15, 0.7099], "expect": {"gd": 0.041261165507297366, "rd": 24.23586410381796}, "tol": 1e-09, "units": "S, Ω", "tag": "typical", "note": "at 1.07 mA: g_d = I_D/(kT/q) = 41.3 mS, so r_d = 24.2 Ω; the tangent to the exponential"},
  {"fn": "storedCharge", "args": [1e+18, 1e+17, 0.0001, 1e-06, 0.0001, 0.7099], "expect": 6.351727435913991e-13, "tol": 1e-09, "units": "C", "tag": "typical", "note": "at 1.07 mA with W = 1 µm: Q_s = 6.35×10⁻¹³ C of minority carriers waiting in the neutral regions"},
  {"fn": "diffusionCap", "args": [1e+18, 1e+17, 0.0001, 1e-06, 0.0001, 0.7099], "expect": 2.442972090739539e-11, "tol": 1e-09, "units": "F", "tag": "typical", "note": "at 1.07 mA: C_d = dQ_s/dV_D = 24.4 pF, and it grows in proportion to the current"},
  {"fn": "transitTime", "args": [1e+18, 1e+17, 0.0001, 1e-06, 0.0001, 0.7099], "expect": 5.920753960058351e-10, "tol": 1e-09, "units": "s", "tag": "typical", "note": "Q_s/I_D = 592 ps: about W²/(2D_p) = 581 ps, the time a hole takes to diffuse across 1 µm"},
  {"fn": "injectionRatio", "args": [1e+18, 1e+17, 0.65], "expect": 0.0007200489933638613, "tol": 1e-09, "units": "", "tag": "typical", "note": "V_D = 0.65 V: the hole excess at the edge is 7.2×10¹³ cm⁻³ against N_D = 10¹⁷ cm⁻³, 0.072 %; low-level injection holds"},
  {"fn": "injectionRatio", "args": [1e+18, 1e+17, 0.85], "expect": 1.5779339904331686, "tol": 1e-09, "units": "", "tag": "breaks", "note": "V_D = 0.85 V: the injected holes, 1.58×10¹⁷ cm⁻³, outnumber the donors; the edge law and I_S·e^(V_D/(kT/q)) both fail, and the real current grows more slowly"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Raise V_D from 0.65 V by 60 mV. By what factor does the current grow, and what happens to the profiles' shape?
   Why: About ten times, because e^(0.0599/0.026) = 10. The edge densities rise tenfold and the profiles scale with
   them; their shape does not change, so neither does anything except the size.
2. The p side is doped ten times more heavily than the n side. Which carrier carries most of the current?
   Why: Holes injected into the n side, 93 %. The minority density on each side is n_i²/N, so the lightly doped side
   starts with ten times more minority carriers and receives ten times more.
3. With W = 1 µm, lower τ from 1 µs to 1 ns. Does the current change much? Now set W = 100 µm and do the same.
   Why: At 1 µm, by only about a third, and only near the end: L is many times W until τ nears 1 ns, so the profile
   stays a straight line and W sets the slope. At 100 µm the diode is long and the carriers die within L, so a
   thousandfold shorter lifetime makes L √1000 times shorter, the slope that much steeper, and the current 32 times
   larger.
4. Reverse the bias to −0.3 V. Why does the current not grow with more reverse voltage?
   Why: The edges are already emptied to almost zero minority carriers. The current is the few that diffuse to the
   edge and are swept across, and emptying an empty edge further changes nothing: I_D ≈ −I_S.
5. At 0.65 V the diode carries 107 µA. What is its small-signal resistance, and what happens to it at ten times the
   current?
   Why: r_d = 26 mV/107 µA = 243 Ω. At ten times the current the exponential is ten times steeper, so r_d falls to a
   tenth, 24.2 Ω.

## Misconceptions

- "A diode turns on at 0.7 V and conducts nothing below it." What the tool shows instead: figure 3 is a straight line
  through every voltage; at 0.5 V the diode already carries 0.335 µA, and each 60 mV multiplies it by ten.
- "The current in the neutral regions is drift, pushed by the applied voltage." What the tool shows instead: the
  neutral regions have no field in this model; the current is the slope of the minority profile times qD.
- "Both sides contribute equally to the current." What the tool shows instead: the lightly doped n side supplies 93 %
  through its hole profile.
- "Reverse current grows with reverse voltage, like a resistor." What the tool shows instead: from −0.1 V down, figure
  3 is flat at I_S.
- "A diode's small-signal resistance is V_D/I_D." What the tool shows instead: at 107 µA, V_D/I_D is 6.07 kΩ, while the
  tangent's r_d is 243 Ω.

## Quiz hooks

- L2 looks like: uses I = I_S(e^(V_D/(kT/q)) − 1) to find a current or a voltage; computes I_S for a short diode with W in
  place of L; computes r_d = (kT/q)/I_D and C_d from a transit time.
- L3 looks like: explains why lowering the barrier multiplies the edge minority density by e^(V_D/(kT/q)); sketches the
  minority profiles for short and long regions and says which sets the current; explains why the lightly doped side
  dominates I_S and why reverse current saturates; reads 60 mV per decade off a log plot; explains why r_d and C_d
  depend on the bias current.
- L4 looks like: knows where the exponential fails (high-level injection, series resistance, recombination in the
  depletion region at low current, breakdown in reverse) and recognises the same edge law in a MOSFET below threshold
  and in a BJT's emitter; uses r_d and C_d to set a diode's small-signal bandwidth.
- Missteps:
  - takes the diode as off below 0.7 V
  - uses V_D/I_D as the small-signal resistance
  - gives the heavily doped side most of the current
  - uses L in place of W for a short diode, or the reverse
  - forgets the −1 and so gives a non-zero current at V_D = 0
  - writes log₁₀ where ln belongs, and gets 26 mV per decade
- Seeds, to be varied and never asked word for word:
  - predict: a diode's lightly doped side is doped four times more heavily; what happens to I_S and to the voltage for
    the same 1 mA?
  - explain: why the minority profile in a short region is a straight line.
  - limit: the forward voltage pushed up until the injected carriers rival the doping; what fails first, and does the
    real current grow faster or slower than the formula?
  - transfer: two identical diodes in parallel carry 2 mA in total; how does each one's V_D compare with a single diode
    carrying 2 mA, and what does that say about matching transistors in a current mirror?

## Where this shows up

- `pn-equilibrium`: forward bias tips the equilibrium balance, and the diffusion that was cancelled is now the current.
- `diffusion-current`: the current in each neutral region is pure diffusion, qD times the slope of the profile.
- `mass-action-law`: the minority densities n_i²/N_A and n_i²/N_D set the size of I_S.
- `small-signal-analysis`: r_d = (kT/q)/I_D is the first small-signal model: the tangent of a curve at its bias point.
- `bjt-operation`: a forward-biased emitter junction injects minority carriers exactly this way, and the collector
  catches them.
- Later: EE 130: high-level injection, generation in the depletion region and the BJT; EE 140: diode-connected devices
  and bandgap references.

## Page text

- Header `Concept:` Forward bias raises the minority density at each depletion edge by e^(V_D/(kT/q)); the current is
  diffusion down from there, so I = I_S(e^(V_D/(kT/q)) − 1), and its tangent at the bias point is r_d = (kT/q)/I_D.
- Header `Course:` EE 105 (forward bias, minority-carrier profiles, diode I–V, diode small-signal model, diffusion
  capacitance)
- Header `Play with:` The diode voltage V_D, the neutral regions' width W and the minority lifetime τ
- Header `Should click:` The current is exponential because the barrier sets the edge density exponentially and the
  current is the slope from there; the light side and the shorter of W and L set I_S.
- Title: The diode: injection, diffusion and the exponential
- Lede: Lower the junction's barrier and carriers spill over it, arriving on the far side as minority carriers. They
  can only diffuse away from the junction, and the slope of their crowd is the current. Move the voltage and watch the
  crowds, the slopes and the current grow together.
- Caption of `profiles`: The excess minority carriers in the two neutral regions: electrons in the p side, holes in the
  n side. The dashed slopes at the edges set the current. The vertical scale follows V_D.
- Caption of `iv`: The current against V_D, with its tangent at the bias point. Drag the triangle or press anywhere in
  the plot; focused, ← → move it 5 mV, with Shift 50 mV.
- Caption of `log`: The same current on a log scale: a straight line, ten times per 59.9 mV, made of a hole part and an
  electron part.
- What should click:
  - **The barrier sets the edge.** Lowering the barrier by V_D lets e^(V_D/(kT/q)) times as many carriers over it, so
    the minority density at each depletion edge rises by that factor.
  - **The current is a slope.** The neutral regions have no field, so the minority carriers can only diffuse. The
    current is qD times the slope at the edge: over W in a short region, over L = √(Dτ) in a long one.
  - **The light side does the work.** Each side's minority density starts at n_i²/N, so the lightly doped side has
    more to inject and carries most of the current.
  - **The tangent is a resistance, the crowd is a capacitance.** Near the bias point a small wiggle sees the slope
    I_D/(kT/q), so r_d = 26 Ω at 1 mA. The carriers waiting in the neutral regions grow with the current, so the diode
    stores charge like a capacitor C_d that grows with the current too.

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
