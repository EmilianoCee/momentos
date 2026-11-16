# EE 105 SP24 homework survey notes

## Scope
All eleven homeworks are Spring 2024, Prof. Alp Sipahigil, issued on Fridays and due a week later (HW9 had two weeks).
- HW1 (issued Jan 19, due Jan 26): EE 16A/B review: KCL/KVL, Thevenin/Norton, RL step, capacitor charging with switched current source.
- HW2 (due Feb 2): LTI systems; RL step/impulse/exponential response; superposition; series RLC resonator with Laplace transfer function and Q.
- HW3 (due Feb 9): Laplace and inverse Laplace practice; bypass capacitors on a power network; reading a Bode plot to build a model.
- HW4 (due Feb 16): convolution; non-ideal op-amp model with finite gain, Rin, Rout; two-pole unity-gain active filter.
- HW5 (due Feb 23): semiconductor basics (bands, Fermi factor, mobility, ni versus T); op-amp offset, bias current and slew rate.
- HW6 (due Mar 1): doped-bar resistivity and current density; diffusion and Einstein relation; IC capacitor and resistor; pn junction charge and field sketches.
- HW7 (due Mar 8): pn junction numerics (built-in potential, width, capacitance, forward current, small-signal); 1/C^2 extraction; qualitative questions.
- HW8 (due Mar 22): MOS capacitor (p and n substrate): regimes, sketches, threshold-voltage build-up.
- HW9 (due Apr 5): MOSFET regions of operation; MOS C-V and threshold; long-channel I-V numbers.
- HW10 (due Apr 12): MOSFET small-signal parameters (gm, ro, gmb, capacitances); NMOS and PMOS common-source gain; body effect.
- HW11 (due Apr 19): single-stage amplifiers: common-gate, PMOS source follower, body-effect gain with gate versus body input.

Pace: about 4 weeks of EE 16B-style circuits and signals, 3 weeks of device physics, then MOS and amplifiers. Homework covers no BJT, no cascode or mirror, no differential pair, no frequency response of amplifiers (Miller, time constants), and no feedback beyond ideal op-amp. Those seed tags have zero items.

## Notation
- Imaginary unit: homework text uses j (exp(j omega t), s = j omega).
- Kirchhoff and Thevenin items are in the EE 16A/B style. Dependent-source op-amp model: input resistance Rin, output resistance Rout, gain A.
- Laplace: u(t) step, delta(t) impulse, loaded Q written Q', K is gain at resonance, standard bandpass form K (w0/Q' s)/(s^2 + (w0/Q') s + w0^2).
- Thermal and Si constants: kT/q = 26 mV (HW7), ni = 1e10 cm^-3 at 300 K, Eg = 1.12 eV, eps_Si = 11.7 eps0 (HW7) or 12 eps0 (HW6, HW8, HW9), eps_ox = 4 eps0, eps0 = 8.854e-12 F/m. Mixed units: cm^-3 doping with m or um geometry; convert before using C/N-m^2.
- Mobility figure: at Nd+Na = 1e18 cm^-3, electrons 330, holes 160 cm^2/Vs. HW7 uses 100 cm^2/Vs (electrons, p side) and 400 (holes, n side), Ln = 2.3 um, Lp = 3.2 um, junction area 1 um^2.
- HW6 doping: 6e15 cm^-3 As and 4e15 cm^-3 B (reading of garbled exponents), 1 um bar, 1 V; pn junction NA = 1e18, ND = 1e17 cm^-3 (reading of garbled exponents), built-in potential 0.9 V given, eps_r Si = 12.
- HW7 doping: ND = 1e17 cm^-3 (n side), NA = 1e20 cm^-3 (p side). Field profile asks for n side on the left, opposite to the usual figure.
- HW8: VFB = -0.53 V, NA = 1e17 cm^-3, tox = 3 nm, n-type MOSCAP ND = 1e17 cm^-3. HW9: VFB = -0.45 V, NA = 1e16 cm^-3, tox = 5 nm; MOSFET: W = 100 um, L = 1 um, tox = 10 nm, NA = 1e15, VFB = -0.2 V, mu_n = 300 cm^2/Vs.
- HW9 Q1: VTN = 0.9 V, |VTP| = 1 V. The PMOS source is the high-potential terminal; use VSG and VSD. No body terminals drawn.
- Region definitions given in HW9: linear for VDS much less than VGS-VT, triode with (VGS-VT-VDS/2)VDS, saturation with (1+lambda VDS) factor; subthreshold ignored (IDS = 0 below VT).
- HW10 Q1: W/L = 10, VT = 0.5 V, mu_n = 400 cm^2/Vs, Cox = 4e-7 F/cm^2 (reading of garbled text), lambda = 0.01 V^-1. HW10 Q3: VGS = 1 V, VDS = 1 V, VSB = 0.2 V, VTN = 0.5 V, W = 10 um, L = 1 um, mu_n = 400, Cox = 3.45e-3 F/m^2, Cj0 = 1e-3 F/m^2, Cjsw0 = 4e-10 F/m, mj = 0.5, phi_b = 0.9 V (junction caps) and 0.3 V (gmb), LD = 0.05 um, fringe C = 1 fF. Use the reader's equations, not the slides (printed warning); phi_b = phi_p reading is garbled.
- HW11: Q1 gm = 15 mA/V, ro infinite, resistors 5k, 10k, 2k; Q2 k_p = mu Cox W/L = 0.75 mA/V^2, VTp = -3 V, VDD = 12 V, VG = 0 V, RL = 3 kohm (Rs symbolic); Q3 VTn = 1 V, k = mu Cox W/L = 1e-3 A/V^2 (reading of garbled exponent), lambda = 0, gamma = 0.5 V^1/2, phi_p = -400 mV (printed), VDD = 5 V, bias divider 2k/3k, RD = 1k, body resistor 1.2k. gmb = gm gamma/(2 sqrt(2|phi_p| - VBS)) per printed hint, sign conventions for VBS and phi_p matter.
- Signs: current direction for op-amp bias currents I1, I2 flows from ground into the inputs (HW5). Offset source polarity + on the left.
- Time constant: capacitor current i = C dv/dt; HW1 Q4 uses 2*I0 sink current and a 50 percent duty cycle with period T.

## Recurring question styles
- Compute a numeric answer from given doping, geometry and constants, with units (HW5-HW9).
- Sketch a profile or waveform with labelled critical points: charge, field, potential, Q-V, C-V, Bode, switched capacitor voltage (HW1, HW3, HW4, HW6, HW8, HW9).
- Derive a transfer function or gain symbolically, then take limits to simplify (HW2, HW4, HW10, HW11).
- Classify an operating region from terminal voltages, with polarity changes for PMOS (HW9, HW10, HW11).
- Short explain or why questions in physical words (HW5, HW7, HW8).
- Extract parameters from a measured plot (Bode in HW3, 1/C^2 in HW7, mobility curve in HW6).
- Draw the small-signal model first, then compute gain, Rin or Zin (HW4, HW10, HW11).
- Multi-part chain: each part reuses the previous result (HW7 Q1, HW8 Q1, HW9 Q2-Q3, HW10 Q1).
- Compare two cases and say which direction a quantity moves (HW5 Q3d, HW11 Q3d, HW1 Q4c).

## Hard spots
- Why current does or does not flow at 0 K, at equilibrium and in steady state (HW5): needs carrier and field reasoning, not formulas.
- Charge, field and potential sketches for a pn junction and a MOSCAP across three regimes, both substrate types (HW6, HW8).
- The precise inversion condition (surface potential equals 2 phi_F), not just Vgs above VT (HW8 Q1a).
- Building a MOS C-V and Q-V curve with VFB, VT, Cox, Cmin marked (HW9 Q2).
- Choosing triode versus saturation by testing VDS against VGS-VT and applying lambda only in saturation (HW9 Q3).
- PMOS polarity and maximum-load design for saturation (HW9 Q1, HW10 Q2a, HW11 Q2e).
- Body effect: gmb enters as a second controlled source; body tied to output changes gain; body driven as input (HW10 Q2c, HW11 Q3).
- Slew-limited output sketch: triangle with calculated rise and fall times (HW5 Q4b).
- Modeling a black box from a Bode plot with one R and two L (HW3 Q3) and from Q, w0 of an RLC (HW2 Q3).
- Op-amp non-ideal model limits: Rin to infinity, Rout to zero, A to infinity in sequence (HW4 Q2).
- Which squares of an IC resistor layout carry current (HW6 Q3b).

## Simulation and lab work
None of the eleven homeworks asks for SPICE, MATLAB, Python or any lab measurement. Netlists in the files are OCR image transcriptions, not assignments. Hand calculation only.

## Problems with the files
- Homework_1.md: math symbols partly lost (subscripts of I1, I2, R1, R2 and the Thevenin figure labels); the Q2 circuit has no OCR so values are read from text only (VS 10 V, IS 0.25 A, resistors 10, 15, 20 ohm); Q4 source magnitude figures partly garbled.
- Homework_2.md: Greek letters appear as (cid:xxxx) codes; Q2 circuit has no OCR and sources are garbled, value names read as I0, V1, Q, t0 only partly.
- Homework_3.md: Q1 variables, Q2 figure text and Q3 values are scrambled (symbols and Greek out of order); Bode plot data are not in the file, only axis ticks, so pole and zero frequencies cannot be recovered.
- Homework_4.md: Q2 circuit labels run together; formula for Q3 hints garbled.
- Homework_5.md: Q4 equation of the input pulse garbled; exponents in Q3c lost in places.
- Homework_6.md: Q1 and Q4 doping exponents garbled (digits run together, "6*10cm of As and 4*10cm of B" and "N=1*10cmand N=1*10cm"); Q3b layout partly interpreted.
- Homework_7.md: Q1 mobility, diffusion length and tau symbols dropped (tau value shown as 1s, units lost); Q2 slope exponents garbled.
- Homework_8.md: epsilon symbols dropped, some hint formulas reflowed; no figure data.
- Homework_9 .md (file name has a space before .md): Q3 final = (probably lambda) value missing; region figure in Q1 is a formula list OCR; several symbols dropped.
- Homework_10.md: Q1 Cox and exponents garbled; Q3 parameter list heavily garbled (units, mj, Cj0, phi values partly run together); Q2 symbols partly lost.
- Homework_11_EE105.md: Q2 circuit is not OCR described and reads from a raw text layout; Q2d k_p units and RS value missing or garbled; Q3 k units, gamma units and body-effect hint formula garbled.
- No file prints a term in plain; all say Spring 2024, so every row uses SP24. Solutions are not included.
