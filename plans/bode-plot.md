# Plan: Bode plot from poles and zeros

```json plan
{
  "id": "bode-plot",
  "title": "Bode plot from poles and zeros",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["bode-plot", "transfer-function", "poles-and-zeros"],
  "prerequisites": ["phasors-impedance", "first-order-system"],
  "size": "M",
  "tool": "systems/bode-plot.html"
}
```

## Concept

A transfer function is a product of poles and zeros. On log axes each one adds a bend of 20 dB per decade at its corner frequency, so you can sketch |H(jω)| and the phase by adding straight lines. An RC or RL circuit is the simplest case: one pole. Shared with EE 120, so build it once for both courses.

## Picture

Figure 1 (640 by 300): magnitude in dB against ω in rad/s on a log axis, from 10⁰ to 10⁷. The straight-line asymptotes are drawn first and the exact curve over them.

Figure 2 (640 by 300): phase in degrees against the same ω axis. The exact curve, and the three-segment straight-line sketch (flat, ±45° per decade across the two decades around the corner, flat) over it.

Figure 3 (360 by 300): the s-plane with σ across and jω up, poles as crosses and zeros as circles, so the plane and the Bode plot always show the same system.

Figure 4 (640 by 240): the chosen circuit (RC low-pass, RC high-pass, RL low-pass, RL high-pass) with, below it, the input and output sinusoids at the cursor frequency in the time domain. The output's amplitude ratio and delay are visible without any formula.

Readouts: corner frequency in rad/s and in Hz (with 1/RC against 1/(2πRC) shown side by side), |H| in dB and as a ratio, phase in degrees.

Colours: `--c1` magnitude (figure 1 and the output waveform), `--c2` phase, `--c3` corner frequency and pole position. The input waveform stays neutral.

## Interaction

Two modes. In circuit mode a selector picks one of the four circuits and sliders set R and C or L; the pole sits at 1/(RC) or R/L. In free mode up to three poles and two zeros are draggable markers on the frequency axis (real ones only). A cursor on the frequency axis drags across both Bode plots and sets the frequency of the time-domain waveforms. All handles are focusable and use the arrow keys.

What should click: the corner is where the real part of the denominator equals the imaginary part, which is why the magnitude is 1/√2 (−3 dB) and the phase is −45° exactly there, and why the phase takes a decade on each side to finish its turn.

## Misconception

"At the corner the output is half the input." It is 0.707 of the amplitude, half the power. Second: "the phase is −90° at the corner." It is −45°, and reaches −90° only far above it. Third: "the corner is at 1/RC Hz." It is at 1/RC rad/s, which is 1/(2πRC) Hz.
