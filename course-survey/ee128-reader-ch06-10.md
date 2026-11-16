# EE 128 text, chapters 6-10 and appendices: concept notes

Source: Arcak and Poolla, "Linear Control Systems: Structure, Stability, Optimality" (book page = PDF page minus 8). Notes are paraphrased; symbols and formulas are as the book writes them. The book uses `j` for the imaginary unit and `*` for the adjoint (conjugate transpose).

## Chapter 6. Observers, Output Feedback, and Integral Control

### 6.A Observers and Observability
- **observer**: a corrected simulation copy of the plant, run in real time with the same input u, that uses the gap between measured y and predicted yhat to pull the state estimate xhat toward the true state x.
  - notation: xhat estimate, yhat predicted output, e := xhat - x estimation error (note sign: estimate minus truth), K output injection matrix (p columns, n rows)
  - formulas: plain simulation copy: xhat' = A xhat + B u, yhat = C xhat + D u, giving e' = A e. Observer: xhat' = A xhat + B u + K(yhat - y). Error: e' = (A + KC) e. If A+KC is Hurwitz, e(t) -> 0; eigenvalues of A+KC set the convergence rate.
  - conditions: the plain copy only works if A is Hurwitz and fast; the injection term is what lets you fix a slow or unstable A. Needs u known and y measured.
  - picture: block diagram (Fig 6.1) with plant feeding an observer box that outputs xhat; the model is a simulator nudged by output mismatch.
  - pitfalls: sign convention is yhat - y with +K, so the error matrix is A+KC (plus sign), unlike state feedback where u = Lx gives A+BL with L already carrying the sign.
- **observability**: the pair (C,A) is observable when rank of the observability matrix is n; equivalently the observer eigenvalues A+KC can be placed anywhere.
  - notation: N observability matrix, p outputs, n states, Sigma(A,*,C,*) for the system
  - formulas: N = [C; CA; CA^2; ...; CA^(n-1)] (stacked rows, np x n). Duality: A_dual = A', B_dual = C', L_dual = K'. Eigenvalues of A+KC equal those of A'+C'K'. So K = L_dual' where L_dual places eigenvalues of A_dual + B_dual L_dual. Theorem 83: eigenvalues of A+KC can be assigned arbitrarily iff (C,A) is observable.
  - conditions: rank N = n (Definition 82, called an operational algebraic definition; insightful definition deferred to Chapter 8).
  - picture: duality, transpose of the controllability problem for (A',C').
  - pitfalls: the book says A_dual+B_dual L_dual, so K is the transpose of the L from a place-style call on dual data.
- **detectability**: weaker than observability; some K exists with A+KC Hurwitz, because the unobservable eigenvalues are already stable.
  - formulas: Definition 84: Sigma detectable iff exists K with A+KC Hurwitz. Detectable iff dual (A',C') is stabilizable.
  - conditions: unobservable modes inherit eigenvalues from A that K cannot move; they must have negative real part.

### 6.A.4 Example: boat observer
- **observer-pole-tradeoff**: observer poles that are too slow or too fast both give bad estimates; pick a balance between sensor noise and model error (Kalman filtering does it optimally, out of scope).
  - notation: states x1 = y (position), x2 = ydot (velocity); u thrust, d disturbance force, z = y + n noisy position measurement, n sensor noise
  - formulas: m ydd = -b ydot + u + d. State space: A = [0 1; 0 -b/m], B = [0; 1/m], C = [1 0], D = 0. Disturbance d = 3 + 2cos(t) - sin(2t) N. Thrust u = 7 N for t in [0,20) min, 0 for [20,30]. The MATLAB listing also uses a simplified model y'' + 0.5 y' = u (A = [0 1; 0 -0.5], B = [0;1]). Observer gain by duality: K = place(A', -C')' (note the minus sign on C' in the listing so that K enters as +KC); place cannot take repeated poles, so use [-5, -5.01].
  - examples used: boat in one dimension, b = 2.5 N s/m, m = 300 kg. Baseline: use z directly and differentiate it numerically: position within about 2 m, velocity off by about 20 m/min while moving, about 3 m/min idle. Table of three cases, observer poles / K / position error / velocity error: A: -0.1,-0.1 / [0.29 0.156] / 20 / 6 (low gain); B: -5,-5 / [5.6 6.5] / 1 / 1 (medium); C: -100,-100 / [199.6 991.0] / 2.2 / 25 (high gain). The extraction drops minus signs in the K column and mixes units in the error columns (position metres, velocity m/min), so the signs of K are not readable; with this convention K is expected to be negative in sign.
  - picture: three error-vs-time plots (Fig 6.4): too slow lags the truth, too fast amplifies sensor noise, middle is best.
  - pitfalls: differentiating noisy data throws away the model and the known throttle; a very aggressive observer amplifies noise.

### 6.B Output Feedback
- **output-feedback**: replace the true state in the feedback law by the observer estimate, giving a dynamic controller with n states, so the closed loop has 2n states.
  - notation: v external input, L state feedback gain, K output injection, xhat observer state
  - formulas: Observer: xhat' = A xhat + B u - K(y - (C xhat + D u)), the same as +K(yhat - y); control: u = L xhat + v. Combined controller: xhat' = (A + KC + BL + KDL) xhat + (B + KD) v - K y, u = L xhat + v. Packed form: [xhat'; u] = [A+KC+BL+KDL, B+KD, -K; L, I, 0] [xhat; v; y]. Plant (6.3): [x'; y] = [A B; C D][x; u].
  - conditions: observer gain convention here is the same K as in 6.A (A+KC Hurwitz), so K is "negative" in the usual sense; the feedback is u = +Lx (so A+BL).
  - picture: Fig 6.5, plant with observer in the feedback path and L acting on xhat, plus v summed in.
  - pitfalls: a controller that has its own states is called a dynamic controller.
- **separation-principle**: eigenvalues of the closed loop are the union of those of A+BL and A+KC, so L and K can be designed independently.
  - formulas: Theorem 85. Closed loop: [x'; xhat'] = [A, BL; -KC, A+KC+BL][x; xhat] + [B; B] v, y = [C DL][x; xhat] + D v. Spec(A_cl) = Spec(A+BL) union Spec(A+KC). Proof: similarity T = [I 0; I I], T^-1 A_cl T = [A+BL, BL; 0, A+KC] (block upper triangular).
  - conditions: LTI plant; fails for nonlinear systems and for constrained controller structure (decentralized control).
  - picture: a block-triangular matrix: the two designs do not interact in the spectrum.
  - pitfalls: spectrum is separate, but transient behaviour of the plant still depends on both gains.
- **static-output-feedback**: u = Gamma y has too few knobs to place eigenvalues in general.
  - notation: Gamma (static gain), gamma scalar in SISO case
  - formulas: u = Gamma y gives x' = (A + B Gamma C) x for D = 0. Example: A = [0 1; 0 0], B = [0;1], C = [1 0]: A + gamma B C = [0 1; gamma 0], eigenvalues +-sqrt(gamma) for gamma > 0, +-j sqrt(|gamma|) for gamma < 0, never asymptotically stable.
  - examples used: double integrator
  - picture: root locus of this example lies on the imaginary axis (real axis split); book does not draw it.
  - pitfalls: controllability of (A,B) does not rescue static output feedback; use an observer.

### 6.C Integral Control
- **steady-state-gain**: the dc gain of a stable system, the output value for a constant input.
  - notation: SSG_{u->y}, xeq, ueq, yeq
  - formulas: xeq = -A^-1 B ueq, yeq = (-C A^-1 B + D) ueq. SSG_{u->y} = -C A^-1 B + D = H(0), where H(s) = C(sI - A)^-1 B + D (Definition 86). x~ = x - xeq obeys x~' = A x~.
  - conditions: A Hurwitz (so A invertible, no eigenvalue at 0).
- **disturbance-rejection**: with plain state feedback a constant disturbance gives a nonzero steady-state error that shrinks only with large gain.
  - notation: d disturbance, E disturbance input matrix
  - formulas: x' = A x + B u + E d, y = C x. With u = Lx: SSG_{d->y} = -C (A+BL)^-1 E. Example x' = u + d, y = x, u = -gamma x gives SSG = 1/gamma.
  - pitfalls: large gamma costs actuator saturation and noise amplification.
  - examples used: load torque on a motor, wind on an aircraft
- **integral-control**: feed the output into an integrator, z' = y; at steady state z' = 0 forces y = 0 for constant disturbances.
  - notation: z integrator state, L_I integral gain, A~, B~_d, C~ augmented matrices
  - formulas: u = Lx + L_I z. Augmented: [z'; x'] = [0 C; B L_I, A+BL][z; x] + [0; E] d, y = [0 C][z; x]. Since [I 0] A~ = C~ ... the book shows C~ A~^-1 = [I 0] up to sign, hence SSG_{d->y} = -C~ A~^-1 B~_d = -[I 0][0; E]... = 0.
  - conditions: A~ Hurwitz. Possible when (A,B) controllable and a mild extra condition (Exercise 6.8: det [D C; B A] nonzero, i.e. the plant has no transmission zero at s = 0).
  - picture: integrator keeps growing until the output error is exactly zero.
  - pitfalls: this is a dynamic controller; only handles constant disturbances.
- **reference-tracking**: with z' = y - r the same integrator drives y to r.
  - notation: r reference
  - formulas: z' = y - r. [z'; x'] = A~ [z; x] + B~_d d + B~_r r with B~_r = [-I; 0]. SSG_{d->y} = 0 and SSG_{r->y} = -C~ A~^-1 B~_r = I.
  - examples used: thermostat room temperature
- **homeostasis-perspective**: biology uses integral feedback (calcium regulation, synthetic genetic circuits, artificial pancreas insulin delivery, MPC mentioned). Background only.

### 6 Exercises
- Kalman decomposition for unobservable systems by duality; discrete-time observer xhat_{k+1} = A xhat_k + K(yhat_k - y_k) and its error; deadbeat observer for A = [1 1; 0 1], C = [1 0]; magnetic ball output feedback (continues 5.2); PD and PID control on a double integrator with disturbance; adaptive cruise control with bias (E = [0;1]); controllability with integrator at input or output; actuator saturation and integrator windup with anti-windup (u_r requested, saturation limit u-bar).

## Chapter 7. Positive Definite Matrices and Adjoints

### 7.A Hermitian and Positive Definite Matrices
- **unitary-matrix**: a square complex matrix whose columns are an orthonormal basis; it preserves length and inner products (a rotation or reflection).
  - notation: U, U* adjoint, real case called orthogonal
  - formulas: U*U = I (Def 87). Rotation U = [cos t, -sin t; sin t, cos t]-type example (signs garbled in the conversion). Theorem 89: ||Ux|| = ||x||, <Ux,Uy> = <x,y>, columns orthonormal, U^-1 = U*, UU* = I.
  - picture: standard basis rotated counter-clockwise by theta.
- **schur-form**: any square A equals U T U* with U unitary and T upper triangular, eigenvalues on the diagonal of T.
  - formulas: Theorem 90. A = U T U*. Proof by induction extending one normalised eigenvector to an orthonormal basis.
  - pitfalls: unlike Jordan form it is numerically reliable; eigenvalue algorithms compute it.
- **hermitian-matrix**: H = H*; the central facts are real eigenvalues and an orthonormal eigenvector set.
  - notation: H, real symmetric is a special case
  - formulas: Def 91. Theorem 92: eigenvalues real; U* H U = diag(lambda_1..lambda_n) with unitary U; columns of U are orthogonal eigenvectors. Proof: take the adjoint of the Schur form.
  - pitfalls: a complex symmetric matrix [1 j; j 1] is NOT Hermitian (A not equal A*).
- **positive-definite-matrix**: a Hermitian P whose quadratic form v*Pv is positive for every nonzero v.
  - notation: P >= 0 (written with the curly succeq) semidefinite, P > 0 (succ) definite, indefinite when the form takes both signs. P1 > P2 means P1 - P2 > 0.
  - formulas: Def 93: P >= 0 iff P = P* and v*Pv >= 0 for all v; P > 0 iff v*Pv > 0 for all v nonzero. Real case: v'Pv with v real. Theorem 97 eigenvalue test: P >= 0 iff all eigenvalues >= 0; P > 0 iff all eigenvalues > 0; indefinite iff mixed signs.
  - examples used: P1 = I (definite), P2 = diag(1,0) (semidefinite), P3 = diag(-1,1) (indefinite), form x^2+y^2 etc.; P = [2 -1; -1 2] is positive definite with form 2x^2 + 2y^2 - 2xy = x^2 + y^2 + (x-y)^2, despite a negative entry; P = [1 2; 2 1] is indefinite (v = [1;0] gives 1, v = [1;-1] gives -2) despite all-positive entries. Fig 7.1: three 3D surface plots, bowl, trough, saddle.
  - picture: quadratic bowl, flat-bottomed trough, saddle.
  - pitfalls: entry signs say nothing; test the eigenvalues. Hermitian requirement is part of the definition; a real nonsymmetric P only sees its symmetric part (P+P')/2.
- **quadratic-form**: v'Pv, only the symmetric part of P matters.
  - formulas: v'Pv = v' P~ v with P~ = (P+P')/2.
- **gram-matrix**: any B*B is positive semidefinite, and positive definite when the null space of B is {0}.
  - formulas: v*(B*B)v = ||Bv||^2 >= 0.
  - picture: squared length of an image vector.
- **matrix-square-root**: P^(1/2) = U D^(1/2) U* for P >= 0, itself Hermitian and >= 0 (and > 0 if P > 0), with P^(1/2) P^(1/2) = P.
  - formulas: Def 98, using the Schur form P = U D U*.

### 7.B Adjoints
- **adjoint**: the adjoint L* of a linear operator L: V -> W is the operator W -> V satisfying <w, L(v)> = <L*(w), v>; for matrices it is the conjugate transpose.
  - notation: script L and L*, <.,.>, V and W inner-product (Hilbert) spaces
  - formulas: Def 99: <w, L v> = <L* w, v>. For L v = A v: L* w = A* w using <x,y> = x*y. Existence guaranteed for Hilbert spaces and continuous L.
- **adjoint-of-integral-operator**: for L(v) = integral over [t0,t1] of G(t) v(t) dt, mapping L2^m[t0,t1] to R^n, the adjoint is (L* w)(t) = G(t)' w.
  - formulas: <w, L v> = w' integral G v dt; matching with integral of u(t)' v(t) dt gives u(t) = G(t)'w. Then L L*(w) = [integral G(t) G(t)' dt] w, an n x n matrix, so range(L) = range(L L*) is found as for matrices.
  - picture: the operator turns a function into a vector; the adjoint turns a vector into a function; the composition is a matrix (this is the controllability Gramian in Chapter 8).
- **range-null-adjoint**: range(L) is the orthogonal complement of null(L*); if range(L) is finite dimensional, W = range(L) direct-sum null(L*).
  - formulas: Theorem 100: range(L)^perp = null(L*). Theorem 101: null(L* L) = null(L); if range finite dim, range(L L*) = range(L). Generalises null(A*A) = null(A), range(AA*) = range(A). Finite dimensionality holds if V or W is finite dimensional (rank-nullity).
- **perspectives**: Heisenberg and matrices (Hermitian matrices give measurable quantities, real eigenvalues), positive definite matrices as energy in state space, pointing ahead to the Lyapunov equation and Gramians.

### 7 Exercises
- Unitary eigenvalues have modulus 1; diagonal entries of PSD matrices; quadratic forms and skew-symmetric matrices, gradient of x'Qx; gradient descent as x_{k+1} = Ax_k and convergence condition on step size alpha; eigenvalue test on example matrices; Rayleigh bounds lambda_min ||x||^2 <= x*Hx <= lambda_max ||x||^2; Gram decomposition A = B*B; Schur complement of M in [K L'; L M] and minimisation over u; order reversal under inversion; adjoint properties; adjoint of Euclidean-to-function-space operator.

## Chapter 8. Controllability, Observability, and the Lyapunov Equation

### 8.A Controllability
- **controllability**: a system is controllable on [t0,t1] if for any x0 and x1 some input u on that interval drives x(t0) = x0 to x(t1) = x1.
  - notation: x(t) in R^n, u(t) in R^m, Phi(t1,t) state transition matrix, [t0,t1] with t1 > t0
  - formulas: Def 103. LTV solution x(t1) = Phi(t1,t0) x0 + integral from t0 to t1 of Phi(t1,t) B(t) u(t) dt. So need x1 - Phi(t1,t0) x0 = integral Phi(t1,t) B(t) u(t) dt (8.1): the integral operator must have range all of R^n.
  - conditions: definition works for nonlinear systems; characterised for linear ones via the range of an integral operator (uses Chapter 7 adjoint results).
  - picture: reach any point in state space; the operator u -> state has full range.
- **controllability-gramian**: the n x n matrix W_c whose rank (or positive definiteness) decides controllability.
  - notation: W_c(t0,t1)
  - formulas: W_c(t0,t1) = integral from t0 to t1 of Phi(t1,t) B(t) B(t)' Phi(t1,t)' dt (8.2). Theorem 104: LTV system controllable on [t0,t1] iff W_c(t0,t1) has full rank. LTI: Phi(t1,t) = e^(A(t1-t)), W_c(t0,t1) = integral from t0 to t1 of e^(A(t1-t)) B B' e^(A'(t1-t)) dt = integral from t0-t1 to 0 of e^(-As) B B' e^(-A's) ds (8.3), with s = t - t1.
  - conditions: W_c is symmetric positive semidefinite (integral of Gram matrices); full rank means positive definite.
  - picture: integral of squared "input-to-state" gains in each direction; zero eigenvalue means a direction input cannot reach.
- **controllable-subspace / controllability-matrix-equivalence**: for LTI, W_c has the same range as the controllability matrix M, so the interval does not matter.
  - formulas: M = [B AB ... A^(n-1) B]. Theorem 105: for any t1 > t0, range(W_c(t0,t1)) = range(M); this range is the controllable subspace (directions the input can move the state relative to the free response). Controllable iff it is all of R^n. Proof: x in null(W_c) iff x'W_c x = 0 iff w(s) = B' e^(-A's) x = 0 on the interval iff x'A^k B = 0 for k = 0,1,2,... iff (Cayley-Hamilton) for k = 0..n-1 iff M'x = 0.
  - conditions: nondegenerate interval, t1 not equal t0.

### 8.B Observability
- **observability-definition**: a system is observable on [t0,t1] if from y and u on that interval the initial state x0 is uniquely determined.
  - notation: y(t) in R^p
  - formulas: Def 106. y(t) = C(t) Phi(t,t0) x0 + C(t) integral Phi(t,s) B(s) u(s) ds + D(t) u(t); known u lets you subtract the last two terms, leaving C(t) Phi(t,t0) x0 which must determine x0 uniquely, i.e. the operator x0 -> C(t)Phi(t,t0)x0 has null space {0} (Exercise 7.11 null-space result).
  - picture: initial state encoded in the output waveform; the question is whether the encoding is one-to-one.
- **observability-gramian**: the n x n matrix W_o whose rank decides observability.
  - notation: W_o(t0,t1)
  - formulas: W_o(t0,t1) = integral from t0 to t1 of Phi(t,t0)' C(t)' C(t) Phi(t,t0) dt (8.4), Theorem 107: observable iff W_o has full rank. LTI: W_o(t0,t1) = integral from 0 to t1-t0 of e^(A's) C'C e^(As) ds (8.5). Theorem 108: for t1 > t0, null(W_o(t0,t1)) = null(N), N the observability matrix of Chapter 6. That shared null space is the unobservable subspace (initial states that do not change the output); observable iff it is {0}.
  - conditions: W_o is positive semidefinite; interval immaterial for LTI. Proof: xi'W_o xi = integral ||C e^(As) xi||^2 ds, zero iff C A^k xi = 0 for k = 0..n-1 (Cayley-Hamilton), iff N xi = 0.
  - picture: Gramian measures output energy produced by an initial condition; unobservable directions produce none.
  - pitfalls: duality between W_c with (A,B) and W_o with (A',C').

### 8.C Back to BIBO Stability
- **bibo-stability**: asymptotic stability implies BIBO stability (Chapter 4, Theorem 70); the converse holds when the realization is controllable and observable.
  - formulas: Theorem 109: if (A,B,C,D) is controllable, observable and BIBO stable, then A is Hurwitz. Proof idea: if A has an eigenvalue with positive real part, controllability steers state to an eigenvector then zero input grows; if on the imaginary axis, apply the bounded input u(t) = B' e^(-lambda t) w... (with conjugate) so w*x(t) grows like t; then observability (choose K with A+KC Hurwitz) turns unbounded state into unbounded output via x' = (A+KC)x - K(y - Du).
  - conditions: both controllable AND observable. Without them, unstable hidden modes can exist while the transfer function is BIBO stable.
  - pitfalls: BIBO stable transfer function does not imply internally stable.

### 8.D Lyapunov Equation
- **lyapunov-equation**: for given Hermitian Q, find P satisfying A*P + PA + Q = 0, i.e. A*P + PA = -Q.
  - notation: A, P, Q (Hermitian), for real matrices A' replaces A* and Hermitian means symmetric
  - formulas: A*P + PA + Q = 0. Theorem 110: if A is Hurwitz and Q Hermitian then (a) unique Hermitian solution P, (b) Q >= 0 implies P >= 0, (c) Q > 0 implies P > 0. Solution formula P = integral from 0 to infinity of e^(A*t) Q e^(At) dt. Proof: d/dt (e^(A*t) Q e^(At)) = A* (..) + (..) A, integrate from 0 to inf to get -Q; uniqueness via the operator L(X) = A*X + XA being n^2 by n^2 and onto, so rank-nullity gives zero nullity. In practice solved by vectorizing (n^2 linear equations).
  - conditions: A Hurwitz for the theorem. Q > 0 not needed for P > 0 in all cases (semidefinite Q can give definite P).
  - examples used: Example 111: A = [0 1; -1 0], Q = 0 has solutions P = 0, P = I, P = -I (uniqueness and sign fail off Hurwitz). Example 112: A = [-1 1; 0 -1], Q = diag(q1,q2), P = [p1 p2; p2 p3] gives equations -2 p1 + q1 = 0 (as printed 2p1 ... with signs garbled), p1 - 2 p2 = 0, 2 p2 - 2 p3 + q2 = 0 up to sign, solution p1 = q1/2, p2 = q1/4, p3 = q1/4 + q2/2. Cases Q = diag(1,0) gives P = [1/2 1/4; 1/4 1/4], Q = diag(0,1) gives P = [0 0; 0 1/2], Q = I gives P = [1/2 1/4; 1/4 3/4]. (The three printed P values are partly garbled: first case P1 is positive definite even though Q1 is only semidefinite; second is semidefinite; third definite.)
  - picture: P as accumulated energy: x0'Px0 = integral of x(t)'Q x(t) dt along the free response from x0.
  - pitfalls: transposition convention. MATLAB lyap(A,Q) solves A X + X A' + Q = 0 (A and A* swapped), so for the book's form use lyap(A',Q); observability Gramian: lyap(A',C'*C); controllability Gramian: lyap(A,B*B').
- **gramian-lyapunov-link**: the Gramians are solutions of Lyapunov equations when A is Hurwitz.
  - formulas: Observability Gramian W_o = W_o(0,inf) = integral e^(A't) C'C e^(At) dt solves A' W_o + W_o A + C'C = 0. Controllability Gramian W_c = integral from 0 to inf e^(As) B B' e^(A's) ds solves A W_c + W_c A' + B B' = 0 (the alternative form, A and A' swapped).
  - examples used: Example 113: same A as 112, C1 = [1 0] gives W_o,1 = [1/2 1/4; 1/4 1/4] (positive definite, observable), C2 = [0 1] gives W_o,2 = [0 0; 0 1/2] (semidefinite, unobservable).
  - picture: definiteness of the Gramian is the continuous version of the rank test.
- **lyapunov-stability-test**: if P > 0 and Q > 0 satisfy the Lyapunov equation then A is Hurwitz (the converse of Theorem 110).
  - formulas: Theorem 114. Algebraic proof: Av = lambda v gives 2 Re(lambda) v*Pv = -v*Qv, so Re(lambda) = -v*Qv / (2 v*Pv) < 0. Trajectory proof: V(x) = x*Px, dV/dt = -x*Qx <= -lambda_min(Q)||x||^2 <= -(lambda_min(Q)/lambda_max(P)) V, so V(t) <= V(0) e^(-alpha t) with alpha = lambda_min(Q)/lambda_max(P); uses Rayleigh bounds lambda_min ||v||^2 <= v*Qv <= lambda_max ||v||^2 and the Comparison Lemma.
  - conditions: P > 0 and Q > 0 both needed.
  - picture: V(x) a bowl, trajectory spirals down the bowl (Fig 8.1: paraboloid with a trajectory on it, axes x1, x2, V(x)).
- **lyapunov-function**: V(x) = x*Px positive for x not 0 with negative definite derivative along trajectories, so V -> 0 and x -> 0.
  - notation: V(x), V(x,t)
  - conditions: for LTI an eigenvalue test is easier; the point is the idea extends to time-varying and nonlinear systems.
  - picture: energy-like bowl with the state sliding downhill.

### 8 Exercises
- Observability of an LTV system with C(t) = [cos t, sin t]; discrete-time observability and stacked output matrix N_k, discrete Gramian N_k'N_k, closed-form x0; sampling can destroy observability (oscillator A = [0 1; -1 0], C = [1 0], bad sampling period T); discrete-time controllability and the k >= n requirement; minimum-energy control for discrete-time (sum of ||u_t||^2, nilpotent example A = [0 1 0;0 0 1;0 0 0], B = [0;0;1]); ellipsoids E(Q) = {Qx : x'Qx <= 1} = {y : y'Q^-1 y <= 1} and image of unit ball under L is E(LL'); reachable set under unit-energy inputs is an ellipsoid (discrete analog of controllability Gramian); Sylvester equation A1 X + X A2 + Q = 0.

## Chapter 9. Optimal Control

### 9.A Finite-Horizon Optimal Control in Discrete Time
- **dynamic-programming**: Bellman's principle: the tail of an optimal decision sequence is itself optimal, so minimise over the first decision after solving the rest optimally, working backward from the final time.
  - notation: V1, V2 variables, F1, F2 functions; value function V_0(x0); cost to go V_k(x_k)
  - formulas: Lemma 115: min over V1,V2 of {F1(V1) + F2(V1,V2)} = min over V1 of {F1(V1) + min over V2 F2(V1,V2)}. Bellman equation (9.2): V_{k-1}(x_{k-1}) = min over u_{k-1} of {g_{k-1}(x_{k-1},u_{k-1}) + V_k(x_k)}, x_k = f(x_{k-1},u_{k-1}), with V_N(x_N) = g_N(x_N); solved backward from k = N to 1.
  - conditions: minimiser may be impossible to find analytically in general; LQR is the solvable case.
  - picture: shortest-path style backward recursion; cost to go as a function of current state.
- **lqr-problem-discrete**: minimise quadratic stage plus terminal cost subject to linear dynamics.
  - notation: Q, R, S weights; u_k, x_k; N horizon; V_0(x0) value function
  - formulas: general cost J(x0; u_0..u_{N-1}) = sum_{k=0}^{N-1} g_k(x_k,u_k) + g_N(x_N). LQR (9.1): minimise sum_{k=0}^{N-1} (x_k'Q x_k + u_k'R u_k) + x_N'S x_N subject to x_{k+1} = A x_k + B u_k. Weights Q >= 0, R > 0 (strictly), S >= 0.
  - conditions: R positive definite so that R + B'PB is invertible.
  - examples used: Example 116: Q = 0, R = gamma I, S = I, i.e. J = gamma sum ||u_k||^2 + ||x_N||^2; large gamma prioritises low effort, small gamma prioritises reaching the origin.
  - picture: trade between state error and control effort via the weights.
- **lqr-finite-horizon / riccati-recursion**: working backward gives a time-varying state feedback with matrices P_k from the Riccati recursion.
  - notation: P_k (cost-to-go matrix, V_k(x) = x'P_k x), u_k = -(...)x_k
  - formulas: P_N = S; P_{k-1} = Q + A'P_k A - A'P_k B (R + B'P_k B)^-1 B'P_k A, for k = N..1 (9.6). Optimal control u_{k-1} = -(R + B'P_k B)^-1 B'P_k A x_{k-1} (9.5), note the minus sign is explicit in the formula (feedback K_k = -(R+B'P_k B)^-1 B'P_k A). Value V_0(x0) = x0'P_0 x0. Uses Lemma 117 (Schur complement): for [K L'; L M] >= 0, M > 0, argmin over u of [x;u]'[K L';L M][x;u] is u = -M^-1 L x and the min is x'(K - L'M^-1 L)x, with K - L'M^-1 L >= 0. Substituting x_N = A x_{N-1} + B u_{N-1} gives the block matrix [Q + A'SA, A'SB; B'SA, R + B'SB].
  - conditions: Q >= 0, R > 0, S >= 0 keep every P_k >= 0.
  - examples used: Example 118: A = [0 1 0; 0 0 1; 0 0 0], B = [0;0;1] (A^3 = 0), Q = 0, R = gamma, S = I, N = 3: P_3 = I, P_2 = diag(0,1,1), P_1 = diag(0,0,1), P_0 = 0 (checked by hand), so V_0 = 0 and all inputs are zero because A^3 = 0 drives x_3 to 0 without control (do nothing).
  - picture: backward sweep of a matrix from the terminal weight S to P_0.
  - pitfalls: gain depends on time k; no single constant gain on a finite horizon.

### 9.B Finite-Horizon Optimal Control in Continuous Time
- **hjb-equation (setup)**: continuous-time cost with stage and terminal parts; value function and cost to go defined analogously.
  - notation: g(x,u) stage cost, sigma(x(T)) terminal cost, V(s,x) value function, s in [0,T], h > 0 small
  - formulas: J(x0;u) = integral from 0 to T of g(x(t),u(t)) dt + sigma(x(T)); V(0,x0) = min over u J; cost to go V(s,x(s)) = min over u on [s,T] of integral from s to T g dt + sigma(x(T)). Principle of Optimality gives V(s,x(s)) = min over u on [s,s+h] of {integral from s to s+h of g dt + V(s+h, x(s+h))}; Taylor expansion in h: V(s+h,x(s+h)) = V(s,x(s)) + (d/ds)V(s,x(s)) h + O(h^2), integral approx g(x(s),u(s)) h.
- **lqr-continuous**: the continuous-time LQR problem.
  - formulas: (9.7): minimise integral from 0 to T of (x'Qx + u'Ru) dt + x(T)'S x(T) subject to x' = Ax + Bu, x(0) = x0, with Q >= 0, R > 0, S >= 0.
- **hjb-equation**: the continuous-time Bellman equation, a PDE for the value function V(s,x).
  - notation: V_s = partial V/partial s, grad_x V column gradient, f(x,u) dynamics
  - formulas: -V_s(s,x) = min over u of { g(x,u) + grad_x V(s,x)' f(x,u) }, V(T,x) = sigma(x) (9.8). Derived by splitting [s,T] at s+h, applying the principle of optimality, Taylor expanding in h, dividing by h.
  - conditions: assumes V differentiable; if HJB has a differentiable solution then its minimiser is an optimal policy (proved in Appendix E).
  - picture: continuous limit of the backward recursion as the time step goes to zero.
- **riccati-equation (differential)**: guessing V(t,x) = x'P(t)x turns the HJB into a matrix ODE solved backward in time.
  - notation: P(t) symmetric, P(T) = S; grad_x V = 2P(t)x; -V_t = -x'P'(t)x (P-dot written P˙)
  - formulas: Riccati Differential Equation (9.9): -P'(t) = P(t)A + A'P(t) + Q - P(t) B R^-1 B' P(t), P(T) = S. Optimal control u(t) = -R^-1 B' P(t) x(t) (time-varying state feedback). Value V(0,x0) = x0' P(0) x0. Derivation uses Lemma 117 on [PA+A'P+Q, PB; B'P, R] and the fact x'Mx = 0 for all x implies M = 0 for symmetric M.
  - conditions: Q >= 0, R > 0, S >= 0.
  - pitfalls: solved backward from t = T to t = 0; the sign convention is P-dot = -(...), so P-dot is minus the right-hand side.
- **riccati-solutions**: examples and two tricks for solving the RDE.
  - formulas: Example 119: Q = S = 0 gives P(t) = 0 and u = 0. Example 120: A = 0, B = 1, Q = 0, R = gamma, S = 1, T = 1 (x' = u, J = gamma integral u^2 dt + x(1)^2): RDE: -P' = -P^2/gamma, i.e. P' = P^2/gamma with P(1) = 1, P(t) = gamma/(gamma + 1 - t), u(t) = -(1/(gamma+1-t)) x(t), x(t) = ((gamma+1-t)/(gamma+1)) x(0), x(1) = gamma/(1+gamma) x(0). As gamma -> 0, x(1) -> 0 (cheap control); as gamma -> infinity, u ~ 0 and x(1) ~ x(0).
  - linearisation (Section 9.B.6): X' = (A - B R^-1 B' P(t)) X, X(T) = I; Y = P X; then [X'; Y'] = [A, -B R^-1 B'; -Q, -A'] [X; Y], [X(T); Y(T)] = [I; S], and P(t) = Y(t) X(t)^-1; X invertible as a state transition matrix. This shows the nonlinear RDE has a well-defined solution. The matrix [A, -BR^-1B'; -Q, -A'] is the Hamiltonian matrix (name not used in the text).
  - forward in time (9.B.7): Pi(t) := P(T-t) satisfies Pi' = A'Pi + Pi A + Q - Pi B R^-1 B' Pi (9.11), Pi(0) = S; V(0,x0) = x0' Pi(T) x0 and u(t) = -R^-1 B' Pi(T-t) x(t).
  - picture: scalar example, P(t) rising toward the terminal value; gamma sets effort vs terminal accuracy.

### 9.C Infinite-Horizon LQR
- **lqr-infinite-horizon**: let the horizon go to infinity with no terminal cost; the time-varying gain converges to a constant gain.
  - notation: Pi limit of Pi(T), J_infinity(x0,u), V_T(x0) = x0' Pi(T) x0
  - formulas: (9.12) minimise integral from 0 to infinity of (x'Qx + u'Ru) dt subject to x' = Ax + Bu, x(0) = x0, no terminal cost. Forward RDE (9.13): Pi' = A'Pi + Pi A + Q - Pi B R^-1 B' Pi, Pi(0) = 0. Lemma 121: with S = 0, V_T(x0) is nondecreasing in T and V_T(x0) <= J_infinity(x0,u) for all u. Lemma 122: (A,B) stabilizable implies some u gives finite J_infinity. Hence Pi := limit as T -> infinity of Pi(T) exists (9.14), Pi >= 0. Because Pi' -> 0, Pi satisfies the Algebraic Riccati Equation (ARE) (9.15): 0 = A'Pi + Pi A + Q - Pi B R^-1 B' Pi.
  - conditions: Q >= 0, R > 0, (A,B) stabilizable.
  - picture: cost-to-go grows with horizon but is bounded; the matrix settles.
- **algebraic-riccati-equation / lqr-optimal-law**: the optimal control is a constant state feedback with gain from Pi, and the closed loop is stable.
  - formulas: Theorem 123: (a) u*(t) = -R^-1 B' Pi x(t) (9.17) is optimal and the minimum cost is J_infinity(x0,u*) = x0' Pi x0. (b) lim x(t)'Qx(t) = 0; if Q > 0 then x(t) -> 0. Closed loop x' = (A - B R^-1 B' Pi) x =: A_cl x. Proof: with the ARE, A_cl'Pi + Pi A_cl = -(Q + Pi B R^-1 B' Pi), so J = -integral d/dt (x'Pi x) dt = x0'Pi x0 - lim x'Pi x. Lemma 124: xi'Pi xi = 0 implies xi'Q xi = 0, so Q > 0 implies Pi > 0. Lemma 125: if Q > 0 the ARE has at most one positive definite solution (proof via Lyapunov A_i'Pi_i + Pi_i A_i + Q_i = 0 with A_i = A - BR^-1B'Pi_i and a Sylvester argument), so the limit is that unique solution.
  - conditions: Q > 0 (or detectability of (C,A) where Q = C'C), R > 0, (A,B) stabilizable.
  - examples used: Example 126: A = 0, B = 1, Q = 1, R = 1: ARE 1 - pi^2 = 0, pi = 1, u* = -x. Example 127: double integrator A = [0 1; 0 0], B = [0;1], Q = I, R = 1: ARE gives pi12 = 1, pi22 = sqrt(1 + 2 pi12) = sqrt 3, pi11 = pi12 pi22 = sqrt 3; Pi = [sqrt3 1; 1 sqrt3], u* = -[1 sqrt3] x, closed loop [0 1; -1 -sqrt3] with characteristic polynomial s^2 + sqrt3 s + 1 and eigenvalues -sqrt3/2 +- j/2.
  - picture: none given; gain K = -R^-1 B'Pi is the feedback matrix; pole locations come out of the weights.
  - pitfalls: the ARE has several solutions; pick the positive definite one (or the positive semidefinite stabilising one). The sign flip: feedback is u = -R^-1 B'Pi x, so the "L" of Chapter 5 is L = -R^-1 B'Pi.
- **lqr-with-semidefinite-Q**: Q >= 0 is fine if (C,A) is detectable with Q = C'C; in practice add a small epsilon.
  - formulas: stabilizable (A,B) and detectable (C,A) give a unique positive semidefinite ARE solution, equal to the limit Pi (proof omitted). Practical trick: replace x1^2 by x1^2 + eps x2^2 with small eps > 0, so Q = diag(1, eps) > 0.
- **lqr-discrete-infinite**: discrete infinite-horizon LQR from the Riccati difference equation run forward.
  - formulas: Pi_0 = S = 0; Pi_{k+1} = Q + A'Pi_k A - A'Pi_k B (R + B'Pi_k B)^-1 B'Pi_k A (9.19), with Pi_k = P_{N-k}. Limit solves the Discrete ARE: Pi = Q + A'Pi A - A'Pi B (R + B'Pi B)^-1 B'Pi A. Control u*_k = -(R + B'Pi B)^-1 B'Pi A x_k, cost x0'Pi x0, and x_k -> 0 if Q > 0.
  - conditions: (A,B) stabilizable, Q >= 0, R > 0.
- **matlab-lqr**: [K,P] = lqr(A,B,Q,R) returns the optimal gain K, with K = -R^-1 B'P as the book writes it, to be substituted in u = Kx; P corresponds to Pi. dlqr(A,B,Q,R) for discrete time returns K and the discrete ARE solution.
  - pitfalls: the book's K carries the minus sign (u = Kx, same role as its L). Real MATLAB lqr returns the positive gain for u = -Kx, so the book's text and the software differ by a sign; flag when writing a tool.

### 9 Exercises
- Scalar discrete-time finite-horizon LQR (a, r, s); LQR with cross term Z in stage cost; making RDE linear on the Example 120 problem; ARE for rotation system A = [0 1; -1 0] with B = I (hint: do not fight the rotation); Q > 0 implies A_cl'Pi + Pi A_cl < 0; variable state weight q on x1 as q -> 0; LQR with uncontrollable mode x2' = a x2.

## Chapter 10. Understanding Linear Systems Through the SVD

(Note: the first pages of this chapter, lines about 10896 to 11365, are doubled and garbled in the conversion: two overlapping versions of the same pages, spaces dropped. They are read through below; the content is the standard SVD introduction.)

### 10.A Anatomy of a Matrix: Singular Value Decomposition
- **svd**: every matrix factors as A = U Sigma V*, with unitary U, V and a diagonal Sigma of nonnegative singular values; multiplication by A is rotate, stretch, rotate.
  - notation: A in C^(m x n), rank r, U in C^(m x m), V in C^(n x n), singular values sigma_1 >= sigma_2 >= ... >= sigma_r > 0, left singular vectors u_i (columns of U), right singular vectors v_i (columns of V), Sigma_1 = r x r diagonal block
  - formulas: Theorem 128 (numbered 122 in one garbled copy): A = U [Sigma_1 0; 0 0] V*. A v_i = sigma_i u_i for i = 1..r. If A real then U, V real orthogonal; singular values real whether A is real or complex. Compact form: A = U_1 Sigma_1 V_1* = sigma_1 u_1 v_1* + ... + sigma_r u_r v_r* with U_1 in C^(m x r), V_1 in C^(n x r) (sum of rank-one terms, each with range spanned by u_i).
  - conditions: Sigma is unique, U and V are not (e.g. flip signs of both U~ = -U, V~ = -V).
  - examples used: Example 129: rank-one A = [1 1 1; 2 2 2] decomposed as column times row, A = (1/sqrt5)[1;2] * sqrt15 * (1/sqrt3)[1 1 1] (sigma_1 = sqrt15, u_1 = [1;2]/sqrt5, v_1 = [1;1;1]/sqrt3).
  - picture: Figure 10.1: unit ball mapped to an ellipsoid with semi-axes sigma_i u_i, v_i mapped to those axes.
  - pitfalls: U and V are square (dimensions match rows and columns), Sigma is m x n like A.
- **svd-geometry**: V* rotates v_i to e_i, Sigma stretches axis i by sigma_i, U reorients sigma_i e_i to sigma_i u_i; so the unit ball goes to an ellipsoid.
  - formulas: ||Ax||_2 <= sigma_1 ||x||_2 with equality at x = v_1; sigma_1 is the induced 2-norm of A (Chapter 2). Chapter refers back to Exercise 8.6: image of unit ball under L is E(LL').
  - picture: Figure 10.2: three steps right to left, rotation V*, axis-aligned stretch Sigma, rotation U.
- **svd-applications-preview**: SVD used for model reduction, robustness analysis, system identification (control) and PCA (statistics: right singular vectors are directions of maximal variance, squared singular values are the variances); it also shows range and null spaces and their complements.
- **range-null-from-svd**: the SVD gives orthonormal bases of all four fundamental subspaces.
  - formulas: Theorem 130, with U = [U1 U2], V = [V1 V2], U1 m x r, V1 n x r: columns of U1 span range(A), U2 span null(A*), V1 span range(A*), V2 span null(A). Rank-nullity as corollary: nullity n - r. Proof uses x = V1 Sigma_1^-1 z.
  - picture: U1/U2 split of the output space, V1/V2 split of the input space.
- **matrix-norm**: the induced 2-norm of A is its largest singular value.
  - notation: ||A||_2 = max over ||x||_2 = 1 of ||Ax||_2 = sigma_1
  - formulas: ||x||_2 = 1 implies ||Ax||_2 <= sigma_1, equality at x = v_1; ||Ax|| <= sigma_1 ||x||.
  - examples used: Exercise 10.6 asks for ||A||_2 of the 3 x 2 all-ones matrix.
  - pitfalls: singular values are not eigenvalues (see condition number below).
- **low-rank-approximation (partial)**: the book writes A as a sum of r rank-one pieces sigma_i u_i v_i* ordered by size, but this range states no Eckart-Young optimal-truncation theorem; truncation is used only for balanced truncation of systems.
  - formulas: A = sigma_1 u_1 v_1* + ... + sigma_r u_r v_r*.

### 10.A.6 Pseudoinverse
- **pseudo-inverse**: the pseudoinverse A-dagger gives the minimum-norm least-squares solution of Ax = b by inverting only the nonzero singular directions.
  - notation: A-dagger written A with a dagger; b = U1 U1* b + U2 U2* b (projection onto range(A) plus onto its orthogonal complement)
  - formulas: when b is not in range(A), solve Ax = U1 U1* b (least squares, minimises ||Ax - b||_2). With A = U1 Sigma_1 V1*: any x with V1* x = Sigma_1^-1 U1* b works; minimum-norm one lies in null(A)-perp = range(V1), giving x = V1 Sigma_1^-1 U1* b. Definition A-dagger := V1 Sigma_1^-1 U1*. For invertible A, A-dagger = A^-1. Special cases (left as exercise): A-dagger = A*(AA*)^-1 when range(A) = C^m (full row rank), A-dagger = (A*A)^-1 A* when null(A) = {0} (full column rank); these were Exercises 3.3 and 3.4.
  - conditions: uses the SVD with rank r.
  - examples used: Exercise 10.5: pseudoinverse of A = [1 1 1; 2 2 2] and minimum-norm least squares for b = [1.2; 1.9].
  - picture: project b onto the range, undo each stretch, stay in the row space.

### 10.A.7 Computing the SVD
- **svd-computation**: singular values are square roots of eigenvalues of AA*; U comes from the eigenvectors of AA*; V1 = A*U1 M^(-1/2).
  - notation: mu_1 >= ... >= mu_r > 0 positive eigenvalues of AA*, M = diag(mu_1..mu_r)
  - formulas: AA* = U [M 0; 0 0] U* (Schur form of a Gram matrix). Theorem 131: sigma_i = sqrt(mu_i); A = U [M^(1/2) 0; 0 0] V*, V = [V1, V2], V1 = A* U1 M^(-1/2), V2 an orthonormal basis of null(A). Proof checks V1*V1 = I and U1 U1* A = A because U2* A = 0.
  - examples used: Example 132: A = [1 1000; 0 1] has eigenvalues 1, 1 but singular values about 10^3 and 10^-3, condition number about 10^6. Example 133: the same rank-one A = [1 1 1; 2 2 2]: AA* = [3 6; 6 12], mu = 15, 0, sigma_1 = sqrt15, U = [1 2; 2 -1]/sqrt5, V1 = [1 1 1]'/sqrt3, V completed with columns [1 -1 0]/sqrt2-type and [1 1 -2]/sqrt6-type (printed as 1/sqrt3 1/sqrt2 1/sqrt6; 1/sqrt3 -1/sqrt2 1/sqrt6; 1/sqrt3 0 -2/sqrt6).
  - picture: condition number = ratio sigma_1 / sigma_n = elongation of the ellipsoid; tiny input error can mean large output error.
  - pitfalls: eigenvalues of A and singular values of A can differ enormously; forming AA* or A*A squares the condition number, so real software uses Golub-Kahan bidiagonalization. A and A* share singular values with U and V swapped, so use A*A when A is tall.

### 10.B Quantifying Controllability and Observability
- **controllability-gramian (energy picture)**: the reachable set from rest in unit input energy is the ellipsoid E(W_c); long axes are easy directions.
  - notation: W_c = integral from -inf to 0 of e^(-At) B B' e^(-A't) dt, L(u) = integral from -inf to 0 of e^(-At) B u(t) dt (10.1) maps input to x(0)
  - formulas: W_c solves A W_c + W_c A' + B B' = 0. Reachable set {L(u) : integral ||u||^2 dt <= 1} = {W_c v : v'W_c v <= 1} = E(W_c); restricting u to range(L*), u = L*(v) = B' e^(-A't) v, gives L(u) = L L*(v) = W_c v and energy v'W_c v. Axes are eigenvectors of W_c, lengths grow with eigenvalues.
  - examples used: W_c = diag(10^4, 1) (10.2): the first state is far easier to control.
  - picture: ellipsoid of states reachable with unit input energy; long axis = cheap direction.
- **observability-gramian (energy picture)**: the output energy from initial state x0 with zero input is x0' W_o x0.
  - formulas: W_o = integral from 0 to inf e^(A't) C'C e^(At) dt solves A'W_o + W_o A + C'C = 0. Output y(t) = C e^(At) x0 and integral ||y||^2 dt = x0' W_o x0 (10.3).
  - examples used: W_o = diag(1, 10^2) (10.4): output is more sensitive to the second state component.
  - picture: initial states aligned with large-eigenvalue eigenvectors ring loudly at the output.

### 10.C Balanced Realizations and Truncation
- **gramians-under-state-transformation**: Gramians depend on the choice of state coordinates; rescaling helps one and hurts the other equally.
  - notation: xhat = T^-1 x, T invertible, Wc-hat, Wo-hat
  - formulas: Wo-hat = T' W_o T; Wc-hat = T^-1 W_c T^-T. Product Wc-hat Wo-hat = T^-1 W_c W_o T is a similarity transform of W_c W_o.
  - examples used: Example 134: scalar x' = -0.5x + 10u, y = x gives W_c = 100, W_o = 1. With xhat = theta^-1 x: xhat' = -0.5 xhat + 10 theta^-1 u, y = theta xhat, so Wc-hat = 100 theta^-2, Wo-hat = theta^2. Choosing theta = sqrt10 gives both equal to 10. Example 135: W_c = diag(10^4,1), W_o = diag(1,10^2), T = diag(10, 10^(-1/2)) gives Wc-hat = Wo-hat = diag(100, 10); the first direction is both easier to control and to observe.
  - pitfalls: increasing controllability artificially by scaling costs the same amount of observability, so neither Gramian alone measures importance of a state.
- **balanced-realization**: coordinates in which the two Gramians are equal and diagonal, with the diagonal sorted from largest to smallest.
  - notation: Sigma = M^(1/2) = diag(sigma_1..sigma_n), sigma_1 >= ... >= sigma_n > 0
  - formulas: W_c^(1/2) W_o W_c^(1/2) = U M U' (10.5), U orthogonal; Sigma = M^(1/2) (10.6). Theorem 136: T = W_c^(1/2) U Sigma^(-1/2) gives the realization (T^-1 A T, T^-1 B, C T, D) with Wc-hat = Wo-hat = Sigma. Check: Wc-hat = Sigma^(1/2) U' W_c^(-1/2) W_c W_c^(-1/2) U Sigma^(1/2)... = Sigma; Wo-hat = Sigma^(-1/2) U' (U Sigma^2 U') U Sigma^(-1/2) = Sigma.
  - conditions: (A,B,C,D) asymptotically stable, controllable and observable (so both Gramians are positive definite).
  - picture: ellipsoids of reachability and observability aligned and equal.
- **hankel-singular-values**: sigma_i from the balancing are intrinsic to the input-output behaviour: square roots of the eigenvalues of W_c W_o.
  - formulas: sigma_i = sqrt(eig_i(W_c W_o)) since W_c^(1/2) W_o W_c^(1/2) and W_c W_o are similar; invariant under state transformation because Wc-hat Wo-hat = T^-1 W_c W_o T. They are the singular values of the Hankel operator: past input u(t), t in (-inf,0), to state x(0) to future unforced output y(t) = C e^(At) x(0), t in (0,inf); finite rank n because the state is n-dimensional.
  - picture: large sigma_i means state i is easy to excite and easy to see; ranking of state importance.
- **balanced-truncation**: drop the states with small Hankel singular values from a balanced realization to get a low-order model.
  - notation: partition A = [A11 A12; A21 A22], B = [B1; B2], C = [C1 C2], A11 in R^(k x k); reduced model (A11, B1, C1, D)
  - formulas: keep the first k states when there is a gap between sigma_k and sigma_{k+1}. Reduce only the stable part; keep unstable dynamics intact.
  - conditions: start from a controllable, observable, stable realization; large models (finite element with thousands of states) motivate it.
  - examples used: 48th-order system with several resonance peaks: 4th-order reduction captures two peaks, 10th-order captures three (Figs 10.3, 10.4, magnitude in dB and phase in degrees against frequency, 10^0 to 10^5). Perspectives: Keck telescope, 36 hexagonal mirror segments, 100 or more states.
  - picture: discard directions that are both weakly controllable and weakly observable (Stoic analogy in the text).
  - pitfalls: balanced truncation does not match any particular frequency range; it keeps the worst-case frequency-response error small, so it can look imperfect at low or high frequency (remark after Exercise 10.9).

### 10 Exercises
- Product of eigenvalue magnitudes equals product of singular values; A = [1 k; 0 1] eigenvalues vs singular values (sigma_1 about k, sigma_2 about 1/k); rotation matrix singular values; Hermitian matrix singular values equal |lambda_i|; singular values via the embedding [0 A; A* 0] (eigenvalues +-sigma_i and n+m-2r zeros); pseudoinverse of the rank-one matrix and a least-squares problem; SVD of the 3 x 2 all-ones matrix, 2-norm, range and null spaces, pseudoinverse; A-dagger = A*(AA*)^-1 and (A*A)^-1 A*; balanced realization for W_c = diag(10^4,1), W_o = diag(1,10^2) (compare Example 135); balanced truncation of A = [-1 -1; 1 -1]... (printed A = [-1 1; -1 -1]-type, signs garbled), B = [1;0], C = [1 0], D = 0, with bodemag comparison.

## Appendices

### Appendix A. Review of Basic Concepts (what the reader is assumed to know)
- Quantifiers "there exists" and "for all" and the order-of-quantifiers trap (cats and dogs); set-builder notation; Cartesian products.
- Proof techniques: if and only if (two directions), set equality as two inclusions, contradiction, contrapositive, induction (sum 0+1+...+n example).
- Complex numbers: z = a + jb, conjugate, |z|^2 = z z-bar, polar form z = r e^(j theta), Euler identity e^(j theta) = cos theta + j sin theta. Uses `j`.
- Functions: domain, co-domain, image, surjective (onto), injective (one-to-one).
- Vectors and matrices: R^n, C^n, R^(m x n), identity, non-commutativity (AB not equal BA; v'v scalar, vv' matrix), matrix-vector product as a weighted sum of columns.
- Block-partitioned matrices and conformable multiplication.
- Linear systems Ax = b: overdetermined (no solution), underdetermined (many), unique.
- Transposes and adjoints: Definition 137 (A' and A* = conjugate transpose); Lemma 138: (A*)* = A, (A+B)* = A* + B*, (AB)* = B*A*.
- Determinants and inverses: Definition 139; Lemma 140 (inverse of product, (A*)^-1 = (A^-1)*); Lemma 141 (det(AB) = det A det B, det A' = det A, det A* = conj det A); Proposition 142 (block inverses, Schur complement Delta = A - B D^-1 C); Corollary 143 (block determinants: det [X Y; 0 Z] = det X det Z, det [A B; C D] = det(A - B D^-1 C) det D).
- Trace: Tr(A) = sum of diagonal; Lemma 145: Tr(A+B), Tr(AB) = Tr(BA), Tr(A*A) = sum |a_ij|^2.

### Appendix B. Rank-Nullity Theorem
- **rank-nullity-statement**: if L: V -> W is linear and V is finite dimensional, then dim V = dim null(L) + dim range(L).

### Appendix C. Cayley-Hamilton Theorem
- **cayley-hamilton-statement**: for A in C^(n x n) with characteristic polynomial chi(s) = sum_{k=0}^n alpha_k s^k, chi(A) = 0. (Used in Chapter 8 to cut infinite conditions x'A^k B = 0 down to k = 0..n-1.)

### Appendix D. Heymann's Lemma
- **heymann-lemma-statement**: Heymann's Lemma: let (A,B,*,*) be a multi-input controllable system and v in R^m with Bv not 0; with b = Bv, there exists L0 in R^(m x n) such that the single-input system (A + B L0, b, *, *) is controllable.
- Theorem 146 (supporting): for x_{t+1} = A x_t + B u_t, x0 = 0, with v such that Bv not 0 and u0 = v (so x1 = Bv): (a) there exist u_1..u_{n-1} such that x_1..x_n are linearly independent; (b) there exists L0 in R^(n x m) (as printed) with u_t = L0 x_t for t = 1..n-1.

### Appendix E. Proof of Optimality from the HJB Equation
- **hjb-verification-theorem**: Theorem 147: suppose V(t,x) is a continuously differentiable solution of the HJB equation -V_t(t,x) = min over u of { g(x,u) + grad_x V(t,x)' f(x,u) } with V(T,x) = sigma(x) and minimiser u = alpha(t,x), and that the closed loop x' = f(x, alpha(t,x)) has unique solutions with trajectory x*(t) from x(0) = x0. Then u*(t) = alpha(t,x*(t)) solves the optimal control problem: J(x0,u*) <= J(x0,u) for every other input u, and J(x0,u*) = V(0,x0).

## Notation and conventions for these chapters

| symbol | meaning | convention |
|---|---|---|
| e := xhat - x | observer estimation error | estimate minus truth; e' = (A+KC) e |
| K | observer (output injection) gain, n x p | enters as +K(yhat - y) = -K(y - yhat); design A+KC Hurwitz; K comes out negative-looking; by duality K = L_dual' with A_dual = A', B_dual = C' |
| L | state-feedback gain, m x n | u = Lx + v (plus sign), closed loop A+BL; the sign is absorbed in L (so LQR gives L = -R^-1 B'Pi) |
| xhat' | observer | A xhat + B u - K(y - (C xhat + D u)); controller with output feedback has the same n states as the plant, closed loop has 2n |
| Spec(A_cl) | separation principle | Spec(A+BL) union Spec(A+KC) |
| N, M | observability, controllability matrix | N = [C; CA; ...; CA^(n-1)] (stacked rows), M = [B AB ... A^(n-1)B] (side by side) |
| (C,A), (A,B) | pair order | the observability pair is written (C,A) (output matrix first); controllability pair (A,B) |
| Sigma(A,*,C,*) | system with B, D irrelevant | star in B and D positions means unspecified |
| Gamma, gamma | static output feedback gain | u = Gamma y, closed loop A + B Gamma C (D = 0) |
| z, L_I | integrator state and gain | z' = y (disturbance rejection) or z' = y - r (tracking); u = Lx + L_I z; augmented A~ = [0 C; B L_I, A+BL]; ordering is [z; x] |
| SSG_{u->y} | steady-state (dc) gain | -C A^-1 B + D = H(0); with state feedback the d to y gain is -C(A+BL)^-1 E |
| E, d | disturbance input matrix and disturbance | x' = Ax + Bu + Ed |
| U, V, U* | unitary matrix, adjoint | U*U = I; * is conjugate transpose, ' or T is plain transpose (used for real data); real unitary is called orthogonal |
| P >= 0, P > 0 | positive semidefinite, definite | written with curly succeq and succ; requires P Hermitian; P1 > P2 means P1 - P2 > 0 |
| lambda_min, lambda_max | Rayleigh bounds | lambda_min ||x||^2 <= x*Hx <= lambda_max ||x||^2 |
| P^(1/2) | square root | U D^(1/2) U*, for P >= 0 |
| script L, L* | linear operator and adjoint | <w, L v> = <L* w, v>; for L(v) = integral G v dt, (L* w)(t) = G(t)' w |
| Phi(t1,t0) | state transition matrix | e^(A(t1-t0)) for LTI |
| W_c | controllability Gramian | integral from 0 to inf of e^(As) B B' e^(A's) ds, solves A W_c + W_c A' + B B' = 0 (A Hurwitz) |
| W_o | observability Gramian | integral from 0 to inf of e^(A't) C'C e^(At) dt, solves A' W_o + W_o A + C'C = 0 |
| Lyapunov equation | form used in text | A*P + PA + Q = 0, i.e. A'P + PA = -Q; solution P = integral e^(A*t) Q e^(At) dt; MATLAB lyap(A',Q) for this form, lyap(A,Q) solves AX + XA' + Q = 0 |
| V(x) = x*Px | Lyapunov function | dV/dt = -x*Qx along x' = Ax |
| Q, R, S | LQR weights | stage cost x'Qx + u'Ru, terminal x'Sx; Q >= 0, R > 0 (strict), S >= 0 |
| discrete LQR cost | finite horizon | sum_{k=0}^{N-1} (x_k'Q x_k + u_k'R u_k) + x_N'S x_N, x_{k+1} = A x_k + B u_k |
| continuous LQR cost | finite horizon | integral from 0 to T of (x'Qx + u'Ru) dt + x(T)'S x(T), x' = Ax + Bu |
| infinite-horizon cost | no terminal term | integral from 0 to inf of (x'Qx + u'Ru) dt |
| P_k, P(t), Pi | cost-to-go matrices | V_k(x) = x'P_k x, V(t,x) = x'P(t)x; Pi = limit of the forward Riccati solution Pi(t) := P(T-t) with Pi(0) = S (S = 0 for infinite horizon) |
| discrete Riccati | backward recursion | P_{k-1} = Q + A'P_k A - A'P_k B (R + B'P_k B)^-1 B'P_k A, P_N = S; u_{k-1} = -(R + B'P_k B)^-1 B'P_k A x_{k-1} |
| RDE | continuous Riccati | -P' = PA + A'P + Q - P B R^-1 B' P, P(T) = S, solved backward; u = -R^-1 B'P(t) x |
| ARE | algebraic Riccati | 0 = A'Pi + Pi A + Q - Pi B R^-1 B' Pi; u* = -R^-1 B'Pi x; A_cl = A - B R^-1 B'Pi; cost x0'Pi x0 |
| lqr (MATLAB) | gain | book writes K = -R^-1 B'P with u = Kx; real MATLAB lqr returns the positive gain for u = -Kx |
| V_k, V(s,x) | cost to go / value function | V_0(x0) is the value of the whole problem |
| sigma_i, u_i, v_i | singular value, left and right singular vectors | A = U Sigma V*, sigma_1 >= ... >= sigma_r > 0, A v_i = sigma_i u_i; U is m x m, V is n x n |
| A-dagger | pseudoinverse | V1 Sigma_1^-1 U1*; minimum-norm least-squares solution x = A-dagger b |
| E(Q) | ellipsoid | {Qx : x'Qx <= 1} = {y : y'Q^-1 y <= 1}; image of unit ball under L is E(LL') |
| T, xhat = T^-1 x | change of state coordinates | Wo-hat = T'W_oT, Wc-hat = T^-1 W_c T^-T; balancing T = W_c^(1/2) U Sigma^(-1/2) |
| sigma_i (system) | Hankel singular values | sqrt of eigenvalues of W_c W_o; independent of realization |
| j | imaginary unit | book uses j |

## Where a visual would help most

1. **Observer pole placement versus noise (observer, observer-pole-tradeoff).** Drag the observer pole location (real, repeated) on a slider; the boat model runs with a noisy position sensor and an unknown disturbance. Move: estimation error traces for position and velocity, plus the true state against the estimate. Click: too slow leaves a lagging estimate, too fast passes noise straight through, and there is a middle pole that balances model trust against sensor trust.
2. **Separation of eigenvalues (separation-principle).** Two pole-placement handles on a complex plane, one for A+BL (controller) and one for A+KC (observer), with the combined 2n closed-loop poles drawn. Move: the closed-loop pole set and the step response of state versus estimate. Click: the closed-loop poles are exactly the union of the two sets, so moving one design never moves the other's poles.
3. **Integral action removes the constant-disturbance error (integral-control, disturbance-rejection).** Toggle between proportional feedback with gain gamma and integral action, then drag a constant disturbance d (and a reference r). Move: output y(t), integrator state z(t), control u(t). Click: with only proportional gain the output settles at d/gamma, with the integrator the output goes to r no matter how big d is, while z soaks up the disturbance. Add the saturation toggle to show windup.
4. **Quadratic form surface and its eigenvalues (positive-definite-matrix, quadratic-form).** Drag the entries of a symmetric 2 x 2 matrix (or its eigenvalues and eigenvector angle). Move: the surface v'Pv and its level curves (ellipses, a line, hyperbolas), eigenvalue readout. Click: the eigenvalue signs decide bowl, trough or saddle; entry signs do not (the [2 -1; -1 2] and [1 2; 2 1] examples).
5. **Gramian ellipsoid in state space (controllability-gramian, observability-gramian).** Drag A (eigenvalues) and B or C for a two-state system. Move: the ellipsoid E(W_c) of states reachable with unit input energy and the ellipsoid of output energy from W_o; trajectories. Click: long axes are cheap-to-reach directions, and an unobservable or uncontrollable mode collapses an axis to zero length.
6. **Lyapunov function as a bowl (lyapunov-equation, lyapunov-function).** Choose A (Hurwitz) and Q with sliders; solve P; show V(x) = x'Px level ellipses with the trajectory crossing them inward. Move: P, level curves, dV/dt = -x'Qx. Click: every trajectory crosses the P-ellipses inward because dV/dt is the negative of a positive quadratic, and P is the accumulated energy integral of x'Qx.
7. **SVD as rotate-stretch-rotate (svd, matrix-norm).** Drag the entries of a 2 x 2 matrix A (or sigma_1, sigma_2 and two angles); the unit circle animates through V*, Sigma, U. Move: the circle, the ellipse, the singular vectors, and the condition number. Click: the semi-axes are the singular values, sigma_1 is the maximum gain ||A||_2, and a shear with eigenvalues 1,1 (A = [1 k; 0 1]) can have huge singular values.
8. **Balanced truncation (balanced-realization, hankel-singular-values, balanced-truncation).** Choose a stable system with several modes and drag the truncation order k. Move: Hankel singular values bar chart, Bode magnitude of full versus reduced model, error bound. Click: dropping states with small Hankel singular values barely changes the input-output response, while rescaling states changes the Gramians but not the singular values.

(Other good candidates: LQR weight sliders for Q and R showing closed-loop poles and cost for the double integrator with Pi = [sqrt3 1; 1 sqrt3]; the Riccati matrix running backward for the scalar example P(t) = gamma/(gamma+1-t).)
