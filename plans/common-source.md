# Plan: Common-source stage: gain and swing

```json plan
{
  "id": "common-source",
  "title": "Common-source stage: gain and swing",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["common-source", "output-swing", "intrinsic-gain"],
  "prerequisites": ["square-law", "mosfet-regions", "channel-length-modulation", "small-signal-analysis"],
  "size": "M",
  "tool": "circuits/amplifiers/common-source.html"
}
```

## Concept

Put a resistor R_D between the drain and V_DD and the output becomes a curve of its own. On its steep middle part, where the transistor is saturated, the gain is −g_m times (R_D in parallel with r_o). That part is bounded by cut-off on one side and triode on the other, and the distance between them is the output swing. The ceiling on the gain is the intrinsic gain g_m·r_o, which belongs to the transistor and not to the resistor.

## Picture

Figure 1 (640 by 360): v_OUT against v_IN (volts). Flat at V_DD in cut-off, a steep fall in saturation, and a flattening again in triode, with the three regions shaded. The bias point is a draggable dot, and the tangent through it shows the slope, which is the gain.

Figure 2 (640 by 240): the input sine and the output sine against time, with the output visibly clipped wherever it leaves saturation.

Figure 3 (360 by 240): the small-signal circuit with its gain written beside it.

Readouts: gain, bias v_OUT, the upper and lower limits of the output swing, and the headroom v_DS − V_OV.

Colours: `--c1` input voltage, `--c2` output voltage, `--c3` gain (the slope), `--c4` the limits of the swing.

## Interaction

Controls: draggable bias point (V_GS), R_D, W/L, the channel-length-modulation parameter λ (which sets r_o), the signal amplitude. A button "R_D → large" sends R_D upward to show the gain flatten at the intrinsic gain while the bias point is forced toward triode. All controls move with the arrow keys.

What should click: raising R_D raises the gain only until the stage runs out of headroom. At a fixed supply, more R_D means either less current (so less g_m) or less voltage across the transistor. The gain cannot be pushed up forever; the ceiling is g_m·r_o.

## Misconception

"The gain is −g_m·R_D, always." It leaves out r_o, and it holds only in saturation. Second: "a bigger R_D gives a bigger swing." It shrinks the swing, because the same current drops more voltage across it. Third: "the minus sign means something is wrong." The stage inverts: the output goes down when the input goes up.
