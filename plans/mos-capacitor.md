# Plan: MOS capacitor and threshold

```json plan
{
  "id": "mos-capacitor",
  "title": "MOS capacitor and threshold",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["mos-capacitor", "accumulation-depletion-inversion", "threshold-voltage", "flatband-voltage", "mos-cv-curve"],
  "prerequisites": ["ic-capacitor", "depletion-region", "potential-vs-doping", "poisson-equation"],
  "size": "L",
  "tool": "devices/mos/mos-capacitor.html",
  "checks": "plans/checks/mos-capacitor.py"
}
```

## Concept

A MOS capacitor is a gate plate on thin oxide over a silicon body. The gate side always answers with a sheet of charge,
but the body can answer in three ways: with holes piled up at the surface (accumulation), with bare acceptor ions
uncovered to a depth x_d (depletion), or, once the surface potential has moved by 2|φ_p|, with a thin sheet of
electrons (inversion). The gate voltage that starts inversion is the threshold, V_T = V_FB + 2|φ_p| + |Q_B,max|/C_ox:
cancel the built-in step, bend the surface by 2|φ_p|, and hold the depletion charge across the oxide. Above V_T every
extra volt adds C_ox worth of electrons, which is the channel charge C_ox(V_GB − V_T) a MOSFET conducts with.

## Picture

The page has a `.bench`: the left column holds figure 1 and the controls under it; the right column (`aside`) holds the
readouts. Under the bench, a `.pair`: figure 2 on the left and figure 3 on the right.

The device: an NMOS capacitor (p-type body). kT/q = 0.026 V, n_i = 10¹⁰ cm⁻³, ε_ox = 3.9 ε₀, ε_si = 11.7 ε₀ with
ε₀ = 8.854×10⁻¹⁴ F/cm, q = 1.602×10⁻¹⁹ C; the gate is n+ poly (φ_gate = +0.55 V) or p+ poly (−0.55 V). Body charge is
positive for holes and negative for ions and electrons.

**Figure 1, `stack`, viewBox 640 by 340.** Two panels sharing one vertical axis, depth.
- Left panel, the cross-section, from x = 20 to x = 300: the gate from y = 20 to y = 60 (fill `--grid`, labelled
  "gate, n+ poly" or "gate, p+ poly"); the oxide from y = 60 to y = 90 (fill `--surface`, `--line` border, labelled
  "oxide, t_ox = 20 nm (not to scale)"); the body from y = 90 to y = 330, labelled "p-type body, N_A = 5.00×10¹⁶ cm⁻³" at its
  bottom. The body's depth scale: 240 px stand for D = 1.25 × x_d,max (x_d at 2|φ_p|), so the depletion always fits;
  ticks on the panel's right edge in nm.
- The charges, each drawn as symbols whose number is round(|Q| / 10 nC/cm²), at most 40, evenly spaced across the panel:
  the gate's charge Q_G = −(Q_acc + Q_dep + Q_inv) as "+" or "−" in `--ink-2` along y = 54; the accumulated holes as
  small `--c2` circles with "+" just under the oxide at y = 97; the inversion electrons as `--c1` dots in a band from
  y = 92 to y = 98; the depletion region as a rectangle from y = 90 down to x_d, filled `--c4` at opacity 0.12, with "−"
  ion marks in `--c4` every 20 px across and down.
- The region's name, centred under the panel title: "accumulation", "depletion" or "inversion".
- Right panel, the potential, from x = 360 to x = 620 on the same vertical axis: the potential relative to the neutral
  body, in `--c3`, 2.4 px: V_GB − V_FB in the gate, falling linearly across the oxide by V_ox to ψ_s at the surface,
  then `potentialAt` down through the depletion region to 0. The potential axis runs across from
  min(−0.5, V_GB − V_FB) to max(1, V_GB − V_FB) V, with ticks every 0.5 V and "potential (V)" at the top; a dotted
  `--ink-3` vertical line at 2|φ_p| labelled "2|φ_p|" near its top; the labels "V_GB − V_FB" (gate),
  "V_ox" (oxide) and "ψ_s" (surface) in `--c3`, each at the height of its layer (V_ox at y = 72 when ψ_s ≥ V_GB − V_FB and at y = 88 otherwise, clear of the
  sloping line), 8 px to the right of the curve, or to
  its left when there is no room before x = 620. Their values are in the readouts.

**Figure 2, `charge`, viewBox 480 by 300.** The body's charges against V_GB. Plot area from x = 60 to x = 460 (V_GB from
−3 V to 3 V, grid every 0.5 V, labels every 1 V) and y = 20 to y = 260 (|Q| from 0 to the largest value on the plot,
rounded up to a multiple of 100 nC/cm², five grid lines with labels in nC/cm²). Drawn: |Q_acc| in `--c2`, |Q_dep| in
`--c4`, |Q_inv| in `--c1`, 2.2 px, 300 points; dashed `--ink-2` vertical lines at V_FB and V_T, labelled; the cursor at
the current V_GB, an `--ink-2` dashed vertical line with a 14 px triangle handle under the axis, and a dot on each
curve. Axis names "V_GB (V)" and "|Q| (nC/cm²)".

**Figure 3, `cv`, viewBox 480 by 300.** C/C_ox against V_GB, plot area and V_GB axis as figure 2, C/C_ox from 0 to 1.1
with grid lines every 0.2. Drawn: `capacitance(…, false)`/C_ox in `--ink`, 2.2 px, labelled "measured slowly";
`capacitance(…, true)`/C_ox dashed (5 4) in `--ink-2`, labelled "measured fast"; the same V_FB and V_T lines and the
same cursor, with a dot on each curve.

**Readouts, in the aside,** in `.read`:
- "φ_p = −(kT/q)·ln(N_A/n_i) = −0.401 V"; "V_FB = φ_p − φ_gate = −0.951 V"; "C_ox = ε_ox/t_ox = 173 nF/cm²";
  "|Q_B,max| = √(2qε_si N_A·2|φ_p|) = 115 nC/cm²".
- "V_T = V_FB + 2|φ_p| + |Q_B,max|/C_ox", then "= −0.951 + 0.802 + 0.668 = 0.519 V", large (`.big`).
- At the cursor: "V_GB = 0.00 V: depletion"; "ψ_s = 0.450 V" and "V_ox = 0.501 V" in `--c3`; "x_d = 108 nm" and
  "Q_dep = −86.4 nC/cm²" in `--c4`; "Q_acc = …" in `--c2` and "Q_inv = …" in `--c1` (shown as 0 when absent);
  "C = 61.7 nF/cm² (0.357 C_ox)".
- Every number has three significant figures and an SI prefix, except the doping, written 5.00×10¹⁶ cm⁻³.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| inversion electrons | Q_inv | `--c1` |
| accumulated holes | Q_acc | `--c2` |
| potentials: gate drive, oxide drop, surface | V_GB − V_FB, V_ox, ψ_s | `--c3` |
| depletion charge and width | Q_dep, x_d | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| V_GB | draggable handle: the triangle under figure 2 or 3, or a press anywhere in either plot | V_GB in V | −3 V to 3 V | 0.01 V | 0 V | ← → 0.01 V, Shift + ← → 0.1 V |
| doping | slider, log | N_A in cm⁻³, slider value log₁₀ N_A | 5×10¹⁴ to 5×10¹⁷ (14.69897 to 17.69897) | 0.1 decade | 5×10¹⁶ (16.69897) | arrows: one step |
| oxide | slider | t_ox in nm | 2 nm to 50 nm | 1 nm | 20 nm | arrows: one step |
| gate | two buttons, "n+ poly gate" and "p+ poly gate" | φ_gate | +0.55 V, −0.55 V | | n+ | Tab and Enter |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "N_A = 5.00×10¹⁶ cm⁻³", "t_ox = 20 nm".
- What moves when each control changes: V_GB moves figure 1, the cursors and the "at the cursor" readouts. Doping, oxide
  and gate change V_FB and V_T, so every curve and readout is redrawn.
- Reset: V_GB = 0 V, N_A = 5×10¹⁶ cm⁻³, t_ox = 20 nm, n+ gate.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: the gate voltage splits between the oxide and the body; the body first answers with
  ever deeper depletion, and once its surface has moved by 2|φ_p| it answers with electrons instead, so the depletion
  stops growing and every further volt buys C_ox worth of channel charge.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. gate is "n+" or "p+"; NA in cm⁻³;
tox in cm; voltages in V; charges per area in C/cm²; capacitances per area in F/cm²; depths in cm.

### `phiP(NA)`, `flatband(gate, NA)`, `cox(tox)`, `qbMax(NA)`, `threshold(gate, NA, tox)`

- Return: φ_p = −(kT/q)·ln(NA/n_i); V_FB = φ_p − φ_gate; C_ox = ε_ox/tox; |Q_B,max| = √(2qε_si·NA·2|φ_p|);
  V_T = V_FB + 2|φ_p| + |Q_B,max|/C_ox.
- Sign convention: φ_p is negative for a p-type body; V_FB is the gate voltage that leaves no charge anywhere.
- Approximation: the gate is degenerately doped (φ_gate = ±0.55 V); no oxide charge; inversion starts when ψ_s = 2|φ_p|.

### `surface(gate, NA, tox, VGB)`

- Returns: `{ region, psiS, xd, Qacc, Qdep, Qinv, Vox }`.
- Formula:
  - VGB ≤ V_FB: "accumulation", ψ_s = 0, x_d = 0, Q_acc = C_ox(V_FB − VGB), V_ox = VGB − V_FB.
  - V_FB < VGB ≤ V_T: "depletion". With γ = √(2qε_si NA)/C_ox, VGB − V_FB = ψ_s + γ√ψ_s, so
    √ψ_s = (−γ + √(γ² + 4(VGB − V_FB)))/2; x_d = √(2ε_si ψ_s/(q NA)); Q_dep = −q NA x_d; V_ox = γ√ψ_s.
  - VGB > V_T: "inversion", ψ_s = 2|φ_p|, x_d at that ψ_s, Q_dep = −|Q_B,max|, Q_inv = −C_ox(VGB − V_T),
    V_ox = VGB − V_FB − 2|φ_p|.
- Approximation: the depletion approximation (a box of ions with a sharp edge); accumulation and inversion charge as
  sheets at the surface; no electrons at all below V_T.

### `capacitance(gate, NA, tox, VGB, high)`

- Returns: C_ox in accumulation (and at x_d = 0); C_ox·C_dep/(C_ox + C_dep) with C_dep = ε_si/x_d in depletion; in
  inversion C_ox when high is false (measured slowly, the electrons follow) and the depletion value at x_d,max when high
  is true (measured fast, they cannot).

### `potentialAt(gate, NA, tox, VGB, x)`

- Returns: the potential at depth x below the surface, relative to the neutral body: ψ_s(1 − x/x_d)² for x < x_d, and 0
  beyond (and everywhere when x_d = 0).
- Formula: Poisson's equation with a uniform charge −qN_A in the depletion region gives a parabola that meets 0 with zero
  slope at x_d.

## Check cases

Computed by `plans/checks/mos-capacitor.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "phiP", "args": [5e+16], "expect": -0.40104866023035773, "tol": 1e-09, "units": "V", "tag": "typical", "note": "p-type body, N_A = 5×10¹⁶ cm⁻³: φ_p = −(26 mV)·ln(5×10⁶) = −0.401 V"},
  {"fn": "flatband", "args": ["n+", 5e+16], "expect": -0.9510486602303578, "tol": 1e-09, "units": "V", "tag": "sign", "note": "n+ poly gate (+0.55 V) on that body: V_FB = φ_p − φ_gate = −0.951 V, negative"},
  {"fn": "flatband", "args": ["p+", 5e+16], "expect": 0.1489513397696423, "tol": 1e-09, "units": "V", "tag": "sign", "note": "p+ poly gate (−0.55 V) on the same body: V_FB = +0.149 V"},
  {"fn": "cox", "args": [2e-06], "expect": 1.72653e-07, "tol": 1e-15, "units": "F/cm²", "tag": "typical", "note": "20 nm of oxide: C_ox = ε_ox/t_ox = 173 nF/cm²"},
  {"fn": "qbMax", "args": [5e+16], "expect": 1.1537387474343017e-07, "tol": 1e-15, "units": "C/cm²", "tag": "typical", "note": "N_A = 5×10¹⁶ cm⁻³ at the onset of inversion: |Q_B,max| = √(2qε_si N_A·2|φ_p|) = 115 nC/cm²"},
  {"fn": "threshold", "args": ["n+", 5e+16, 2e-06], "expect": 0.5192900156856939, "tol": 1e-09, "units": "V", "tag": "typical", "note": "n+ gate, N_A = 5×10¹⁶ cm⁻³, t_ox = 20 nm: V_T = −0.951 + 0.802 + 0.668 = 0.519 V"},
  {"fn": "threshold", "args": ["n+", 5e+17, 2e-06], "expect": 2.176319786699292, "tol": 1e-09, "units": "V", "tag": "typical", "note": "ten times the doping: V_T rises to 2.18 V, mostly through the depletion charge the oxide must hold"},
  {"fn": "threshold", "args": ["n+", 5e+16, 5e-07], "expect": 0.018108999094191697, "tol": 1e-09, "units": "V", "tag": "typical", "note": "the same body with 5 nm of oxide: V_T falls to 0.018 V; a thinner oxide holds the same charge with less voltage"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, -2], "expect": {"region": "accumulation", "psiS": 0.0, "xd": 0.0, "Qacc": 1.8110459566524802e-07, "Qdep": 0.0, "Qinv": 0.0, "Vox": -1.0489513397696422}, "tol": 1e-12, "units": "V, cm, C/cm²", "tag": "typical", "note": "V_GB = −2 V, below V_FB: accumulation, 181 nC/cm² of holes at the surface, all of V_GB − V_FB across the oxide"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, 0], "expect": {"region": "depletion", "psiS": 0.45033631334047974, "xd": 1.0792695234404256e-05, "Qacc": 0.0, "Qdep": -8.644948882757809e-08, "Qinv": 0.0, "Vox": 0.5007123468898779}, "tol": 1e-12, "units": "V, cm, C/cm²", "tag": "typical", "note": "V_GB = 0 V: depletion, the surface 0.450 V above the bulk, 108 nm of bare acceptors, 0.501 V across the oxide"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, 1.5], "expect": {"region": "inversion", "psiS": 0.8020973204607155, "xd": 1.4403729680827737e-05, "Qacc": 0.0, "Qdep": -1.1537387474343017e-07, "Qinv": -1.693225209218179e-07, "Vox": 1.648951339769642}, "tol": 1e-12, "units": "V, cm, C/cm²", "tag": "typical", "note": "V_GB = 1.5 V: inversion, ψ_s pinned at 2|φ_p| = 0.802 V, the depletion stopped at 144 nm, and 169 nC/cm² of electrons"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, -0.951], "expect": {"region": "depletion", "psiS": 4.2523869747576116e-09, "xd": 1.048764115431572e-09, "Qacc": 0.0, "Qdep": -8.400600564606892e-12, "Qinv": 0.0, "Vox": 4.865597797088316e-05}, "tol": 1e-09, "units": "V, cm, C/cm²", "tag": "limit-zero", "note": "V_GB just above V_FB = −0.9512 V: almost no charge anywhere; the bands are nearly flat"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, 4], "expect": {"region": "inversion", "psiS": 0.8020973204607155, "xd": 1.4403729680827737e-05, "Qacc": 0.0, "Qdep": -1.1537387474343017e-07, "Qinv": -6.00955020921818e-07, "Vox": 4.148951339769642}, "tol": 1e-12, "units": "V, cm, C/cm²", "tag": "limit-infinity", "note": "V_GB = 4 V: the depletion has not grown past 144 nm; every extra volt adds C_ox·1 V = 173 nC/cm² of electrons"},
  {"fn": "surface", "args": ["n+", 5e+16, 2e-06, 0.519], "expect": {"region": "depletion", "psiS": 0.8018925917560956, "xd": 1.440189134710197e-05, "Qacc": 0.0, "Qdep": -1.1535914969028677e-07, "Qinv": 0.0, "Vox": 0.668156068474262}, "tol": 1e-09, "units": "V, cm, C/cm²", "tag": "breaks", "note": "at threshold the model says no electrons at all, though the surface is as n-type as the body is p-type (5×10¹⁶ cm⁻³ at the surface): the charge-sheet picture ignores the electrons below threshold"},
  {"fn": "capacitance", "args": ["n+", 5e+16, 2e-06, 0, false], "expect": 6.168860838239053e-08, "tol": 1e-15, "units": "F/cm²", "tag": "typical", "note": "in depletion at 0 V: C_ox in series with ε_si/x_d gives 61.7 nF/cm², 0.357 of C_ox"},
  {"fn": "capacitance", "args": ["n+", 5e+16, 2e-06, 2, true], "expect": 5.0771011780919404e-08, "tol": 1e-15, "units": "F/cm²", "tag": "typical", "note": "in inversion at high frequency the electrons cannot follow: C stays at its minimum, 50.8 nF/cm²"},
  {"fn": "capacitance", "args": ["n+", 5e+16, 2e-06, 2, false], "expect": 1.72653e-07, "tol": 1e-15, "units": "F/cm²", "tag": "typical", "note": "the same, measured slowly: the electron sheet answers at the surface and C is back to C_ox"},
  {"fn": "potentialAt", "args": ["n+", 5e+16, 2e-06, 0, 5.4e-06], "expect": 0.11243173047878438, "tol": 1e-09, "units": "V", "tag": "typical", "note": "at 0 V, 54 nm down, halfway through the 108 nm depletion region: the potential is a quarter of ψ_s, 0.112 V"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Start at V_GB = 0 V and raise it slowly. Where does the extra gate charge find its partner in the body, below V_T and
   above it?
   Why: Below V_T, deeper in: the depletion region widens and uncovers more acceptors. Above V_T, at the surface: electrons
   gather there and the depletion stops at 144 nm.
2. With an n+ gate, is V_FB positive or negative?
   Why: Negative, −0.951 V. The n+ gate sits 0.55 V above intrinsic and the p body 0.40 V below it, so the gate must be
   pulled down by their difference to flatten the bands.
3. Raise N_A tenfold. Does V_T go up or down, and which part grows most?
   Why: Up, from 0.52 V to 2.18 V. 2|φ_p| grows by only 0.12 V; the depletion charge the oxide must hold grows about
   3.4 times (√10, and a little more because 2|φ_p| grew too), and that term dominates.
4. Thin the oxide from 20 nm to 5 nm. What happens to V_T, and to the channel charge per volt above it?
   Why: V_T falls to about 0.02 V, because a thinner oxide holds the same depletion charge with less voltage; and C_ox
   quadruples, so each volt above V_T buys four times the electrons.
5. In inversion, why does the slowly measured capacitance come back to C_ox while the fast one stays low?
   Why: Slowly, new electrons have time to appear right at the surface, one oxide-thickness from the gate. Fast, they do
   not, and the charge has to come from the edge of the depletion region, far below.

## Misconceptions

- "Inversion means the depletion region keeps widening." What the tool shows instead: x_d stops at x_d,max at V_T, and
  in figure 2 |Q_dep| goes flat while |Q_inv| rises.
- "The flatband voltage is zero." What the tool shows instead: with an n+ gate the charges are zero at −0.951 V, not at
  0 V.
- "An NMOS capacitor has an n-type body." What the tool shows instead: the body is p-type; the N names the electrons of
  the inversion layer.
- "All of the gate voltage appears across the oxide." What the tool shows instead: figure 1's potential splits V_GB − V_FB
  into V_ox and ψ_s, and in depletion ψ_s takes a large share.

## Quiz hooks

- L2 looks like: computes φ_p, V_FB, C_ox, |Q_B,max| and V_T from given values; names the region for a given V_GB.
- L3 looks like: sketches the charge in the body in each region; explains each term of V_T; says why the depletion stops
  at V_T; predicts what doping, oxide thickness and gate material do to V_FB and V_T; explains the C–V curve's dip and
  why it returns to C_ox only when measured slowly.
- L4 looks like: knows that below V_T there are electrons the charge-sheet model ignores (subthreshold); includes oxide
  charge and body bias in V_T; knows why modern gates use thin oxides and metal or high-k stacks.
- Missteps:
  - takes V_FB as zero or with the wrong sign
  - uses |φ_p| instead of 2|φ_p| in V_T
  - keeps widening the depletion region above V_T
  - uses Q_B,max/C_ox with the wrong doping or an oxide thickness in the wrong units
  - calls the body of an NMOS capacitor n-type
- Seeds, to be varied and never asked word for word:
  - predict: an NMOS capacitor's body doping is quadrupled; which terms of V_T change, and does V_T rise or fall?
  - explain: why the depletion region stops growing once the inversion layer forms.
  - limit: the oxide made very thin; what is V_T heading toward, and what stops anyone from making it that thin?
  - transfer: a PMOS capacitor on an n-type body with a p+ gate: write its V_FB and V_T with the signs right.

## Where this shows up

- `mos-capacitor`: the gate, oxide and body as a capacitor whose body plate can answer three ways.
- `accumulation-depletion-inversion`: the three answers, in figure 1 and figure 2.
- `threshold-voltage`: V_T = V_FB + 2|φ_p| + |Q_B,max|/C_ox, built term by term in the readout.
- `flatband-voltage`: V_FB = φ_p − φ_gate, where all charges vanish.
- `mos-cv-curve`: C/C_ox against V_GB in figure 3.
- `triode-region`: above V_T the electron sheet C_ox(V_GB − V_T) is the channel that carries the drain current.
- Later: EE 130: subthreshold conduction, oxide charge and the body effect; EE 140: V_T and C_ox set every MOSFET's
  numbers.

## Page text

- Header `Concept:` The body answers the gate with holes, then with a widening layer of bare acceptors, then, once its
  surface has moved by 2|φ_p|, with a sheet of electrons; V_T = V_FB + 2|φ_p| + |Q_B,max|/C_ox.
- Header `Course:` EE 105 (MOS capacitor, flatband and threshold, C–V curve)
- Header `Play with:` The gate voltage, the body doping, the oxide thickness and the gate material
- Header `Should click:` Below threshold the body answers deeper, with depletion; above it, at the surface, with electrons:
  the depletion stops growing and every further volt buys C_ox worth of channel charge.
- Title: MOS capacitor and threshold
- Lede: Put a metal plate on thin glass over p-type silicon and raise its voltage. The silicon must answer with an equal
  and opposite charge, and it has three ways to do it: holes, bare acceptor ions, or a sheet of electrons. Drag the gate
  voltage and watch which answer it gives, and where the voltage goes.
- Caption of `stack`: Left, the charges: holes in orange, bare acceptors in purple, electrons in blue. Right, the
  potential through the same stack, measured from the neutral body.
- Caption of `charge`: The body's charge against the gate voltage. Drag the cursor or press anywhere in the plot; focused,
  ← → move it 0.01 V, with Shift 0.1 V.
- Caption of `cv`: The capacitance is the slope of the charge. Measured fast, the electrons cannot keep up.
- What should click:
  - **The body has three answers.** Below V_FB, holes pile up at the surface. Above it, holes are pushed away and bare
    acceptors answer, deeper and deeper. Above V_T, electrons answer, right at the surface.
  - **The voltage splits.** V_GB − V_FB = V_ox + ψ_s: part across the oxide, part bending the body's surface. In depletion
    the body takes a large share; in inversion its share is pinned at 2|φ_p|.
  - **Threshold is three steps.** Cancel the built-in step (V_FB), bend the surface by 2|φ_p| so it is as n-type as the
    body is p-type, and put |Q_B,max|/C_ox across the oxide to hold the depletion charge.
  - **Above V_T, a volt buys C_ox of electrons.** Q_inv = −C_ox(V_GB − V_T). That sheet of electrons is the channel of a
    MOSFET, and its charge per volt is why C_ox appears in every MOSFET equation.

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
