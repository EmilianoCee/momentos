# Plan: Bode plot from poles and zeros

```json plan
{
  "id": "bode-plot",
  "title": "Bode plot from poles and zeros",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["bode-plot", "transfer-function", "poles-and-zeros"],
  "prerequisites": ["phasors-impedance", "first-order-system"],
  "size": "M",
  "tool": "systems/bode-plot.html",
  "checks": "plans/checks/bode-plot.py"
}
```

## Concept

A transfer function is a product of poles and zeros. On log axes each one bends |H(jω)| by 20 dB per decade from its
corner frequency on, and turns the phase by 90° over the two decades around that corner, so a Bode plot is a sum of
straight lines. An RC or RL circuit is the simplest case: one pole. Shared with EE 120, so it is built once for both
courses.

## Picture

The page has a `.bench`: the left column holds figures 1 and 2 stacked, the controls under figure 2, and figure 4
under the controls; the right column (`aside`) holds figure 3 and the readouts under it.

All transfer functions have the form H(s) = K · s^m · (1 + s/z₁)(1 + s/z₂) / ((1 + s/p₁)(1 + s/p₂)(1 + s/p₃)): a pole at
s = −p and a zero at s = −z, with p and z positive corner frequencies in rad/s, and m zeros at the origin.

**Figure 1, `mag`, viewBox 640 by 300.** Magnitude in dB against ω in rad/s. The plot area runs from x = 56 to
x = 620 and from y = 16 to y = 262. The ω axis is logarithmic, 10⁰ to 10⁷ rad/s (seven decades, 80.57 px each), with
a grid line at each decade labelled 10⁰ to 10⁷ under the axis and "ω (rad/s)" at the right end. The dB axis is
linear: −80 dB to +20 dB in circuit mode and −120 dB to +40 dB in free mode, with a grid line and a label every
20 dB, and "|H| (dB)" at the top left. Drawn in this order:
1. A dotted vertical `--c3` line at each pole and zero corner, through both figure 1 and figure 2.
2. The straight-line sketch from `asymDb`: dashed (6 4), 1.6 px, `--c1` at opacity 0.45.
3. The exact curve from `magDb`, 2.4 px, `--c1`, sampled at 400 points evenly spaced in log ω. Values outside the
   dB range are clipped to the plot area.
4. The pole and zero markers on the ω axis line (y = 262), in `--c3`: a cross of half-size 6 px for a pole, a
   circle of radius 6 px for a zero. Two markers at the same ω are drawn 8 px apart vertically.
5. In circuit mode, at the corner: a small `--c1` dot on the exact curve and the label "−3 dB" beside it.
6. The cursor: a vertical line in `--ink-2`, dashed (3 3), across figures 1 and 2, with a `--c1` dot where it
   meets the exact magnitude curve and a 14 px wide triangle handle above the plot area, pointing down.

**Figure 2, `phase`, viewBox 640 by 300.** Phase in degrees against the same ω axis, plot area as in figure 1. The
phase axis is linear: −90° to +90° in circuit mode and −270° to +180° in free mode, with a grid line every 45° and
a label every 45° in circuit mode and every 90° in free mode. "∠H (°)" at the top left. Drawn: the corner lines
(continued from figure 1); the three-segment sketch from `asymPhaseDeg`, dashed (6 4), 1.6 px, `--c2` at opacity
0.45; the exact curve from `phaseDeg`, 2.4 px, `--c2`; in circuit mode a `--c2` dot at the corner with the label
"−45°" (low-pass) or "+45°" (high-pass); the cursor line with a `--c2` dot on the exact curve.

**Figure 3, `splane`, viewBox 360 by 300.** The s-plane, linear in both directions, σ (rad/s) across and jω (rad/s)
up, axes in `--line` with the labels "σ" at the right end and "jω" at the top. The origin sits at (300, 250). The
scale follows the cursor: the point s = jω_cursor is always drawn at (300, 50), so 200 px stand for ω_cursor rad/s.
A note under the axes says "scale: 200 px = ω, so the dot on the jω axis is always s = jω". Drawn:
- the point s = jω as a 5 px `--ink` dot labelled "jω";
- each pole as a `--c3` cross and each zero as a `--c3` circle on the σ axis at x = 300 − 200·p/ω;
- a thin `--ink-3` line from each pole and zero to the jω point;
- at each pole and zero inside the plot, a `--c2` arc of radius 22 px between the σ axis and that line, labelled
  with the angle in degrees to the nearest degree (the angle is |phaseDeg| of that one factor);
- a pole or zero further left than x = 14 is drawn as a `--c3` arrow "◂" at x = 14 on the σ axis, with no line or
  arc, and listed at the top left as "◂ pole at −10.0 krad/s", one line each;
- a zero at the origin (the high-pass circuits) is a `--c3` circle at (300, 250), and its line is vertical: 90°.

**Readouts, under figure 3,** in `.read`:
- Circuit mode, in `--c3`: "corner ω_c = 1/(RC) = 1.00 krad/s" (or "R/L" for the RL circuits) and, on the same
  line, "f_c = 1/(2πRC) = 159 Hz".
- Free mode, in `--c3`: one line per pole and per zero, "pole p₁ = 100 rad/s (15.9 Hz)".
- At the cursor: "ω = 1.00 krad/s (159 Hz)" in `--ink`; "|H| = −3.01 dB = ×0.707" in `--c1`, large (`.big`);
  "∠H = −45.0°" in `--c2`; "delay = 785 µs" in `--c2`, written "lead = 785 µs" when the delay is negative;
  "sketch: 0 dB, 0°" in `--ink-3` (the straight-line values at the cursor).
- Every number has three significant figures and an SI prefix (µ, m, k, M): `eng(785e-6, "s")` gives "785 µs".

**Figure 4, `wave`, viewBox 640 by 240.** Left part (x from 0 to 230): in circuit mode, the circuit, drawn in
`--ink`: a sine source on the left, the series element on the top wire, the shunt element from the output node to
ground, and "v_out" at the output node. RC low-pass: R in series, C in shunt. RC high-pass: C in series, R in shunt.
RL low-pass: L in series, R in shunt. RL high-pass: R in series, L in shunt. Each element is labelled with its value
("1 kΩ", "1 µF"). In free mode the left part shows H(s) written out with the current corners, in `--ink`, one factor
per line, the zeros above a rule and the poles below it.
Right part (x from 250 to 630, centre line y = 120): the input and the output against time, over two periods of
2π/ω_cursor. The input 1 V · sin(ωt) is drawn in `--ink-2`, 1.6 px; the output from `outputAt` in `--c1`, 2.4 px.
The vertical scale is 80 px per max(1, |H|) volts, so the larger of the two fills ±80 px. Under the axis:
"t (two periods of 2π/ω = 12.6 ms)". A `--c2` bracket joins the input's first peak and the output's next peak, at
the height of the output's peak, labelled with the delay. Legend at the top right: "input 1 V" in `--ink-2`,
"output 0.707 V" in `--c1`.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| magnitude, and the output waveform | \|H\|, v_out | `--c1` |
| phase, delay, and the angles in the s-plane | ∠H | `--c2` |
| corner frequencies, pole and zero positions | ω_c, p, z | `--c3` |

The input waveform and the cursor stay neutral. `--c4` is not used.

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| mode | two buttons, "circuit" and "free" | which system is shown | circuit, free | | circuit | Tab and Enter |
| circuit | four buttons, "RC low-pass", "RC high-pass", "RL low-pass", "RL high-pass" (circuit mode only) | the circuit | the four | | RC low-pass | Tab and Enter |
| R | slider, log | R in Ω, slider value log₁₀ R | 100 Ω to 100 kΩ (2 to 5) | 0.05 decade | 1 kΩ (3) | arrows: one step |
| C | slider, log (RC circuits) | C in F, slider value log₁₀ C | 10 nF to 10 µF (−8 to −5) | 0.05 decade | 1 µF (−6) | arrows: one step |
| L | slider, log (RL circuits) | L in H, slider value log₁₀ L | 10 mH to 10 H (−2 to 1) | 0.05 decade | 100 mH (−1) | arrows: one step |
| poles | three buttons, "1", "2", "3" (free mode only) | number of poles | 1 to 3 | | 2 | Tab and Enter |
| zeros | three buttons, "0", "1", "2" (free mode only) | number of zeros | 0 to 2 | | 0 | Tab and Enter |
| pole and zero markers | draggable handles on the ω axis of figure 1 (free mode only) | p₁, p₂, p₃, z₁, z₂ in rad/s | 10⁰ to 10⁷ rad/s | 0.05 decade | p = 10², 10⁴, 10⁶; z = 10³, 10⁵ | ← → one step, Shift + ← → 0.5 decade |
| cursor | draggable handle: the triangle above figure 1, or a press anywhere in the plot area of figure 1 or 2 away from a marker | ω in rad/s | 10⁰ to 10⁷ rad/s | 0.05 decade | 10³ rad/s | ← → one step, Shift + ← → 0.5 decade |
| cursor to corner | button | | | | | Enter |
| reset | button | | | | | Enter |

- Free mode uses K = 1 and m = 0. Circuit mode uses `circuitSystem`.
- A slider's readout beside it gives the value with its unit: "R = 1.00 kΩ".
- In circuit mode the pole marker is drawn but is not a handle: R and C or L move it.
- What moves when each control changes: mode, circuit, R, C, L, the number of poles and zeros, and the markers
  change the system, so every figure and readout is redrawn. The cursor moves the cursor line, the dots, figure 3's
  scale, figure 4's waveforms and the "at the cursor" readouts.
- "cursor to corner" puts the cursor at ω_c in circuit mode and at p₁ in free mode.
- Reset: circuit mode, RC low-pass, R = 1 kΩ, C = 1 µF, L = 100 mH, two poles and no zeros at their starting
  positions, cursor at 10³ rad/s.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: at the corner the real and imaginary parts of 1 + jω/p are equal, so the
  magnitude is 1/√2 (−3 dB) and the phase is −45°, and the phase needs a decade on each side to finish its turn.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. A system `sys` is an object
`{ "gain": K, "origin": m, "poles": [p, ...], "zeros": [z, ...] }`: K a pure number (in (rad/s)^(−m)), m a whole
number, each p and z a positive corner frequency in rad/s.

### `omegaRC(R, C)`

- Arguments: R in Ω, C in F.
- Returns: the corner frequency in rad/s.
- Formula: 1/(R·C).
- Valid for: R > 0, C > 0.
- Approximation: none.

### `omegaRL(R, L)`

- Arguments: R in Ω, L in H.
- Returns: the corner frequency in rad/s.
- Formula: R/L.
- Valid for: R > 0, L > 0.
- Approximation: none.

### `radToHz(w)`

- Arguments: w, an angular frequency in rad/s.
- Returns: the frequency in Hz.
- Formula: w/(2π).
- Valid for: any w.
- Approximation: none.

### `circuitSystem(kind, R, X)`

- Arguments: kind, one of "rc-low", "rc-high", "rl-low", "rl-high"; R in Ω; X the capacitance in F for "rc-…" and
  the inductance in H for "rl-…".
- Returns: a system object. With ω_c = `omegaRC(R, X)` or `omegaRL(R, X)`: for a low-pass
  `{ gain: 1, origin: 0, poles: [ω_c], zeros: [] }`; for a high-pass `{ gain: 1/ω_c, origin: 1, poles: [ω_c], zeros: [] }`,
  which is H(s) = (s/ω_c)/(1 + s/ω_c).
- Formula: from the divider. RC low-pass: (1/(sC))/(R + 1/(sC)) = 1/(1 + sRC). RC high-pass: R/(R + 1/(sC)) =
  sRC/(1 + sRC). RL low-pass: R/(R + sL) = 1/(1 + sL/R). RL high-pass: sL/(R + sL).
- Valid for: R, X > 0. The source is ideal and the output is not loaded.
- Approximation: none.

### `mag(sys, w)`

- Arguments: sys; w in rad/s.
- Returns: |H(jw)|, a pure number.
- Formula: K · w^m · Π √(1 + (w/z)²) / Π √(1 + (w/p)²).
- Valid for: w > 0.
- Approximation: none.

### `magDb(sys, w)`

- Returns: 20·log₁₀(`mag(sys, w)`), in dB.
- Approximation: none.

### `phaseDeg(sys, w)`

- Arguments: sys; w in rad/s.
- Returns: the phase of H(jw) in degrees.
- Formula: 90·m + Σ atan(w/z) − Σ atan(w/p), each atan in degrees. It is summed term by term and not wrapped, so
  three poles reach −270°.
- Sign convention: positive means the output leads the input.
- Valid for: w > 0, poles and zeros in the left half-plane.
- Approximation: none.

### `asymDb(sys, w)`

- Returns: the straight-line magnitude in dB.
- Formula: 20·log₁₀ K + 20·m·log₁₀ w + Σ max(0, 20·log₁₀(w/z)) − Σ max(0, 20·log₁₀(w/p)).
- Approximation: each factor 1 + jw/p is replaced by 1 below its corner and by jw/p above it. The error is
  largest at a corner: 3.01 dB for each pole or zero there.

### `asymPhaseDeg(sys, w)`

- Returns: the three-segment phase sketch in degrees.
- Formula: 90·m + Σ 90·r(w, z) − Σ 90·r(w, p), with r(w, c) = 0 for w ≤ c/10, 1 for w ≥ 10c, and
  (log₁₀(w/c) + 1)/2 between.
- Approximation: the arctangent is replaced by a straight line in log w across two decades. The error is largest
  at c/10 and 10c: 5.71°.

### `delaySec(sys, w)`

- Returns: the time by which the output lags the input, in s.
- Formula: −(`phaseDeg(sys, w)` in radians)/w.
- Sign convention: positive is a lag; a negative delay is a lead.
- Approximation: none, for a sinusoid in steady state. The delay is only defined to within whole periods 2π/w.

### `outputAt(sys, w, t)`

- Arguments: sys; w in rad/s; t in s.
- Returns: the steady-state output in V for the input 1 V · sin(w·t).
- Formula: `mag(sys, w)` · sin(w·t + `phaseDeg(sys, w)` in radians).
- Approximation: steady state only: the transient that dies away after the input is switched on is left out.

Figure 3's angle for one pole or zero is `phaseDeg` of a system holding only that factor
(`{ gain: 1, origin: 0, poles: [p], zeros: [] }`), so the main script needs no formula of its own.

## Check cases

Computed by `plans/checks/bode-plot.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "omegaRC", "args": [1000, 1e-06], "expect": 1000.0, "tol": 1e-09, "units": "rad/s", "tag": "typical", "note": "R = 1 kΩ and C = 1 µF put the corner at 1/(RC) = 1000 rad/s"},
  {"fn": "radToHz", "args": [1000], "expect": 159.15494309189535, "tol": 1e-09, "units": "Hz", "tag": "typical", "note": "1000 rad/s is 1000/(2π) = 159.2 Hz, not 1000 Hz"},
  {"fn": "omegaRL", "args": [1000, 0.1], "expect": 10000.0, "tol": 1e-09, "units": "rad/s", "tag": "typical", "note": "R = 1 kΩ and L = 100 mH put the corner at R/L = 10 000 rad/s"},
  {"fn": "circuitSystem", "args": ["rc-low", 1000, 1e-06], "expect": {"gain": 1.0, "origin": 0, "poles": [1000.0], "zeros": []}, "tol": 1e-09, "units": "", "tag": "typical", "note": "RC low-pass, 1 kΩ and 1 µF: H(s) = 1/(1 + s/1000), one pole at 1000 rad/s"},
  {"fn": "circuitSystem", "args": ["rl-high", 1000, 0.1], "expect": {"gain": 0.0001, "origin": 1, "poles": [10000.0], "zeros": []}, "tol": 1e-09, "units": "", "tag": "typical", "note": "RL high-pass, 1 kΩ and 100 mH: H(s) = (s/10 000)/(1 + s/10 000), a zero at the origin and a pole at 10 000 rad/s"},
  {"fn": "mag", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000], "expect": 0.7071067811865476, "tol": 1e-09, "units": "", "tag": "typical", "note": "one pole at 1000 rad/s, at ω = 1000 rad/s: |H| = 1/√2 = 0.707 of the input amplitude, half the power"},
  {"fn": "magDb", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000], "expect": -3.0102999566398116, "tol": 1e-09, "units": "dB", "tag": "typical", "note": "the same point in decibels: −3.01 dB"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000], "expect": -45.0, "tol": 1e-09, "units": "°", "tag": "typical", "note": "one pole at 1000 rad/s, at ω = 1000 rad/s: the phase is −45°, not −90°"},
  {"fn": "delaySec", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000], "expect": 0.0007853981633974483, "tol": 1e-09, "units": "s", "tag": "typical", "note": "−45° at 1000 rad/s is a delay of (π/4)/1000 = 0.785 ms"},
  {"fn": "outputAt", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000, 0.002356194490192345], "expect": 0.7071067811865476, "tol": 1e-09, "units": "V", "tag": "typical", "note": "input sin(ωt) of 1 V at 1000 rad/s through one pole at 1000 rad/s: at t = 2.356 ms the output is at its peak, 0.707 V, 0.785 ms after the input's peak at 1.571 ms"},
  {"fn": "magDb", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1], "expect": -4.342942646911995e-06, "tol": 1e-09, "units": "dB", "tag": "limit-zero", "note": "one pole at 1000 rad/s, at ω = 1 rad/s, three decades below: |H| is 1 to within 0.000004 dB"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1], "expect": -0.057295760414500616, "tol": 1e-09, "units": "°", "tag": "limit-zero", "note": "the same point: the phase is only −0.057°"},
  {"fn": "magDb", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 10000000.0], "expect": -80.00000004342944, "tol": 1e-09, "units": "dB", "tag": "limit-infinity", "note": "one pole at 1000 rad/s, at ω = 10⁷ rad/s, four decades above: −80 dB, falling 20 dB per decade"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 10000000.0], "expect": -89.99427042206779, "tol": 1e-09, "units": "°", "tag": "limit-infinity", "note": "the same point: the phase has nearly finished its turn, at −89.994°"},
  {"fn": "asymDb", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 1000], "expect": 0.0, "tol": 1e-09, "units": "dB", "tag": "breaks", "note": "the straight-line sketch says 0 dB at the corner of a pole at 1000 rad/s; the true value is −3.01 dB"},
  {"fn": "magDb", "args": [{"gain": 1, "origin": 0, "poles": [1000, 1000], "zeros": []}, 1000], "expect": -6.020599913279624, "tol": 1e-09, "units": "dB", "tag": "breaks", "note": "two poles both at 1000 rad/s: the sketch still says 0 dB at the corner, the curve is at −6.02 dB"},
  {"fn": "asymPhaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 100], "expect": 0.0, "tol": 1e-09, "units": "°", "tag": "breaks", "note": "the three-segment phase sketch says 0° a decade below a pole at 1000 rad/s; the true phase there is −5.71°"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [1000], "zeros": []}, 100], "expect": -5.710593137499643, "tol": 1e-09, "units": "°", "tag": "breaks", "note": "the true phase a decade below the pole at 1000 rad/s, at 100 rad/s: −5.71°"},
  {"fn": "phaseDeg", "args": [{"gain": 0.001, "origin": 1, "poles": [1000], "zeros": []}, 1000], "expect": 45.0, "tol": 1e-09, "units": "°", "tag": "sign", "note": "RC high-pass with its corner at 1000 rad/s: at the corner the output leads by +45°"},
  {"fn": "delaySec", "args": [{"gain": 0.001, "origin": 1, "poles": [1000], "zeros": []}, 1000], "expect": -0.0007853981633974483, "tol": 1e-09, "units": "s", "tag": "sign", "note": "a lead of 45° at 1000 rad/s is a negative delay: the output peaks 0.785 ms before the input"},
  {"fn": "magDb", "args": [{"gain": 0.001, "origin": 1, "poles": [1000], "zeros": []}, 1000], "expect": -3.0102999566398116, "tol": 1e-09, "units": "dB", "tag": "typical", "note": "the high-pass is also −3.01 dB at its corner"},
  {"fn": "asymDb", "args": [{"gain": 1, "origin": 0, "poles": [100, 10000], "zeros": []}, 1000], "expect": -20.0, "tol": 1e-09, "units": "dB", "tag": "typical", "note": "poles at 100 rad/s and 10 000 rad/s, at 1000 rad/s: the sketch is one decade down a −20 dB/decade line, −20 dB"},
  {"fn": "magDb", "args": [{"gain": 1, "origin": 0, "poles": [100, 10000], "zeros": []}, 1000], "expect": -20.086427475652854, "tol": 1e-09, "units": "dB", "tag": "typical", "note": "the same point on the true curve: −20.09 dB, close to the sketch because both corners are a decade away"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [100, 10000], "zeros": []}, 1000], "expect": -90.0, "tol": 1e-09, "units": "°", "tag": "typical", "note": "the same point: −84.29° from the first pole and −5.71° from the second, −90° in all"},
  {"fn": "asymPhaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [100, 10000], "zeros": []}, 1000], "expect": -90.0, "tol": 1e-09, "units": "°", "tag": "typical", "note": "the phase sketch at the same point: −90° from the first pole and 0° from the second"},
  {"fn": "asymDb", "args": [{"gain": 1, "origin": 0, "poles": [100], "zeros": [10000]}, 100000.0], "expect": -40.0, "tol": 1e-09, "units": "dB", "tag": "typical", "note": "a pole at 100 rad/s and a zero at 10 000 rad/s, at 10⁵ rad/s: −60 dB from the pole plus 20 dB from the zero, −40 dB, and the line is flat again"},
  {"fn": "phaseDeg", "args": [{"gain": 1, "origin": 0, "poles": [100, 10000, 1000000], "zeros": []}, 10000000.0], "expect": -264.23153814429077, "tol": 1e-09, "units": "°", "tag": "limit-infinity", "note": "poles at 100, 10⁴ and 10⁶ rad/s, at 10⁷ rad/s: the phase has gone past −180°, to −264.23°"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. RC low-pass, R = 1 kΩ, C = 1 µF. Put the cursor at the corner. Is the output half the input?
   Why: No. It is 1/√2 = 0.707 of the amplitude, −3 dB. Half the power, not half the voltage.
2. At the same corner, what is the phase: −90° or −45°?
   Why: −45°. At the corner 1 + jω/ω_c = 1 + j, whose angle is 45°. The phase reaches −90° only far above the corner.
3. The corner is at 1000 rad/s. What frequency in Hz is that, and where does a 1000 Hz sine land on the plot?
   Why: 1000 rad/s is 159 Hz. A 1000 Hz sine is ω = 6283 rad/s, almost a decade above the corner, at about −16 dB.
4. Double C. Which way does the corner move, and by how much on the log axis?
   Why: To half the frequency, ω_c = 1/(RC). Halving is 0.301 of a decade to the left, and the whole curve slides
   with it without changing shape.
5. Free mode, two poles at 10² and 10⁴ rad/s. What is the slope at 10³ rad/s and at 10⁶ rad/s?
   Why: −20 dB per decade between the two corners, −40 dB per decade above both. Each pole adds its own −20.

## Misconceptions

- "At the corner the output is half the input." What the tool shows instead: the readout says ×0.707 and −3.01 dB at
  the corner, and the output waveform in figure 4 is plainly more than half the input's height.
- "The phase is −90° at the corner." What the tool shows instead: the dot on the phase curve at the corner sits on
  −45°, and in figure 3 the line from the pole to jω makes 45° with the σ axis.
- "The corner is at 1/RC Hz." What the tool shows instead: the readout writes 1/(RC) in rad/s beside 1/(2πRC) in Hz,
  and the ω axis is labelled in rad/s.
- "The straight lines are the Bode plot." What the tool shows instead: the dashed sketch and the curve part by
  3 dB at each corner, and by 6 dB where two poles share one.

## Quiz hooks

- L2 looks like: writes H(jω) for an RC filter, computes 1/(RC), and draws the −20 dB/decade line from the corner by
  following the rules.
- L3 looks like: explains −3 dB and −45° from 1 + j at the corner; sketches the magnitude and phase of a two-pole
  function by adding lines; predicts the slide of the curve when R or C changes; reads the s-plane picture of a
  pole's angle to jω.
- L4 looks like: reads poles and zeros off a measured Bode plot, knows the sketch fails by 3 dB per pole at a corner
  and badly for close or complex poles, and knows the phase sketch fails when poles are less than a decade apart.
- Missteps:
  - takes the −3 dB point as half the amplitude
  - puts −90° of phase at the corner
  - reads 1/RC as a frequency in Hz
  - starts the phase turn at the corner instead of a decade before it
  - adds a pole's slope only from where the previous one ends, instead of from its own corner
- Seeds, to be varied and never asked word for word:
  - predict: a low-pass RC with its corner at some ω_c; the capacitor is doubled. Where does the corner go, and what
    is |H| in dB at the old corner?
  - explain: why the phase of one pole is −45° at its corner and needs two decades to turn by 90°.
  - limit: two poles brought closer together until they coincide; when does the straight-line sketch stop being
    good to 1 dB?
  - transfer: an amplifier gain with a low-frequency zero at the origin from a coupling capacitor and a high pole
    from a load capacitor; sketch its midband, and say where its bandwidth ends.

## Where this shows up

- `transfer-function`: H(s) read off the circuit is the thing being drawn; each factor is one line on the plot.
- `poles-and-zeros`: each pole bends the magnitude down and each zero bends it up, at the pole's distance from the
  origin.
- `first-order-system`: an RC circuit is one pole; its corner 1/τ is where the gain starts to fall.
- `frequency-response`: the Bode plot is H(jω) drawn on log axes so that products become sums.
- `phasors-impedance`: the divider with Z = 1/(jωC) is where H(jω) comes from.
- `loop-gain`: the phase margin is read off the Bode plot of the loop gain.
- Later: EE 140: amplifier bandwidth and compensation are read and designed on Bode plots. EE 128: loop shaping and
  phase margin.

## Page text

- Header `Concept:` Each pole bends |H| down by 20 dB per decade from its corner, and each zero bends it up, so a
  Bode plot is a sum of straight lines with a smooth curve over them.
- Header `Course:` EE 105 (frequency response of amplifiers); EE 120 (Bode plots, poles and zeros)
- Header `Play with:` An RC or RL circuit with sliders for R, C and L, or up to three poles and two zeros dragged
  along the ω axis; a cursor that sets the frequency of the sine waves
- Header `Should click:` At the corner the real and imaginary parts are equal, so |H| is 1/√2 (−3 dB) and the phase
  is −45°; the phase needs a decade on each side to finish its turn.
- Title: Bode plot from poles and zeros
- Lede: Each pole bends the magnitude down by 20 dB per decade from its corner on, and each zero bends it up. Draw
  the straight lines, add them, and the true curve follows them except near the corners. Move the cursor and watch
  a sine wave go in and come out smaller and later.
- Caption of `mag`: Drag the cursor (or press anywhere in the plot); in free mode drag the crosses and circles along
  the ω axis. Focused, ← → move one twentieth of a decade, with Shift half a decade.
- Caption of `phase`: The same cursor. The dashed lines are the three-segment sketch: flat, a straight turn across
  two decades, flat.
- Caption of `splane`: The pole is a cross on the σ axis, the zero a circle. The angle of each line to jω is that
  factor's share of the phase.
- Caption of `wave`: The input is 1 V at the cursor frequency. The output is the input scaled by |H| and shifted by
  the delay.
- What should click:
  - **The corner is where real and imaginary are equal.** At ω = p the factor 1 + jω/p is 1 + j: its length is √2
    and its angle 45°. So one pole leaves 1/√2 of the amplitude (−3 dB, half the power) and lags by 45°, never
    half the amplitude and never 90°.
  - **On log axes, factors add.** 20 log₁₀ of a product is a sum, and the angle of a product is a sum of angles. Each
    pole is one straight line, bending down 20 dB per decade from its corner; each zero bends up. Draw them one at a
    time and add.
  - **The phase is slow.** A pole's angle goes from 0° to −90° as ω goes from far below to far above the corner, but
    a decade below it is already −5.7° and a decade above it still has 5.7° to go. That is why the sketch spreads the
    turn over two decades.
  - **rad/s is not Hz.** 1/(RC) is an angular frequency. The corner in Hz is 1/(2πRC), six times smaller.

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
