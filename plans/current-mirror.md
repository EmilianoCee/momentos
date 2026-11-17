# Plan: Current mirror

```json plan
{
  "id": "current-mirror",
  "title": "Current mirror",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["current-mirror", "diode-connected-transistor", "current-source-load"],
  "prerequisites": ["square-law", "channel-length-modulation", "mos-small-signal-model"],
  "size": "M",
  "tool": "circuits/amplifiers/current-mirror.html"
}
```

## Concept

A diode-connected transistor turns a reference current into a gate voltage. A second transistor given the same gate voltage copies the current, scaled by the ratio of their W/L. It acts as a current source: flat while it stays in saturation, with a small slope set by r_o, and collapsing once its drain voltage falls below the overdrive V_OV. Used as a load in place of R_D it gives a common-source stage a gain of g_m·r_o. Old exams only, so it ranks below the other amplifier tools.

## Picture

Figure 1 (640 by 300): the circuit. The reference current I_REF into a diode-connected M1, a second transistor M2 whose drain sits on a source of variable voltage V_out.

Figure 2 (640 by 360): I_out against V_out (milliamps against volts). Flat in saturation, falling to zero in triode below V_OV, with a small slope of 1/r_o on the flat part. A dashed horizontal line marks the ideal copy I_REF multiplied by the W/L ratio.

Figure 3 (360 by 240): the same M2 replacing R_D in a common-source stage, drawn with its small-signal gain.

Readouts: I_out, the copy error as a percentage, r_o, and the lowest V_out at which M2 is still in saturation.

Colours: `--c1` reference current, `--c2` output current, `--c3` the shared gate voltage, `--c4` overdrive.

## Interaction

Controls: the W/L ratio of M2 to M1 in whole steps, V_out as a draggable dot along the curve, λ, and a toggle that swaps R_D for M2 in the third figure. All controls move with the arrow keys.

What should click: the copy is exact only when the two drain voltages match. Any difference shows as an error of ΔV/r_o, and the mirror stops working at all below V_OV.

## Misconception

"A mirror copies the current whatever the output voltage." It copies it only inside saturation, and only roughly, because of r_o. Second: "the diode-connected transistor is a plain resistor of 1/g_m." That is its small-signal resistance at one bias; its large-signal behaviour is the square law.
