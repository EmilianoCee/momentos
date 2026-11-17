# Plan: Loop gain, bandwidth and phase margin

```json plan
{
  "id": "loop-gain",
  "title": "Loop gain, bandwidth and phase margin",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["loop-gain", "gain-bandwidth-product", "phase-margin"],
  "prerequisites": ["bode-plot", "first-order-system", "ideal-op-amp"],
  "size": "M",
  "tool": "systems/control/loop-gain.html"
}
```

## Concept

Feedback divides the gain by 1 + T and multiplies the bandwidth by the same factor, so for a one-pole amplifier the product of gain and bandwidth is fixed. The loop is safe only while its phase has not reached −180° where the loop gain |T| is still 1. The phase margin is how far it is from there.

## Picture

Figure 1 (640 by 300): the open-loop gain |A(jω)| in dB against ω on a log axis, with one dominant pole and an optional second pole. A horizontal line at 1/β (the closed-loop gain, in dB, where β is the fraction of the output fed back) cuts it; the crossing is the loop-gain crossover, marked.

Figure 2 (640 by 240): the loop's phase in degrees against the same axis, with the phase margin drawn as an arc from −180° up to the phase at the crossover.

Figure 3 (480 by 240): the closed-loop step response against time. It is smooth with a large margin and rings with a small one.

Readouts: closed-loop gain, closed-loop bandwidth, gain-bandwidth product, phase margin in degrees, overshoot in percent.

Colours: `--c1` open-loop gain, `--c2` phase, `--c3` the crossover and the 1/β line, `--c4` the step response.

## Interaction

Controls: the DC gain A₀, the dominant pole, the second pole (with an on/off toggle), and the line 1/β as a draggable handle on figure 1. All handles are focusable and move with the arrow keys.

What should click: lower the closed-loop gain and the crossover slides toward the second pole, the margin shrinks and the step response starts to ring. A unity-gain buffer is the hardest case to keep stable, not the safest.

## Misconception

"More feedback is always better." It gains accuracy and bandwidth and costs margin. Second: "the closed-loop bandwidth equals the open-loop bandwidth." It is larger by 1 + T. Third: "a follower is the safe configuration." It has the largest β and so the lowest margin.
