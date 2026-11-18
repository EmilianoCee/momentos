# Plan: Carriers and doping

```json plan
{
  "id": "carriers-and-doping",
  "title": "Carriers and doping",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["doping", "mass-action-law", "intrinsic-carriers", "energy-bands", "potential-vs-doping"],
  "prerequisites": ["electrons-and-holes", "boltzmann-factor"],
  "size": "M",
  "tool": "devices/semiconductors/carriers-and-doping.html",
  "checks": "plans/checks/carriers-and-doping.py"
}
```

## Concept

Heat lifts a few electrons across silicon's 1.12 eV gap, each leaving a hole, so pure silicon has n = p = n_i,
10¹⁰ cm⁻³ at 300 K. Donors add electrons without holes and acceptors add holes without electrons; the larger wins by
the difference. Whatever the doping, np stays at n_i², so on a logarithmic scale n sits as far above n_i as p sits
below it. That logarithmic scale is an energy scale: the Fermi level E_F moves (kT/q)·ln 10 = 59.9 meV for each
tenfold step in density, which is where every potential in a pn junction and a MOS capacitor comes from.

## Picture

The page has a `.bench`: the left column holds figure 1 and the controls under it; the right column (`aside`) holds the
readouts. Figure 2 sits in the left column too, under the controls.

The material: silicon with E_g = 1.12 eV, E_i at mid-gap, every dopant ionised. kT/q = 0.026 V × T/300 K, and
n_i(T) = 10¹⁰ cm⁻³ × (T/300 K)^1.5 × e^(E_g/(2 × 0.026 eV) − E_g/(2kT)), so the course's 26 mV and 10¹⁰ cm⁻³ hold at
300 K.

**Figure 1, `ladder`, viewBox 640 by 380.** One vertical axis, energy measured from E_i, from −0.70 eV at y = 360 to
+0.70 eV at y = 20: y = 190 − 242.857 × (E − E_i) in eV. Two panels share it.
- The band panel, from x = 70 to x = 330.
  - E_c at +0.56 eV and E_v at −0.56 eV: `--ink` lines, 2.4 px, labelled "E_c" and "E_v" at x = 62, end-anchored.
  - The conduction band, from y = 20 down to E_c, and the valence band, from E_v down to y = 360: rectangles filled
    `--grid` (the figure's own background is `--surface`), labelled "conduction band" (x = 200, y = 30) and "valence
    band" (x = 200, y = 357) in `--ink-2`.
  - The gap: a double-headed `--ink-3` arrow at x = 90 from E_c to E_v, with "E_g = 1.12 eV" beside it at x = 96,
    start-anchored, at y = 230 when E_F ≥ E_i and at y = 160 otherwise, so it stays clear of the E_F − E_i label.
  - E_i: a dashed (4 3) `--ink-3` line, 1.2 px, from x = 70 to x = 470, labelled "E_i" at x = 62, end-anchored.
  - E_F: a `--c3` line, 2.4 px, from x = 70 to x = 470, labelled "E_F" at x = 62, end-anchored, in `--c3`. When E_F is
    within 10 px of E_i, the "E_i" label moves 12 px down. When E_F is within 12 px of E_c its label goes to E_c + 18 px,
    and within 12 px of E_v to E_v − 10 px, so it never sits on the "E_c" or "E_v" label.
  - An arrow in `--c3` at x = 300 from E_i to E_F, with "E_F − E_i = 0.359 eV" at x = 294, end-anchored, halfway between
    them. It is hidden when |E_F − E_i| < 0.02 eV.
  - Donor levels, drawn only when N_D > 0: eight short `--ink-2` dashes, 14 px long, at E_c − 0.045 eV from x = 120 to
    x = 260, labelled "donors" at x = 266, start-anchored, 10 px (clear of the n and p labels, which end at x = 458). Acceptor levels, drawn only when N_A > 0: the same at
    E_v + 0.045 eV, labelled "acceptors".
  - The carriers, to scale: the more numerous carrier gets 30 symbols, the other 30 × (fewer/more) rounded to the
    nearest whole number, so a minority 10¹² times rarer gets none. Electrons are `--c1` dots of radius 3 in two rows of
    15, at E_c − 7 px and E_c − 14 px (in the conduction band), from x = 110 to x = 320; holes are `--c2` open circles
    of radius 3, 1.4 px stroke, in two rows at E_v + 7 px and E_v + 14 px. The rows fill left to right, the first row
    first.
  - The warning, shown only when `edgeMargin` is under 3kT: "E_F is within 3kT of a band edge:" and "the Boltzmann
    formulas fail here" on two lines in `--ink`, 12 px, centred at x = 200, on a `--surface` rectangle with a `--line`
    border from x = 52, 296 by 36 px. The rectangle's top is at y = 246 when E_F ≥ E_i and at y = 98 otherwise: on the
    side of E_i away from E_F, so it never covers the E_F − E_i label.
- The density panel, from x = 400 to x = 620.
  - The axis: an `--ink-2` vertical line at x = 470 from y = 20 to y = 360, titled "density (cm⁻³), log scale" at
    x = 470, y = 12.
  - A tick for every whole decade 10^k whose energy (kT/q)·ln(10^k/n_i) lies inside ±0.70 eV, from x = 464 to x = 476,
    and the label "10^k" (with a superscript) at x = 482, start-anchored, for even k only.
  - The mirror line: a dashed (5 4) `--c2` line, 1.6 px, at −(E_F − E_i), from x = 330 to x = 470, labelled "mirror of
    E_F" at x = 340, 14 px below it, in `--c2`, 11 px; the label is hidden when |E_F − E_i| < 0.03 eV.
  - n: a `--c1` dot of radius 5 at (470, E_F), with "n = 1.00×10¹⁶" 6 px above the line at x = 458, end-anchored, in
    `--c1`. p: a `--c2` dot at (470, the mirror), with "p = 1.00×10⁴" the same way, in `--c2`. n_i: an `--ink-2` dot at
    (470, E_i) with "n_i" at x = 458, y = 184, end-anchored, hidden when n or p is within 20 px of E_i. When n and p are
    within 14 px of each other the p label goes 16 px under its line instead of above.

**Figure 2, `heat`, viewBox 640 by 300.** Densities against temperature. Plot area from x = 70 to x = 610 (T from
200 K to 700 K, grid every 50 K, labels every 100 K) and from y = 20 to y = 250 (log₁₀ of the density from 0 at the
bottom to 20 at the top, grid every 2 decades, labels "10⁰" to "10²⁰"). Drawn, each from 201 points spaced 2.5 K and
clipped to the plot area:
- n in `--c1`, 2.2 px; p in `--c2`, 2.2 px; n_i as a dashed (5 4) `--ink-2` line, 1.6 px. Each is labelled at its right
  end, x = 614, start-anchored, in its colour: "n", "p", "n_i", pushed apart so that each is at least 11 px below the
  one above it. When N_D = N_A, n and p both lie on n_i and only "n = p = n_i" is written, end-anchored at x = 614.
- |N_D − N_A| as a dotted (2 3) `--ink-3` horizontal line labelled "|N_D − N_A|" at x = 76, 5 px above it,
  start-anchored, drawn only when it is at least 1 cm⁻³.
- The cursor at T: a dashed `--ink-2` vertical line, with a 14 px triangle handle under the axis at y = 262 and a dot
  on each curve.
- Axis names "T (K)" under the axis and "density (cm⁻³)" rotated on the left.

**Readouts, in the aside,** in `.read`:
- "N_D = 1.00×10¹⁶ cm⁻³", "N_A = none", "T = 300 K".
- "n_i = 1.00×10¹⁰ cm⁻³", "kT/q = 26.0 mV".
- The kind, large (`.big`): "n-type", "p-type" or "nearly intrinsic".
- "n = 1.00×10¹⁶ cm⁻³" in `--c1` and "p = n_i²/n = 1.00×10⁴ cm⁻³" in `--c2` when n ≥ p; when p > n, "p = 6.00×10¹⁶ cm⁻³"
  first and "n = n_i²/p = 1.67×10³ cm⁻³".
- "n·p = 1.00×10²⁰ cm⁻⁶ = n_i²".
- "E_F − E_i = (kT/q)·ln(n/n_i) = +0.359 eV" in `--c3`, then "so the potential from intrinsic is φ_n = +0.359 V" in
  `--c3` (written φ_p when p-type and φ when nearly intrinsic).
- "One decade of density = (kT/q)·ln 10 = 59.9 meV".
- "E_F is 0.201 eV below E_c" (or "above E_v" when E_F < E_i).
- Densities are written with three significant figures as a.bc×10^k cm⁻³; energies in eV with three decimals; kT/q
  in mV with one decimal.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| electrons | n | `--c1` |
| holes | p | `--c2` |
| Fermi level and the potential it gives | E_F − E_i, φ | `--c3` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| donors | slider, log | N_D in cm⁻³, slider value log₁₀ N_D | 11 to 19, where 11 means none (N_D = 0) | 0.1 decade | 16 (10¹⁶ cm⁻³) | arrows: one step |
| acceptors | slider, log | N_A in cm⁻³, slider value log₁₀ N_A | 11 to 19, where 11 means none (N_A = 0) | 0.1 decade | 11 (none) | arrows: one step |
| temperature | slider, and the triangle handle in figure 2 (drag it, or press anywhere in the plot) | T in K | 200 K to 700 K | 5 K | 300 K | slider arrows: 5 K; on the focused handle ← → 5 K, Shift + ← → 50 K |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "N_D = 1.00×10¹⁶ cm⁻³" or "N_D = none", "T = 300 K".
- What moves when each control changes: every control redraws figure 1, the curves and cursor of figure 2, and the
  readouts. Figure 1 has nothing to drag.
- Reset: N_D = 10¹⁶ cm⁻³, N_A = none, T = 300 K.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: n and p are mirror images about n_i on a log scale, so adding electrons removes
  holes; and that log scale is an energy scale, 59.9 meV per decade, which is how far E_F moves.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. ND and NA in cm⁻³, T in K, energies
in eV, densities in cm⁻³. E_g = 1.12 eV.

### `thermalVoltage(T)`

- Returns: kT/q in V.
- Formula: 0.026 × T/300.
- Approximation: none beyond scaling the course's 26 mV with T.

### `intrinsic(T)`

- Returns: n_i in cm⁻³.
- Formula: 1e10 × (T/300)^1.5 × exp(E_g/(2 × 0.026) − E_g/(2 × thermalVoltage(T))).
- Valid for: 200 K to 700 K.
- Approximation: E_g held at 1.12 eV (it shrinks by about 0.05 eV between 300 K and 600 K); N_cN_v taken as ∝ T³.

### `carriers(ND, NA, T)`

- Returns: `{ n, p, kind }`, densities in cm⁻³ and kind "n-type", "p-type" or "nearly intrinsic".
- Formula: with N = ND − NA and h = |N|/2, the majority density is h + √(h² + n_i²) and the minority density is
  n_i²/(majority). The majority is n when N ≥ 0 and p otherwise. kind is "n-type" when n ≥ 100p, "p-type" when
  p ≥ 100n, and "nearly intrinsic" otherwise.
- Sign convention: N > 0 is net donors.
- Approximation: every dopant ionised (fails below about 100 K, outside the range); charge neutrality; Boltzmann
  statistics (see `edgeMargin`).

### `fermiLevel(ND, NA, T)`

- Returns: E_F − E_i in eV.
- Formula: thermalVoltage(T) × ln(n/n_i). The same number in volts is the potential of the material measured from
  intrinsic silicon, φ = (kT/q)·ln(n/n_i).
- Sign convention: positive above E_i (n-type), negative below (p-type).
- Approximation: Boltzmann statistics, E_i at mid-gap.

### `edgeMargin(ND, NA, T)`

- Returns: E_g/2 − |E_F − E_i| in eV, the distance from E_F to the nearer band edge.
- Use: the Boltzmann formulas need a margin of at least 3kT; below that the page shows its warning.

### `perDecade(T)`

- Returns: thermalVoltage(T) × ln 10 in V, the step in E_F (in eV) for a tenfold change in density.

## Check cases

Computed by `plans/checks/carriers-and-doping.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "thermalVoltage", "args": [300], "expect": 0.026, "tol": 1e-09, "units": "V", "tag": "typical", "note": "T = 300 K: kT/q = 26 mV, the course's value"},
  {"fn": "intrinsic", "args": [300], "expect": 10000000000.0, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "T = 300 K: n_i = 1.00×10¹⁰ cm⁻³, the course's value"},
  {"fn": "intrinsic", "args": [309], "expect": 19575076062.66296, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "T = 309 K, 9 K warmer: n_i = 1.96×10¹⁰ cm⁻³, about double; the gap is crossed by a Boltzmann factor e^(−E_g/2kT)"},
  {"fn": "intrinsic", "args": [200], "expect": 114510.57989614563, "tol": 1e-09, "units": "cm⁻³", "tag": "limit-zero", "note": "T = 200 K: n_i = 1.14×10⁵ cm⁻³, five decades down; toward 0 K it goes to zero and pure silicon stops conducting"},
  {"fn": "carriers", "args": [1e+16, 0, 300], "expect": {"n": 1.000000000001e+16, "p": 9999.99999999, "kind": "n-type"}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "N_D = 10¹⁶ cm⁻³ at 300 K: n = 1.00×10¹⁶ cm⁻³, p = n_i²/n = 1.00×10⁴ cm⁻³; six decades up for electrons, six down for holes"},
  {"fn": "carriers", "args": [4e+16, 1e+17, 300], "expect": {"n": 1666.6666666666204, "p": 6.000000000000166e+16, "kind": "p-type"}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "N_D = 4×10¹⁶ and N_A = 10¹⁷ cm⁻³: p-type, p = 6.00×10¹⁶ cm⁻³ (the difference), n = 1.67×10³ cm⁻³"},
  {"fn": "carriers", "args": [1e+16, 1e+16, 300], "expect": {"n": 10000000000.0, "p": 10000000000.0, "kind": "nearly intrinsic"}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "N_D = N_A = 10¹⁶ cm⁻³: the two cancel and n = p = n_i, though the crystal is full of ions"},
  {"fn": "carriers", "args": [0, 0, 300], "expect": {"n": 10000000000.0, "p": 10000000000.0, "kind": "nearly intrinsic"}, "tol": 1e-09, "units": "cm⁻³", "tag": "limit-zero", "note": "no dopants at 300 K: n = p = n_i = 10¹⁰ cm⁻³"},
  {"fn": "carriers", "args": [1e+16, 0, 700], "expect": {"n": 1.43416663807339e+16, "p": 4341666380733900.0, "kind": "nearly intrinsic"}, "tol": 1e-09, "units": "cm⁻³", "tag": "limit-infinity", "note": "N_D = 10¹⁶ cm⁻³ at 700 K: n_i = 7.9×10¹⁵ cm⁻³ has caught up with the doping; n = 1.43×10¹⁶, p = 4.34×10¹⁵ cm⁻³, nearly intrinsic"},
  {"fn": "fermiLevel", "args": [1e+16, 0, 300], "expect": 0.3592032745070971, "tol": 1e-09, "units": "eV", "tag": "typical", "note": "N_D = 10¹⁶ cm⁻³ at 300 K: E_F sits 0.359 eV above E_i, 6 decades × 59.9 meV"},
  {"fn": "fermiLevel", "args": [0, 1e+16, 300], "expect": -0.3592032745070971, "tol": 1e-09, "units": "eV", "tag": "sign", "note": "N_A = 10¹⁶ cm⁻³ at 300 K: E_F sits 0.359 eV below E_i; p-type puts it below the middle"},
  {"fn": "fermiLevel", "args": [1e+17, 0, 300], "expect": 0.4190704869249166, "tol": 1e-09, "units": "eV", "tag": "typical", "note": "N_D = 10¹⁷ cm⁻³: ten times the doping raises E_F by one step of 59.9 meV, to 0.419 eV"},
  {"fn": "perDecade", "args": [300], "expect": 0.05986721241784519, "tol": 1e-09, "units": "eV", "tag": "typical", "note": "T = 300 K: (kT/q)·ln 10 = 59.9 mV per decade of density"},
  {"fn": "edgeMargin", "args": [1e+16, 0, 300], "expect": 0.20079672549290295, "tol": 1e-09, "units": "eV", "tag": "typical", "note": "N_D = 10¹⁶ cm⁻³: E_F is 0.201 eV below the conduction band edge, far more than 3kT = 78 meV, so Boltzmann statistics hold"},
  {"fn": "edgeMargin", "args": [1e+19, 0, 300], "expect": 0.021195088239393423, "tol": 1e-09, "units": "eV", "tag": "breaks", "note": "N_D = 10¹⁹ cm⁻³: E_F is only 21 meV below the edge, under 3kT; the silicon is nearly degenerate and n = n_i e^((E_F−E_i)/kT) no longer holds"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Start from pure silicon (both sliders at none), then add 10¹⁶ cm⁻³ donors. The electrons rise six decades. What do
   the holes do?
   Why: They fall six decades, to 10⁴ cm⁻³. Pairs are still made at the same rate, but with a million times more
   electrons about, each hole is filled a million times sooner, so np stays at n_i².
2. Raise N_D from 10¹⁶ to 10¹⁷ cm⁻³. How far does E_F move?
   Why: Up by 59.9 meV, one decade's worth. E_F follows the logarithm of the density, so every tenfold step moves it
   the same amount.
3. Set N_D to 4×10¹⁶ cm⁻³ (slider at 16.6) and N_A to 10¹⁷ cm⁻³. n-type or p-type, and how many majority carriers?
   Why: p-type, with about 6×10¹⁶ cm⁻³ holes. Each donor's spare electron fills one acceptor's missing bond, so the two
   cancel and only the difference is left.
4. Keep N_D = 10¹⁶ cm⁻³ and warm the sample from 300 K toward 700 K. When does it stop being n-type?
   Why: The label changes at 590 K, where n_i has reached a tenth of the doping and n is no longer 100 times p. Until
   then n stays pinned at N_D while p climbs as n_i²/N_D; near 700 K heat makes pairs about as fast as the donors gave
   electrons, and n and p close in.
5. Push N_D to 10¹⁹ cm⁻³. What does the warning mean?
   Why: E_F has come within 3kT of the conduction band. The logarithm assumes most states near E_F are empty, which is
   no longer true, so it places E_F too low; the silicon is close to degenerate.

## Misconceptions

- "Adding donors adds electrons and leaves the holes alone." What the tool shows instead: p falls by exactly the factor
  n rises; on the ladder they move as mirror images about n_i.
- "With both dopants present, the material behaves as if doped by their sum." What the tool shows instead: N_D = N_A
  gives n = p = n_i, and N_A = 10¹⁷ with N_D = 4×10¹⁶ cm⁻³ gives 6×10¹⁶ cm⁻³ holes, the difference.
- "Doping moves the bands." What the tool shows instead: E_c and E_v stay put; only E_F moves, 59.9 meV per decade.
- "A doped semiconductor's majority density rises steeply with temperature." What the tool shows instead: in figure 2,
  n stays flat at N_D for hundreds of kelvin while p climbs by decades.

## Quiz hooks

- L2 looks like: finds n and p for a given N_D or N_A with np = n_i²; takes the difference for a compensated sample;
  computes E_F − E_i = (kT/q)·ln(n/n_i).
- L3 looks like: explains why np is fixed (generation set by temperature, recombination by the product); says why
  doping lowers the minority density; reads 60 mV per decade off the log scale and uses it without a calculator;
  explains why n_i grows so fast with temperature (a Boltzmann factor in E_g/2kT).
- L4 looks like: knows when the formulas fail (degenerate doping near 10¹⁹ cm⁻³, freeze-out at low temperature, the
  intrinsic limit at high temperature) and why that sets an upper operating temperature for silicon devices; uses the
  potentials from intrinsic as the building blocks of φ_bi and φ_p.
- Missteps:
  - adds N_D and N_A instead of taking the difference
  - forgets that the minority density falls when the majority rises
  - uses log₁₀ where ln belongs in (kT/q)·ln(n/n_i), or the reverse with 60 mV per decade
  - puts E_F above E_i for p-type material
  - treats n_i as a constant when the temperature changes
- Seeds, to be varied and never asked word for word:
  - predict: a sample's acceptor doping is raised a hundredfold; how many millivolts does E_F move, and which way?
  - explain: why a crystal full of dopant ions can still have n = p = n_i.
  - limit: the temperature raised until n_i matches the doping; what happens to the device made from it?
  - transfer: two regions of the same chip, one n-type at 10¹⁷ cm⁻³ and one p-type at 10¹⁵ cm⁻³; what potential step
    must form between them if they touch, from the two ladders alone?

## Where this shows up

- `drift-current`: n and p set the current a field drives, J = q(nμ_n + pμ_p)E, and the minority term is decades down.
- `built-in-potential`: the step across a junction is φ_n − φ_p, the two potentials read off this ladder.
- `threshold-voltage`: the MOS body's φ_p = −(kT/q)·ln(N_A/n_i) is this tool's E_F for p-type material.
- `diode-iv`: the minority densities n_i²/N_A and n_i²/N_D set a diode's saturation current.
- Later: EE 130: Fermi–Dirac statistics, degenerate doping and band-gap narrowing.

## Page text

- Header `Concept:` n and p are mirror images about n_i on a log scale, because np = n_i², and that log scale is an
  energy scale: E_F moves 59.9 meV per decade of density.
- Header `Course:` EE 105 (energy bands, intrinsic carriers, mass-action law, doping, potential and doping)
- Header `Play with:` The donor and acceptor doping and the temperature
- Header `Should click:` Adding electrons removes holes, the dopants cancel to their difference, and every decade of
  density moves the Fermi level the same 59.9 meV.
- Title: Carriers and doping
- Lede: Pure silicon has a few free electrons, each with a hole left behind. Add donors and the electrons outnumber the
  holes by a million; add acceptors and the reverse. Move the doping and the temperature, and watch the electrons, the
  holes and the Fermi level move together.
- Caption of `ladder`: Left, the bands with the carriers drawn to scale: electrons in blue, holes in orange. Right, the
  same heights read as densities: n sits as far above n_i as p sits below.
- Caption of `heat`: The densities against temperature. Drag the triangle or press anywhere in the plot; focused,
  ← → move it 5 K, with Shift 50 K.
- What should click:
  - **n and p are mirror images.** Pairs are made at a rate set by temperature and destroyed at a rate set by n·p, so
    in equilibrium np = n_i². On a log scale n sits as far above n_i as p sits below it.
  - **The dopants cancel.** Each donor's spare electron can fill one acceptor's missing bond, so only N_D − N_A counts.
  - **The log scale is an energy scale.** n = n_i·e^((E_F − E_i)/kT), so each tenfold step in density moves E_F by
    (kT/q)·ln 10 = 59.9 meV. The same number in volts is the material's potential from intrinsic silicon, and every
    built-in potential is a difference of two of them.
  - **Heat makes pairs.** n_i is a Boltzmann factor in E_g/2kT and doubles about every 9 K near 300 K. A doped sample's
    majority density stays at the doping until n_i catches up; then it is no longer n-type or p-type.

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
