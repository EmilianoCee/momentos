# EECS 16B homework survey, Fall 2025

## Scope
Term: Fall 2025 (FA25). The course is titled "Introduction to Circuits & Devices" on every set. All nine sets are circuits only. There is no linear algebra, state-space, eigenvalue, SVD or feedback-control content in any problem, so none of the state-space seed tags occur. Problems cite textbook numbers of the form UMF x.y. Each set is nominally one week long.

- PSET1, due Fri Sep 19: Fourier series (coefficients, time shift, partial-sum plots); charge and current; resistivity; power loss in cables; KCL/KVL.
- PSET2, due Fri Sep 26: series-parallel resistors; resistive dividers; battery-threshold design; KCL/KVL equations; node-voltage with a dependent source; superposition.
- PSET3, due Fri Oct 3: mesh analysis; superposition from data; Wheatstone bridge and ADC resolution; Thevenin/Norton; black-box Thevenin and max power.
- HW4, due Fri Oct 10 (solutions Oct 12, midterm week): linear-network black box; series-parallel capacitors; capacitor v-i and energy; power-rail IR drop; decoupling capacitor and ripple.
- HW5, due Fri Oct 24 (assigned Oct 17): DC steady state with L and C; series-parallel inductors; inductor v-i and energy; first-order RC with switches.
- HW6 (solution file), due Fri Oct 31: RL transients (one with a dependent source); complex numbers in polar form; phasor conversion; series R with parallel L-C in the frequency domain and average power.
- HW7, due Fri Nov 7 (late to Nov 9 because Midterm 2 is Nov 13): impedance from v and i; in-phase condition; complex power balance; Bode plot of an RC current divider; transfer function from a Bode plot.
- HW8, due Fri Nov 21: straight-line Bode sketches of four transfer functions; series RLC; parallel RLC; mixed RL and RC transient.
- HW9 (solution file), assigned Sun Nov 23, due Mon Dec 8: op-amp finite-gain model; ideal op-amp with inverting, TIA, summing, instrumentation, integrator, differentiator and an AC low-pass; supply rails and linear range.

## Notation
- Imaginary unit is j. Polar form is A∠Φ in degrees. The HW6 solution says polar form (not exponential) is required on exams.
- Phasors use the cosine reference with peak amplitude: 4cos(377t-30°) V becomes 4∠-30° V. A sine is converted by subtracting 90° from its phase (sin(x) = cos(x-90°)). The time function is written back as cosine, with ω = 2πf.
- Transfer functions are written H(jω) (some HW8 forms H(ω) with jω inside the expression). Gain in the Bode plot is M in dB against log ω; phase in degrees against log ω. Corner frequency is ω_c, in rad/s. Current transfer functions such as H = i_C/i_s occur, not only voltage ones.
- Impedances: R, jωL, 1/(jωC). Z is written in rectangular form x+jy for some parts and polar for others.
- Complex power: S = P + jQ = (1/2) V I* with peak phasors, equal to V_rms I_rms∠(Φ_V - Φ_I). Average resistor power is I_rms² R = |I|²R/2.
- Transient answers are written x(t) = A + B e^(-t/τ) with the values x(0-), x(0+), x(∞); the rubric accepts τ or α. Time constants: τ = RC, τ = L/R_eq (R_eq found with a test source or Voc/Isc when a dependent source is present).
- Op-amp: golden rules V_p = V_n and i_p = i_n = 0 (v_+, v_- called V_p, V_n); gain G = v_o/v_s; feedback resistor R_f; supply written V_cc; "rail-to-rail" means output limited to the supply.
- Sign conventions: mesh currents clockwise; V_ab = V(a) - V(b); i_C and v_C polarities are marked on each figure.
- Typical values: 5 V/0.5 ohm and 50 V/50 ohm (PSET1), kΩ with µF/nF/mF/mH, 377 rad/s (60 Hz), 5×10^4 rad/s, 2π·10^4 rad/s, 2000 rad/s with R=2 kΩ, 10 kΩ, C=0.1 µF.

## Recurring question styles
- Find a state at t=0-, t=0+ and t=infinity with the switch moved, then write the exponential (RC, RL, RLC).
- Equivalent resistance, capacitance or inductance of a network with crossings or equal parts.
- Superposition, Thevenin or black-box inference from measured data, then power or max power.
- Write the node or mesh equations, then solve them, often with a dependent source.
- Convert between time domain and phasors (sine/cosine, sums of sinusoids), then compute Z and i(t).
- Derive an op-amp gain with the golden rules, then check the output is inside the supply rails.
- Plot or sketch: waveform from a waveform, Bode straight-line from H, H from a Bode plot.
- Choose a component to meet a spec (threshold, power, in-phase condition, critical damping, ripple).
- Short "explain/predict" stems: more overdamped means R up or down, lag or lead, limits at DC and infinity.
- Reuse of a hand result: the answer to part (a) is plugged into later parts and checked against the textbook formula.

## Hard spots
- Initial conditions across a switch for inductors and capacitors, especially when a dependent source stops a plain RC or L/R reading (HW6 Q1b).
- Damping classification and the direction of change with R in series versus parallel RLC (HW8 Q2f, Q3e).
- Parallel LC above resonance looks capacitive; the sign of Z flips (HW6 Q4).
- In-phase condition and lead or lag as the frequency moves off it (HW7 Q2).
- Building H(jω) from a piecewise Bode plot, including flat ends and a double zero (HW7 Q5).
- Straight-line Bode with 1/jω, repeated poles, quadratic factors and a j factor (HW8 Q1).
- Integrator and differentiator from the same op-amp layout, with the initial output kept (HW9 Q5).
- Rail limits and linear input range for an inverting amp, including Rf = 0 (HW9 Q2c).
- Design with a power rating or resolution limit (PSET2 Q1c, PSET3 Q3b, HW4 Q4e).
- Fourier coefficients by integration by parts, and what a time shift does to phase (PSET1 Q1).

## Problems with the files
- EECS16B_PSET1.md: page text runs words together in places (Q2, Q3 have lost spaces and some exponents, such as the conductivity in Q3c(i) and the electron count in Q3b). Figures are only given as OCR text.
- EECS16B_PSET2.md, EECS16B_PSET3.md, EECS16B_HW4.md, EECS16B_HW5 (1).md, EECS16B_HW7 (1).md, EECS16B_HW8 (1).md: no spaces between words; minus signs, degree marks and square roots are dropped in many equations (for example HW8 Q2 "t>=0" parts, HW7 Q3 source phasor angles, HW7 Q1 and Q4 angles). Several figures (PSET2 Fig 2, 5; PSET3 Fig 2, 5; HW4 Fig 4, 8-11) are only scattered symbols or OCR labels; the OCR transcription is usually enough.
- HW5 Q5: the OCR circuit puts the switch between R1 and C1; I could not confirm the intended i(t) from the file alone.
- EECS16B_HW6_sol (1).md: Q1 solutions are handwritten and OCR'd, parts of several equations are cropped (end of Q1b method 2, page 7 equations). In Q4(b) the text prints omega as "510" but the solution uses 5×10^4 rad/s; Q4(e) final line prints 5×10^3 where 5×10^4 is meant. Only Q1 (a, b) plus Q2, Q3, Q4 exist; the first page of Q2 is cut at the left edge.
- EECS16B_HW9_sol.md: Q2 is printed as 50 pt but only parts a, b, c (30 pt) are present; Q3 is 34 pt but only a, b (20 pt) are present. Probably parts are missing or the totals are mislabelled. Q2b is mislabelled "1(b)" by the OCR. Several solutions are cut at the bottom of the image (Q2c(2) Rf = 0 result, Q3 final lines, Q6a boxed result, Q5b component values).
- HW6 and HW9 files contain solutions only for the problems shown; no rubric points sum check was possible for the sub-parts.
