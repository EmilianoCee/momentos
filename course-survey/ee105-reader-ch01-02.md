# EE 105 reader, chapters 1-2: concept notes

Source: reader lines 660-2295. Most display equations were lost in the conversion (blank lines). Where a formula below is marked "(reconstructed)", the reader's text names or implies it but the equation itself is missing, and it is written in the reader's notation from the surrounding text. Everything else is stated in the text or in a surviving table row.

## Chapter 1. Linear Time-Invariant Systems

### 1.2 Example: Analyzing an RLC Circuit (RC low-pass, the "hard way")
- **rc-lowpass**: A series R feeding a shunt C, with output vo across C, is the running example; it passes slow signals and attenuates fast ones.
  - notation: vs input, vo output (V); R (ohm), C (F); time constant tau = RC (s); omega (rad/s); Vs, Vo amplitudes; phi output phase (rad or deg)
  - formulas: KVL loop with i = C dvo/dt gives vs = vo + tau dvo/dt (reconstructed). Input vs(t) = Vs cos(wt); output vo(t) = Vo cos(wt + phi). Phase: tan(phi) = -tau*w, so phi = -arctan(tau*w) (Eq. 1.8-1.9). Magnitude: Vo/Vs = 1/sqrt(1 + (tau*w)^2) (Eq. 1.15)
  - typical values: cutoff w = 1/tau; magnitude 0.707 (= 1/sqrt 2, half power) and phase -45 deg at w = 1/tau; magnitude about 0.1 at w = 10/tau; phase tends to -90 deg; plot axes in the figure run to w = 10/tau
  - approximations: w near 0 passes the signal unchanged; w to infinity is "shorted out by the capacitor"
  - picture: Plots of magnitude (linear, 1 down to 0) and phase (0 to -90 deg) against omega, with the passband edge marked at 1/tau.
  - pitfalls: The reader calls the direct-sinusoid method "the wrong way": substitute the guessed form, expand with angle-sum identities, and use linear independence of sin and cos to split into two equations. It works but is painful.
- **frequency-response**: The magnitude and phase of the output relative to the input, as functions of the input frequency, are what characterise the circuit in steady state.
  - notation: Vo/Vs (unitless), phi (deg), dB
  - formulas: dB = 20 log10(Vo/Vs) (10 log10 for power; 20 for voltage because power goes as voltage squared)
  - typical values: at the cutoff the magnitude is -3 dB (half power); beyond the cutoff the roll-off is 20 dB/decade; "double the frequency, 6 dB" (the reader's text writes "6 dB/decade" in the same sentence, which is an error: it is 6 dB per octave)
  - picture: Log-log magnitude plot in dB (0 to -40 dB over 0.1 to 100 in normalised frequency) that bends at the cutoff and then falls as a straight line.
  - pitfalls: Slope is 20 dB per decade of frequency, equivalently about 6 dB per doubling; the "20 versus 10" in the dB definition comes from power being voltage squared.

### 1.3 Linear Time-Invariant Systems
- **lti-system**: A system L is linear if scaling and summing inputs scales and sums the outputs, and time-invariant if delaying the input only delays the output.
  - notation: L operator; x(t) input, y(t) output
  - formulas: linearity: L{a x1 + b x2} = a L{x1} + b L{x2} (reconstructed). Time invariance: y(t) = L{x(t)} implies L{x(t - T)} = y(t - T) (reconstructed)
  - picture: The system "has no clock": the same input today or tomorrow gives the same output, only shifted.
  - pitfalls: none stated
- **eigenfunction-property**: Finite-dimensional linear algebra carries over: vectors become functions of time, matrices become integrals, eigenvectors become eigenfunctions, an orthonormal basis becomes a function expansion x(t) = sum phi_n(t) x_n (Eq. 1.25).
  - notation: phi_n(t) basis functions; x_n coefficients
  - picture: Input and output are "infinite-dimensional vectors" with one entry per instant; the system's eigenvalues (the spectrum) are what matter.
  - pitfalls: The reader says this is only a teaser and can be skipped.

### 1.4 The Complex Exponential Technique
- **complex-exponential-technique**: Driving a linear circuit with e^{jwt} turns differentiation and integration into multiplication by jw and division by jw, so differential equations become algebra.
  - notation: j imaginary unit; omega (rad/s); z = x + jy = |z| e^{j phi}; phi = angle(z) = arctan(y/x)
  - formulas: d/dt e^{jwt} = jw e^{jwt}; integral of e^{jwt} = e^{jwt}/(jw) (reconstructed). Euler: e^{j phi} = cos(phi) + j sin(phi); |e^{j phi}| = 1; cos(x) = (e^{jx} + e^{-jx})/2, sin(x) = (e^{jx} - e^{-jx})/(2j) (reconstructed)
  - picture: e^{jwt} is a point on the unit circle turning counter-clockwise at w rad/s, once per 2 pi/w seconds; real and imaginary parts are its projections. e^{-jwt} turns clockwise. Two counter-rotating arrows add to a cosine.
- **eigenfunction-property**: A sinusoid (or complex exponential) into any LTI circuit comes out as the same frequency with a new amplitude and phase; the complex multiplier is the eigenvalue H.
  - notation: H(w) complex (unitless for a voltage ratio); |H(w)| magnitude response; angle H(w) phase response
  - formulas: input e^{jwt} gives output H(w) e^{jwt} = |H(w)| e^{j(wt + angle H)}. "Any linear circuit" means R, C, L, mutual inductors, transformers and linear dependent sources
  - picture: A black box of any linear circuit; a sinusoid in, the same sinusoid out, scaled in amplitude and shifted in phase.
- **transfer-function**: The spectrum of eigenvalues H(w) over all frequencies characterises the system completely; probing with real sinusoids in the lab is equivalent.

### 1.5 The Low Pass Filter Again
- **complex-exponential-technique** (soft way): Put vs = Vs e^{jwt} and vo = Vo e^{jwt} into the RC equation, cancel e^{jwt}, and solve in one line.
  - formulas: Vs = Vo (1 + jw tau) (Eq. 1.39), so H(jw) = Vo/Vs = 1/(1 + jw tau). Magnitude and phase match the hard way. The complex Vo includes the phase: |Vo| e^{j(wt + phi)}
  - picture: Same answer as Section 1.2, in a few lines instead of a page.
- **superposition**: Real sinusoid response equals the real part of the complex exponential response, and equivalently the sum of the responses to e^{jwt} and e^{-jwt}.
  - formulas: for real circuits and real input the two terms must be complex conjugates, so |H(-w)| = |H(w)| (magnitude even in frequency) and angle H(-w) = -angle H(w) (phase odd). Output: Re{H(w) e^{jwt}} = |H| cos(wt + angle H)
  - picture: Two counter-rotating phasors, each scaled by H and its conjugate, whose sum stays on the real axis.
  - pitfalls: The shortcut works only because Re and L commute for a linear real system.

### 1.6 Generalization to any Linear Circuit
- **transfer-function**: Any linear circuit is built from constant multipliers, time derivatives and integrals, so each term for e^{jwt} input is a constant times e^{jwt}; these sum to H.
  - formulas: H(jw) = H(s) at s = jw. General input e^{st}: output H(s) e^{st}
  - approximations: H(jw) is the steady-state sinusoidal response; H(s) also gives the transient response.
- **poles-zeros** (s-plane picture): The complex number s in e^{st} chooses the waveform: real part sigma sets growth or decay, imaginary part w sets oscillation rate.
  - notation: s = sigma + jw (1/s); sigma = Re[s]; w = Im[s]
  - picture: s-plane with example marks: on the real axis pure exponentials, on the imaginary axis steady sinusoids, off-axis damped or growing sinusoids. Sample values include (-0.2, 1), (-2, 0), (-0.2, 0).

### 1.7 Time Domain Characterization of Linear Systems
- **impulse-response**: Any input can be built from narrow rectangles of unit area; as the width Delta goes to 0 they become the Dirac delta, which "sifts" out function values.
  - notation: r(t) unit-area rectangle of width Delta and height 1/Delta; delta(t); u(t) unit step
  - formulas: integral of delta = 1; integral x(t) delta(t - tau) dt = x(tau) (sifting); x(t) = integral x(tau) delta(t - tau) dtau (reconstructed)
  - picture: Rectangles get taller and thinner as Delta shrinks; delta is like the unit vector e_n with a 1 in the n-th slot.
  - pitfalls: delta is not an ordinary function (a distribution); define it by sifting. The reader notes Heaviside introduced it about 1900, Dirac gets the name.

### 1.8 Back to Time Domain: Impulse Response
- **convolution**: The output is the input weighted by the impulse response: y(t) = integral x(tau) h(t - tau) dtau = (x * h)(t).
  - notation: h(t) impulse response (response to delta at t = 0); * convolution operator; tau dummy variable
  - formulas: y(t) = integral over all tau of x(tau) h(t - tau) dtau; equivalent form with swapped roles (substitute x = t - tau). Causal: h(t) = u(t) h_bar(t), so y(t) = integral from -inf to t of x(tau) h(t - tau) dtau
  - picture: Reflect h, slide it along the tau axis, and at each t take the overlap-weighted sum with x.
  - pitfalls: tau here is a dummy variable, not the RC time constant. Why flip h: output at t weights past inputs by how long ago they were applied.
- **impulse-response** (causality and memory): h(t) = 0 for t < 0 because the output cannot precede the input; the duration of h(t) is the system's memory.
  - picture: Two example h(t): long and oscillating (long memory, resonance-like) versus short and exponentially decaying. A hammer strike excites natural modes that die out through loss.
  - pitfalls: A memoryless system has h(t) proportional to delta(t). Capacitors and inductors provide memory (stored energy); L plus C allows exchange between the two stores, giving resonance.

### 1.9 Step and Pulse Response
- **impulse-response** (RC example): h(t) = (1/tau) e^{-t/tau} u(t) for the RC low-pass (reconstructed from "tau = 1/3" with peak about 3 in the figure).
  - typical values: tau = RC = 1/3 s in the figure; peak h about 3
  - picture: The impulse instantly charges the capacitor, then it decays through R; only inputs from about the last tau matter.
- **step-response**: Convolving u(t) with h(t) gives the output "smoothed" because each point averages current and past input.
  - formulas: y(t) = (1 - e^{-t/tau}) u(t) (reconstructed; "familiar result"); the integral lower limit changes because u(t - x) = 0 for x > t
  - typical values: figure runs from 0 to 1 over 10 time units
  - picture: A sharp input step comes out as a smooth rise toward 1; output cannot track instantly because all past inputs were zero.
- **time-constant**: tau = RC is how long the system remembers; it separates "slow" inputs (passed) from "fast" inputs (averaged away).
  - formulas: slow means input frequency below about 1/tau; fast means above
  - approximations: for very slow input, h looks like a delta (no memory) and the output follows the input
  - pitfalls: Fig. 1.20 caption says "slow means period smaller than tau", which looks backwards (a slow input has period much longer than tau); treat it as a typo.
- **step-response** (pulse): A pulse is two unit steps (one delayed, one negated) by superposition.
  - approximations: wide pulse (width >> tau) settles and is reproduced faithfully; narrow pulse (width < tau) is distorted and reduced
  - picture: Output pulse for a wide input rises to full height; for a narrow input it peaks low and tails off.
  - pitfalls: Bandwidth must be enough for the shortest pulses in high-speed communication.

### 1.10 Frequency Domain Characterization of Linear Systems
- **transfer-function** (H and h related): H(s) is the Laplace transform of h(t); H(jw) is H(s) on the imaginary axis (the Fourier transform of h).
  - formulas: H(s) = integral from 0 (or -inf) to inf of h(t) e^{-st} dt (reconstructed); derived by equating the convolution of h with e^{st} to H(s) e^{st}. Convolution in time becomes product in frequency: Y(s) = H(s) X(s)
  - picture: Two probes of the same system: e^{st} gives H(s); delta(t) gives h(t).
  - pitfalls: The reader will mostly use H(jw), not Laplace, and says Laplace tables and partial fractions are used rather than the integral. Only the transform property and pairs tables (Figs. 1.22-1.23) are included; they are Wikipedia images, partly garbled.
- **convolution** (frequency view): Multiplying spectra is easier than convolving in time; a filter is picture-able as a curve multiplying a spectrum.
  - notation: X(jw), N(jw) input and noise spectra; |H(jw)| filter; |Y(jw)| output
  - picture: Tones as spikes plus a flat noise floor; a low-pass curve multiplied in; noise above the corner drops and a third tone is attenuated.
- **fourier-series**: A periodic signal is a sum of complex exponentials at multiples of f0 = 1/T with coefficients c_n; the Fourier transform extends this to non-periodic signals.
  - notation: f0 = 1/T (Hz); c_n coefficients
  - formulas: f(t) = sum c_n e^{j 2 pi n f0 t} (reconstructed)
- **frequency-response** (audio demo): Low-pass filtering reduces noise without hurting a low-frequency signal; band-pass filtering around the tone removes more noise; a wider passband lets in more noise.
  - typical values: tone 261.626 Hz plus third harmonic; noise power 10x lower gives SNR = 10 dB
  - approximations: white noise is flat in frequency (stated, not proved)
- **small-signal-linearisation**: Nonlinear parts (diodes, transistors) are linearised about an operating point, giving small-signal models that are valid as long as signals deviate little.
  - pitfalls: Outside small signals, nonlinear techniques are needed.

## Chapter 2. AC Circuits and AC Analysis

### 2.2 Transfer Functions
- **transfer-function**: Between two ports of an LTI circuit the ratio of output to input phasor, at a given frequency, is one complex number; four kinds exist.
  - notation: G_v = V2/V1 (voltage gain, unitless); G_i = I2/I1 (current gain); Z = V2/I1 (trans-impedance, ohm); G = I2/V1 (trans-admittance, S). Port 1 and 2 voltages V1(f), V2(f), currents I1(f), I2(f)
  - formulas: as above; Z = V/I and Y = I/V for one-port self transfer functions (Fig. 2.6)
  - pitfalls: Gain is not limited to active circuits: RLC and transformers give voltage or current gain, and even RC can, though less easily. Gain above 1 is gain, below 1 is loss or attenuation.
- **two-port-models**: Source and load impedances change the transfer function; check which quantity is the true input.
  - notation: mic/speaker inverting amplifier with R2 and C; source resistance Rs; transimpedance amplifier with feedback R_F and photodiode capacitance C_D
  - approximations: for omega*C >> R2 (reconstructed: "wC >> R2" is as written in the reader, probably meant 1/(wC) << R2) the capacitor dominates and gain is small
  - picture: Virtual ground makes a naive voltage-to-voltage view look shorted; with the source resistance the circuit is really a current-to-voltage transfer.
  - pitfalls: With an ideal op-amp the voltage-to-voltage function is undefined because the input node is a virtual ground; the photodiode is a current source, not a shorted diode; ECG amplifier is a differential-to-single-ended transfer with 50/60 Hz common-mode noise.

### 2.3 Transfer Function Poles/Zeros
- **poles-zeros**: A rational transfer function is fixed by the roots of numerator (zeros) and denominator (poles); the number is set by the energy-storage elements.
  - notation: H(s) = N(s)/D(s); zeros z_i, poles p_i; G0 DC gain; K (count of poles or zeros at DC)
  - formulas: standard form H = G0 (s/z1 - 1...)/(...) (not recoverable); "DC gain explicit" form uses a power s^K times G0. Substitute s = jw for AC
  - picture: Tent: zeros are stakes at ground, poles are the peaks pushing the surface up; a finite set describes the whole frequency response.
  - pitfalls: Number of poles/zeros relates to memory elements (L, C, M, dependent sources).

### 2.4 AC Circuits Review
- **phasors-impedance**: Drop the e^{jwt} factor and keep only amplitude and phase as a complex number (a phasor); R, L, C become complex resistances.
  - notation: tilde V1 = V1 e^{j phi1}; Ic, Vc phasors; Z (ohm), Y (S)
  - formulas: capacitor: I_c = jwC V_c (Eq. 2.26), so Z_C = 1/(jwC); inductor: V = jwL I, Z_L = jwL (reconstructed from the method); resistor Z_R = R
  - picture: Impedance behaves like resistance with a phase, so KVL, KCL, nodal and mesh analysis all carry over without writing a differential equation.

### 2.5 Example AC Circuit Problems
- **rc-lowpass** (voltage divider): H = Z_C/(Z_R + Z_C) = 1/(1 + jwRC), the same as Chapter 1, in one line.
  - notation: Z_R = R, Z_C = 1/(jwC)
- **phasors-impedance** (two-stage RC): R1, C1, R2, C2 ladder via Thevenin equivalent seen from C2.
  - formulas: open-circuit voltage is the first divider; the Thevenin impedance combines R1 || C1 with R2; final answer is another divider (equations missing).
- **rlc-resonance**: A series R, L, C with output across R is a resonant band-pass.
  - notation: Z input impedance (ohm); omega0 (rad/s); Z0 characteristic impedance (ohm); vR, vL, vC component voltages
  - formulas: Z = R + jwL + 1/(jwC); resonance when Im(Z) = 0, i.e. wL = 1/(wC); omega0 = 1/sqrt(LC); Z0 = sqrt(L/C); at resonance Z is minimal and equal to R
  - typical values: transfer-function plot shows Q = 1, 10, 100 curves, H(j w0) = 1, axis from 0.5 to 4 times w0
  - picture: Phasor diagrams: below w0 capacitor voltage dominates; at w0 vL and vC cancel and vR = vs; above w0 vL dominates. vL and vC are 180 degrees apart.
  - pitfalls: The reader's text says the resonance is at w = +/- 1/sqrt(LC), a signed frequency; physically only positive w matters.
- **quality-factor**: Q measures how large the reactive voltage is relative to the source at resonance, and sets selectivity.
  - notation: Q (unitless)
  - formulas: Q = w0 L / R = 1/(w0 R C) = Z0 / R (reconstructed from "equivalent forms" and "Z0 = sqrt(L/C)"); at resonance |vL| = |vC| = Q |vs|, vL = jQ vs
  - approximations: ideal L and C assumed; this circuit Q differs from the intrinsic Q of the inductor and capacitor (footnote)
  - picture: Phasor vectors for L and C are much longer than the vector for R: voltage gain without power gain (passive circuit); this is the impedance-transformer idea.
  - pitfalls: Voltage gain at resonance is not power gain.
- **transfer-function** (RLC): H = R / (R + jwL + 1/(jwC)); a zero at DC (cannot pass DC current); denominator is quadratic in jw; standard form uses w0 and Q: H = (jw/(Q w0)) / (1 + jw/(Q w0) + (jw/w0)^2) (reconstructed).
  - formulas: poles have constant magnitude |p| = w0 (stated); complex poles require Q > 1/2 (text says "assumption Q > w", garbled)
- **quality-factor** (bandwidth): The -3 dB band around w0 narrows as Q rises.
  - formulas: half-power points where |H|^2 = 1/2; bandwidth Delta w = w0/Q, normalised bandwidth Delta w / w0 = 1/Q; w0 = sqrt(w1 w2), the geometric mean of the -3 dB frequencies; peak gain is 1 for any Q
  - picture: Three curves peak at 1 and narrow as Q goes 1, 10, 100.
  - pitfalls: As Q goes to infinity the circuit passes only w0. The reader says "four solutions" (two positive, two negative frequencies) from the squared magnitude.

### 2.6 Bode Plots
- **bode-plot**: A Bode plot is a sketch on a log frequency axis of magnitude in dB and phase, built by adding the dB and phase contributions of each pole and zero.
  - notation: breakpoint w = 1/tau (rad/s); dB = 20 log10 |H|
  - formulas: |H| = G0 times product of |zero terms| over product of |pole terms|; dB values add. Phase: sum of zero phases minus pole phases; multiplication by j adds +90 degrees. At DC, K > 0 gives zero DC gain, K < 0 infinite, K = 0 gives G0
  - approximations: asymptotic straight-line sketch accurate away from the breakpoint, with 3 dB error at the breakpoint
  - pitfalls: The reader's sentence about K sign is as written; for K zeros at DC the gain at w = 0 is zero.
- **bode-plot** (RL high-pass example): H = R-L divider; output across L: H = jw tau / (1 + jw tau), tau = L/R (reconstructed: "normalised time constants", "inductor open at high freq, short at DC").
  - typical values: at w = 1/tau, |H| = 1/sqrt 2 (not 1/2: the L and R voltages are 90 degrees apart); high frequency |H| goes to 1; DC |H| = 0
  - picture: Numerator |jw tau| is a straight line rising 20 dB/decade through 0 dB at w = 1/tau; denominator flat then falling 20 dB/decade; composite flat above the breakpoint. Phase: +90 degrees minus arctan(w tau); straight-line estimate starts at 0.1/tau and ends at 10/tau (45 degrees at 1/tau).
  - pitfalls: Check the equations against limiting behaviours (high frequency, DC, breakpoint).

### 2.7 Power Flow in AC Circuits
- **ac-power**: Instantaneous power is p = v i; the average over a period depends on the phase between voltage and current.
  - notation: P_av (W), |V|, |I| amplitudes, phi_v, phi_i, PF power factor
  - formulas: P_av = (|V| |I| / 2) cos(phi_i - phi_v); PF = cos(phi_i - phi_v); for 90 degrees apart P_av = 0 (inductors and capacitors dissipate nothing)
  - picture: Reactive element: power flows in for half a cycle and back out the other half; resistor: v and i in phase, power is always positive, twice per cycle.
  - pitfalls: Power is nonlinear, so P_av is not Re of the phasor product V I (the 1/2 and the conjugate matter). Corrected form: P_av = (1/2) Re{V I*} (reconstructed).
- **rms**: V_rms = V / sqrt 2 and I_rms = I / sqrt 2, so P_av = V_rms I_rms cos(phi).
  - typical values: mains 120 V_rms (not 120 V peak); RMS derived with R = 1 ohm and 2 sin^2 x = 1 + cos 2x, integrating over whole cycles
  - approximations: factor sqrt 2 is for sinusoids; other waveforms (square wave) differ.
- **ac-power** (impedance form): in terms of Z the average power is (1/2)|I|^2 Re(Z) = (1/2)|V|^2 Re(1/Z*)  (reconstructed; text says check with a resistor).

## Notation and conventions for these chapters

| symbol | meaning | unit | sign convention |
|---|---|---|---|
| j | imaginary unit (not i) | none | j^2 = -1; multiplication by j is +90 degrees |
| e^{jwt} | time convention; ccw rotation | none | positive w turns counter-clockwise |
| omega (w) | angular frequency | rad/s | f = w/2pi |
| tau | RC time constant (also dummy integration variable in convolution) | s | tau = RC (RC), L/R (RL) |
| phi | phase of output or of a complex number | rad or deg | phi = -arctan(w tau) for RC low-pass (output lags) |
| H(jw), H(s) | transfer function, s = sigma + jw | depends | H(jw) = H(s) at s = jw |
| h(t) | impulse response | 1/s for voltage ratio | zero for t < 0 (causal) |
| u(t) | unit step | none | 0 before t = 0, 1 after |
| delta(t) | Dirac delta | 1/s | unit area, sifting property |
| dB | 20 log10 of voltage or current ratio | dB | 10 log10 for power |
| Vo/Vs, G_v, G_i | voltage and current gain | none | G > 1 gain, G < 1 loss |
| Z, Y | impedance, admittance | ohm, S | Z = V/I, Y = I/V; Z_R = R, Z_C = 1/(jwC), Z_L = jwL |
| tilde V = V e^{j phi} | phasor, e^{jwt} dropped | V | amplitude is the peak value, not RMS |
| omega0, Q, Z0 | resonant frequency, quality factor, characteristic impedance | rad/s, none, ohm | w0 = 1/sqrt(LC), Q = w0 L/R = Z0/R, Z0 = sqrt(L/C) |
| Delta w | -3 dB bandwidth | rad/s | Delta w = w0/Q |
| P_av, PF | average power, power factor | W, none | PF = cos(phi_i - phi_v); P_av = (|V||I|/2) PF |
| V_rms | RMS voltage | V | V/sqrt 2 for sinusoids; mains 120 V_rms |
| f0 | Fourier fundamental | Hz | 1/T |

## Where a visual would help most

1. **RC low-pass, time and frequency together.** Drag the input frequency w*tau (and tau) on a sinusoid driving the RC. The output sinusoid shrinks and slides in phase while a dot moves on the magnitude and phase plots. Click: at w = 1/tau amplitude is 0.707 and lag is 45 degrees, and far above it each decade costs 20 dB.
2. **Rotating complex exponential and phasors.** Drag w and the phasor H(jw) and see e^{jwt} and the H e^{jwt} arrows rotate at the same rate, with a cosine as the sum of two counter-rotating arrows. Click: the output is the input scaled and rotated, same frequency.
3. **s-plane to waveform.** Drag a point s = sigma + jw in the plane; the waveform e^{st} (real part) shown beside it grows, decays or oscillates. Click: sigma sets the envelope, w sets the oscillation, and the left half-plane decays.
4. **Convolution slider.** Drag t to slide the flipped h(t - tau) over x(tau), shading the overlap area that builds y(t). Switch h between short decay and long oscillation. Click: output is a memory-weighted average of the past, and short h means little memory.
5. **Step and pulse through RC.** Change tau and pulse width; watch the output rise as 1 - e^{-t/tau} and the narrow pulse fail to settle. Click: pulse width compared with tau decides distortion (bandwidth).
6. **Series RLC resonance with phasor diagram.** Drag w and Q (via R); the vR, vL, vC vectors rotate and change length, with vL + vC cancelling at w0 and the |H| curve highlighted. Click: at w0 the reactive voltages are Q times the source, yet vR = vs and peak gain is 1.
7. **Bandwidth versus Q.** Drag Q from 1 to 100 and watch the -3 dB points w1 and w2 on |H|; check w0 = sqrt(w1 w2) and Delta w = w0/Q. Click: higher Q is narrower, with the same unity peak.
8. **Bode builder.** Add or drag poles and zeros on a log axis; the asymptotic lines sum, with the exact curve overlaid and the 3 dB gap at each breakpoint. Phase straight-line rule (0.1x to 10x) shown. Click: dB contributions add, and each pole bends the slope by -20 dB/decade.
