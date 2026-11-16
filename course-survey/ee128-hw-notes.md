## Scope
Fall 2026 (dates printed in the files). No point values are printed anywhere. HW2 has no solutions file; HW5 to HW9 have solutions only.
- HW1, issued Aug 27, due Sep 4: DC motor transfer function and simulation; determinants, inverses, rotation and unitary matrices, adjoint, similarity, block matrices.
- HW2, Sep 4 to Sep 11: linearity and time invariance, linearization of an amplifier, RC network transfer functions, equilibria (cart-pole, predator-prey), satellite linearization.
- HW3, Sep 10 to Sep 18: linearization about a trajectory (LTV), cart-pole Jacobians, frequency response, resonance peak, eigenpairs.
- HW4, Sep 17 to Sep 25: similarity and spectra, matrix exponential, functions of a matrix, Cayley-Hamilton, Jordan block exponential.
- HW5, Sep 24 to Oct 2: marginal stability, stability classification, Bloch equation, discrete-time stability, discretization.
- HW6, Oct 1 to Oct 8: ODE to transfer function and state space, controllability, magnetic ball state feedback, sampling versus gain, controllable canonical form.
- HW7, Oct 8 to Oct 16: observability, PD and PID, cruise control, observers, output feedback, integral action against a bias.
- HW8 (the file prints "Homework 7"), Oct 22 to Oct 30: step response from poles, root locus, DC motor compensators (P, I, lead), tape drive. No homework was issued between Oct 8 and Oct 22.
- HW9, Oct 29 to Nov 6: quadratic forms, PSD and PD tests, unitary matrices, finite-horizon discrete LQR with Bellman recursion.
- Midterm practice problems (version Oct 10) headings: A. Transfer Function and State Space Models (items 1-4); B. Matrix Theory (5-11); C. Stability and Control (12-17).

## Notation
- State space is x' = Ax + Bu, y = Cx + Du, with Laplace H(s) = C(sI - A)^-1 B + D. Discrete time uses x[k] (HW5) or x_k (HW6, HW9).
- State feedback is u = -Fx or u = -Kx (minus sign) in the homeworks. The practice problems (C16, C17) print u = Lx and u = Kx with NO minus: closed loop is A + BK.
- Observer is xhat' = A xhat + Bu + K(yhat - y), error matrix A + KC, so the gains come out negative (K = (-20, -295.9) in HW7 Q5). Discrete observer error also uses A + KC.
- HW1 writes the transfer function as y = Kt/(La Jm) / ((s - 1/tau1)(s - 1/tau2)), so the tau are negative (tau1 = -1/60, tau2 = -1/600) and the poles sit at 1/tau.
- HW1 uses i for the imaginary unit (and e^(i theta)); HW3 onward uses j. Adjoint is A*; transpose is A^T.
- Second-order form: H = wn^2/(s^2 + 2 zeta wn s + wn^2), poles -sigma +- j wd, Mp = e^(-pi sigma/wd), tp = pi/wd, 1 percent settling ts about 4.6/sigma.
- Typical numbers: DC motor Kt=10, La=0.5, Ra=50, Jm=1 (HW1) and J=0.01, L=0.5, R=1, k=0.1 giving 20/(s^2+2s+2) (HW8); magnetic ball A=[0 1;195.9 0], B=(0,-16.1), xeq=0.1 m, ueq=1.212, poles -5 (controller) and -10 (observer); cruise control alpha=1.84e-4, beta=1.96e-3, vL=29 m/s, heq=58 m, ueq=78.951, poles -0.2; tape drive J=0.1, b=1; heat exchanger f=0.1, beta=0.2, V=1.
- Cart-pole parameters are symbolic (m1, m2, l). The HW3 solution calls x3 = 0 pole-down and x3 = pi inverted, as the model's signs are written there.

## Recurring question styles
- Linearize a nonlinear model: find equilibria first, then the Jacobians A and B (HW2, HW3, HW7, MTP A1, A2, A4).
- Check controllability or observability by writing the rank matrix (HW6 Q2, Q3a, HW7 Q1, Q3c, Q5a).
- Place poles by matching a characteristic polynomial coefficient by coefficient, then verify with trace and determinant (HW6, HW7).
- Classify stability from eigenvalues, with Jordan block size deciding the imaginary-axis cases (HW5, MTP C12).
- Prove or give a counterexample on a matrix statement (HW1, HW4, MTP B5, B6, B11).
- Design, simulate the nonlinear model in MATLAB from several initial conditions, and comment (HW6 Q3c, HW7).
- Read time response specs from pole geometry (angle sets overshoot, real part sets settling) (HW8 Q1, Q2, Q5).
- Compensator design against specs for overshoot, settling and steady-state error, with root locus (HW8 Q4).
- Backward Bellman recursion with quadratic value functions (HW9 Q5, Q6).

## Hard spots
- Jordan block size on the imaginary axis: marginal versus unstable (HW5 Q1, Q2, MTP C12).
- Matrix exponential does not obey e^(A+B) = e^A e^B unless A and B commute (HW4 Q3).
- e^A is always invertible, so a singular A gives a nonzero determinant (HW4 Q4).
- Resonance peak exists only for zeta below 1/sqrt2, with an explicit peak frequency (HW3 Q4).
- Root locus: more gain cannot speed settling when branches run vertically; limiting-case reasoning (HW8 Q2).
- Trade-offs in design: integral action removes steady-state error but costs speed and a gain limit (HW8 Q4c); disturbance gain forces low damping (HW8 Q5).
- Discretization can destabilize a stabilizing gain: gamma below 2/T (HW6 Q4).
- Separation principle: block triangular closed loop, observer faster than controller (HW7 Q5).
- Integral action gives zero steady-state gain from a constant disturbance (HW7 Q2, Q6).
- Stabilizability versus controllability: an uncontrollable stable mode is allowed (MTP C16).
- Well-posedness of a feedback loop, I + D1 D2 invertible (MTP C14).
- Eigenvalue test for definiteness, including indefinite and semidefinite cases (HW9 Q4).

## MATLAB or simulation work
- HW1 Q1b: step responses of the motor, open loop and with gain K, to a torque disturbance.
- HW3 Q3(g): simulate sinusoid inputs over a range of frequencies and compare amplitude with |H(jw)|.
- HW6 Q3c: ode45 simulation of the nonlinear ball under the linear controller from three or more initial offsets.
- HW7 Q2c, Q2e: PD and PID closed loop with a disturbance step at t = 10; Q3d: nonlinear cruise control; Q5d: nonlinear ball with observer; Q6: bias d in {-1,0,1} with integral action.
- HW8 (all): step, stepinfo (1 percent threshold), rlocus, feedback, controlSystemDesigner for Q1b, Q2b, Q3, Q4b to Q4d; Q5 asks for an accurate hand sketch of the response.
- HW2, HW4, HW5, HW9: no simulation asked. MTP: none.

## Problems with the files
- EE128_HW1_Solutions.md: from Q1b on, spaces are dropped and symbols are scattered (matrix function section, Q2 and Q3a unreadable in places); figures only as OCR tick labels.
- EE128_HW2.md: the RC network figure (Q2) lost its topology; labels are scattered, so circuit (i) versus (ii) is not recoverable. No solutions file. Q3's figure only as text.
- EE128_HW3_Solutions.md: Q1(e) has a typo (D x-tilde instead of D u-tilde); Q3 changes B to (0,1) from the book.
- EE128_HW3.md and EE128_HW4.md: Q3 to Q6 (HW3) and Q1 to Q3 (HW4) just cite book exercises (1.2, 1.3, 3.6, 3.7, 3.8, 3.9, 3.14, 3.17); the solutions files restate them.
- EE128_HW5_Solutions.md, HW6, HW7, HW8, HW9: no problem statements apart from restatements in the solutions; HW5 Q3 (Bloch) matrix partly scattered.
- EE128_HW6_Solutions.md: pages 3 to 4 garbled (code with no spaces, plots as OCR); Q1 matrices are block [A B; C D] form.
- EE128_HW7_Solutions.md: pages 4 to 6 garbled (ACC controller, ball code, closed-loop block matrix); Q1 refers to "Homework 3, Problem 3" for the satellite but it is HW2 Q6; Q6 says "Exercise 5.3" meaning 5.4 (book typo); plot labels uncertain.
- EE128_HW8_Solutions.md: header prints "Homework 7" though it is HW8 (Oct 22 issue date); several tables partly scrambled.
- EE128_HW9_Solutions.md: readable.
- Midterm Practice Problems.md: items 13 to 16 are garbled. In item 13 the matrices A and B are scrambled and were reconstructed as A=-I (3x3), B=(0,1,1), uncertain. Item 3 is a 3x3 block [A B; C D] with D=3 shown as a matrix. Item 11(b) as printed, (I+A)^-1 (I+A), is trivially I; probably meant (I+A)^-1 (I-A). Item 12(1) is printed ambiguously (jw_1 and jw_2).
- No HW2 solutions, so HW2 rows are based on the problem statements alone.
- The folder also holds lab files and a textbook, not covered here.
