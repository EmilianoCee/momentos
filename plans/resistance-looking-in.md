# Plan: Resistance looking in

```json plan
{
  "id": "resistance-looking-in",
  "title": "Resistance looking in",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["resistance-looking-in", "source-degeneration", "source-follower", "common-gate"],
  "prerequisites": ["thevenin-norton", "mos-small-signal-model", "common-source"],
  "size": "L",
  "tool": "circuits/amplifiers/resistance-looking-in.html"
}
```

## Concept

To find the resistance seen at a node, turn off the independent sources, apply a test voltage v_x there, find the current i_x it draws through the small-signal model, and divide. The transistor's controlled source can push current back against the test source, and that is why a resistor in the source raises the output resistance seen at the drain, and why the source follower has a low one. This is the most heavily examined skill in the amplifier chapters (29 questions in the survey), and the one most often done as a procedure with no picture.

## Picture

Figure 1 (640 by 400): the small-signal circuit of the chosen stage, with the test source v_x drawn at the chosen node and the current i_x as an arrow whose thickness follows the current. The controlled current g_m·v_gs is drawn as a second arrow, and r_o, R_S and R_D as boxes labelled with their voltage drops. The loop of current through the controlled source is highlighted when it opposes i_x.

Figure 2 (360 by 400): the solution as numbered lines that fill in one at a time: the v_gs the test source creates, the current in each branch, the sum at the node, then R = v_x / i_x.

Readouts: the resistance at the chosen node, and what it would be with the controlled source off, so that the boost factor is visible.

Colours: `--c1` test voltage v_x, `--c2` test current i_x, `--c3` controlled current g_m·v_gs, `--c4` resistances.

## Interaction

Buttons choose the stage and node: looking into the drain of a common-source stage with a resistor in the source, looking into the source of a source follower, looking into the source of a common-gate stage, and looking into the gate. Sliders: g_m, r_o, R_S. A "Next step" button reveals the solution one line at a time, and a "controlled source off" toggle shows the answer without the feedback through it. All controls move with the arrow keys.

What should click: with a resistor in the source, the controlled source pushes against the test source, so the resistance seen at the drain is multiplied by roughly one plus g_m·R_S. The full plan derives the exact expression and checks it with the reference script.

## Misconception

"The resistance looking into the drain is just r_o." It is r_o as seen through the feedback of the source resistor. Second: "turn off all the sources, including the controlled one." Only the independent sources are turned off; the controlled source stays, because it responds to the test source. Third: "the resistance looking into a source is always 1/g_m." That holds only when r_o is large and the load is small.
