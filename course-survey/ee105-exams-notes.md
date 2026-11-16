## Per exam
- SP05 MT2: Prof. Roger T. Howe; 50 pts; 3 questions; MOS-based (NMOS common-gate, PMOS mirror plus follower); phasor and Bode of an RC input model, common-gate current amp with a photodiode, mirror-biased source follower supply with body effect.
- SP06 MT1: Prof. Ming C. Wu; 100 pts; 5 questions; MOS-based (device physics, no amplifiers); pn diode small-signal and depletion capacitance, MOS capacitor threshold, regions, C-V and charge sketch, metal gate, NMOS turn-on and drain current.
- FA06 MT2: Jan M. Rabaey (called EECS 105); 25 pts; 3 questions; MOS-based; bias and regions in mirror and divider circuits, reading gm/gmb/ro off printed curves, PMOS CS bandwidth and gain design.
- SP07 FINAL: Prof. Ming C. Wu; 100 pts (30+25+15+15+15, summed from parts); 5 questions; both (Q2, Q3 bipolar and mixed, Q4, Q5 MOS); carrier type, flatband, threshold, diode, BJT amp with mirror load, cascoded mirror, CMOS stage poles, two-stage CMOS swing. Open book, 180 min.
- SP08 MT2: instructor not printed; 80 pts; 4 questions; both (Q1, Q3 MOS, Q2 BJT, Q4 mixed cascodes); cascode and degenerated CS, BJT common-base with mirror and Bode, PMOS facts, MOS-versus-BJT cascode comparison.
- FA10 FINAL: instructor not printed; 80 pts; 4 questions; both (Q3 BJT, Q2 and Q4 MOS); pn and slab physics, velocity saturation, MOS charge sketch, gain-boost design, BJT diode-loaded stages, mirrors, diff-pair noise and design.
- SP14 MT1: D. J. Allstot; 100 pts; 3 questions; bipolar-based; ten true/false items, mirror with finite beta, gain-ratio derivation of two BJT stages.
- SP14 MT2: D. J. Allstot; 100 pts (cover table 60+40); 2 questions; MOS-based Q1 (CS frequency response, zero cancellation), bipolar Q2 (mirror sizing, ground resistance, cascode mirror with beta 100).
- SP23 MT: Prof. Jun-Chau Chien; 89 pts summed from parts (no total printed); 8 questions; no transistors; IC R and C, doped Si bar, pn junction, Laplace ODE, delay/LPF system, instrumentation amp, closed-loop op-amp with offset and settling.
- SP24 MT: Prof. Alp Sipahigil; 100 pts (30+29+21+20); 4 questions; no transistors; differentiator op-amp and loop gain Bode, pn junction, compensated GaAs bar, diode small-signal.

## Notation
- Thermal voltage printed as 26 mV (SP05-SP14, SP23), 0.026 V (SP08, FA10), 25.9 mV (SP24). ln(10)*VT = 60 mV is printed on SP08 and FA10.
- ni = 1e10 cm^-3 for Si; GaAs ni = 2e6 cm^-3 (SP24). q = 1.6e-19 C. Si permittivity 11.7 eps0, eps0 = 8.854e-14 F/cm; SiO2 3.9.
- Mobility is read from a printed curve vs total doping (SP06, SP08, FA10); SP23 and SP24 give constants (Si 1000 and 400 cm^2/Vs; GaAs 8000 and 400).
- Mobility, drift and diffusion formulas given as J = sigma E, Jdiff,p = -q Dp dp/dx, D = (kT/q) mu (SP23, SP24 equation sheet).
- MOSFET: k = mu*Cox in uA/V^2, typical NMOS 50, 100 or 200 and PMOS 25 or 50; VTn 0.4 to 0.5 V, VTp -0.5 V; lambda 0.025 to 0.1 V^-1, sometimes 0.1/L with L in um. Saturation current (W/L)(mu Cox/2)(VGS-VTn)^2(1+lambda VDS). gm = mu Cox (W/L)(VGS-VT), ro about 1/(lambda ID), gmb = gamma gm/(2 sqrt(...)), gamma 0.5 V^1/2, -2 phi_p 0.9 V (SP05). Cgs = (2/3)WL Cox + overlap (SP06 sheet).
- MOS caps like CGS 20 fF, CGD 5 fF, CDB and CSB 2.5 fF (SP07). Symbols VTH vs VTn/VTp: SP08 uses VTH for both, others use Tn/Tp.
- Bipolar: Is 1e-15 to 1e-17 A, VA 10 to 50 V, beta 100, emitter areas given (ratios of 10), Cpi 100 fF, Cmu 10 fF, Ccs 20 fF (SP08). Small-signal symbols r_pi, gm, ro (written rp, r0 in OCR). Cmu is Cu.
- Op-amp: A(s) = A0/(1+s tau) with A0 = 1e4, tau 0.1 ms (SP23) or 1 us (SP24); loop gain A*beta; Laplace tables supplied. j or s notation both used; SP05 uses phasors with j.
- Supplies: 3 V or 2 V (SP07, SP08), +/-1.5 V (SP05), 2.5 V; current references 100 uA; 1 mA tail/bias for cascodes.
- Bias-current subscripts: ISUP, IBIAS, IREF, IOUT used for sources and mirror currents. Gain written Av = vo/vi, sometimes sign shown as 180 degrees phase.
- Pn junction exams use Region 1 = p at x<0, Region 2 = n at x>0, depletion edges x = -x1 and x2.

## Recurring question styles
- Compute bias point and region of each MOS or BJT in a mirror or stack, usually ignoring or then adding lambda or finite beta (SP05, FA06, SP07, SP14 MT1, SP14 MT2).
- Small-signal parameters first (gm, ro, r_pi) then gain, Rin and Rout of one named topology (SP05, FA06, SP07, SP08, FA10).
- Single-stage frequency response: build small-signal model with caps, find poles, dominant pole, 3 dB bandwidth, sometimes a Bode sketch (SP05, FA06, SP07, SP08, SP14 MT2, SP23, SP24).
- Compare two circuits that differ by one element (cascode versus not, MOS versus BJT, with and without diode load) and say which wins (SP08, SP14 MT1, FA10).
- pn junction set: built-in voltage, x1 and x2, sketch of rho, E and V, capacitance at two reverse biases, diode current (SP06, SP07, SP23, SP24, FA10).
- Doped-semiconductor numbers: n and p from doping and ni, conductivity, drift or diffusion current (SP06, FA10, SP23, SP24).
- MOS capacitor and MOSFET physics: threshold, flatband, regime, C-V, charge profile, velocity saturation (SP06, SP07, FA10).
- Ideal op-amp with virtual short, then non-ideal loop gain, offset, bandwidth (SP23, SP24).
- True/false and single-choice concept checks (SP07 Q1a-d, SP14 MT1 Q1, SP08 Q3, FA10 Q4b).
- Draw or sketch with quantities marked (charge, field, Bode, I-V, small-signal circuit) (SP05, SP06, SP08, SP23, SP24, FA10).

## Hard spots
- Cascode and degenerated stages: which transistor sets Rout, and why gain is not simply doubled (SP08 Q1, Q4; SP14 MT1).
- Mirror accuracy with finite beta, and effect of parasitic ground resistance (SP07 Q2e, SP14 MT2 Q2).
- Body effect and the follower or source-degenerated output shift (SP05 Q3e, FA06 Q2).
- Picking a bias point from measured curves for swing and gain, and extracting gm, gmb, ro from them (FA06 Q2).
- Zero in a CS transfer function: its phase at high frequency and how to cancel it (SP14 MT2 Q1e-g).
- Sketching rho, E, V at a junction and the MOS charge profile in accumulation and inversion (SP06 Q3, SP23 Q4c, SP24 Q2c, FA10 Q2c).
- Explaining why a depletion layer forms at a doped/undoped boundary, and drift versus diffusion under bias (FA10 Q1).
- Velocity saturation: deriving ID and telling from curves whether it dominates (FA10 Q2a, b).
- Design to a spec: bias current from bandwidth, width from gain, gain -100 when gmRL is only 10 (FA06 Q3, FA10 Q3a).
- Output swing limits that change with load resistance (SP07 Q5c, d; SP14 MT1 Q1f).
- Compensated doping in GaAs and in Si (SP23 Q3e, SP24 Q3).
- Loop gain Bode with op-amp pole plus RC pole, and settling time to 0.1 percent (SP23 Q8, SP24 Q1d, e).

## Old versus recent
2023 and 2024 midterms drop transistor amplifiers entirely and examine doped-semiconductor transport, pn junctions, IC resistors and capacitors, and op-amp feedback with Laplace-transform signals and systems material (ODEs, delays, loop-gain Bode, settling), written for a first-half-of-course midterm. The 2005 to 2014 exams are dominated by MOS and BJT amplifier analysis (bias, small-signal, cascodes, mirrors, frequency response); they have no Laplace ODE, op-amp offset or settling questions, and use no ideal op-amp circuits.

## Problems with the files
- Berkeley ...ee105_sp05_mt2.md: every circuit is cropped or reduced to OCR fragments; question text readable, topology not. I rendered PDF pages 2, 5 and 8 to PNG (swift PDFKit into the scratchpad, since the Read tool's pdftoppm was missing) to identify circuits.
- Berkeley ...ee105_sp07_f.md: Q3, Q4, Q5 circuit labels and values scrambled; I rendered PDF page 3 to read Q3 and Q4. Q5 (page 4) circuit not viewed; its tags rest on the printed parameters and text.
- Berkeley ...ee105_sp08_mt2.md: Q1 and Q2 circuits not in the markdown; opened PDF pages 3 and 5 to identify topologies. Q3 and Q4 text only; Q4 circuit not viewed (gain/Rout questions are clear from text).
- Berkeley ...ee105_fa06_mt2.md: Q1 circuits cropped and parameters partly missing; topologies inferred from the OCR netlists. Q2 curves are described only as text axes. PDF not opened.
- Berkeley ...ee105_fa10_f.md: font-garbled text blocks (cid codes) on page 2-3; questions still readable. Points for Q3b(i)/(ii) not split (10 total).
- Berkeley ...ee105_sp14_mt1.md: figure text partly lost; Q2 and Q3 circuit identities (which devices are cascoded or degenerated) uncertain. Sub-part points of Q2 not printed.
- Berkeley ...ee105_sp14_mt2.md: Q1 equations are OCR fragments; Q2 header says 30 pts but cover table says 40, and sub-part points sum to 30.
- Berkeley ...ee105_sp06_mt1.md: usable; equation sheet is OCR LaTeX.
- ee105_midterm_sp2023.md: handwritten solutions scribbled over pages (garbled CJK-like OCR); pages 5, 6, 8, 9, 11, 12, 15, 16, 18, 19 are blank worksheets. No total printed; parts sum to 89.
- Midterm_Sp2024_EE105.md: handwritten solutions garble the text of Q1 and Q4; question statements recovered. Q1e plot area blank in OCR.
- PDFs opened (as rendered PNG): sp05_mt2 (pp 2, 5, 8), sp08_mt2 (pp 3, 5), sp07_f (p 3).
