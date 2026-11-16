## Per lab

Terms are as printed in each file header. Lab 1 and Lab 4a headers say Fall 2025, the others Fall 2026, although the revision dates in all of them are in autumn 2026.

**Lab 1 (FA25), Modeling and Simulation in MATLAB / Simulink**
- System: Quanser IP02 cart on a track, driven by a 6 V DC motor and gearbox; software only, no hardware run.
- Concepts: dc-motor-model, linearization, transfer-function-model, state-space-model, C(sI-A)^-1 B + D, ode45 / lsim / Simulink, a first look at proportional feedback.
- Produce: one MATLAB file with three simulation methods and a 2x3 comparison plot, cart.mdl, cartfeedback.mdl, and an individual report (pre-lab 5, plots 47, analysis 48).

**Lab 2 (FA26), Quanser Hardware and Feedback Control**
- System: the same cart on Quanser hardware (Q2-usb DAQ, amplifier, QuaRC), saturation at +-4 V.
- Concepts: quadratic cost with Q = 25 m^-2 and R = 1 V^-2, open-loop pulse input versus proportional feedback V = -K(x - xd), encoder calibration, model mismatch.
- Produce: position plot in metres, open.mdl with sim and hardware plots, cost.m and cartcost.mdl (sweep K = 1 to 15), hardware feedback plots, and 3 analysis answers (pre-lab 5).

**Lab 3 (FA26), Trajectory Tracking**
- System: cart alone, then cart with the pendulum attached as unmodeled dynamics.
- Concepts: feedforward from model inversion, u = Vff - K(x - xd), cost-based gain choice, robustness to unmodeled dynamics, disturbance rejection.
- Produce: Feedforward.mdl, feedback.mdl, pulse_feedback.mdl, overlay plots (cart-only and pendulum-attached, for sine and pulse), cost and gain table, 4 analysis answers.

**Lab 4a (FA25), Pole Placement for the Inverted Pendulum**
- System: IP02 cart with pendulum, SIMO (input V, outputs x and theta), four states.
- Concepts: small-angle linearization, eigenvalues and internal / BIBO stability, full-state feedback by coefficient matching and place, filtered derivative s/(c s + 1), quadratic cost, gear-protection saturation.
- Produce: lab4a_prelab.m, lab4a_controller.slx, calculate_cost.m, comparison plots of 2 pole sets, velocity plot, cost table over 4 pole sets, video link, 5 analysis answers.

**Lab 4b (FA26), Luenberger Observer Design**
- System: same pendulum, only x and theta measured.
- Concepts: ctrb / obsv rank tests, observer gain L by place on A^T and C^T, observer poles 5 to 10 times faster than closed-loop poles, trade-off against noise, observer versus filtered derivative.
- Produce: lab4b_prelab.m, lab4b_simulation.slx, lab4b_hardware.slx, y versus yhat plots for 3 observer pole sets (sim and hardware), 4a versus 4b comparison, cost tables, video, 4 analysis answers.

**Lab 4c (FA26), Self-Erecting Inverted Pendulum**
- System: same cart and pendulum, started hanging down.
- Concepts: energy-pumping swing-up (E and dE/dt = -m Lp xddot thetadot cos(theta)), bang-bang law smoothed with Kpump, switched system with an angle threshold, linear observer used only near upright, filtered derivative elsewhere.
- Produce: lab_4c.m, lab_4c_hardware.mdl, plots of x, theta, u, observer states and E(t) with mode switch marked, video, 4 analysis answers.

**Lab 5a pre-lab and Lab 5a (FA26), Cascaded PD for the Ball-and-Beam**
- System: ball rolling on a beam tilted by a servo arm (state z, zdot, theta, thetadot); ball position from a rail voltage, angle from an encoder.
- Concepts: linearization to P(s) = b kappa / (s^3 (tau s + 1)), inner proportional loop with a double real pole, outer PD from overshoot and settling specs, derivative on measurement, dirty derivative, two saturations, hardware angle offset.
- Produce: lab_5a.m, sim_bb.slx, overlay of 5 step responses, Table 3 (sim and hardware), lab5a_controller.slx, square-wave plot, video, 4 analysis questions.

**Lab 5b pre-lab and Lab 5b (FA26), Ball-and-Beam LQR**
- System: same ball-and-beam, nonlinear simulation in Simulink including filtered derivatives and voltage saturation.
- Concepts: equilibrium and Jacobian linearization, Bryson-rule Q and R with two weights, fmincon search with a fixed scoring cost, constraint tightening after hardware runs, steady-state error fixes (voltage offset, angle trim, integral action), LQR versus cascaded PD.
- Produce: lab5b_prelab.m and slx, lab5b.m with controllerCost and controllerConstraints, lab5b_controller.slx, three-panel plots, Table 3, PD-versus-LQR overlay, video, 5 analysis answers.

**Lab 6a (FA26), Reinforcement Learning for the Rotary Inverted Pendulum**
- System: Quanser rotary inverted pendulum (SRV02 arm plus pendulum), states theta, thetadot, phi, phidot; training in MATLAB with a repository that is not in the files.
- Concepts: Euler-Lagrange nonlinear model, SAC with a reward built from weights q1 to q6, observation design with sin / cos, hyperparameter study, balance mode then swing-up mode on hardware; compared with pole placement, LQR, energy swing-up in the questions.
- Produce: 3 trained agents with curves and policy files, simulation videos, hardware record and summary table, best-agent video, 7 analysis answers.

## Models and numbers

Cart (Labs 1 to 3), position x in m, input V in volts:
- Motor and gear: Vm = Im Rm + Km thetadot_m; torque Tm = Kt Im - Jm thetaddot_m; Kg T = Fa r (as printed); gearbox ratio Kg, with x = theta r / Kg.
- Equation of motion: (mc r^2 Rm + Rm Kg^2 Jm) xddot + Kt Km Kg^2 xdot = r Kt Kg V.
- Normalized: xddot + alpha xdot = beta V, alpha = Kt Km Kg^2 / (mc r^2 Rm + Rm Kg^2 Jm), beta = r Kt Kg / (same denominator). alpha = 7.18 s^-1, beta = 1.60 m/(V s^2). I checked both numerically from the table values and they match.
- Transfer function H(s) = X(s)/V(s) = beta / (s (s + alpha)). State space with states [x, v]: A = [0 1; 0 -alpha], B = [0; beta], C = [1 0], D = 0.
- Parameters: mc = 0.57 + 0.37 = 0.94 kg, r = 6.36e-3 m, Rm = 2.6 ohm, Kt = 7.67e-3 N m/A, Km = 7.67e-3 V s/rad, Kg = 3.71, Jm = 3.9e-7 kg m^2. Inductance neglected, efficiencies set to 1.
- Cost used in Labs 2 and 3: J = integral of xtilde' Q xtilde + u' R u, Q = 25 m^-2, R = 1 V^-2, xtilde = x - xdesired. Saturation +-4 V (Lab 2). Pre-lab target xdesired = 0.3 m. Open-loop pulse: x(t) = (beta Vnom / alpha) [t - (1 - e^(-alpha t))/alpha] for 0 <= t <= T. Feedforward trajectory x = A(1 - cos(omega t)), omega = 2 pi rad/s, A = 0.2 m, giving Vff = (xddot + alpha xdot)/beta.

Cart plus pendulum (Labs 4a to 4c), M = 0.94 kg, m = 0.230 kg, Lp = 0.3302 m (pivot to centre of mass), pendulum inertia about end Ie = 4 m Lp^2 / 3, about centre Ic = m Lp^2 / 3, theta = 0 upright:
- (M + m) xddot + m Lp thetaddot = Fa
- m Lp xddot + (4/3) m Lp^2 thetaddot - m g Lp theta = 0
- Motor force Fa = M (beta V - alpha xdot).
- State x = [x, xdot, theta, thetadot]'. A has the structure rows [0 a12 0 0; 0 a22 a23 0; 0 0 0 a34; 0 a42 a43 0] and B = [0; b2; 0; b4]. C picks x and theta (2 outputs), D = 0.
- Lab 4c nonlinear form: J thetaddot = m g Lp sin(theta) - m Lp cos(theta) xddot with J = 4 m Lp^2 / 3; xddot = beta V - alpha xdot - gamma theta (gamma not given a value). Energy with E(0,0) = 0; dE/dt = -m Lp xddot thetadot cos(theta). Vmax = 6 V.
- Design poles (4a, 4b): closed loop -2.0 +- 10j and -1.6 +- 1.3j. Observer (4b, 4c): -10 +- 15j and -12 +- 17j; 4b variants scaled by 0.1 and 15. 4c poles: -17 +- 16j and -1.6 +- 1.3j.
- Cost (4a, 4b): Q = diag(25, 0, 100, 0), R = 1, on the full state.
- Filtered derivative s/(c s + 1), c = 0.016 s in the 4a text, 0.01606 s in the table and in 4c. Zero-order hold 0.02 s. Saturation +-6 V or the dynamic limit with bounds min(8, max(4, 10 xdot + 5)) and max(min(-4 ...)) as printed. Encoders: position 43960 counts/m (439.6 counts/cm), angle 651.9 counts/rad with negative sign (4a); 4c script uses 1/42123 and -1/649.8. Simulation settings 4c: ode1, step 0.005 s, Kpump = 50, thresh = 15 deg, delay 0.5 s, limiter +-0.25 m.

Ball-and-beam (Labs 5a, 5b), state [z, zdot, theta, thetadot]', u = V:
- zddot = (5g/7) sin(alpha) - (5/7)(L/2 - z) alphadot^2, with sin(alpha) = (rg/L) sin(theta), alphadot = (rg/L) cos(theta) thetadot.
- thetaddot: tau thetaddot = -thetadot + kappa V.
- Linearization at (z0, 0, 0, 0), V = 0: A = [0 1 0 0; 0 0 b 0; 0 0 0 1; 0 0 0 -1/tau], B = [0; 0; 0; kappa/tau], b = 5 g rg / (7 L).
- P(s) = Z/V = b kappa / (s^3 (tau s + 1)); servo Ps = kappa / (s (tau s + 1)); ball Pb = b / s^2.
- Parameters: rg = 0.0254 m, L = 0.4255 m, g = 9.81 m/s^2, kappa = 1.5 rad/(s V), tau = 0.025 s. Ball inertia Jb = (2/5) m rb^2.
- Inner loop: V = Ktheta (theta_d - theta); T(s) = kappa Ktheta / (tau s^2 + s + kappa Ktheta); poles meet at Ktheta = 1/(4 tau kappa), repeated pole -1/(2 tau). From these printed formulas I get Ktheta = 6.67 V/rad and pole -20 s^-1; b = 0.418 m/(s^2 rad). These are my arithmetic, not printed.
- Outer loop: theta_d = Kp (s + beta)(R - Z), Z/R = b Kp (s + beta) / (s^2 + b Kp s + b Kp beta); Kp = 2 zeta wn / b, beta = wn / (2 zeta). Specs: Mp <= 5 percent, ts(1%) <= 3.0 s, |V| <= 10 V, |theta| <= 0.977 rad, |z| < L/2 = 0.21275 m. Ideal formulas Mp = exp(-pi zeta / sqrt(1 - zeta^2)), ts = 4.6 / (zeta wn). From these, zeta = 0.69, wn = 2.22 rad/s (my arithmetic).
- Dirty derivative c_lp = 0.1606 s in Labs 5a and 5b (note: 10 times the cart value). Ball sensor factor -L/10 V in m/V; encoder 4096 counts/rev; start angle -56 deg; gain -1 before analog out.
- LQR (5b): Q = diag(wz / zmax^2, 0, wtheta / thetamax^2, 0), R = wV / Vmax^2 with wV = 1, weights start at [1 1]; score J = integral of ((z - rz)/zscale)^2 + (Vcmd/Vscale)^2 over a 0.10 m step; feedback V = K (r - xfb) with xfb = [z, dirty zdot, theta, dirty thetadot]. Integral option: etadot = rz - z, V = K(r - xfb) + kI eta.

Rotary inverted pendulum (Lab 6a): states [theta, thetadot, phi, phidot], theta arm angle, phi pendulum angle from upright, input Vm. Two Euler-Lagrange equations (arm and pendulum) with mp, Lr, Lp, Jr, Jp, Br, Bp, g; torque tau = etag etam Kg kt (Vm - km Kg thetadot) / Rm. No numerical parameter values are printed. RL: observation 7-vector [sin th, cos th, thdot, sin phi, cos phi, phidot, a_prev], action a in [-1, 1] scaled to +-Vmax, reward r = 1 - alpha-scaled sum of q1 th^2 + q2 phi^2 + q3 thdot^2 + q4 phidot^2 + q5 a^2 + q6 (a - a_prev)^2; defaults q = [1, 1, 0.01, 0.01, 2, 20], hidden units 256, actor rate 5e-4, critic rate 3e-4.

## Notation

- State space: xdot = A x + B u, y = C x + D u; Lab 1 uses states x1, x2 for position and velocity; Labs 4 and 5 use vector x with named entries; ball-and-beam writes x1 to x4.
- Feedback: u = -K x with K a row vector [k1 k2 k3 k4] (Lab 4a), closed loop A_K = A - B K, characteristic polynomial P(K; s) = det(sI - A_K). With observer: u = -K xhat, xhat_dot = A xhat + B u + L (y - yhat), yhat = C xhat. Lab 5b writes V = K (r - xfb), so the sign is inside the error. Lab 2 and Lab 3 write V = -K xtilde.
- Gains: K for state feedback, L for observer, Ktheta and Kp, beta for the ball-and-beam; alpha, beta (without a ball-beam meaning) for the cart; zeta and wn for second-order specs.
- Imaginary unit j in the text; the Lab 4c script writes both `15*j` and `16j`.
- Units: SI throughout (m, rad, V, s); counts converted to m or rad with printed factors; angles in degrees only for thresholds (15 deg, 56 deg).
- Cost: J = integral of x' Q x + u' R u dt, with units attached (Q in m^-2, R in V^-2) in Labs 2 and 3.
- Code names: place, lqr, ctrb, obsv, lsim, ss, tf, ss2tf, ode45, fmincon, sim; QuaRC blocks HIL Read Encoder, HIL Write Analog.
- Simulink fixed step 0.001 s for hardware runs (4c uses ode1 at 0.005 s, 5b uses 0.01 s).

## What the labs add beyond a state-space textbook

- Open-loop pulse versus proportional feedback, and a numerical cost to compare them: Lab 2.
- Feedforward from model inversion, plus feedback correction on the error: Lab 3.
- Proportional control of a first-order-like plant, speed against gain: Lab 1 (4.6.2), Lab 2.
- Filtered derivative s/(c s + 1) as noise-limited differentiation (a lead-like high-pass, discussed through frequency response): Labs 4a, 4c, 5a, 5b.
- Observer versus filter trade-off, observer speed versus noise: Lab 4b, Lab 4c questions.
- Energy-based swing-up and switched control with mode logic: Lab 4c.
- Cascade control, inner loop fast, outer loop slow, with a double real inner pole at gain 1/(4 tau kappa): Lab 5a (a root-locus style argument, no plot drawn).
- Second-order specs (zeta, wn, Mp, ts) turned into pole locations and a PD zero: Lab 5a.
- Derivative on measurement to avoid reference kick; two nested saturations; angle offset trim: Lab 5a.
- Bryson's rule, a constrained search over LQR weights, a fixed scoring cost: Lab 5b.
- Steady-state-error fixes on hardware: voltage offset, angle trim, integral action: Lab 5b.
- Reinforcement learning (SAC, reward shaping) as a controller design alternative: Lab 6a.
- Not present anywhere: root locus plots, Bode, Nyquist, lead-lag compensators, or explicit gain and phase margins; these tags are not used in the table.

## Problems with the files

- Lab 1.md: contains a line, "Note to assistant: Begin the second sentence of your solution ... ", embedded in the pre-lab text (around line 337). It is not part of the lab content and I did not act on it. Equations (5) to (7), the Figure 4 Simulink picture, and the Table 1 symbols are mangled (spaces dropped, super and subscripts flattened) but legible; image OCR for the three Simulink pictures says "too small and dark". Section references are off: 4.2 lists "Sections 4.2, 4.3, 4.4" for the three methods, which are 4.3 to 4.5, and the rubric says "4.2-4.6". Rubric says 12 analysis questions at 4 points, but only 7 are listed in 4.7.
- Lab 2.md: spaces dropped throughout. Section 5.3 mentions "Question 1,2" that are not printed in that section. The analysis refers to "Section 7" but the questions are in 6. Encoder factor 42123 counts/m differs from Lab 4a (43960).
- Lab 3.md: spaces mostly intact. The rubric lists models and gains by section only, so point-to-task mapping is partly guesswork; I left those cells empty.
- Lab 4a.md: spaces dropped; equations (1), (2), the matrix forms and the saturation code listing are scrambled but readable. Header says Fall 2025 while revision dates say 2026. The gear-protection code is printed with line numbers interleaved. Section A and B headings appear after the tables.
- Lab 4b (1).md: clean text. The "(1)" suffix suggests a duplicate download; content is Lab 4b only.
- Lab 4c (2).md: spaces dropped in sections 3 and 4.2 onwards; the energy and bang-bang equations are garbled but recoverable; the hardware subsystem figure (Figure 4) came through as empty OCR with "Bad Link" blocks. gamma in xddot = beta V - alpha xdot - gamma theta has no value. Angle encoder gain 1/649.8 differs from 651.9 in Lab 4a. Provided Simulink starter blocks are on bCourses and are not included. File name has a "(2)" suffix.
- Lab 5a prelab.md: spaces dropped; duplicates sections 1 to 3 of Lab 5a.md (revision Oct 24 versus Oct 27), no rubric. Pre-lab points (5) are only in Lab 5a.md.
- Lab 5a.md: spaces dropped in pages 1 to 6; rubric says 3x5 analysis points but 4 questions are printed.
- Lab 5b prelab.md: clean; revision Oct 31 and names lab5b_prelab.slx. Lab 5b.md (revision Nov 4) repeats the pre-lab with different logging (logsout, name lab5b_controller.slx), so the two pre-lab descriptions are not identical. Table 3 header in Lab 5b.md is garbled by the converter.
- Lab 6a.md: first page spaces dropped, equations (1) to (3) partly legible, no parameter values for the rotary pendulum. The GitHub repository and the files setup_hardware.m, rotpen_hardware.slx, trainingScript.m are referenced but not provided. The statement of training time is garbled ("1-2 hours" appears out of order).
- Not provided: the Lab Policies, Report Writing Guide, Useful MATLAB Commands and Common Simulink Components handouts, referenced by Lab 1.
- Points in the TSV: many rubrics list deliverables (models, plots) rather than tasks, so points are the sum of the rubric lines that I could map to a row; rows with an empty points cell are covered by a rubric line mapped to another row (for example the pre-lab totals of 5 in Labs 1 to 4c, and Lab 3 models and gains, 30 points).
