## Week by week

Item ids: HW rows use the printed id (HW5.1c); discussion rows use P<problem><part>. No points are printed anywhere, so the points column is empty. Sub-part ids such as 4.4b-c are my groupings. HW due dates are Fridays 23:59 (accepted 2 days late) unless noted.

Homework:
- HW1, due Fri 28 Aug 2026: complex numbers, roots of unity, Euler, geometric sum of e^{i n theta}.
- HW2, due 4 Sep: Euler phasor sum, linearity and time-invariance (DT), DT convolution, doublet edge detector, FIR as polynomial.
- HW3, due 11 Sep: periodicity (CT and DT), recursive IIR frequency response, LCCDE to H(w) and back.
- HW4, due 18 Sep: periodicity under up/downsampling, causality and BIBO, DAG diagrams, notch filter.
- HW5, due 25 Sep: Fibonacci system, DT state space, Dirac delta sampling, sifting, scaling.
- HW6, due Mon 5 Oct: CT convolution, RC circuit (LCCDE, H, IAG), RLC state space and damping.
- HW7, due 16 Oct: HW5.1 repeat, feedback and BIBO stability, complex inner product, DTFS expansions.
- HW8, due 23 Oct: DTFS, LTI on periodic input, DTFS as change of basis, Parseval, DFT.
- HW9, due 6 Nov: CTFS puzzle, trig Fourier series, DTFT warm-up and properties, reversing DTFT.
- HW10, due 13 Nov: CTFT of signum, step, impulse train, rect, Gaussian; heat equation; AM mismatch; QAM.

Discussions (the printed date on DIS1 is 23 Jan 2026, which looks left over from an earlier term; the rest follow Fridays):
- DIS1: moving-average filter, Euler, DT convolution, LTI test.
- DIS2 (11 Sep): DAG to LCCDE to H(w) to h[n]; magnitude response matching; one-delay implementation.
- DIS3 (18 Sep): causal/stable impulse responses, causality of non-LTI systems, thermostat state space.
- DIS4 (25 Sep): memory, causality, BIBO; Dirac delta and CT convolution.
- DIS5 (2 Oct): parallel RC (h, H two ways), CT causality and stability, series RLC.
- DIS6 (9 Oct): parallel RLC state space, damping, H(w), IAG.
- DIS7 (16 Oct): feedback stabilization with Black's formula; DTFS as change of basis.
- DIS8 (23 Oct): mystery DTFS signal, DTFS properties proof, periodic replication of h; includes a DTFS properties sheet.
- DIS9 (30 Oct): CTFS practice, DTFT multiplication property, area of a signal.
- DIS10 (6 Nov): DTFT with partial fractions, mechanical CTFT pairs, derivative-like system.
- DIS11 (13 Nov): sinc squared, CLT via convolution of transforms, modulation-filter-modulation.

Pace: Fourier series in DT (weeks 7-8) and DTFT (week 9) come before CTFT (week 10-11). CT convolution and Dirac delta come late (weeks 4-6), after DT systems and state space. Laplace, z, sampling, Bode are not yet seen.

## Notation

- Signals: CT is x(t), t in R; DT is x[n], n in Z, but some items (HW7, parts of DIS2, DIS9, DIS10) print x(n) or y(n) for DT. Types are written as maps, for example F: [Z -> R] -> [Z -> R].
- Frequency: both CT and DT use the same letter w (omega), in rad/s and rad/sample. DT spectra are 2pi-periodic. Fundamental frequency is w0 = 2pi/p (DT, period p, also called N) or 2pi/T or 2pi/p (CT). Harmonic index is k. The notation <p> means any run of p consecutive integers.
- Imaginary unit: i throughout (e^{i w t}, 1/(1+RC i w)). j appears only by slip: DIS5 P1(c) writes e^{-jwt}; the HW10.4/10.5 figure OCR shows H(j w), probably OCR. Use i.
- Impulse and step: delta[n] is the Kronecker delta, delta(t) the Dirac delta, both used with the sampling property x(t)delta(t-t0)=x(t0)delta(t-t0) and the sifting integral. u[n]=1 for n>=0; u(t)=1 for t>=0 (value 1 at 0). sgn(t)=+1 for t>=0 in HW10.
- Convolution: (x*h)[n] = sum_m x[m]h[n-m]; (x*y)(t)=integral x(tau)y(t-tau)dtau. The frequency-domain convolution is written with a circled star (X (*) Y)(w) = (1/2pi) integral_<2pi> X(lambda)Y(w-lambda)dlambda for DTFT.
- Inner product: HW7.3 and HW8.4/8.5 use <x,y> = x^T y* (conjugate on the SECOND argument); DIS7 P2 writes a*b = sum a[n]-bar... b[n] with conjugate on the FIRST. Projection: proj_psi x = <x,psi>/||psi||^2 psi.
- DTFS: x[n] = sum_{k in <p>} X_k e^{i k w0 n} (no factor); X_k = (1/p) sum_{n in <p>} x[n]e^{-i k w0 n}; coefficients X_k are p-periodic. Parseval: (1/p) sum |x|^2 = sum |X_k|^2. Impulse train has X_k = 1/p. Same pattern for CTFS: x(t)=sum_k X_k e^{i k w0 t}, with the 1/p on the analysis integral; trig form uses A0=X0, A_k=2Re X_k, B_k=-2Im X_k, with (2/p) integrals.
- DFT: built from basis phi_k = psi_k scaled (the scale factor in the file is garbled, most likely 1/sqrt(p), which makes the DFT unitary); X[k] relates to X_k by that factor. Matrices are named F_DFT and F_iDFT. Check the exact factor against the lecture notes before building a tool.
- DTFT: X(w)=sum_n x[n]e^{-i w n}; x[n] = (1/2pi) integral_<2pi> X(w)e^{i w n}dw (inferred from the multiplication property and HW9.4). Pair given: alpha^n u[n] <-> 1/(1-alpha e^{-i w}), |alpha|<1; sin(wc n)/(pi n) <-> rect on [-wc, wc].
- CTFT: X(w)=integral x(t)e^{-i w t}dt; x(t)=(1/2pi) integral X(w)e^{i w t}dw (from HW10.3 with x as the variable). Pairs given: Gaussian 1/sqrt(2 pi) e^{-t^2/2} <-> e^{-w^2/2}; sinc(t)=sin(pi t)/(pi t) (normalised) <-> rect on |w|<=pi (DIS11); but DIS10 uses sin(Tt)/(pi t), unnormalised. Fourier pairs are written with a script F over a double arrow.
- Frequency response: H(w) is the eigenvalue for e^{i w n} or e^{i w t}: DT H(w)=sum h[n]e^{-i w n}; CT H(w)=integral h(t)e^{-i w t}dt. Written H(w) not H(e^{iw}) or H(jw). Black's formula for feedback.
- Block diagrams: DAG (delay-adder-gain) in DT with box D; IAG (integrator-adder-gain) in CT. State space: q[n+1]=Aq[n]+Bx[n], y=Cq+Dx, and CT q'(t)=Aq+Bx. States are q1, q2.
- Mod: n mod N in {0..N-1}, so -4 mod 3 = 2.

## Recurring question styles

- Classify a system (linear, time-invariant, causal, memoryless, BIBO) with a "twist" such as an additive constant, time reversal or decimation.
- Read an LCCDE, a block diagram (DAG or IAG), a frequency response and an impulse response from each other, in any direction.
- Sketch a magnitude (and phase) response from vector lengths in the complex plane, then name the filter type.
- Circuit problems recast as LCCDE, state space and frequency response (RC, RLC), used as examples rather than circuit analysis.
- Convolution by sketching: boxes, deltas, impulse trains, steps; also undoing a convolution to find h.
- Prove a Fourier or inner-product property from the analysis and synthesis equations.
- "Puzzle" problems: several clues (period, mean, energy, symmetry) pin down one signal.
- Change-of-basis view: DTFS and DFT as orthogonal projections and matrices, with Parseval from norms.
- Compute a transform using properties (differentiation, shift, duality, multiplication) instead of the defining integral.
- Repeated problems: HW5.1 returns as HW7.1; HW7.4 returns as HW8.1; HW8.4 returns as DIS7 P2; HW1.6 as DIS1 P2; HW2.2 as DIS1 P4 and DIS4 P1.

## Hard spots

- Periodicity in DT: when a signal is not periodic (cos(n)), when frequencies are not rational multiples of pi, and what up/downsampling does to period.
- Eigenfunction view of LCCDEs, including building an LCCDE from a given H(w) and a one-delay implementation.
- Pole and zero geometry for notch and band-pass shapes, with the limit a close to 1; approximating output phase.
- BIBO versus internal stability and observability; why state-space eigenvalues decide stability only when modes are observable.
- Feedback: loop gain, forward gain, Black's formula, and finding the gain range that keeps the closed loop BIBO stable.
- Dirac delta as an operational definition: scaling, evenness, sifting over a narrow window, deltas in the frequency domain.
- Existence conditions in DTFS and DTFT: no expansion for non-periodic signals; signals like (1/2)^{-n} u(-n-1) that converge only on one side.
- Causal real signals determined by real or imaginary part alone; spectral factorization with non-unique answers (HW9.4, HW9.5).
- Orthogonal versus orthonormal bases, conjugation conventions in inner products, and how normalization moves between DTFS and DFT.
- Modulation with mismatched or phase-offset carriers (HW10.4, 10.5): why information is lost, and the size of crosstalk.
- Gaussian transform by ODE trick and CLT via transform of repeated convolution.

## Not yet covered by HW10 and DIS11

invertibility, group-delay, linear-phase, all-pass, gibbs-phenomenon, sampling-theorem, aliasing, reconstruction-interpolation, zero-order-hold, dt-processing-of-ct, envelope-detection, single-sideband, frequency-division-multiplexing, hilbert-transform, laplace-transform, laplace-roc, laplace-inverse, laplace-properties, unilateral-laplace, poles-zeros, stability-from-poles, initial-final-value, z-transform, z-roc, z-inverse, z-properties, unilateral-z, root-locus, bode-plot, nyquist-criterion, gain-phase-margin, correlation, matched-filter, windowing, spectral-leakage. (linear-phase is only touched by HW4.4d's "phase near zero" remark and was not tagged.)

## Problems with the files

- fa26-hw1.md: HW1.7 figure lost (rotation of x-hat and y-hat); matrices partly garbled. Spaces dropped everywhere.
- fa26-hw2.md: HW2.3 and HW2.4 are badly scrambled (text out of order, figures replaced by OCR junk). HW2.4's input-output plot, which defines the problem, is unreadable.
- fa26-hw3.md: HW3.2 diagram lost and text scrambled.
- EE120-FA26-HW04.md: HW4.2 answer pages (a),(b) are blank; DAG diagrams in HW4.3 are only partly captured. Overview says "Casality". Prose labels y1 as upsampled and y2 as downsampled, opposite to their definitions.
- EE120-FA26-HW05.md: HW5.2(a)(iv) figure of X(w) is lost, with text interleaved and OCR failure messages.
- EE120-FA26-HW06-v1.md: HW6.2 and 6.3 text out of order; circuit diagrams only as OCR; the RLC circuit in HW6.3 is unclear, and the printed LCCDE has x absent. Version "v1" may be superseded.
- EE120-FA26-HW7.md: HW7.2 diagram OCR only; the impulse response and G(w) text is scrambled; HW7.4(c) frequency is ambiguous (likely sqrt(2) pi n / 5).
- EE120-FA26-HW08.md: HW8.5 normalization of phi_k is garbled.
- HW9.md: HW9.5(a) shows "5/4 - cos w" after OCR; check against the original.
- EE120-FA26-HW10.md: page 13-15 text is mixed with OCR transcriptions, including "H(j w)" and spice netlists; plots of LPF unreadable; HW10.5 first text scrambled.
- ee120-fa26-disc1.md: dated 23 Jan 2026; signal figures for P3 lost.
- ee120-fa26-disc2-final.md: plot labels reversed (|H|(w) printed as "|)ω(H|"); the four candidate plots are not readable.
- disc3.md, disc4.md: DIS4 P1 contains typos x(-n) for x[-n]. Fine otherwise.
- Discussion5.md: uses j in one place. The circuit figures lost.
- disc7.md: P2(a) x[n] likely cos(pi n)+sin(pi n/2); the "/2" is displaced to a stray "2". Figure 1 loop structure is not readable.
- disc8_v1.md: version v1 may be superseded; DTFS reference sheet at end is not a problem.
- disc10_v1.md: P1(b) question text is missing (only the spectrum and a hint remain, tick labels garbled); P3 plot of H(w) is lost. Version v1 may be superseded.
- disc11.md: X(w) and H(w) plots in P3 are unreadable; tick labels only.
- Discussion files carry no point values; homework files carry none either.
