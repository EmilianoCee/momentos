# Plan: Thévenin and Norton equivalents

```json plan
{
  "id": "thevenin-norton",
  "title": "Thévenin and Norton equivalents",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105"],
  "topics": ["thevenin-norton"],
  "prerequisites": ["ohms-law", "kvl", "dividers", "nodal-analysis"],
  "size": "S",
  "tool": "circuits/thevenin-norton.html"
}
```

## Concept

Seen from two terminals, a network of resistors and sources is one voltage source V_th (volts) in series with one resistance R_th (ohms). R_th is the number the later tools keep asking for: the resistance a capacitor charges through, and the resistance an amplifier presents at its input and output. This is the bridge tool for the RC and amplifier tools, which is why it comes first despite its low weight in the curriculum.

## Picture

Figure 1 (640 by 360): a fixed ladder of three resistors and one source on the left, terminals A and B on the right, and a load R_L across them. Each node shows its voltage and each branch an arrow whose thickness follows the current.

Figure 2 (420 by 360): v_AB (volts) against i (milliamps). The network is a straight line from the open-circuit voltage V_oc on the voltage axis to the short-circuit current I_sc on the current axis. The load is a second line through the origin. They cross at the operating point.

Readouts: V_oc, I_sc, R_th = V_oc / I_sc, v_AB, i.

Colours: `--c1` voltage (V_oc, v_AB), `--c2` current (I_sc, i), `--c3` resistance (R_th, R_L).

## Interaction

Sliders: the three ladder resistances, the source voltage and R_L (log scale for the resistances). A "source off" toggle replaces the source by a short and draws an ohmmeter across A and B, which reads R_th: this shows that "turn the sources off and look in" gives the same number as V_oc / I_sc. A "Norton" toggle redraws the equivalent as I_sc in parallel with R_th. All sliders move with the arrow keys.

What should click: V_th is what the terminals see with nothing connected, R_th is what they see with the sources off, and the load line then answers every possible load at once.

## Misconception

"R_th is the resistors in series with the source." In the ladder, one resistor sits across the terminals and, with the source off, it is in parallel with the rest. Second: "the equivalent behaves like the original inside." Only the behaviour at the terminals matches; the power dissipated inside the network is different.
