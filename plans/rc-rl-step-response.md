# Plan: RC and RL step response

```json plan
{
  "id": "rc-rl-step-response",
  "title": "RC and RL step response",
  "status": "stub",
  "kind": "tool",
  "courses": ["EE 105", "EE 120"],
  "topics": ["first-order-system", "step-response"],
  "prerequisites": ["ohms-law", "kvl", "thevenin-norton"],
  "size": "M",
  "tool": "systems/rc-rl-step-response.html"
}
```

## Concept

An RC or RL circuit with one energy store and a constant source follows x(t) = x_final + (x_start − x_final)e^(−t/τ), where x is the capacitor voltage v_C or the inductor current i_L. Find three numbers (the start, the final value and τ) and the circuit is solved. Overlap: EE 120 asks the same thing of first-order systems, so one tool serves both courses.

## Picture

Figure 1 (640 by 300): the circuit. A source V_S (volts), a switch, a resistor R (ohms), and the store: a capacitor C (farads) or an inductor L (henries), chosen by a toggle. A second resistor R_2 can be added across the store, so that τ must use the Thévenin resistance the store sees (R_1 in parallel with R_2) and not just the nearest resistor. A "t = 0⁺" view redraws the store as a voltage source (capacitor) or a current source (inductor) holding its starting value. A "t → ∞" view redraws it as an open circuit (capacitor) or a short (inductor).

Figure 2 (640 by 360): the state variable against time in seconds. The start is a dot, the final value a dashed line, and the tangent at t = 0⁺ runs up to the final value and meets it at t = τ. Marks at τ, 2τ, 3τ and 5τ say how much of the change is done. A thin second trace shows the quantity that jumps at the switch (i_C for the capacitor, v_L for the inductor). Readouts: τ, x_start, x_final, x at the cursor.

Colours: `--c1` state variable (v_C or i_L), `--c2` the quantity that jumps (i_C or v_L), `--c3` time constant (τ, tangent, marks), `--c4` source.

## Interaction

Sliders (log where the range is large): R, C or L, V_S, the starting value of the state, R_2 (when present). A switch button closes and opens the circuit. A "square wave" mode opens and closes it every half period, with the period as a multiple of τ. A draggable cursor on time reads off x(t). Every handle is focusable and moves with the arrow keys.

What should click: only the state variable is continuous. v_C and i_L cannot jump; every other voltage and current can, and the circuit at t = 0⁺ and at t → ∞ is a resistor circuit you already know how to solve.

## Misconception

"A bigger C charges faster." It charges slower, because more charge has to move through the same R. Second: "τ uses the nearest resistor." It uses the resistance the store sees looking out, with the sources turned off. Third: "the capacitor reaches V_S after time RC." It reaches 63% of the change, and about 99% after 5τ.
