# Plan: Ideal op-amp and the virtual short

```json plan
{
  "id": "ideal-op-amp",
  "title": "Ideal op-amp and the virtual short",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["ideal-op-amp", "feedback"],
  "prerequisites": ["kcl", "dividers", "nodal-analysis"],
  "size": "M",
  "tool": "circuits/amplifiers/ideal-op-amp.html"
}
```

## Concept

An op-amp has a very large gain A. With negative feedback it moves its output until its two inputs are at the same voltage. That pins the inverting input (the virtual short), no current enters either input, and the gain of the circuit is set by two resistors alone. Overlap: EE 120 asks about feedback in the same terms, so the tool serves both.

## Picture

Figure 1 (640 by 360): the circuit, with a node voltage on every wire and an arrow on every branch whose thickness follows the current. A small gauge beside the input pair shows v_diff = V₊ − V₋ in microvolts, so it can be seen shrinking to zero.

Figure 2 (480 by 300): the closed-loop gain against the open-loop gain A (log axis, 10 to 10⁶). The curve climbs toward the ideal gain and flattens against it, which is drawn as a dashed line.

Panel (beside figure 1): the three-line recipe: V₊ = V₋, no current into the inputs, KCL at the pinned node.

Readouts: v_out, v_diff, the gain error as a percentage.

Colours: `--c1` voltages (v_in, v_out), `--c2` currents, `--c3` v_diff, `--c4` resistances.

## Interaction

Controls: a topology selector (inverting, non-inverting, follower), sliders for R₁, R₂, v_in and A, and a toggle that clips v_out at the supply rails. A "swap the inputs" toggle turns the feedback positive and shows the output slam to a rail, so the learner sees that the virtual short needs negative feedback. All controls move with the arrow keys.

What should click: as A rises, v_diff shrinks toward zero and the gain stops depending on A. The error falls in proportion to 1/(loop gain), which the next tool makes visible.

## Misconception

"A virtual short means the inputs are joined by a wire." No current flows between them; they only sit at the same voltage. Second: "the rule holds for any connection." It holds only with negative feedback. Third: "the output sets the input difference." The reverse: the difference is the output divided by A.
