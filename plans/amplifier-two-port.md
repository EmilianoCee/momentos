# Plan: Amplifier as a two-port, and loading

```json plan
{
  "id": "amplifier-two-port",
  "title": "Amplifier as a two-port, and loading",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["amplifier-two-port"],
  "prerequisites": ["dividers", "thevenin-norton"],
  "size": "S",
  "tool": "circuits/amplifiers/amplifier-two-port.html"
}
```

## Concept

Seen from outside, any amplifier is three numbers: its input resistance R_in, its open-circuit gain A_v0 (the gain with nothing connected to the output), and its output resistance R_out. The source and the load each form a voltage divider with them, so the gain you get depends on what you connect.

## Picture

Figure 1 (640 by 260): a source v_s with its resistance R_S, the amplifier as a box with R_in, a controlled source A_v0·v_in and R_out, then a load R_L. Voltages are labelled at the input node (v_in) and the output node (v_out).

Figure 2 (640 by 200): a staircase of bars for v_s, v_in, A_v0·v_in and v_out. The drop at each divider is visible as the step down, so the reader sees where the signal is lost.

Readouts: the two loss factors R_in/(R_in + R_S) and R_L/(R_L + R_out), and the net gain v_out / v_s.

Colours: `--c1` voltages, `--c2` gain factors, `--c3` resistances.

## Interaction

Sliders for R_S, R_in, A_v0, R_out and R_L, with log scales for the resistances. Preset buttons load typical numbers for a common-source stage, a source follower and a common-gate stage. An "ideal voltage amplifier" checkbox sets R_in very large and R_out very small. All controls move with the arrow keys.

What should click: the gain you get is A_v0 times two dividers. A good voltage amplifier has R_in much larger than R_S and R_out much smaller than R_L. That is why a source follower, whose A_v0 is a little under 1, is still worth building: it protects the gain of the stage in front of it.

## Misconception

"The gain of the amplifier is A_v0, whatever you connect." It falls as the load gets heavier or the source gets weaker. Second: "a high output resistance is a good thing." For a voltage amplifier it is a loss; for a current source it is the whole point.
