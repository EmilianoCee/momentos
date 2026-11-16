## Per exam
- MT1 (EECS 16B FA25, Fall 2025, 1 h 20 min; instructors not printed): 100 pts, 6 questions. Fourier-series symmetry, wire resistance and resistivity, DC steady state with capacitors, Thevenin/Norton and max power, capacitor current to voltage, mesh analysis.
- MT2 (EECS 16B FA25, Fall 2025, 1 h 20 min; instructors not printed): 100 pts, 5 questions. Switched circuit with C and L (initial and final values, energy), RL step response, sinusoidal steady state with phasors, high-pass transfer function with Bode plots, matching six filters to magnitude plots.
- FINAL (EECS 16B FA25, Fall 2025, 2 h 50 min; instructors not printed): 100 pts, 8 questions. Breadboard to schematic, feedback sign, parallel-plate capacitor, RC divider transfer function, pole-zero Bode sketches, ideal op-amp, switched series RLC (second order), Thevenin/Norton with a dependent source.

Big observation: none of the three exams touches linear algebra, state-space models, eigenvalues, SVD, controllability, discretization, DFT or sampling. They cover only the circuits and first signals part of the course. The seed tags for those topics have zero rows.

## Notation
- Imaginary unit: j (jω in impedances). Phasor of V0 cos(ωt+φ) is V0 e^(jφ), also written V0 angle φ. Sines are converted to cosine first (sin(t+45 deg) = cos(t-45 deg)).
- Transfer function written H(ω) or H(jω) = Vout/Vin; magnitude |H|, phase angle H in degrees; Bode in log ω versus dB, with slopes in dB/dec.
- Corner frequency called ωc (rad/s); Bode asymptote sketches are accepted, with -3 dB measured relative to the passband level, not to 0 dB.
- Poles and zeros are given in the form (100+jω)/(10ω(10+jω)): the "s" variable is jω, and a pole at ω=0 is allowed.
- Feedback blocks: forward gain A, feedback gain β, summing junction with signed inputs; negative feedback gives Y/x = A/(1+Aβ).
- Second-order response: α (damping, here 40), ω0 = 1/sqrt(LC), ωd = sqrt(ω0^2-α^2); solution written e^(-αt)[D1 cos ωd t + D2 sin ωd t] + final value.
- First-order response: τ = L/Req or RC, x(t) = x(∞)(1-e^(-t/τ)) form.
- Source polarity: + at the top, "(+)" and "(-)" on sources; current arrows and VC polarity are always drawn; IB can come out negative.
- Switch exams: t=0-, 0+, ∞; continuity of VC and IL.
- No state-space or x' = Ax notation appears anywhere. No i versus j conflict (j only).
- Typical values: R from 0.5 ohm to 150 ohm in MT1, MT2 and Q6-Q8; R=10 kohm with C=3 uF in the final RC divider; C=1 uF to 1 F; L = 4 H or 8 H, 1 H in the final; sources 2 V to 100 V; ω = 1 rad/s in MT2 phasor problem.
- Units are demanded on every answer and have rubric points.

## Recurring question styles
- Steady-state or t=0-, 0+, ∞ analysis with C open and L short, then energy 1/2 CV^2 or 1/2 LI^2.
- Thevenin and Norton equivalents by open-circuit voltage and short-circuit current, with Rth = Vth/Isc (MT1 Q4, Final Q8).
- Transfer function of a small RC or RL network, then magnitude, phase and corner frequency (MT2 Q3 and Q4, Final Q4).
- Bode magnitude and phase sketches by asymptotes with slopes and levels labeled (MT2 Q4, Final Q5).
- Sketch a waveform from a piecewise input: capacitor current to voltage, or read Fourier symmetry from a plot.
- Draw the equivalent circuit for a time interval (t<0 or t>0) before computing.
- Match or classify from pictures: filters to plots (MT2 Q5), feedback sign (Final Q2), and parallel-plate capacitor changes (Final Q3).
- Write loop or node equations (mesh in MT1 Q6, KCL on ideal op-amp in Final Q6) and then use a constraint such as I=0.
- Switched RLC: derive second-order ODE, classify damping, fit initial conditions (Final Q7).
- Rubrics give partial credit for the correct setup, so each question is a chain of 2 to 5 sub-answers.

## Hard spots
- Final Q7c: needs dv/dt(0+) from iC(0+) = -iL(0+) and the initial-condition fit; iL(0-) is negative.
- Final Q5: pole at ω=0 makes the starting slope -20 dB/dec and the phase start at -90 or 0; the rubric penalises the wrong start. Phase flat at -45 deg between pole and zero needs thought.
- MT2 Q4 and Final Q4: corner frequency is where gain is 1/sqrt2 of the passband gain, not -3 dB absolute; the passband level is 3/4 (about -2.5 dB) or 1/2, not 1. The corner is 2/RC (R parallel with R), not 1/RC.
- MT2 Q3: converting sin to cos before taking the phasor, and noting that ω is read from the source (1 rad/s).
- MT1 Q5c: first reaching a value (10 V) requires counting the net gain per cycle and choosing the end of a rising segment.
- MT1 Q4: sign of Vth and of IN (both negative) and the efficiency at max power transfer (50 percent).
- Final Q2: classify the feedback sign when the forward block is -A or the feedback block is -β; sign of the whole loop is what counts.
- Final Q8: dependent source in Thevenin; Rth must come from Vth/Isc (or a test source), not by zeroing the source.
- MT2 Q5: matching needs the high-frequency and low-frequency limits for each circuit, including the pure wire (flat) and the divider (flat).
- Final Q3: predict which parameter changes double or halve the charge from Q = C V, C = εA/d, and avoid assuming one answer.

## Problems with the files
- All three files: figures are OCR'd to LaTeX, ASCII schematic and SPICE netlist, so the question text is often interleaved with generated netlists. Some OCR descriptions are wrong or invent unlabeled parts (MT1 Q3 solution schematic shows an unspecified "R_X"; the shunt and node names are added by the converter).
- Exam_Midterm1_Solution.md: Q1 plots described only in OCR text; Q2b area printed as "2A=4mm" (garbled; read as 4 mm^2); Q3 sub-part letters do not match between the question (a, b=12 pts, c, d, e) and solution/rubric (a=12, b=4, c=2, d=2), so rows are Q3a and Q3b-d; Q3 solution says "V_C1 = 4" in the energy line where VC1 is 2 V (E = 2 uJ still correct); Q5 solution has typos ("3 ms", "0.01 x 1"); Q6 solution equations are scrambled and the part b OCR uses I1, V_ac for I20, V_DC.
- Midterm_2_rubrics_solution.md: Q1 and Q2 solution OCR has the wrong schematics in places (Q2a lists R2=9 ohm, an invented R3; Q2b lists R2=6 ohm); the real values are 8, 8, 4 ohm and 4 H from the problem text. Q5 is only a short answer key (a-iii, b-i, c-i, d-iii, e-ii, f-ii) and the key is not consistent with the circuits as drawn (a is RL with output across L, a high-pass), so I tagged it without re-deriving; the rubric lists point values e and f twice (3+3+3+3+4+4 = 20). The right-hand plots are not readable beyond labels.
- Final_exam_EECS16B_solution.md: cover table lists Problems 1 to 7 and Problem 8 is on page 2; points still sum to 100 (10, 6, 4, 10, 15, 20, 20, 15). Q4a handwritten solution is cropped (reads "62.7 rad/..." and "66.7 rad/s"; 66.7 = 2/(RC) is the consistent value). Q5 part c solution plot has only 0 deg and -45 deg annotations. Q7 per-part points are inferred from the rubric (3, 3, 14); the printed statement gives only 20 total. Q6 solution part e says "I_1 ohm" for the 10 ohm resistor.
- No PDFs were opened: the markdown was enough to tell what each question tests.
