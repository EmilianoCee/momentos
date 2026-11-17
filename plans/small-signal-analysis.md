# Plan: Bias point and small-signal analysis

```json plan
{
  "id": "small-signal-analysis",
  "title": "Bias point and small-signal analysis",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["operating-point", "small-signal-analysis", "transconductance", "mos-small-signal-model"],
  "prerequisites": ["square-law", "mosfet-regions"],
  "size": "M",
  "tool": "circuits/amplifiers/small-signal-analysis.html"
}
```

## Concept

A transistor amplifier is a DC bias that picks a point on a curve, plus a small wiggle that sees only the slope there. The transconductance g_m (siemens) is that slope, and the small-signal model is the tangent line redrawn as a circuit: a current source g_m·v_gs, with r_o across it.

## Picture

Figure 1 (640 by 360): the saturated NMOS curve i_D against v_GS (milliamps against volts). The bias point is a dot, the tangent through it is drawn over the curve, and a small sine on v_GS sits below the horizontal axis. The resulting drain-current waveform stands beside the vertical axis, as in the classic rotated-waveform picture, so the reader sees the wiggle go up the slope and come out the side.

Figure 2 (640 by 240): two circuits side by side. On the left the transistor with V_DD and R_D, with all the DC sources drawn. On the right its small-signal version: v_gs, the source g_m·v_gs, r_o and R_D, with the DC sources replaced by ground, because they do not change.

Readouts: V_GS, I_D, the overdrive V_OV = V_GS − V_T, g_m, and the second harmonic of the drain current as a percentage of the fundamental, which is the error of the linear model.

Colours: `--c1` gate voltage (V_GS and v_gs), `--c2` drain current (I_D and i_d), `--c3` transconductance (the tangent), `--c4` overdrive.

## Interaction

Controls: a draggable bias point on the curve (V_GS), a signal amplitude slider, a W/L slider, and a toggle that fades the DC sources and shows the small-signal circuit alone. A second toggle chooses between the total waveform and the signal part only. All controls move with the arrow keys.

What should click: g_m is not a property of the transistor alone, it is a property of the bias point. Move the dot and the slope changes. Raise the amplitude and the output stops looking like the input, which is what "small" means.

## Misconception

"The small-signal model is a different transistor." It is the same transistor, linearised about one point. Second: "DC sources are zero volts in the real circuit." They are zero change: they hold their voltage, and the signal does not move them. Third: "g_m is a fixed number, like R." It moves with I_D.
