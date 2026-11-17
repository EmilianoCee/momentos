# Plan: RC and RL step response

```json plan
{
  "id": "rc-rl-step-response",
  "title": "RC and RL step response",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["first-order-system", "step-response"],
  "prerequisites": ["ohms-law", "kvl", "thevenin-norton"],
  "size": "M",
  "tool": "systems/rc-rl-step-response.html",
  "checks": "plans/checks/rc-rl-step-response.py"
}
```

## Concept

An RC or RL circuit with one energy store and a constant source follows x(t) = x_final + (x_start − x_final)·e^(−t/τ),
where x is the capacitor voltage v_C or the inductor current i_L. Find three numbers (the start, the final value and
τ) and the circuit is solved. EE 120 asks the same thing of first-order systems, so one tool serves both courses.

## Picture

The page has a `.bench`: the left column holds figure 1, its view buttons, the controls and figure 2 under them;
the right column (`aside`) holds the readouts and, under them, the "three numbers" panel.

The circuit: a two-way switch puts either V_S or ground on the left end of R₁. R₁ runs to the top node of the store
(a capacitor C or an inductor L) whose bottom end is ground. R₂, when added, sits across the store. So "switch on" is
a step of the input from 0 V to V_S, and "switch off" a step from V_S to 0 V, and τ is the same both ways.

**Figure 1, `circuit`, viewBox 640 by 300.** Wires and elements in `--ink`, 1.6 px. The bottom wire runs at y = 250
from x = 60 to x = 500, the top wire at y = 70 from the switch to x = 500.
- The source V_S: a circle of radius 18 at (60, 160) with "+" and "−", in `--c4`, wired up to (60, 70) and down to
  the bottom wire, labelled "V_S = 5.00 V" in `--c4` to its left.
- The switch: a pivot at (160, 70) and a blade 40 px long; contact "on" at (120, 70), wired left to the source;
  contact "off" at (120, 110), wired down to the bottom wire. The blade points at the contact in use. The words
  "on" and "off" in `--ink-3` beside the contacts.
- R₁: a zigzag from x = 190 to x = 290 at y = 70, labelled "R₁ = 1.00 kΩ" above it in `--ink-2`.
- The store at x = 400, from y = 120 to y = 200, wired to the top and bottom wires. The capacitor: two plates 24 px
  wide; "v_C" with "+" at the top and "−" at the bottom, in `--c1`. The inductor: four bumps; an arrow "i_L" pointing
  down beside it, in `--c1`.
- R₂, when added, at x = 500, from y = 120 to y = 200, wired to the top and bottom wires, labelled "R₂ = 1.00 kΩ".
- The quantity that jumps, in `--c2`: an arrow "i_C" pointing down beside the capacitor, or "v_L" with "+" at the
  top beside the inductor.

Three view buttons under the figure change only the store's drawing:
- "circuit": the store as above.
- "t = 0⁺": the capacitor redrawn as a voltage source (a circle with "+" and "−") labelled
  "v_C(0⁺) = 0 V", or the inductor as a current source (a circle with a downward arrow) labelled "i_L(0⁺) = 0 mA",
  in `--c1`. Beside it, in `--c2`, the jump: "i_C(0⁺) = 5.00 mA" or "v_L(0⁺) = 5.00 V".
- "t → ∞": the capacitor redrawn as an open gap (two stubs, no plates) labelled "open: i_C = 0", or the inductor as a
  plain wire labelled "short: v_L = 0", with the final value beside it in `--c1`: "v_C(∞) = 5.00 V" or
  "i_L(∞) = 5.00 mA".

**Figure 2, `plot`, viewBox 640 by 360.** The state x against time. Plot area from x = 64 to x = 580 and from
y = 20 to y = 320. The time axis is linear from 0 to 6τ in step mode and from 0 to four periods in square-wave mode,
with a grid line and a label in seconds (SI prefix) at each τ in step mode and each half period in square-wave mode,
and "t" at the right end. The left axis is the state in `--c1` ("v_C (V)" or "i_L (mA)"), from
min(0, x_start, x_final) to max(0, x_start, x_final), padded by 10% of the span on each side (span at least 1 V or
1 mA), with five labelled grid lines. The right axis is the jumping quantity in `--c2` ("i_C (mA)" or "v_L (V)"),
scaled so that its largest magnitude over the window fills 90% of the half-height above and below its own zero.
Drawn:
1. Step mode only: a dashed (6 4) `--c1` line at x_final labelled "final"; the tangent at t = 0⁺ in `--c3`, dashed
   (4 3), from (0, x_start) to (τ, x_final), with a `--c3` dot where it meets the final line and the label "τ";
   vertical `--c3` dotted marks at τ, 2τ, 3τ and 5τ, labelled "63%", "86%", "95%" and "99%" at the top of the plot.
2. Square-wave mode only: the input, 0 V or V_S, as a thin `--c4` step line along the top 24 px of the plot, labelled
   "V_S on" and "off".
3. The jumping quantity, `--c2`, 1.6 px, 300 samples, with a vertical jump drawn at each switching moment.
4. The state x, `--c1`, 2.6 px, 300 samples.
5. A `--c1` dot of radius 5 at (0, x_start), the start.
6. The cursor: a vertical `--ink-2` dashed (3 3) line with a `--c1` dot on the state and a `--c2` dot on the
   jumping quantity, and a 14 px wide triangle handle under the time axis.

**Readouts, in the aside,** in `.read`: "τ = R_th·C = 1.00 ms" in `--c3` (or "τ = L/R_th"), large; "R_th = R₁ = 1.00 kΩ"
or "R_th = R₁ ∥ R₂ = 500 Ω" in `--ink-2`; "x_start = v_C(0⁺) = 0 V" and "x_final = v_C(∞) = 5.00 V" in `--c1`; then
"at the cursor": "t = 1.00 ms = 1.00 τ", "v_C = 3.16 V" in `--c1`, "63.2 % of the change done" in `--c3` (step
mode only), "i_C = 1.84 mA" in `--c2`. Every number has three significant figures and an SI prefix.

**The three numbers panel, under the readouts,** headed "Three numbers", in `.read`: "start: what the store held just
before, v_C(0⁻) = v_C(0⁺)"; "final: solve the t → ∞ circuit"; "τ: the resistance the store sees, sources off"; then
"x(t) = x_final + (x_start − x_final)·e^(−t/τ)" with the current numbers substituted.

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| the state variable | v_C, i_L | `--c1` |
| the quantity that jumps | i_C, v_L | `--c2` |
| the time constant, the tangent and the marks | τ | `--c3` |
| the source | V_S | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| store | two buttons, "capacitor" and "inductor" | the store | C, L | | capacitor | Tab and Enter |
| R₁ | slider, log | R₁ in Ω, slider value log₁₀ R₁ | 100 Ω to 100 kΩ (2 to 5) | 0.05 decade | 1 kΩ (3) | arrows: one step |
| C | slider, log (capacitor only) | C in F, slider value log₁₀ C | 10 nF to 100 µF (−8 to −4) | 0.05 decade | 1 µF (−6) | arrows: one step |
| L | slider, log (inductor only) | L in H, slider value log₁₀ L | 1 mH to 10 H (−3 to 1) | 0.05 decade | 1 H (0) | arrows: one step |
| V_S | slider | V_S in V | 0 V to 10 V | 0.5 V | 5 V | arrows: one step |
| start | slider | v_C(0⁻) in V, or i_L(0⁻) in mA | −10 to 10 | 0.5 | 0 | arrows: one step |
| R₂ | checkbox "add R₂ across the store", and a log slider shown while it is ticked | R₂ in Ω, slider value log₁₀ R₂ | 100 Ω to 100 kΩ (2 to 5) | 0.05 decade | off; 1 kΩ (3) | Space; arrows: one step |
| switch | button, "switch: on" or "switch: off" (step mode only) | the input after t = 0 | V_S, 0 V | | on | Enter |
| mode | two buttons, "step" and "square wave" | | step, square wave | | step | Tab and Enter |
| period | slider (square-wave mode only) | the period as a multiple of τ | 1 to 20 | 1 | 10 | arrows: one step |
| view | three buttons, "circuit", "t = 0⁺", "t → ∞" | figure 1's drawing of the store | | | circuit | Tab and Enter |
| cursor | draggable handle: the triangle under figure 2, or a press anywhere in its plot area | t in s | 0 to the end of the window | 1/120 of the window | τ | ← → one step, Shift + ← → 1/12 of the window |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "R₁ = 1.00 kΩ", "start = 0 V".
- The switch sets which input holds after t = 0: "on" means V_S, "off" means 0 V. The start slider is the state just
  before t = 0, whatever the switch did before.
- In square-wave mode the input is V_S for the first half period and 0 V for the second, repeating; the switch button
  is disabled; the start slider still sets the state at t = 0.
- What moves when each control changes: every control redraws both figures and every readout. The view buttons
  redraw only the store in figure 1. The cursor moves only the cursor, its dots and the "at the cursor" readouts.
- When the window changes length (a new τ, or the period), the cursor keeps its time as a multiple of τ.
- Reset: capacitor, R₁ = 1 kΩ, C = 1 µF, L = 1 H, V_S = 5 V, start 0, no R₂ (slider at 1 kΩ), switch on, step mode,
  period 10τ, view "circuit", cursor at τ.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: only the state variable is continuous. v_C and i_L cannot jump; every other voltage
  and current can, and the circuit at t = 0⁺ and at t → ∞ is a resistor circuit you already know how to solve.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. `store` is "C" or "L". R₁ and R₂
are in Ω; R2 is `null` when R₂ is absent. X is C in F or L in H. V_S is in V. The state x is in V (capacitor) or in A
(inductor); the tool shows i_L in mA by multiplying by 1000 for display only.

### `rTh(R1, R2)`

- Returns: the resistance the store sees with the source turned off, in Ω.
- Formula: R1 if R2 is null, else R1·R2/(R1 + R2). With the source off the switch's left end is grounded either way,
  so R₁ and R₂ are in parallel across the store.
- Approximation: none.

### `vTh(VS, R1, R2)`

- Returns: the open-circuit voltage at the store's terminals, in V, for an input VS.
- Formula: VS if R2 is null, else VS·R2/(R1 + R2).
- Approximation: none.

### `tau(store, R1, R2, X)`

- Returns: the time constant in s.
- Formula: `rTh`·X for the capacitor; X/`rTh` for the inductor.
- Valid for: R1, X > 0; R2 > 0 or null.
- Approximation: ideal components: no leakage in C, no winding resistance in L.

### `finalValue(store, VS, R1, R2)`

- Returns: the state as t → ∞ with the input held at VS: V for the capacitor, A for the inductor.
- Formula: capacitor `vTh` (an open circuit carries no current); inductor `vTh`/`rTh`, which is VS/R1 (a short:
  R₂ carries nothing).
- Approximation: none.

### `stateAt(start, final, tau, t)`

- Arguments: start and final in the state's unit; tau in s; t in s after the switching moment.
- Returns: final + (start − final)·e^(−t/tau).
- Valid for: t ≥ 0, a constant input after t = 0.
- Approximation: none.

### `tangentAt(start, final, tau, t)`

- Returns: start + (final − start)·t/tau, the straight line that keeps the slope at t = 0⁺.
- Approximation: it is the curve only for t ≪ tau; it reaches the final value at t = tau, where the curve has done 63%.

### `fractionDone(n)`

- Arguments: n, the time as a multiple of τ.
- Returns: 1 − e^(−n), the fraction of the change done.
- Approximation: none.

### `jumpAt(store, VS, R1, R2, x)`

- Arguments: VS, the input now; x, the state now.
- Returns: capacitor: i_C = (`vTh` − x)/`rTh`, in A; inductor: v_L = `vTh` − `rTh`·x, in V.
- Sign convention: i_C is positive into the top plate (charging); v_L is positive with the top end higher.
- Approximation: none.

### `squareWave(store, VS, R1, R2, X, x0, half, t)`

- Arguments: x0, the state at t = 0; half, the half period in s; t in s.
- Returns: the state at t when the input is VS for the first half period, 0 V for the next, repeating.
- Formula: with T = `tau(store, R1, R2, X)`, step through whole half periods k = 0, 1, 2, … while (time done + half)
  ≤ t, each time setting x to `stateAt(x, finalValue(store, VS or 0, R1, R2), T, half)` (VS for even k, 0 for odd k);
  then return `stateAt` over the time left, toward the final value of the current half period.
- Approximation: none.

The main script draws the step-mode curve with `stateAt`, the square-wave curve with `squareWave`, the jumping
quantity with `jumpAt` applied to the state and the input at each sample, and the marks with `fractionDone`.

## Check cases

Computed by `plans/checks/rc-rl-step-response.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "tau", "args": ["C", 1000, null, 1e-06], "expect": 0.001, "tol": 1e-09, "units": "s", "tag": "typical", "note": "R1 = 1 kΩ, C = 1 µF, no R2: τ = RC = 1 ms"},
  {"fn": "tau", "args": ["C", 1000, 1000, 1e-06], "expect": 0.0005, "tol": 1e-09, "units": "s", "tag": "typical", "note": "the same with R2 = 1 kΩ across C: the capacitor sees 1 kΩ ∥ 1 kΩ = 500 Ω, so τ = 0.5 ms, not 1 ms"},
  {"fn": "tau", "args": ["L", 1000, null, 1], "expect": 0.001, "tol": 1e-09, "units": "s", "tag": "typical", "note": "R1 = 1 kΩ, L = 1 H: τ = L/R = 1 ms"},
  {"fn": "tau", "args": ["L", 1000, 1000, 1], "expect": 0.002, "tol": 1e-09, "units": "s", "tag": "typical", "note": "the same with R2 = 1 kΩ across L: L/(500 Ω) = 2 ms. A smaller resistance makes the inductor slower"},
  {"fn": "rTh", "args": [1000, 3000], "expect": 750.0, "tol": 1e-09, "units": "Ω", "tag": "typical", "note": "R1 = 1 kΩ in parallel with R2 = 3 kΩ: 750 Ω, what the store sees with the source turned off"},
  {"fn": "finalValue", "args": ["C", 5, 1000, null], "expect": 5, "tol": 1e-09, "units": "V", "tag": "typical", "note": "V_S = 5 V through 1 kΩ into a capacitor: it ends at 5 V, an open circuit carrying no current"},
  {"fn": "finalValue", "args": ["C", 5, 1000, 1000], "expect": 2.5, "tol": 1e-09, "units": "V", "tag": "typical", "note": "with R2 = 1 kΩ across it, the capacitor ends at the divider's 2.5 V, not at 5 V"},
  {"fn": "finalValue", "args": ["L", 5, 1000, 1000], "expect": 0.005, "tol": 1e-09, "units": "A", "tag": "typical", "note": "V_S = 5 V, R1 = 1 kΩ, R2 = 1 kΩ across an inductor: it ends as a short carrying 5 V/1 kΩ = 5 mA, and R2 carries nothing"},
  {"fn": "stateAt", "args": [0, 5, 0.001, 0.001], "expect": 3.1606027941427883, "tol": 1e-09, "units": "V", "tag": "typical", "note": "from 0 V toward 5 V with τ = 1 ms, after 1 ms: 3.16 V, 63% of the way, not all of it"},
  {"fn": "fractionDone", "args": [1], "expect": 0.6321205588285577, "tol": 1e-09, "units": "", "tag": "typical", "note": "after one τ, 63.2% of the change is done"},
  {"fn": "fractionDone", "args": [5], "expect": 0.9932620530009145, "tol": 1e-09, "units": "", "tag": "typical", "note": "after five τ, 99.3% of the change is done"},
  {"fn": "stateAt", "args": [0, 5, 0.001, 0], "expect": 0.0, "tol": 1e-09, "units": "V", "tag": "limit-zero", "note": "at t = 0⁺ the capacitor is still at its start, 0 V: its voltage cannot jump"},
  {"fn": "jumpAt", "args": ["C", 5, 1000, null, 0], "expect": 0.005, "tol": 1e-09, "units": "A", "tag": "limit-zero", "note": "at t = 0⁺, with v_C = 0 V, the capacitor acts as a 0 V source: i_C jumps from 0 to 5 V/1 kΩ = 5 mA"},
  {"fn": "jumpAt", "args": ["L", 5, 1000, null, 0], "expect": 5, "tol": 1e-09, "units": "V", "tag": "limit-zero", "note": "at t = 0⁺, with i_L = 0 A, the inductor acts as a 0 A current source, an open circuit: v_L jumps to the full 5 V"},
  {"fn": "stateAt", "args": [0, 5, 0.001, 0.02], "expect": 4.999999989694232, "tol": 1e-09, "units": "V", "tag": "limit-infinity", "note": "after 20 τ the capacitor is at 5 V to within 0.00000001 V: the open-circuit picture"},
  {"fn": "jumpAt", "args": ["C", 5, 1000, null, 5], "expect": 0.0, "tol": 1e-09, "units": "A", "tag": "limit-infinity", "note": "when v_C has reached 5 V the capacitor current is 0 A: an open circuit"},
  {"fn": "tangentAt", "args": [0, 5, 0.001, 0.001], "expect": 5.0, "tol": 1e-09, "units": "V", "tag": "breaks", "note": "the tangent at t = 0⁺ reaches the final 5 V at t = τ = 1 ms; the curve itself is only at 3.16 V. Keeping the starting slope is wrong after the first few percent"},
  {"fn": "jumpAt", "args": ["C", 0, 1000, null, 5], "expect": -0.005, "tol": 1e-09, "units": "A", "tag": "sign", "note": "the switch flips to ground with the capacitor at 5 V: i_C = −5 mA, the capacitor drives current back out through R1"},
  {"fn": "stateAt", "args": [5, 0, 0.001, 0.001], "expect": 1.8393972058572117, "tol": 1e-09, "units": "V", "tag": "sign", "note": "discharging from 5 V toward 0 V with τ = 1 ms: after 1 ms it is at 1.84 V, 63% of the way down"},
  {"fn": "squareWave", "args": ["C", 5, 1000, null, 1e-06, 0, 0.001, 0.0015], "expect": 1.9170024978210178, "tol": 1e-09, "units": "V", "tag": "typical", "note": "square wave with half period 1 ms = τ: charging for 1 ms reaches 3.16 V, then 0.5 ms toward 0 V leaves 1.92 V"},
  {"fn": "squareWave", "args": ["C", 5, 1000, null, 1e-06, 0, 0.01, 0.01], "expect": 4.999773000351188, "tol": 1e-09, "units": "V", "tag": "typical", "note": "square wave with half period 10 ms = 10 τ: by the end of the first half the capacitor is at 5 V to within 0.0002 V"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Double C. Does the capacitor reach 5 V sooner or later?
   Why: Later. τ = RC doubles: twice the charge has to move through the same resistor at the same current.
2. Close the switch with the capacitor at 0 V. What is the current the instant after, and what is it a long time
   later?
   Why: 5 mA, then 0. At t = 0⁺ the capacitor is a 0 V source, so all of V_S sits across R₁. At t → ∞ it is an open
   circuit.
3. Add R₂ = 1 kΩ across the capacitor. What happens to τ and to the final voltage?
   Why: Both halve. The capacitor sees R₁ ∥ R₂ = 500 Ω, and the divider leaves it 2.5 V.
4. After one τ, is the capacitor at 5 V?
   Why: No: at 63% of the way, 3.16 V. It is within 1% of 5 V only after about 5τ. The tangent line is what reaches
   5 V at τ.
5. Switch to the inductor and add R₂. Does the inductor get faster or slower?
   Why: Faster. τ = L/R_th, and R₂ makes R_th smaller. A capacitor and an inductor answer a smaller resistance in
   opposite ways.
6. Square wave with the period at 2τ. Does the capacitor ever reach 0 V or 5 V?
   Why: No. Each half period is one τ, so it goes 63% of the way and turns back. It settles into a ripple between
   about 1.34 V and 3.66 V.

## Misconceptions

- "A bigger C charges faster." What the tool shows instead: the τ readout and the marks move right as C grows, and the
  curve at any fixed time is lower.
- "τ uses the nearest resistor." What the tool shows instead: adding R₂ across the store changes τ, and the readout
  writes R_th = R₁ ∥ R₂.
- "The capacitor reaches V_S after time RC." What the tool shows instead: the mark at τ says 63%, the tangent reaches
  the final line at τ while the curve is still below it, and the 99% mark sits at 5τ.
- "The capacitor's current is continuous too." What the tool shows instead: the `--c2` trace jumps at every switching
  moment while the `--c1` trace never does.

## Quiz hooks

- L2 looks like: computes τ = RC or L/R for a single resistor and writes the exponential from the start and final
  values.
- L3 looks like: finds the start from continuity of v_C or i_L, the final value from the t → ∞ circuit and τ from the
  Thévenin resistance the store sees; predicts the jump in i_C or v_L at the switching moment; says how far the change
  has gone after 1, 3 and 5 τ.
- L4 looks like: handles a second switching before the first transient has settled; reads τ off a measured curve from
  the tangent or the 63% point; knows the model needs a constant input after the switch and ideal components, and
  what a real inductor does when its current is interrupted.
- Missteps:
  - uses the nearest resistor instead of the Thévenin resistance for τ
  - lets v_C jump at the switching moment, or keeps i_C continuous
  - takes the final value of a capacitor with a resistor across it as V_S instead of the divider's value
  - writes the exponential with the start and final values swapped
  - thinks the inductor's τ grows with resistance
- Seeds, to be varied and never asked word for word:
  - predict: a capacitor charged through R₁ with R₂ across it; R₂ is removed. What happens to τ and to the final
    voltage?
  - explain: why a capacitor's voltage cannot jump but its current can.
  - limit: the half period of a square wave made much shorter than τ; what does the capacitor's voltage look like?
  - transfer: a sensor with a time constant read by a sampling circuit: how long after a step must it wait for the
    reading to be within 0.1%?

## Where this shows up

- `first-order-system`: one store, one τ: the step response covers 63% of what is left every τ.
- `step-response`: the switch on is a step input; where the curve settles is the circuit's gain for a constant input.
- `thevenin-norton`: the store sees a Thévenin source; its resistance is τ's R and its voltage is the final value.
- `kvl`: at t = 0⁺ the store is a source and KVL around the loop gives the jump.
- `bode-plot`: the same circuit in the frequency domain is one pole at 1/τ.
- Later: EE 105: the time constants of an amplifier set its bandwidth. EE 120: first-order systems and their step
  responses in the Laplace domain.

## Page text

- Header `Concept:` With one energy store and a constant source, the store's voltage or current moves exponentially
  from where it was to where the t → ∞ circuit puts it, covering 63% of what is left every τ.
- Header `Course:` EE 105 (RC and RL transients, time constants); EE 120 (first-order systems, step response)
- Header `Play with:` A capacitor or an inductor, R₁, R₂ across the store, V_S, the starting value, the switch, a square
  wave, and views of the circuit at t = 0⁺ and t → ∞
- Header `Should click:` Only v_C and i_L are continuous. Every other voltage and current can jump, and the circuits at
  t = 0⁺ and t → ∞ are resistor circuits you already know how to solve.
- Title: RC and RL step response
- Lede: A capacitor's voltage and an inductor's current cannot jump. So when a switch moves, they start where they
  were and slide exponentially to where the circuit will leave them. Three numbers solve it: the start, the final
  value and τ.
- Caption of `circuit`: The switch puts V_S or ground on the left end of R₁. "t = 0⁺" redraws the store as the source
  it is at that instant; "t → ∞" as the open circuit or short it becomes.
- Caption of `plot`: The state in blue, the quantity that jumps in orange. Drag the cursor or press in the plot;
  focused, ← → move it, with Shift ten times further.
- What should click:
  - **The state cannot jump.** A capacitor's voltage is its charge over C, and charge takes time to move. An
    inductor's current is its flux over L. So v_C and i_L at t = 0⁺ are what they were at t = 0⁻. Everything else,
    including i_C and v_L, can jump.
  - **Two resistor circuits give the two ends.** At t = 0⁺ the capacitor is a voltage source and the inductor a current
    source, holding their values. At t → ∞ the capacitor is open and the inductor a short. Solve each and you have the
    jump and the final value.
  - **τ is the resistance the store sees.** Turn the source off and look out from the store's terminals: R_th. Then
    τ = R_th·C or L/R_th. A resistor across the store counts.
  - **63% of what is left, every τ.** After τ the change is 63% done, after 3τ 95%, after 5τ 99%. The starting slope,
    kept up, would finish at τ: the tangent.

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
