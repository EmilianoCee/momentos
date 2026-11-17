# Plan: Ideal op-amp and the virtual short

```json plan
{
  "id": "ideal-op-amp",
  "title": "Ideal op-amp and the virtual short",
  "status": "built",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["ideal-op-amp", "feedback"],
  "prerequisites": ["kcl", "dividers", "nodal-analysis"],
  "size": "M",
  "tool": "circuits/amplifiers/ideal-op-amp.html",
  "checks": "plans/checks/ideal-op-amp.py"
}
```

## Concept

An op-amp has a very large gain A. With negative feedback it moves its output until its two inputs are at almost the
same voltage. That pins the inverting input (the virtual short), no current enters either input, and the gain of the
circuit is set by two resistors alone. EE 120 asks about feedback in the same terms, so the tool serves both courses.

## Picture

The page has a `.bench`: the left column holds figure 1 with the controls under it; the right column (`aside`) holds
the recipe panel and the readouts. Under the bench, a `.pair`: figure 2 on the left, the loop-gain readout on the
right.

The op-amp model: v_out = A·(v₊ − v₋), no current into either input, no output resistance, and v_out held between
−12 V and +12 V when the rails are on.

**Figure 1, `circuit`, viewBox 640 by 360.** The circuit, wires and elements in `--ink`, 1.6 px. The op-amp is a
triangle with its left edge at x = 330 from y = 130 to y = 250 and its apex, the output, at (440, 190). Its top input
pin is at (330, 165) and its bottom one at (330, 215), marked "−" and "+" inside the triangle (and "+" and "−" when
the inputs are swapped). The output wire runs from (440, 190) to (560, 190), ending in an open circle labelled
"v_out". The feedback path leaves the node N at (220, 165), goes up to y = 80, right to x = 500, and down to the
output wire at (500, 190).
- Inverting: an open circle "v_in" at (70, 165), R₁ horizontal from x = 120 to x = 200 at y = 165, a wire on to N,
  N to the top pin; R₂ on the feedback path from x = 340 to x = 420 at y = 80; the bottom pin wired left to
  (290, 215) and down to a ground symbol at (290, 250).
- Non-inverting: "v_in" at (70, 215), wired straight to the bottom pin; R₁ horizontal from x = 120 to x = 200 at
  y = 165 between N and a ground symbol at (100, 190) reached by a wire from (100, 165); N to the top pin; R₂ on the
  feedback path as above.
- Follower: "v_in" at (70, 215) wired to the bottom pin; N to the top pin; the feedback path is a plain wire, with
  no R₁ and no R₂.

On the figure:
- Voltages in `--c1`: v_in beside its circle, v_out beside its circle, "v₋ = …" just left of the − pin and
  "v₊ = …" just left of the + pin.
- Currents in `--c2`: an arrow along R₁ and one along R₂, pointing the way the current flows, whose stroke width is
  1.5 + 5·min(1, |i| / 2 mA) px, labelled "0.500 mA". In the inverting circuit i₁ is taken from v_in into N and i₂
  from N to v_out; in the non-inverting circuit i₂ from v_out into N and i₁ from N to ground; a negative value flips
  the arrow. Beside each input pin, a small "0 A" in `--c2`.
- Resistances in `--c4`: "R₁ = 1.00 kΩ" above R₁ and "R₂ = 10.0 kΩ" above R₂.
- The gauge for v_diff = v₊ − v₋, in `--c3`, under the triangle: a horizontal track from x = 300 to x = 470 at
  y = 300 with its centre at x = 385, and a bar from the centre whose length is 85·clamp((log₁₀|v_diff| + 7)/8, 0, 1)
  px, to the right when v_diff is positive and to the left when negative. Tick marks at 1 µV, 1 mV and 1 V on each
  side; the three on the right are labelled "1 µV", "1 mV" and "1 V" under the track. Above it: "v_diff = −50.0 µV".
- When the output is held by a rail: the text "at the rail: −12 V" beside v_out, in `--accent`.

**Recipe panel, at the top of the aside,** headed "The recipe", three numbered lines in `--ink`:
1. V₊ = V₋: the output moves until the inputs agree.
2. No current flows into either input.
3. KCL at the pinned node gives v_out.
Under it, the same three steps worked for the current topology with the current numbers, for example (inverting):
"v₋ = v₊ = 0 V", "i₁ = (v_in − 0)/R₁ = 0.500 mA, all of it on through R₂", "v_out = 0 − i₁R₂ = −5.00 V".
When the feedback is positive this block is replaced by "No negative feedback: step 1 does not hold."

**Readouts, under the recipe,** in `.read`: "v_out = −5.00 V" large (`.big`) in `--c1`; "ideal: −R₂/R₁ · v_in =
−5.00 V" in `--ink-2`; "v_diff = −50.0 µV" in `--c3`; "gain error = −0.011 %" in `--ink`, replaced by "gain error: no gain, the output sits on a rail" when the inputs
are swapped and by "gain error: none to speak of, the rail holds the output" when a rail holds it. Every number has three
significant figures and an SI prefix (µ, m, k, M).

**Figure 2, `gain`, viewBox 480 by 300.** The closed-loop gain |G| against A. Plot area from x = 56 to x = 460 and
from y = 20 to y = 250. The A axis is logarithmic, 10¹ to 10⁶, with a grid line and label at each decade and "A" at
the right end. The |G| axis is linear from 0 to 1.25·|G_ideal|, with five grid lines and labels, and "|G|" at the
top left. Drawn: the ideal |G_ideal| as a dashed (6 4) `--ink-2` line labelled "ideal 10" at its right end; the
curve |`closedGain`| against A in `--c1`, 2.4 px, 200 points evenly spaced in log A; a `--c1` dot at the current A;
a dotted `--ink-3` vertical line where Aβ = 1, labelled "Aβ = 1".

**Loop-gain readout, beside figure 2:** "β = R₁/(R₁ + R₂) = 0.0909", "Aβ = 9.09 k", "error = 1/(1 + Aβ) = 0.011 %",
and one sentence in `--ink-2`: "Ten times more A, ten times less error."

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| voltages, and the gain v_out/v_in | v_in, v_out, v₊, v₋, G | `--c1` |
| currents | i₁, i₂ | `--c2` |
| the input difference | v_diff | `--c3` |
| resistances | R₁, R₂ | `--c4` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| topology | three buttons, "inverting", "non-inverting", "follower" | the circuit | | | inverting | Tab and Enter |
| R₁ | slider, log (hidden for the follower) | R₁ in Ω, slider value log₁₀ R₁ | 100 Ω to 100 kΩ (2 to 5) | 0.05 decade | 1 kΩ (3) | arrows: one step |
| R₂ | slider, log (hidden for the follower) | R₂ in Ω, slider value log₁₀ R₂ | 100 Ω to 100 kΩ (2 to 5) | 0.05 decade | 10 kΩ (4) | arrows: one step |
| v_in | slider | v_in in V | −2 V to 2 V | 0.05 V | 0.5 V | arrows: one step |
| A | slider, log | A, slider value log₁₀ A | 10 to 10⁶ (1 to 6) | 0.1 decade | 10⁵ (5) | arrows: one step |
| rails | checkbox, "clip at ±12 V" | | on, off | | on | Space |
| swap | checkbox, "swap the inputs" | | on, off | | off | Space |
| reset | button | | | | | Enter |

- Each slider has its value beside it with its unit: "R₁ = 1.00 kΩ", "v_in = 0.50 V", "A = 100 k".
- What moves when each control changes: every control calls `solve` and redraws figure 1, the recipe, the readouts,
  and figure 2 (whose axis follows |G_ideal|).
- While "swap the inputs" is on, the rails checkbox is ticked and disabled, with the note "positive feedback:
  without the rails the output would run away without limit".
- Reset: inverting, R₁ = 1 kΩ, R₂ = 10 kΩ, v_in = 0.5 V, A = 10⁵, rails on, inputs not swapped.
- Motion: nothing animates. The figures are redrawn only when a control changes, so prefers-reduced-motion needs
  nothing different.
- The one thing that should click: as A rises, v_diff shrinks toward zero and the gain stops depending on A; the
  error falls in proportion to 1/(1 + Aβ).

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments. `top` is one of "inverting",
"non-inverting", "follower". R₁ and R₂ are in Ω (the follower ignores them), A is a pure number, voltages are in V,
currents in A.

### `beta(top, R1, R2)`

- Returns: the fraction of v_out fed back to the − input, a pure number.
- Formula: R1/(R1 + R2) for the inverting and non-inverting circuits; 1 for the follower.
- Approximation: none.

### `idealGain(top, R1, R2)`

- Returns: v_out/v_in for A → ∞, a pure number.
- Formula: inverting −R2/R1; non-inverting 1 + R2/R1; follower 1.
- Approximation: A is infinite.

### `closedGain(top, R1, R2, A)`

- Returns: v_out/v_in for a finite A, a pure number, with no rails.
- Formula: inverting −(R2/(R1 + R2))·A/(1 + Aβ), from v₋ = (R2·v_in + R1·v_out)/(R1 + R2) and v_out = −A·v₋;
  non-inverting and follower A/(1 + Aβ), from v_out = A·(v_in − β·v_out). Here β = `beta(top, R1, R2)`.
- Valid for: A > 0.
- Approximation: no input current and no output resistance.

### `gainErrorPct(top, R1, R2, A)`

- Returns: 100·(`closedGain` − `idealGain`)/`idealGain`, in %. It equals −100/(1 + Aβ).
- Sign convention: negative means the gain falls short of the ideal.

### `solve(top, R1, R2, A, vin, Vsat, clip, swapped)`

- Arguments: as above; vin in V; Vsat, the rail, in V (the tool always passes 12); clip, a boolean, true when the
  rails are on; swapped, a boolean, true when the input pins are exchanged.
- Returns: `{ vout, vplus, vminus, vdiff, i1, i2, saturated }`: the output, the voltages at the + and − pins, their
  difference vplus − vminus, the currents i1 and i2 (directions as in the Picture), and whether a rail holds the
  output.
- Formula. Write fb for the voltage at node N and other for the voltage on the other input's wire, for a given
  v_out: inverting fb = (R2·vin + R1·vout)/(R1 + R2) and other = 0; non-inverting fb = R1·vout/(R1 + R2) and
  other = vin; follower fb = vout and other = vin.
  - Not swapped: vout = `closedGain`·vin; if clip and |vout| > Vsat, vout = ±Vsat with the sign of vout and
    saturated = true. Then vminus = fb and vplus = other.
  - Swapped: the + pin is on N. push = fb − other with vout = 0. vout = +Vsat if push > 0, −Vsat if push < 0, and 0
    if push = 0; saturated is true unless push = 0. Then vplus = fb and vminus = other, for that vout.
  - Currents: inverting i1 = (vin − fb)/R1 and i2 = (fb − vout)/R2; non-inverting i1 = fb/R1 and
    i2 = (vout − fb)/R2; follower both 0.
- Sign convention: vdiff = vplus − vminus. A positive current flows in the direction named in the Picture.
- Approximation: with the inputs swapped, the linear balance exists but is unstable; the output leaves it in the
  direction of the first push and the feedback carries it to the rail. push = 0 is the unstable balance, kept only
  because nothing disturbs it.

## Check cases

Computed by `plans/checks/ideal-op-amp.py`. Copy this block into the tool unchanged.

```json check-cases
[
  {"fn": "idealGain", "args": ["inverting", 1000, 10000], "expect": -10.0, "tol": 1e-09, "units": "", "tag": "typical", "note": "inverting, R1 = 1 kΩ, R2 = 10 kΩ: the ideal gain is −R2/R1 = −10"},
  {"fn": "idealGain", "args": ["non-inverting", 1000, 10000], "expect": 11.0, "tol": 1e-09, "units": "", "tag": "typical", "note": "non-inverting, R1 = 1 kΩ, R2 = 10 kΩ: the ideal gain is 1 + R2/R1 = 11"},
  {"fn": "beta", "args": ["non-inverting", 1000, 10000], "expect": 0.09090909090909091, "tol": 1e-09, "units": "", "tag": "typical", "note": "R1 = 1 kΩ to ground and R2 = 10 kΩ from the output: a fraction 1/11 of v_out is fed back"},
  {"fn": "closedGain", "args": ["inverting", 1000, 10000, 100000], "expect": -9.99890012098669, "tol": 1e-09, "units": "", "tag": "typical", "note": "inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is −9.9989, a hair short of −10"},
  {"fn": "closedGain", "args": ["non-inverting", 1000, 10000, 100000], "expect": 10.99879013308536, "tol": 1e-09, "units": "", "tag": "typical", "note": "non-inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is 10.9988, a hair short of 11"},
  {"fn": "closedGain", "args": ["follower", 1000, 10000, 1000], "expect": 0.999000999000999, "tol": 1e-09, "units": "", "tag": "typical", "note": "follower with A = 1000 (R1 and R2 unused): the gain is 1000/1001 = 0.999"},
  {"fn": "gainErrorPct", "args": ["inverting", 1000, 10000, 100000], "expect": -0.01099879013310101, "tol": 1e-09, "units": "%", "tag": "typical", "note": "inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is 0.011% short, which is 1/(1 + Aβ) with Aβ = 9091"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 100000, 0.5, 12, true, false], "expect": {"vout": -4.999450060493345, "vplus": 0.0, "vminus": 4.99945006050356e-05, "vdiff": -4.99945006050356e-05, "i1": 0.000499950005499395, "i2": 0.000499950005499395, "saturated": false}, "tol": 1e-09, "units": "V, A", "tag": "typical", "note": "inverting, 1 kΩ and 10 kΩ, A = 10⁵, v_in = 0.5 V: v_out = −4.9995 V, the − input sits 50 µV above ground, and 0.5 mA flows through both resistors"},
  {"fn": "solve", "args": ["non-inverting", 1000, 10000, 100000, 0.5, 12, true, false], "expect": {"vout": 5.49939506654268, "vplus": 0.5, "vminus": 0.49994500604933456, "vdiff": 5.499395066543844e-05, "i1": 0.0004999450060493345, "i2": 0.0004999450060493345, "saturated": false}, "tol": 1e-09, "units": "V, A", "tag": "typical", "note": "non-inverting, 1 kΩ and 10 kΩ, A = 10⁵, v_in = 0.5 V: v_out = 5.4994 V and the two inputs differ by 55 µV"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 100000, 0, 12, true, false], "expect": {"vout": -0.0, "vplus": 0.0, "vminus": 0.0, "vdiff": 0.0, "i1": 0.0, "i2": 0.0, "saturated": false}, "tol": 1e-09, "units": "V, A", "tag": "limit-zero", "note": "inverting with v_in = 0 V: everything sits at 0 V and no current flows"},
  {"fn": "gainErrorPct", "args": ["inverting", 1000, 10000, 10], "expect": -52.38095238095239, "tol": 1e-09, "units": "%", "tag": "limit-zero", "note": "inverting, 1 kΩ and 10 kΩ, with a small A = 10: the gain is −4.76, 52% short of −10. The virtual short needs a large A"},
  {"fn": "closedGain", "args": ["inverting", 1000, 10000, 1000000000.0], "expect": -9.99999989, "tol": 1e-09, "units": "", "tag": "limit-infinity", "note": "inverting, 1 kΩ and 10 kΩ, A = 10⁹: the gain is −10 to eight figures. The resistors alone set it"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 1000000000.0, 0.5, 12, true, false], "expect": {"vout": -4.999999945, "vplus": 0.0, "vminus": 5.000000039052049e-09, "vdiff": -5.000000039052049e-09, "i1": 0.0004999999949999999, "i2": 0.000499999995, "saturated": false}, "tol": 1e-12, "units": "V, A", "tag": "limit-infinity", "note": "the same with v_in = 0.5 V: the input difference has shrunk to 5 nV"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 100000, 2, 12, true, false], "expect": {"vout": -12, "vplus": 0.0, "vminus": 0.7272727272727273, "vdiff": -0.7272727272727273, "i1": 0.0012727272727272728, "i2": 0.0012727272727272726, "saturated": true}, "tol": 1e-09, "units": "V, A", "tag": "breaks", "note": "inverting, gain −10, v_in = 2 V asks for −20 V but the rail stops it at −12 V: the − input is pulled to 0.727 V and the virtual short is gone"},
  {"fn": "solve", "args": ["non-inverting", 1000, 10000, 100000, 0.5, 12, true, true], "expect": {"vout": -12, "vplus": -1.0909090909090908, "vminus": 0.5, "vdiff": -1.5909090909090908, "i1": -0.0010909090909090907, "i2": -0.001090909090909091, "saturated": true}, "tol": 1e-09, "units": "V, A", "tag": "sign", "note": "non-inverting with its inputs swapped, v_in = 0.5 V: the feedback is positive and the output slams to −12 V, with 1.59 V between the inputs"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 100000, 0.5, 12, true, true], "expect": {"vout": 12, "vplus": 1.5454545454545454, "vminus": 0.0, "vdiff": 1.5454545454545454, "i1": -0.0010454545454545454, "i2": -0.0010454545454545456, "saturated": true}, "tol": 1e-09, "units": "V, A", "tag": "sign", "note": "inverting with its inputs swapped, v_in = 0.5 V: the output slams to +12 V, not to the −5 V the resistors ask for"},
  {"fn": "solve", "args": ["inverting", 1000, 10000, 100000, 2, 12, false, false], "expect": {"vout": -19.99780024197338, "vplus": 0.0, "vminus": 0.0001999780024201424, "vdiff": -0.0001999780024201424, "i1": 0.00199980002199758, "i2": 0.00199980002199758, "saturated": false}, "tol": 1e-09, "units": "V, A", "tag": "other", "note": "the same as the clipped case with the rails off: v_out = −19.998 V and the inputs differ by 200 µV"}
]
```

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. Inverting, R₁ = 1 kΩ, R₂ = 10 kΩ, v_in = 0.5 V. What is v_out, and what voltage sits on the − input?
   Why: −5 V, and almost exactly 0 V: the output moves until the − input matches the grounded + input. With A = 10⁵
   it is 50 µV off.
2. Lower A from 10⁵ to 10³. Does the gain change by a factor of 100?
   Why: No. It goes from −9.9989 to −9.89, about 1% short. The error is 1/(1 + Aβ), and Aβ is still 91.
3. Swap the inputs. Where does the output go?
   Why: To a rail. Any difference now pushes the output the way that makes the difference bigger, so it runs until the
   rail stops it. The virtual short needs negative feedback.
4. Set v_in = 2 V with the rails on. Is the − input still at 0 V?
   Why: No. The output wants −20 V but stops at −12 V, so it can no longer pull the − input down: it sits at 0.73 V.
   The virtual short holds only while the output is free to move.
5. Follower with A = 1000. What is the gain?
   Why: 1000/1001 = 0.999. All of the output is fed back, β = 1, so Aβ = 1000 and the error is 0.1%.

## Misconceptions

- "A virtual short means the inputs are joined by a wire." What the tool shows instead: the "0 A" at each input pin
  and the current arrows, which run through R₁ and R₂ and never between the pins.
- "The rule holds for any connection." What the tool shows instead: with the inputs swapped the output sits on a rail
  and the gauge shows volts between the inputs, not microvolts.
- "The output sets the input difference." What the tool shows instead: the gauge reads v_out/A: raise A and the
  difference shrinks while v_out stays where the resistors put it.
- "A bigger A gives a bigger gain." What the tool shows instead: figure 2 flattens against the dashed ideal; past
  Aβ ≈ 100 the gain hardly moves.

## Quiz hooks

- L2 looks like: writes v_out = −(R₂/R₁)·v_in and v_out = (1 + R₂/R₁)·v_in from memory and applies them to the
  standard circuits.
- L3 looks like: solves an unfamiliar op-amp circuit with the recipe (V₊ = V₋, no input current, KCL at the pinned
  node); explains the virtual short as the output moving until the inputs agree; predicts the error from 1/(1 + Aβ).
- L4 looks like: checks that the feedback is negative before using the virtual short; knows it fails at a rail, with
  positive feedback and when Aβ is small; estimates the error of a finite-gain op-amp and says when the
  input current or output resistance matters.
- Missteps:
  - uses the virtual short in a circuit with positive feedback or a saturated output
  - lets current flow into the op-amp's inputs when writing KCL
  - treats the virtual short as a wire and sends current through it
  - takes the non-inverting gain as R₂/R₁
  - computes β with the wrong resistor on top
- Seeds, to be varied and never asked word for word:
  - predict: an inverting amplifier with a given R₁ and R₂ whose op-amp's A falls by a factor of ten; by how much does
    the gain change?
  - explain: why the − input of an inverting amplifier sits at ground although nothing connects it to ground.
  - limit: raise v_in until the output reaches a rail; what happens to v₋, and why does the recipe stop working?
  - transfer: a summing amplifier with two inputs through two resistors into one node; find v_out with the recipe.

## Where this shows up

- `feedback`: the op-amp in a loop is G/(1 + GH) with G = A and H = β; when Aβ is large the gain is 1/β.
- `kcl`: step 3 of the recipe is KCL at the pinned node, with no current into the input.
- `dividers`: β is the divider R₁/(R₁ + R₂) from the output back to the − input.
- `op-amp-model`: a finite A, input resistance and output resistance give errors of about 1/(1 + Aβ).
- `loop-gain`: Aβ is the loop gain, and it sets how close the circuit comes to ideal.
- Later: EE 140: op-amp design is the design of A and of the loop that keeps the feedback negative. EE 128:
  feedback control loops in the same terms.

## Page text

- Header `Concept:` With negative feedback an op-amp moves its output until its two inputs agree, so the − input is
  pinned (the virtual short), no current enters it, and two resistors set the gain.
- Header `Course:` EE 105 (op-amps and feedback); EE 120 (feedback)
- Header `Play with:` The topology, R₁, R₂, v_in and the open-loop gain A; the rails; swapping the inputs
- Header `Should click:` As A rises, the voltage between the inputs shrinks toward zero and the gain stops depending
  on A. The rule needs negative feedback and an output that is free to move.
- Title: Ideal op-amp and the virtual short
- Lede: An op-amp multiplies the difference between its inputs by a huge number. Wire its output back to the −
  input and it chases its own tail: the output moves until the two inputs agree. Watch the difference shrink to
  microvolts as you raise A, and the gain settle on a ratio of two resistors.
- Caption of `circuit`: Voltages in blue, currents in orange (thicker for more current), resistances in purple. The
  gauge under the op-amp is the voltage between its inputs, on a log scale.
- Caption of `gain`: The gain against the open-loop gain A. It climbs toward the ratio the resistors set and
  flattens against it.
- What should click:
  - **The output chases the inputs.** v_out = A·(v₊ − v₋), so v₊ − v₋ = v_out/A. A few volts out of an amplifier with
    A = 10⁵ needs only tens of microvolts in. That is the virtual short: not a wire, a difference too small to matter.
  - **Then the resistors decide.** With v₋ pinned and no current into the input, KCL at the pinned node fixes v_out.
    A no longer appears: the gain is −R₂/R₁ or 1 + R₂/R₁.
  - **The error is one over the loop gain.** The gain falls short of ideal by 1/(1 + Aβ). Ten times more A, ten times
    less error.
  - **Only with negative feedback.** Swap the inputs and the output runs away from the balance instead of toward it,
    until a rail stops it. At a rail the output cannot move, and the inputs are no longer pinned.

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
