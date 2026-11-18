# Plan: Drift and mobility

```json plan
{
  "id": "drift-and-mobility",
  "title": "Drift and mobility",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["drift-current", "mobility", "resistivity", "velocity-saturation"],
  "prerequisites": ["electrons-and-holes", "doping", "mass-action-law", "ohms-law"],
  "size": "L",
  "tool": "devices/semiconductors/drift-and-mobility.html",
  "checks": "plans/checks/drift-and-mobility.py"
}
```

## Concept

Carriers in silicon move at about 10⁷ cm/s in random directions and are knocked off course by a collision every few
tenths of a picosecond. A field adds a small push between collisions, so on average they creep along it at v = μE,
where the mobility μ = qτ_c/m* says how far one push gets before the next collision undoes it. Current density is
charge × density × that velocity, J = q(nμ_n + pμ_p)E, which is Ohm's law for a doped bar. Dopant ions are extra
obstacles, so mobility falls as doping rises; and at high fields the drift stops growing near 10⁷ cm/s.

## Picture

The page has a `.bench`: the left column holds figure 1 and the controls under it; the right column (`aside`) holds the
readouts. Under the bench, a `.pair`: figure 2 on the left and figure 3 on the right.

Silicon at 300 K: n_i = 10¹⁰ cm⁻³, q = 1.602×10⁻¹⁹ C, kT/q = 0.02585 V; conductivity masses m*_n = 0.26 m₀ and
m*_p = 0.39 m₀ with m₀ = 9.109×10⁻³¹ kg. One kind of dopant at a time, fully ionised.

**Figure 1, `lattice`, viewBox 640 by 300.** A slowed-down picture of the majority carriers. The box runs from x = 20 to
x = 620 and from y = 50 to y = 290, drawn with a `--line` border: 600 nm by 240 nm, 1 px per nm.
- The lattice: dots of radius 1 px in `--grid` every 40 px.
- The dopant ions: round(3·(log₁₀N − 13)) ions at fixed pseudo-random places (the same places for the same count),
  drawn as a circle of radius 5 px in `--ink-3` with "+" inside for donors or "−" for acceptors. A note at the bottom
  right inside the box, in `--ink-3`: "ions not to scale".
- The carriers: 40 majority carriers, dots of radius 3.5 px in `--c1` (electrons) or `--c2` (holes), each with a trail of
  its last 40 positions (0.2 ps) at opacity 0.35. Carrier 0 is drawn larger (radius 5 px) with a trail of its last 600
  positions (3 ps),
  so its zigzag between collisions is visible.
- The field: an arrow along the top from x = 60 to x = 580 at y = 26, pointing right, in `--c3`, labelled at its left end
  "E = 1.00 kV/cm".
- The time line, top right, `--ink-3`: "t = 12.40 ps (1 s of animation is 1 ps)".
- Each carrier starts at a random place with speed v_th in a random direction. Every frame the simulation advances in
  steps of 0.005 ps, 1 ps per second of real time, calling `stepCarrier` with the acceleration from `acceleration`, the
  collision time from `collisionTime` (in ps) and the thermal speed from `thermalVelocity` (in nm/ps), and two fresh
  `Math.random()` numbers per carrier per step. The simulation keeps τ_c fixed at all fields.

**Figure 2, `mobility`, viewBox 480 by 300.** μ against N, both log. Plot area from x = 60 to x = 460 (N from 10¹⁴ to
10²⁰ cm⁻³) and y = 20 to y = 260 (μ from 50 to 2000 cm²/(V·s)), grid lines at each decade of N and at 50, 100, 200,
500, 1000 and 2000. Drawn: `mobility("n", N)` in `--c1` and `mobility("p", N)` in `--c2`, 2.4 px, 200 points, labelled
"μ_n" and "μ_p" at their left ends; a dashed `--ink-2` vertical line at the current N; a dot on each curve there. Axis
names "N (cm⁻³)" and "μ (cm²/V·s)".

**Figure 3, `velocity`, viewBox 480 by 300.** Drift speed against field, both log. Plot area as figure 2, E from 10 to
10⁶ V/cm across, v from 10³ to 10⁸ cm/s up. Drawn: `velocity` for electrons in `--c1` and holes in `--c2`, 2.4 px;
`driftVelocity` (the plain μE) for each, dashed (5 4) 1.2 px in the same colours; a dotted `--ink-3` horizontal line at
`thermalVelocity("n")` labelled "electrons' thermal speed"; a dashed `--c3` vertical line at the current E; a dot on each
solid curve there. Axis names "E (V/cm)" and "v (cm/s)".

**Readouts, in the aside,** in `.read`:
- "N = 1.00×10¹⁶ cm⁻³ donors" (or "acceptors").
- "n = 1.00×10¹⁶ cm⁻³" in `--c1`, "p = 1.00×10⁴ cm⁻³" in `--c2`, from `carriers`.
- "μ_n = 1218 cm²/V·s" in `--c1`, "μ_p = 437 cm²/V·s" in `--c2`.
- For the majority carrier: "τ_c = μm*/q = 0.180 ps", "thermal speed = 2.29×10⁷ cm/s", "drift μE = 1.22×10⁶ cm/s", and
  "with saturation: 1.21×10⁶ cm/s" from `velocity`, in the carrier's colour.
- "J = 1.95 kA/cm²" in `--c4`, large (`.big`), then "J = q(nμ_n + pμ_p)E, along E; ρ = 0.512 Ω·cm" (ρ in Ω·cm, three
  significant figures, no prefix), "R_□ = 5.12 kΩ/□ for a layer 1 µm thick", "R = 51.2 kΩ for a bar 100 µm × 10 µm × 1 µm".
- From the simulation: "measured drift so far: 1.19×10⁶ cm/s over 12.4 ps (the simulation's μE: 1.22×10⁶ cm/s)", the mean
  displacement of the 40 carriers along x (with `laps` counted) divided by the elapsed time.
- Above 10 kV/cm, in `--accent`: "the simulation keeps τ_c fixed, so it never saturates; real carriers are slower (figure 3)".
- Numbers have three significant figures; densities are written as a×10ⁿ, and other values with SI prefixes.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| electrons: density, mobility, velocity | n, μ_n | `--c1` |
| holes: density, mobility, velocity | p, μ_p | `--c2` |
| electric field | E | `--c3` |
| current density | J | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| type | two buttons, "n-type (donors)" and "p-type (acceptors)" | the dopant | n, p | | n | Tab and Enter |
| doping | slider, log | N in cm⁻³, slider value log₁₀ N | 10¹⁴ to 10¹⁹ (14 to 19) | 0.1 decade | 10¹⁶ (16) | arrows: one step |
| field | slider, log | E in V/cm, slider value log₁₀ E | 10 V/cm to 100 kV/cm (1 to 5) | 0.05 decade | 1 kV/cm (3) | arrows: one step |
| play | button, "pause" or "play" | | | | playing, or paused under prefers-reduced-motion | Enter |
| step | button, "advance 1 ps" | | | | | Enter |
| restart | button, "restart the carriers" | | | | | Enter |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "N = 1.00×10¹⁶ cm⁻³", "E = 1.00 kV/cm".
- What moves when each control changes: type, doping and field redraw figures 2 and 3 and the readouts, and restart the
  simulation (new carriers, t = 0). "advance 1 ps" runs 200 steps at once and redraws. "restart the carriers" starts the
  simulation again with the same settings.
- Reset: n-type, N = 10¹⁶ cm⁻³, E = 1 kV/cm, simulation restarted, playing (paused under prefers-reduced-motion).
- Motion: figure 1 animates while playing. Under prefers-reduced-motion it starts paused, and "advance 1 ps" moves it on;
  the trails show where each carrier went. Nothing else moves, and nothing is redrawn while paused.
- The one thing that should click: the drift is a small bias on a fast random motion; the mobility is how much of each
  push survives to the next collision, so more obstacles (dopants) mean a lower mobility and a resistivity that falls
  less than the doping rises.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. carrier is "n" (electrons) or "p"
(holes); kind is "n" (donors) or "p" (acceptors); N in cm⁻³; E in V/cm; lengths in cm unless stated.

### `mobility(carrier, N)`

- Returns: μ in cm²/(V·s): μ_min + Δ/(1 + (N/N_ref)^0.88), with electrons μ_min = 88, Δ = 1252, N_ref = 1.26×10¹⁷ and
  holes μ_min = 54.3, Δ = 407, N_ref = 2.35×10¹⁷.
- Valid for: silicon at 300 K, N the total ionised doping (N_D + N_A).
- Approximation: a fit to measured silicon (the Caughey–Thomas form with Arora's 300 K parameters), good to about 10 %.

### `carriers(kind, N)`

- Returns: `{ n, p }` in cm⁻³: the majority density N/2 + √((N/2)² + n_i²) and the minority density n_i²/(majority).
- Formula: charge neutrality with full ionisation and np = n_i².

### `conductivity(kind, N)`, `resistivity(kind, N)`, `currentDensity(kind, N, E)`

- Return: σ = q(nμ_n + pμ_p) in S/cm (μ_n and μ_p both at the same N); ρ = 1/σ in Ω·cm; J = σE in A/cm².
- Sign convention: J points along E for both carriers.
- Approximation: low field (μ constant).

### `driftVelocity(carrier, N, E)` and `velocity(carrier, N, E)`

- Return: the speed in cm/s: μE; and μE/(1 + (μE/v_sat)^β)^(1/β) with electrons v_sat = 10⁷ cm/s, β = 2, and holes
  v_sat = 8×10⁶ cm/s, β = 1.
- Sign convention: magnitudes. Electrons drift against E, holes along it.
- Approximation: the saturating form is a fit; μE alone fails above about 10⁴ V/cm.

### `collisionTime(carrier, N)` and `thermalVelocity(carrier)`

- Return: τ_c = μm*/q in s (μ converted to m²/(V·s)); and √(3kT/m*) in cm/s.
- Approximation: the Drude picture with one collision time and the conductivity mass.

### `barResistance(kind, N, L, W, t)` and `sheetResistance(kind, N, t)`

- Return: R = ρL/(W·t) in Ω and R_□ = ρ/t in Ω per square, for lengths in cm.

### `acceleration(carrier, E)`

- Returns: qE/m* in nm/ps² (1 m/s² = 10⁻¹⁵ nm/ps²), negative for electrons.

### `stepCarrier(c, a, dt, tau, vth, r1, r2, width, height)`

- Arguments: c = `{ x, y, vx, vy, laps }` in nm and nm/ps; a in nm/ps²; dt and tau in ps; vth in nm/ps; r1 and r2 random
  numbers in [0, 1); width and height of the box in nm.
- Returns: the new c. First vx += a·dt. If r1 < 1 − e^(−dt/tau), a collision: vx = vth·cos 2πr2, vy = vth·sin 2πr2.
  Then x += vx·dt and y += vy·dt. x wraps round the box, adding 1 to laps for each wrap to the right and taking 1 for
  each to the left; y reflects off 0 and height (position mirrored, vy negated).
- Approximation: each collision forgets the old velocity entirely; between collisions the carrier moves freely.

## Check cases

Computed by `plans/checks/drift-and-mobility.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "mobility", "args": ["n", 1e+16], "expect": 1218.4069532889587, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "typical", "note": "electrons in silicon with 10¹⁶ cm⁻³ dopants: about 1220 cm²/(V·s)"},
  {"fn": "mobility", "args": ["p", 1e+16], "expect": 437.48406060211533, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "typical", "note": "holes at the same doping: about 437 cm²/(V·s); electrons outrun them about 2.8 times"},
  {"fn": "mobility", "args": ["n", 1e+19], "expect": 114.10827586472902, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "typical", "note": "electrons with 10¹⁹ cm⁻³ dopants: about 114 cm²/(V·s), a twelfth of the clean-crystal value: the ions scatter them"},
  {"fn": "mobility", "args": ["n", 1000000000000.0], "expect": 1339.9593309393322, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "limit-zero", "note": "almost no dopants: the lattice alone scatters, μ_n → 88 + 1252 = 1340 cm²/(V·s)"},
  {"fn": "mobility", "args": ["n", 1e+22], "expect": 88.06108143339878, "tol": 1e-09, "units": "cm²/(V·s)", "tag": "limit-infinity", "note": "enormous doping: the fit's floor, close to 88 cm²/(V·s)"},
  {"fn": "carriers", "args": ["n", 1e+16], "expect": {"n": 1.000000000001e+16, "p": 9999.99999999}, "tol": 1e-09, "units": "cm⁻³", "tag": "typical", "note": "10¹⁶ cm⁻³ donors: n = 10¹⁶ cm⁻³ and p = n_i²/n = 10⁴ cm⁻³, twelve decades fewer"},
  {"fn": "carriers", "args": ["p", 1000000.0], "expect": {"n": 9999500012.5, "p": 10000500012.5}, "tol": 1e-09, "units": "cm⁻³", "tag": "limit-zero", "note": "10⁶ cm⁻³ acceptors, far below n_i = 10¹⁰ cm⁻³: n and p both stay near n_i; the doping barely registers"},
  {"fn": "resistivity", "args": ["n", 1e+16], "expect": 0.5123244935999901, "tol": 1e-09, "units": "Ω·cm", "tag": "typical", "note": "n-type, 10¹⁶ cm⁻³: ρ = 1/(q n μ_n) = 0.51 Ω·cm"},
  {"fn": "resistivity", "args": ["n", 1e+17], "expect": 0.08029180540179913, "tol": 1e-09, "units": "Ω·cm", "tag": "typical", "note": "ten times the doping: ρ = 0.0857 Ω·cm, only 6.4 times lower, because μ_n fell from 1218 to 777 cm²/(V·s)"},
  {"fn": "resistivity", "args": ["p", 1e+16], "expect": 1.4268399275663572, "tol": 1e-09, "units": "Ω·cm", "tag": "typical", "note": "p-type, 10¹⁶ cm⁻³: ρ = 1.43 Ω·cm, nearly three times the n-type bar's, because holes are slower"},
  {"fn": "currentDensity", "args": ["n", 1e+16, 1000], "expect": 1951.8879391715645, "tol": 1e-09, "units": "A/cm²", "tag": "typical", "note": "n-type 10¹⁶ cm⁻³ in a field of 1 kV/cm: J = σE = 1.95 kA/cm²"},
  {"fn": "driftVelocity", "args": ["n", 1e+16, 1000], "expect": 1218406.9532889586, "tol": 1e-09, "units": "cm/s", "tag": "typical", "note": "electrons at 10¹⁶ cm⁻³ in 1 kV/cm: v = μE = 1.22×10⁶ cm/s, about a twentieth of their thermal speed"},
  {"fn": "thermalVelocity", "args": ["n"], "expect": 22903409.174605817, "tol": 1e-09, "units": "cm/s", "tag": "typical", "note": "electrons at 300 K with m* = 0.26 m₀: √(3kT/m*) = 2.29×10⁷ cm/s, in random directions"},
  {"fn": "collisionTime", "args": ["n", 1e+16], "expect": 1.8012496402948644e-13, "tol": 1e-09, "units": "s", "tag": "typical", "note": "electrons at 10¹⁶ cm⁻³: τ_c = μm*/q = 0.18 ps between collisions"},
  {"fn": "velocity", "args": ["n", 1e+16, 1000], "expect": 1209462.695113649, "tol": 1e-09, "units": "cm/s", "tag": "typical", "note": "at 1 kV/cm the saturating law gives 1.21×10⁶ cm/s, within 1% of μE"},
  {"fn": "velocity", "args": ["n", 1e+16, 100000], "expect": 9966488.189641675, "tol": 1e-09, "units": "cm/s", "tag": "breaks", "note": "at 100 kV/cm μE would be 1.22×10⁸ cm/s; the electrons actually reach 9.97×10⁶ cm/s. v = μE no longer holds"},
  {"fn": "velocity", "args": ["n", 1e+16, 1000000000.0], "expect": 9999999.99966319, "tol": 1e-09, "units": "cm/s", "tag": "limit-infinity", "note": "an absurd field: the speed stops at v_sat = 10⁷ cm/s"},
  {"fn": "barResistance", "args": ["n", 1e+16, 0.01, 0.001, 0.0001], "expect": 51232.449359999, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "a bar 100 µm long, 10 µm wide, 1 µm thick, n-type 10¹⁶ cm⁻³: R = ρL/(Wt) = 51.1 kΩ"},
  {"fn": "sheetResistance", "args": ["n", 1e+16, 0.0001], "expect": 5123.244935999901, "tol": 1e-09, "units": "Ω/□", "tag": "typical", "note": "the same layer 1 µm thick: R_□ = ρ/t = 5.11 kΩ per square; the bar is 10 squares long"},
  {"fn": "acceleration", "args": ["n", 1000], "expect": -67.64231487033112, "tol": 1e-09, "units": "nm/ps²", "tag": "sign", "note": "electrons in +1 kV/cm are pushed the other way: −67.6 nm/ps²"},
  {"fn": "stepCarrier", "args": [{"x": 100, "y": 50, "vx": 0, "vy": 0, "laps": 0}, -67.6, 0.01, 0.18, 229, 0.9, 0.25, 600, 240], "expect": {"x": 99.99324, "y": 50.0, "vx": -0.6759999999999999, "vy": 0, "laps": 0}, "tol": 1e-09, "units": "nm, nm/ps", "tag": "sign", "note": "an electron at rest, no collision this step (0.9 > 1 − e^(−0.01/0.18)): after 0.01 ps it moves −0.00676 nm, against the field"},
  {"fn": "stepCarrier", "args": [{"x": 599, "y": 50, "vx": 200, "vy": 0, "laps": 3}, 0, 0.01, 0.18, 229, 0.01, 0.25, 600, 240], "expect": {"x": 599.0, "y": 52.29, "vx": 1.4022205850237195e-14, "vy": 229.0, "laps": 3}, "tol": 1e-09, "units": "nm, nm/ps", "tag": "other", "note": "a collision (0.01 < 0.054) turns the carrier to point along +y at 229 nm/ps; it stays inside the box"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. At 1 kV/cm, how fast do the electrons drift compared with how fast they move?
   Why: About a twentieth: 1.2×10⁶ cm/s of drift on top of 2.3×10⁷ cm/s of random motion. Watch carrier 0: it zigzags in
   every direction, and only its average creeps against the field.
2. Raise the doping from 10¹⁶ to 10¹⁷ cm⁻³. Does the resistivity fall ten times?
   Why: No, about 6.4 times. Ten times more carriers, but the extra ions scatter them and μ_n falls from 1218 to
   777 cm²/(V·s).
3. Switch to p-type at the same doping. Is the bar a better or worse conductor?
   Why: Worse, about 2.8 times: holes are heavier and their mobility is lower.
4. Which way do the electrons go, and which way does their current flow?
   Why: The electrons drift against E; their charge is negative, so their current flows along E. Holes drift and carry
   current along E. Both currents point the same way.
5. Turn the field up to 100 kV/cm. Does the drift keep growing ten times per decade?
   Why: No: figure 3 bends over near 10⁷ cm/s, close to the thermal speed. The carriers lose energy to the lattice as fast
   as the field gives it. The simulation, which keeps τ_c fixed, does not show this.
6. In an n-type bar with 10¹⁶ cm⁻³ donors, why can the holes be ignored?
   Why: There are 10⁴ cm⁻³ of them against 10¹⁶ cm⁻³ electrons: twelve decades fewer, and slower too.

## Misconceptions

- "Carriers move along the field at the drift velocity." What the tool shows instead: carrier 0 darts in all directions
  at the thermal speed; only the average of many carriers over many collisions creeps along.
- "More doping, proportionally less resistance." What the tool shows instead: tenfold doping gives a 6.4-fold drop in ρ,
  and figure 2 shows μ falling as N grows.
- "Electron current flows the way the electrons go." What the tool shows instead: the electrons drift left while J, in
  `--c4`, is reported along E, to the right.
- "Drift velocity grows without limit with the field." What the tool shows instead: figure 3's solid curves flatten
  near 10⁷ cm/s while the dashed μE lines keep rising.

## Quiz hooks

- L2 looks like: computes v = μE, J = qnμE, ρ = 1/(qNμ) and R = ρL/(Wt) from given values; reads μ off a chart at a
  doping.
- L3 looks like: explains mobility as μ = qτ_c/m* (pushes undone by collisions); explains why μ falls with doping and why
  electrons are faster; predicts how ρ changes when doping changes, including the fall in μ; says why minority
  carriers can be ignored; gets the directions of drift and current right for both carriers.
- L4 looks like: knows μE fails at high field and what velocity saturation does to short transistors; uses total
  ionised doping (N_D + N_A) for μ in a compensated sample; estimates a resistor's value and its sensitivity to doping.
- Missteps:
  - takes μ at the net doping instead of the total ionised doping
  - assumes ρ falls in proportion to the doping
  - gives the electron current the electrons' direction
  - uses the drift velocity as the carriers' speed
  - keeps v = μE at fields above 10⁴ V/cm
- Seeds, to be varied and never asked word for word:
  - predict: a bar's doping is raised a hundredfold; by roughly how much does its resistance fall, and why less than a
    hundred?
  - explain: why a heavier carrier, or a crystal with more ions in it, has a lower mobility.
  - limit: the field across a short bar raised by decades: where does Ohm's law for the bar stop holding?
  - transfer: an IC resistor of a given sheet resistance must be 10 kΩ: how many squares, and what happens to it if the
    implant dose is 20 % high?

## Where this shows up

- `drift-current`: J = q(nμ_n + pμ_p)E, the field's small push averaged over many collisions.
- `mobility`: μ = qτ_c/m*; it falls with doping and is 2 to 3 times higher for electrons.
- `resistivity`: ρ ≈ 1/(qNμ), set by the majority carriers alone.
- `velocity-saturation`: the drift stops near 10⁷ cm/s, close to the thermal speed.
- `doping`: the dopants set the carriers and, as obstacles, the mobility.
- `triode-region`: a MOSFET's channel is a sheet of electrons drifting in the field from source to drain: the same J = qnμE.
- Later: EE 105's MOSFET: μ_nC_ox is mobility times the channel's charge per volt; EE 130: scattering, high fields and
  hot carriers.

## Page text

- Header `Concept:` Carriers move fast in random directions and collide every few tenths of a picosecond; a field adds a
  small average drift v = μE, so J = q(nμ_n + pμ_p)E, and dopants, as extra obstacles, lower μ.
- Header `Course:` EE 105 (carriers, drift, mobility, resistivity, velocity saturation)
- Header `Play with:` n- or p-type doping, the doping density, the field; a slowed-down simulation of the carriers
- Header `Should click:` The drift is a small bias on fast random motion; mobility is how much of each push survives to the
  next collision, so more dopants mean lower mobility and a resistivity that falls less than the doping rises.
- Title: Drift and mobility
- Lede: Inside a silicon bar the carriers race about at ten million centimetres per second, bouncing off the lattice and
  the dopant ions. A field cannot stop that; it only tilts it. Between collisions each carrier gains a little speed
  along the field, and on average they creep along at v = μE. That creep is the current.
- Caption of `lattice`: 600 nm of silicon, slowed so that 1 s is 1 ps. The large dot leaves its full trail: a zigzag
  of free flights between collisions.
- Caption of `mobility`: Mobility against doping. More ions, more collisions, lower mobility.
- Caption of `velocity`: Drift speed against field. The dashed lines are μE; the solid curves bend over near 10⁷ cm/s.
- What should click:
  - **Fast motion, slow drift.** The carriers move at about 2×10⁷ cm/s in random directions. A field of 1 kV/cm adds an
    average of about 10⁶ cm/s along it: a small tilt on a fast random walk.
  - **Mobility is a push that survives.** Between collisions the field accelerates a carrier by qE/m*. A collision every
    τ_c undoes it, so the average drift is (qτ_c/m*)E = μE. Heavier carriers or more frequent collisions, lower μ.
  - **Dopants are obstacles too.** Every ionised dopant scatters carriers. Tenfold doping gives tenfold carriers but a
    lower μ, so ρ falls less than tenfold.
  - **Current follows the field.** Electrons drift against E, holes along it; both currents point along E:
    J = q(nμ_n + pμ_p)E. In a doped bar the majority term is all that matters.

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
