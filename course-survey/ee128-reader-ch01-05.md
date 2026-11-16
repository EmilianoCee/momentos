# EE 128 text, chapters 1-5: concept notes

Source: Arcak and Poolla, "Linear Control Systems: Structure, Stability, Optimality" (version Feb 28, 2026). Book page = PDF page minus 8. Covered: PDF pages 9-110 (book pp. 1-102).
Not in this range (do not assume the book has taught them yet): observability, observers, output feedback, Lyapunov equations, SVD, Gram-Schmidt, optimal control. Chapter 6 (observers) starts at PDF page 111. The text refers forward to "Chapter 8, Section C" for BIBO = asymptotic stability under controllable and observable, and "Chapter 10" for the induced 2-norm = largest singular value.

## Chapter 1. Transfer Function and State Space Models

### 1.A Transfer function models (book A.1-A.6)
- **transfer-function-model**: an LTI input-output ODE has the exponential-in-exponential-out property: input e^{st} gives output H(s) e^{st}, so H(s) is a ratio of polynomials that turns the ODE into algebra.
  - notation: u input, y output, y^[k] = d^k y/dt^k, coefficients a_k, b_k real constants, n = order, m = numerator degree, s in C, H(s), a(s), b(s), delta = n - m relative degree.
  - formulas: ODE (1.1) `y^[n] + a_{n-1} y^[n-1] + ... + a_1 y' + a_0 y = b_m u^[m] + ... + b_1 u' + b_0 u`; `u = e^{st} => y = H(s) e^{st}`; `H(s) = (b_m s^m + ... + b_0)/(s^n + a_{n-1} s^{n-1} + ... + a_0) = b(s)/a(s)`. Formal replacement `d/dt -> s`, so `a(s) y = b(s) u` is shorthand for the ODE (Heaviside's operational calculus; the book does not use the Laplace transform for this, it solves ODEs with matrix exponentials instead).
  - conditions: valid when a(s) != 0 (s not a pole). It describes only the forced response; initial conditions are ignored. Poles = roots of a(s) (n of them). Zeros = roots of b(s). Complex poles and zeros come in conjugate pairs because coefficients are real. Proper: delta >= 0. Strictly proper: delta > 0. If s is a zero, forced response to e^{st} is 0.
  - examples used: `H(s) = (3s+9)/(s^2+4s+13)`: poles -2 +/- 3j, zero -3, delta = 1. 3-input 2-output MIMO ODE: `y1'' + 2y1' + 6y1 = u1'' + u2' - 3u3`, `y2' + 3y2 = 2u2 - u3'`.
  - picture: the system scales and shifts the rotating exponential input; poles are the exponents where the response blows up; zeros are exponents the system blocks.
  - pitfalls: linear means no u^2, y' u, tan y'; time-invariant means constant coefficients; transfer function says nothing about transients from initial conditions.

- **block-diagram**: interconnections of LTI systems become products, sums and inverses of transfer functions (matrices in the MIMO case, so order matters).
  - notation: H(s), G(s), p x m transfer function matrix for m inputs and p outputs, I identity.
  - formulas: cascade `u -> H -> v -> G -> y` gives `P = G(s) H(s)`; sum gives `G + H`; negative feedback `y = G (u - H y) => y = (I + G H)^{-1} G u`.
  - conditions: matrix products do not commute, keep the order the signals flow right to left.
  - examples used: Figure 1.1 cascade; Figure 1.2 cascade, sum, feedback (negative feedback with minus sign at summing junction).
  - picture: boxes in series multiply, boxes in parallel add, feedback loop closes with 1/(1+GH).
  - pitfalls: do not reorder matrix transfer functions.

- **frequency-response**: set s = j w and the transfer function gives gain and phase for a sinusoid; the second-order system shows a resonance peak that depends on damping.
  - notation: j = sqrt(-1), w (omega) rad/s, H(jw), |H(jw)|, arg H(jw), w0 natural frequency, zeta (damping ratio).
  - formulas: `u = e^{jwt} = cos(wt) + j sin(wt) => y = H(jw) e^{jwt}`. Second order: `a(s) = s^2 + 2 zeta w0 s + w0^2`, `b(s) = w0^2` so H(0) = 1, `H(jw) = 1 / ((jw/w0)^2 + 2 zeta (jw/w0) + 1)`. Plotted as `20 log10 |H(jw)|` versus w on a log axis (Figure 1.3, w0 = 1, zeta = 0.1, 0.2, 0.4, 0.7, 1.0, 1.5).
  - conditions: peak (resonance) exists for zeta in (0, 1/sqrt(2)); peak height grows as zeta decreases; peak near w0 (Exercise 1.3: peak frequency w* -> w0 as zeta -> 0). Changing w0 only stretches the frequency axis.
  - examples used: second-order system with unit DC gain; Exercise 1.2 system with `|H(jw)| ~ 1/w^2` at high frequency.
  - picture: a rotating phasor in, a scaled and rotated phasor out; magnitude curve with a bump that sharpens as damping shrinks.
  - pitfalls: low frequencies matter most (dominant slow dynamics); a model matching measured gain and phase there, resonance included, is regarded as adequate.

### 1.B State space models (book B.1-B.13)
- **state-space-model**: an nth-order ODE becomes n coupled first-order equations in a state vector; the state is exactly the information needed to predict future output given future input.
  - notation: x state (n), u input (m), y output (p), matrices `A in R^{n x n}, B in R^{n x m}, C in R^{p x n}, D in R^{p x m}`; packed as `Sigma = [A B; C D]`; D = feedthrough (throughput); dimension of a realization = n. Letters m, n, p are inputs, states, outputs.
  - formulas: `x' = A x + B u, y = C x + D u`. From transfer function: `s x = A x + B u => x = (sI - A)^{-1} B u`, `H(s) = C (sI - A)^{-1} B + D = C adj(sI - A) B / det(sI - A) + D`. Chosen states `x1 = y, x2 = y', x3 = y''` for `y''' + 3y'' + 4y' + 7y = u`.
  - conditions: poles of H(s) are a subset of eigenvalues of A (cancellations in C adj(sI-A) B can hide some); D != 0 iff relative degree 0, D = 0 gives delta >= 1. The "state" for a rigid body in 3-D has 12 dimensions.
  - examples used: `H = 1/(s^3 + 3s^2 + 4s + 7)`; point mass with force input (state = position, velocity); 3-D rigid body (12 states); MATLAB `ss`, `lsim`, `A = [0 1 0; 0 0 1; -2 -3 -4]`.
  - picture: the state is the memory of the system; pack n integrators with A wiring them.
  - pitfalls: transfer functions are numerically fragile for high order (multiplying rational functions, root-finding); state space uses stable linear algebra (eigenvalues, SVD). Adjugate is the transpose of the cofactor matrix, not the adjoint (conjugate transpose).

- **realization**: a state space model (A,B,C,D) with transfer function H(s) is a realization; they are not unique, and canonical forms give standard choices.
  - notation: `H(s) ~ [A B; C D]` ("realized by"), controllable canonical form, observable canonical form, dual realization `Sigma_dual = [A^T C^T; B^T D^T]`, T invertible, `x_new = T^{-1} x`.
  - formulas: controllable canonical form for `H(s) = (beta_{n-1} s^{n-1} + ... + beta_0)/(s^n + alpha_{n-1} s^{n-1} + ... + alpha_0) + d`: A has ones on the super-diagonal, bottom row `[-alpha_0 -alpha_1 ... -alpha_{n-1}]`; `B = [0 ... 0 1]^T`; `C = [beta_0 beta_1 ... beta_{n-1}]`; `D = d`. Example: `(3s^2 + 7s + 2)/(s^3 + 9s^2 + 4s + 5)` gives bottom row `[-5 -4 -9]`, `C = [2 7 3]`, D = 0 (use `q = u/a(s)`, states q, q', q''). Observable form = transpose (dual). Similarity: `A_new = T^{-1} A T, B_new = T^{-1} B, C_new = C T, D_new = D`, and `H_new(s) = H(s)`. Sum: `H1 + H2 ~ [A1 0 B1; 0 A2 B2; C1 C2 D1+D2]`. MIMO column stack `[H1; H2] ~ [A1 0 B1; 0 A2 B2; C1 0 D1; 0 C2 D2]`; row stack `[H1 H2] ~ [A1 0 B1 0; 0 A2 0 B2; C1 C2 D1 D2]`.
  - conditions: D = 0 and B is zero except bottom 1; the states of the numerator example are not y, y', y'' (the book asks the reader to work out what they are in terms of u and y and derivatives).
  - examples used: `1/(s^3 + 9s^2 + 4s + 5)`; `(3s^2 + 7s + 2)/(s^3 + 9s^2 + 4s + 5)`; MIMO examples.
  - picture: same input-output behavior, different coordinates for the state; a chain of integrators with coefficients fed back.
  - pitfalls: do not assume the realization is unique or that library routines (tf2ss) return the matrices you started with (Exercise 1.5b).

- **modal-form**: with distinct real poles, a transfer function is a sum of first-order pieces, giving a diagonal A.
  - notation: poles p_k, residues c_k, constant d.
  - formulas: `H(s) = d + sum_k c_k/(s - p_k) ~ [diag(p_1..p_n) 1; c_1..c_n d]` (B all ones). Repeated pole r times: `c/(s-p)^r ~` Jordan block with p on diagonal and ones on super-diagonal, `B = e_r (last)`, `C = [c 0 ... 0]`. Complex poles `-a +/- j w`: `H = (c1 (s+a) + c2 w)/((s+a)^2 + w^2) ~ [-a w 1; -w -a 0; c1 c2 0]`.
  - picture: parallel bank of first-order lags, one per pole.

- **ltv-systems**: allowing A,B,C,D to depend on time gives a linear time-varying model with no transfer function.
  - formulas: `x'(t) = A(t) x(t) + B(t) u(t), y = C(t) x + D(t) u`.
  - conditions: arises most commonly from linearizing about a trajectory (1.C.6).

- **discrete-time-systems**: difference equations give the same state space structure with x_{k+1} instead of x'.
  - notation: index k, `x_{k+1} = A_k x_k + B_k u_k, y_k = C_k x_k + D_k u_k`; LTI when matrices do not depend on k.
  - formulas: Fibonacci `y_{k+2} - y_{k+1} - y_k = 0, y_0 = 0, y_1 = 1` as `x_k = [y_{k+1}; y_k], A = [1 1; 1 0], x_0 = [1; 0], C = [0 1]`, giving y = 1, 1, 2, 3 ...
  - examples used: Fibonacci sequence; ARMA models in economics as intrinsically discrete.
  - pitfalls: discrete models arise either by discretizing a continuous system (method deferred to Exercise 4.11) or intrinsically.

### 1.C Nonlinear models (book C.1-C.6)
- **nonlinear-state-space**: general model `x' = f(x,u), y = h(x,u)` with vector-valued f and h; LTI is the special case f = Ax + Bu, h = Cx + Du.
  - notation: f_i, h_i scalar functions, `x = [x1..xn]^T, u, y`.
  - examples used: magnetically suspended ball (Figure 1.4): mass m = 0.15 kg, coupling c = 0.01 kg m^3/Coul^2, y = position measured downward from the magnet, `F_up = -c u^2/y^2`, `m y'' = m g - c u^2/y^2`; states `x1 = y, x2 = y'`, `x1' = x2`, `x2' = g - (1/15)(u/x1)^2`, g = 9.8, y = x1 (c/m = 1/15).

- **equilibrium**: an equilibrium is a pair (x_eq, u_eq) with f(x_eq,u_eq) = 0; the state stays put under constant input.
  - notation: `x^eq, u^eq, y^eq = h(x^eq, u^eq)`, xi = (x^eq, u^eq).
  - formulas: `f(x_eq,u_eq) = 0`. Ball: `x1_eq = beta, x2_eq = 0, u_eq = 12.12 beta` (free parameter y_eq = beta, from `u/x1 = sqrt(9.8*15)`).
  - conditions: uniqueness of solutions needs mild conditions such as continuously differentiable f; h plays no role in finding equilibria.
  - pitfalls: equilibria are pairs of state and input, not just states.

- **linearization**: Jacobian linearization replaces the nonlinear model by an LTI model for deviations from an equilibrium (or an LTV model along a trajectory).
  - notation: Jacobian `d phi/dx` is the m x n matrix of partials (row vector for scalar phi); evaluated at xi written `(d phi/dx)(xi)` (the book prints "@xi"); deviations `x~ = x - x_eq, u~ = u - u_eq, y~ = y - y_eq`.
  - formulas: Taylor `phi(x) = phi(xi) + (d phi/dx)(xi)(x - xi) + higher order`; `A = df/dx at xi, B = df/du at xi, C = dh/dx at xi, D = dh/du at xi`; `x~' = A x~ + B u~, y~ = C x~ + D u~`. Trajectory version: `x~ = x - x_nom(t)` etc., `A(t) = df/dx at xi(t)` and so on, giving an LTV system. Ball at y_eq = beta: `A = [0 1; 19.6/beta 0], B = [0; -1.61/beta... ]` (numbers printed garbled: with beta = 0.1 the exercise gives `A = [0 1; 195.9 0], B = [0; -16.1], C = [1 0], D = 0`).
  - conditions: good only while (x,u) stays close to the equilibrium, so x~, u~ near 0; guaranteed in control by designing u~ to keep deviations small.
  - examples used: ball (open-loop equilibrium unstable, local feedback stabilizes it); Jacobian example `phi = [x1 sin x2; x2^2 cos x3]` at (1, pi/2, 0); Exercises on predator-prey, mass-spring with geometric nonlinearity (bifurcation when spring natural length exceeds offset), satellite about circular orbit.
  - picture: tangent plane approximating a surface (Figure 1.5), valid near the touching point.
  - pitfalls: a linearization says nothing far from the equilibrium; LTI methods apply to the approximation only.

### 1 Perspectives
- Heaviside and operational calculus; book uses s as formal d/dt symbol, solves ODEs via matrix exponentials (Chapter 4), not Laplace transforms.

### 1 Exercises (one line)
Convert ODEs to transfer functions and state space and classify proper; transfer function from (A,B,C,D) and exponential responses and frequency response with simulation; resonance peak frequency; similarity invariance of H; MIMO conversion by computer (tf2ss, ss2tf); realization of a feedback block diagram; linearization of predator-prey, mass-spring, satellite.

## Chapter 2. Vector Spaces

### 2.A Algebraic aspects (A.1-A.5)
- **vector-space**: a set with addition and scalar multiplication obeying closure, commutativity, associativity, distributivity, zero and additive inverse; it abstracts R^3 and covers matrices, polynomials, sequences, functions.
  - notation: V, scalars F = R or C, `circ` for scalar multiplication (usually omitted).
  - examples used: R^n, C^n, R^{m x n}, R[s] polynomials, C[a,b] continuous functions, L_p[a,b] (integral of |f|^p finite), sequence space l_p.
  - picture: a matrix as a long vector by stacking its columns.
  - pitfalls: infinite dimensional spaces need a notion of convergence (needs a norm) to sum infinitely many vectors; only finite linear combinations are allowed.

- **basis-dimension**: independent vectors that span give unique coordinates; the dimension is the maximal number of independent vectors.
  - notation: `S = {v_i}`, `alpha_i`, standard basis `e_i`.
  - formulas: dependent iff a nontrivial finite combination `sum alpha_i v_i = 0`. Linear combination as matrix-vector product `[v1 v2 v3 v4] alpha`. Theorem 14: n independent vectors in an n-dimensional space form a basis. dim R^n = n, dim R^{m x n} = m n.
  - conditions: Basis means every vector is a unique finite combination.
  - examples used: v1 = (1,2,3), v2 = (2,4,6), v3 = (0,1,0), v4 = (1,0,1) in R^3; `(1,2),(2,3),(3,4)` in R^2 with `-v1 + 2 v2 - v3 = 0`; `{1, t, t^2, ...}` independent in C[0,1]. Bases are not unique (both 1 and -1 are bases of R).

- **subspace**: a subset closed under addition and scalar multiplication (so it contains 0): lines and planes through the origin in R^3.
  - notation: S, T, `Span{...}`, `S + T`, `S ∩ T`, `S ∪ T`.
  - formulas: Theorem 16 subspace iff closed; `S + T = {s + t}`; sum and intersection are subspaces, union is not.
  - picture: planes and lines through the origin (Figure 2.1).
  - pitfalls: union of two subspaces is not a subspace.

- **direct-sum**: when S1 + S2 = V and S1 ∩ S2 = {0}, every vector splits uniquely into a part in each.
  - notation: `V = S1 ⊕ S2`.
  - formulas: Theorem 20 unique decomposition `v = y1 + y2`.
  - examples used: even and odd polynomials in P_N (Exercise 2.3).

### 2.B Geometric aspects (B.1-B.11)
- **norm**: a norm is a length function with non-negativity, scaling and triangle inequality; the only nontrivial axiom is the triangle inequality.
  - notation: `||v||`, `||v||_1, ||v||_2, ||v||_inf`, Frobenius `||M||_F = (sum |m_ij|^2)^{1/2} = [trace(M* M)]^{1/2}`, induced p-norm.
  - formulas: `||v||_1 = sum |v_i|`, `||v||_2 = (sum |v_i|^2)^{1/2} = sqrt(v* v)`, `||v||_inf = max |v_i|`; induced norm `||M||_p = sup_{x != 0} ||M x||_p / ||x||_p` (= max over ||x||_p = 1, largest amplification); function and sequence norms for L_p and l_p; for all x in C^n: `||x||_inf <= ||x||_1 <= n ||x||_inf` and `||x||_1 <= sqrt(n) ||x||_2` (the conversion also shows `||x||_2` in the chain; these are the printed relations). Induced 1-norm = max absolute column sum; induced inf-norm = max absolute row sum; the induced 2-norm will be the largest singular value (Chapter 10).
  - conditions: in finite dimensions all norms are equivalent (Definition 25: `m <= ||v||_a / ||v||_b <= M`); not true in infinite dimensions.
  - picture: unit-norm balls in the plane (diamond, circle, square for p = 1, 2, inf; Exercise 2.4).
  - pitfalls: "norm ball" is used for p != 2 even though not round.

- **inner-product**: a pairing giving angles and perpendicularity; it induces a norm.
  - notation: `<v, w>`, `v* w`, adjoint `*` = conjugate transpose; "linear in the second argument, conjugate-linear in the first".
  - formulas: axioms `<v,w> = conj(<w,v>)`, `<v, alpha w> = alpha <v,w>`, additive, `<v,v> >= 0` with equality iff v = 0; `<v,w> = ||v|| ||w|| cos(theta)`; on R^n `v^T w`; on C^n `v* w`; on R^{m x n} `trace(A^T B)`; on l_2 `sum conj(v_k) w_k`; on L_2 `integral f g dt`. Cauchy-Schwarz `|<v,w>| <= ||v|| ||w||` (Theorem 28). Induced norm `||v|| = <v,v>^{1/2}`. Parallelogram law (Exercise 2.7).
  - conditions: Figure 2.3 nesting: inner-product spaces inside normed spaces inside vector spaces.
  - pitfalls: convention for which argument is conjugated (second argument linear here).

- **orthogonality**: v perpendicular to w iff `<v,w> = 0`; Pythagoras holds.
  - notation: `v ⊥ w`, `v ⊥ S`, orthonormal sets (norm 1 each).
  - formulas: Pythagoras `v ⊥ w => ||v + w||^2 = ||v||^2 + ||w||^2`.

- **projection**: the closest point in a subspace to v is the projection, and the error is perpendicular to the subspace.
  - notation: s-hat, S = Span{b_1..b_m}, Gram matrix `G_ij = <b_i, b_j>`.
  - formulas: one unit vector b: `s-hat = <b,v> b`, `v - s-hat ⊥ S`. Projection Theorem: `argmin_{s in S} ||v - s||` has unique solution `s-hat = alpha_1 b_1 + ... + alpha_m b_m` with `G alpha = [<b_1,v>; ...; <b_m,v>]` (G invertible when the b_i are independent; Exercise 2.10). In C^n with `B = [b_1 ... b_m]`: `s-hat = B (B* B)^{-1} B* v`; if orthonormal, `B* B = I` and the projector is `B B*`.
  - conditions: b_i linearly independent.
  - picture: v dropping a perpendicular onto a line or plane through the origin (Figures 2.4, 2.5).

- **least-squares**: the formula B(B*B)^{-1}B* v is called the least squares approximation of v in the subspace.
  - formulas: later exercises (3.3, 3.4): tall full-column-rank A, minimize ||Ax - b|| by projecting b onto R(A); fat full-row-rank A, minimum-norm solution `x-hat = A*(AA*)^{-1} b`; system identification of `x_{k+1} = alpha x_k + beta u_k` by stacking data (Exercise 3.5).

- **orthogonal-complement**: S-perp is all vectors perpendicular to S; for finite-dimensional S, V = S ⊕ S-perp and (S-perp)-perp = S.
  - notation: `S^⊥`.
  - formulas: Lemma 35: S-perp is a subspace, `S ∩ S^⊥ = {0}`, `S ⊂ T => T^⊥ ⊂ S^⊥`. Lemma 36: `V = S ⊕ S^⊥`, `(S^⊥)^⊥ = S`. Exercise 2.11: `(S ∩ T)^⊥ = S^⊥ + T^⊥`.
  - picture: a plane and its normal line in R^3 (Figure 2.6).

- **completeness**: a normed space is complete when every Cauchy sequence converges, which tests convergence without knowing the limit.
  - notation: Cauchy sequence `||v_m - v_n|| -> 0`, Banach space (complete normed), Hilbert space (complete inner product).
  - conditions: all finite-dimensional spaces are complete; polynomials P[0,1] are not complete (partial sums of e^t are Cauchy under max norm but the limit is not a polynomial).

### 2 Exercises (one line)
Basis for matrices; subspaces and sum/intersection/union; direct sum of even/odd polynomials; unit-norm balls; norm equivalence; induced 1- and inf-norm as column and row sums; parallelogram law; complexifying a real inner product; orthogonal polynomials on [-1,1] with `<f,g> = integral f g`; Gram matrix invertibility; orthogonal complement of an intersection.

## Chapter 3. Linear Operators and Matrix Representations

### 3.A Linear operators (A.1-A.3)
- **linear-operator**: a map between vector spaces preserving addition and scaling.
  - notation: `L: V -> W` (script L), additivity `L(v1 + v2) = L(v1) + L(v2)`, homogeneity `L(alpha v) = alpha L(v)`.
  - examples used (linear): `L(x) = Ax`; evaluation `f -> f(0)` on C(-inf,inf); differentiation `P_N -> P_{N-1}`; Sylvester operator `L(X) = A X + X B` on R^{n x n}. Not linear: `L(x) = A x + b` with b != 0; `L(X) = X A X + X`.
  - pitfalls: affine maps (with an offset) are not linear.

- **matrix-representation**: once bases are fixed, a linear operator acts as matrix-vector multiplication on coordinate vectors; the matrix depends on the chosen bases.
  - notation: bases `{v_j}` for V, `{w_i}` for W, matrix `A = [a_ij]`.
  - formulas: `L(v_j) = sum_i a_ij w_i` (column j = coordinates of the image of the j-th basis vector); for `v = sum alpha_j v_j`, `L(v) = sum beta_i w_i` with `beta = A alpha` (3.1).
  - examples used: rotation by theta counterclockwise on R^2 with standard basis: `A = [cos t, -sin t; sin t, cos t]`; differentiation on polynomials with bases `{1, t, ..., t^N}` and `{1, ..., t^{N-1}}`: `N x (N+1)` matrix with `1, 2, ..., N` on the shifted diagonal giving `beta_i = i alpha_{i+1}`.
  - picture: columns of A are where the basis vectors land.
  - pitfalls: the same operator looks different in different bases; a matrix is a representation, not just an array.

### 3.B Range and null spaces (B.1-B.3)
- **range-nullspace**: R(A) is the set of all Ax (column span), N(A) the set with Ax = 0; the four fundamental subspaces pair up orthogonally.
  - notation: `R(L)`, `N(L)`, adjoint `A* = conj(A)^T` (just A^T for real A).
  - formulas: Theorem 45: `R(A)^⊥ = N(A*)`; `C^m = R(A) ⊕ N(A*)`; `N(A* A) = N(A)`; `R(A A*) = R(A)`; applying to A*: `C^n = R(A*) ⊕ N(A)`.
  - examples used: `A = [1 1; 1 1; 1 1]` (3 x 2): Figure 3.1 shows R(A) a line in R^3 and N(A*) its orthogonal plane, then R(A*) a line in R^2 and N(A) its orthogonal complement.
  - picture: domain splits into row space plus null space, codomain into column space plus left null space, all at right angles.

- **rank-nullity**: rank plus nullity equals the number of columns.
  - notation: rank(A) = dim R(A), nullity(A) = dim N(A).
  - formulas: `rank(A) + nullity(A) = n` (Theorem 48, A in C^{m x n}); `rank(A) = rank(A*)`; `rank(A) <= min{m, n}`.

- **linear-equations**: Ax = b is solvable iff b is in R(A); the solution is unique iff N(A) = {0}; a unique solution for every b iff rank(A) = m = n.
  - formulas: Theorem 51; invertible iff rank = n iff det(A) != 0; solutions differ by elements of N(A); x = A^{-1} b depends linearly on b.
  - conditions: invertibility is only for square matrices.

### 3.C Eigenvalues and eigenvectors (C.1-C.3)
- **eigenvalues-eigenvectors**: an eigenvector is a direction that A only stretches; eigenvalues are roots of the characteristic polynomial.
  - notation: `chi_A(s) = det(sI - A) = s^n + alpha_{n-1} s^{n-1} + ... + alpha_1 s + alpha_0` (note: the book's coefficient index here runs alpha_0..alpha_{n-1}, with the text sometimes writing alpha_n-1); `Spec(A)` spectrum with multiplicity; `Av = lambda v`.
  - formulas: eigenvalue iff `det(lambda I - A) = 0` iff `(lambda I - A) v = 0` has v != 0. `det(A) = lambda_1 ... lambda_n`, `Tr(A) = lambda_1 + ... + lambda_n` (derived from Jordan form being upper triangular, and similarity invariance of det and trace). Exercise 3.7 similar matrices share eigenvalues; 3.8 block diagonal spectrum is union; 3.9 `[A1 A2; A2 A1]` has spectrum `Spec(A1+A2) ∪ Spec(A1-A2)`.
  - conditions: "simple" = distinct eigenvalues; "semi-simple" = n linearly independent eigenvectors (simple implies semi-simple, not conversely).
  - examples used: `A = [2 -3; 1 -2]` eigenvalues 1 and -1, eigenvectors `[3;1]` and `[1;1]`; `[0 sigma; sigma 0]` (Exercise 3.6).

- **diagonalization**: for a simple matrix the eigenvectors form a basis, and in that basis the operator is diagonal.
  - notation: `T = [v_1 ... v_n]`, `Lambda = diag(lambda_i)`.
  - formulas: `T^{-1} A T = Lambda`; Example 57: `T = [3 1; 1 1]`, `T^{-1} A T = diag(1, -1)`.
  - conditions: needs n independent eigenvectors (distinct eigenvalues suffice); order of eigenvalues in Lambda matches order of columns of T.
  - picture: T^{-1} A T is the same operator written in the eigenvector basis.

- **jordan-form**: any square matrix is similar to a block-diagonal matrix of Jordan blocks with eigenvalues on the diagonal and ones on the super-diagonal in places.
  - notation: blocks J_l for eigenvalue lambda_l with multiplicity m_l; sub-blocks `J_{i,l}` with lambda on diagonal and 1 on super-diagonal.
  - conditions: semi-simple iff Jordan form diagonal; book deemphasizes it for numerical reasons and points to Schur forms later.
  - examples used: `A_eps = [1+eps 1; 0 1]` has Jordan form `diag(1+eps, 1)` for eps != 0 but `[1 1; 0 1]` at eps = 0.
  - pitfalls: Jordan form is not a continuous function of the entries, hence numerically unstable.

### 3.D Functions of a square matrix (D.1-D.5)
- **functions-of-a-matrix**: reuse a scalar power series with matrix argument; the result is computed by applying f to the eigenvalues.
  - notation: `f(A) = sum alpha_i A^i`, `A^0 = I`, `p(A)`.
  - formulas: Lemma 60: `f(A) g(A) = g(A) f(A)`; `f(T^{-1} A T) = T^{-1} f(A) T`; `f(diag(A,B)) = diag(f(A), f(B))`. For simple A: `f(A) = T diag(f(lambda_i)) T^{-1}`. Spectral Mapping Theorem (61): `(lambda, v)` eigenpair of A gives `(f(lambda), v)` for f(A).
  - conditions: power series must converge on Spec(A) (valid for non-diagonalizable A via Jordan form).
  - pitfalls: determinant is not a power-series function.

- **cayley-hamilton**: every matrix satisfies its own characteristic polynomial, so A^n is a combination of I, A, ..., A^{n-1}.
  - formulas: `chi_A(A) = A^n + alpha_{n-1} A^{n-1} + ... + alpha_0 I = 0` (Theorem 62; proof in Appendix C). Exercise 3.11: diagonal case `prod (lambda_i I - A) = 0`; any polynomial of A reduces to degree <= n-1. Exercise 3.12 minimal polynomial (e.g. `A = [1 1 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 2]`).
  - picture: used repeatedly to cap the powers of A to those below n (controllability matrix, relative degree).

- **matrix-exponential**: `e^A = I + A + A^2/2! + A^3/3! + ...` is defined for every square matrix and is the solution operator of x' = Ax.
  - notation: `e^{At}`, `expm` (versus entrywise `exp`), nilpotent (`A^k = 0`).
  - formulas: Theorem 63: `e^0 = I`; `A e^A = e^A A`; `det(e^A) = e^{Tr A}`; `AB = BA => e^{A+B} = e^A e^B = e^B e^A`; `e^A` invertible with inverse `e^{-A}`. Simple case `e^{At} = T e^{Lambda t} T^{-1}`, `e^{Lambda t} = diag(e^{lambda_i t})`. Example 64: with `A = [2 -3; 1 -2]`, `e^{At} = [1.5 e^t - 0.5 e^{-t}, -1.5 e^t + 1.5 e^{-t}; 0.5 e^t - 0.5 e^{-t}, -0.5 e^t + 1.5 e^{-t}]`. Exercises: `e^{(sigma I + A0) t} = e^{sigma t} e^{A0 t}`; `A = [sigma omega; -omega sigma]` has rotation-scaling form; Jordan block gives `e^{lambda t}, t e^{lambda t}, t^2 e^{lambda t}/2` in upper-triangular Toeplitz form.
  - conditions: `e^{A+B} = e^A e^B` needs AB = BA (Exercise 3.14 counterexample `A = [0 1; 0 0]`, `B = [0 0; 1 0]`).
  - pitfalls: eigen-decomposition is analytically instructive but not a reliable numerical method; MATLAB `expm` uses scaling and squaring.

### 3 Exercises (one line)
Range and null space subspaces; rank of products; minimum-norm and least-squares solutions; system identification by least squares; eigenvalue problems (symmetric 2x2, block matrices, similarity, nilpotent); characteristic and minimal polynomials; verifying matrix function properties; non-commuting exponentials; shifted matrices; complex-eigenvalue and Jordan-block exponentials; relative degree and Markov parameters (`D, CB, CAB, ...`; relative degree is the number of differentiations of y before u appears, and `C A^k B` is similarity invariant).

## Chapter 4. Trajectories and Stability of Linear Systems

### 4.A Solution of state space equations (A.1-A.3)
- **solution-of-state-equations**: the state is the free response from the initial state plus a convolution of the input with e^{A(t - tau)}.
  - notation: `x(0) = xi`, `y_free`, `y_forced`, impulse response `h(t) = C e^{At} B`, `tau` integration variable.
  - formulas: `x(t) = e^{At} xi + integral_0^t e^{A(t-tau)} B u(tau) d tau` (4.1); `y(t) = C e^{At} xi + integral_0^t C e^{A(t-tau)} B u(tau) d tau + D u(t)`; free response `C e^{At} xi` (4.2); forced response `integral ... + D u(t)` (4.3). Discrete: `x_k = A^k xi + sum_{l=0}^{k-1} A^l B u_{k-1-l}`, `y_k = C A^k xi + sum_{l=0}^{k-1} C A^l B u_{k-1-l} + D u_k`; stacked lower-triangular block Toeplitz matrix with entries `C A^{k-1} B ... C B, D`.
  - conditions: u bounded on every finite interval; uniqueness from continuously differentiable f (Lipschitz is enough, omitted).
  - picture: free part is a flow from the initial state; forced part is a superposition of past inputs each propagated forward by e^{A(t - tau)}.
  - pitfalls: D term is the immediate effect of u on y; D = 0 means no instantaneous response.

- **modes**: the free response is a combination of e^{lambda t} (or lambda^k) for each eigenvalue, and the eigenvalue position in the plane decides growth, decay and oscillation.
  - notation: lambda = sigma + j omega, Figure 4.1 (real part of e^{lambda t} across the complex plane), Figure 4.2 (real part of lambda^k).
  - formulas: continuous: `e^{lambda t} = e^{sigma t} [cos(omega t) + j sin(omega t)]`; real lambda gives monotone, no oscillation, decay if lambda < 0, growth if > 0, constant at 0; complex gives oscillation, frequency increases with omega = Imag(lambda), decay iff sigma < 0, pure sinusoid at sigma = 0. Non-semisimple: terms `e^{lambda t}, t e^{lambda t}, ..., t^{q-1} e^{lambda t}`, q = largest Jordan block for that eigenvalue; `e^{Jt}` upper triangular with `t^k/k! e^{lambda t}` on the k-th super-diagonal. Discrete: `lambda = |lambda| e^{j theta}`, `lambda^k = |lambda|^k e^{j theta k}`; growth if |lambda| > 1, decay if < 1, constant amplitude if = 1.
  - examples used: grids of eigenvalue locations in the complex plane.
  - picture: left half-plane = decay, right = growth, vertical position = oscillation rate; in discrete time the unit circle replaces the imaginary axis and the angle gives the oscillation rate.

### 4.B LTV systems
- **state-transition-matrix**: for x' = A(t) x there is no closed form in general, but the solution is x(t) = Phi(t, t0) xi where Phi holds the solutions from the n standard basis initial conditions.
  - notation: `Phi(t, t0)`, columns `phi_i(t, t0)`, e_i.
  - formulas: `d/dt Phi(t,t0) = A(t) Phi(t,t0), Phi(t0,t0) = I` (4.4); `x(t) = Phi(t,t0) xi`; forced LTV: `x(t) = Phi(t,t0) xi + integral_{t0}^t Phi(t,s) B(s) u(s) ds`. LTI: `Phi(t,t0) = e^{A(t - t0)}`. Exercise 4.2: `Phi(t2,t1) Phi(t1,t0) = Phi(t2,t0)`, `Phi^{-1}(t,t0) = Phi(t0,t)`; 4.3 shifted: `Phi = e^{sigma(t - t0)} Phi_0(t,t0)`.
  - conditions: not an explicit solution, only a characterization; compute n solutions numerically then reuse.
  - picture: Phi is the map that carries any starting state to where it ends up at time t.

### 4.C Stability (C.1-C.3)
- **internal-stability** (asymptotic stability): the free response goes to zero from every initial condition iff all eigenvalues of A have negative real part (continuous time) or magnitude below 1 (discrete time).
  - notation: system written `(A, *, *, *)` (stars for matrices that do not matter), "Hurwitz" matrix.
  - formulas: Definition 66: `lim_{t->inf} x(t) = 0` for `x' = Ax, x(0) = xi`. Theorem 67: asymptotically stable iff `Real(lambda) < 0` for all lambda in Spec(A). Discrete: `x_{k+1} = A x_k`, `x_k = A^k xi`, stable iff `|lambda| < 1` for all lambda in Spec(A). Marginal stability (Exercise 4.4): state bounded from all initial conditions iff eigenvalues have nonpositive real part and any with real part 0 have Jordan blocks of size 1.
  - conditions: LTV may have uniform asymptotic stability (convergence uniform in t0); for LTI the initial time is immaterial. Proof "only if": start at an eigenvector (complex: use v + conj(v)).
  - examples used: Exercise 4.5 matrices `[0 1;-1 0]`, `[0 1;0 0]`, `[-1 -1;1 -1]`, `[0 0;0 0]`; Bloch equation (precession time T2, longitudinal T1); ring oscillator `tau x_i' = -x_i + h(x_{i-1})` with `h(x) = -alpha tanh(beta x)` and critical mu = alpha beta (limit cycle when linearization is unstable but nonlinearity saturates).
  - pitfalls: zero real part with a Jordan block of size >= 2 grows (polynomially); linearization instability does not mean unbounded growth in the nonlinear model (limit cycle).

- **bibo-stability**: every bounded input gives a bounded output; for LTI this follows from asymptotic stability but not the converse.
  - notation: bound K_u, `||u(t)|| <= K_u < inf`, `h(t) = C e^{At} B`.
  - formulas: Theorem 70: asymptotically stable implies BIBO; proof bounds the output by `K_u integral_0^inf ||h(s)|| ds` plus the D term, finite because terms `t^k e^{lambda t}` are absolutely integrable when Real(lambda) < 0.
  - examples used: `A = [1 0; 0 -1], B = [0; 1], C = [0 1]`: eigenvalue +1 (unstable) but `h(t) = e^{-t}` so BIBO stable (unstable mode neither reached by B nor seen by C).
  - conditions: BIBO implies asymptotic stability for controllable and observable systems (Chapter 8, Section C, not yet covered). Example: `sin(t)` is bounded, `t` is not.
  - pitfalls: BIBO only looks at the part of the state that connects input to output.

- **ltv-stability-pitfall**: for time-varying A(t), negative real parts of the frozen eigenvalues at every t do not imply stability.
  - notation: Mathieu equation `y'' + 2 mu y' + (w0^2 + epsilon cos 2t) y = 0`, states `x1 = y, x2 = y'`, `A(t) = [0 1; -(w0^2 + eps cos 2t), -2 mu]`, period pi.
  - formulas: undamped (mu = 0) unstable at w0 = 1, 2, 3, ... for eps != 0; damped at w0 = 1 unstable if `eps > 2 mu`; frozen characteristic polynomial `s^2 + 2 mu s + (w0^2 + eps cos 2t)` has positive coefficients for eps < 1, mu > 0, so roots always in the left half-plane yet system unstable for `mu in (0, eps/2)`. Periodic case test: `Phi(k pi, 0) = Phi(pi,0)^k`, unstable if `Phi(pi,0)` has eigenvalues outside the unit circle.
  - picture: parametric resonance: modulating a parameter at frequency ratio 2 : n to the natural frequency feeds energy at the right phase so amplitude grows.
  - pitfalls: not the same as ordinary resonance, which needs an external forcing term.

- **discretization** (Exercises 4.11 and 4.12, not in the body text): sampled with zero-order hold at period T gives `x_{k+1} = A_bar x_k + B_bar u_k`.
  - notation: `A_bar, B_bar, C_bar, D_bar`, sampling period T, `x_k = x(kT)`, zero-order hold `u(t) = u_k` on `[kT, (k+1)T)`.
  - formulas: derive from the variation-of-constants formula over one interval; Euler approximation `x_{k+1} = x_k + T f(x_k, u_k)`, giving `A_hat = I + T A`, `B_hat = T B` for LTI; double-integrator example `A = [0 1; 0 0], B = [0; 1]`.
  - conditions asked: relation of eigenvalues of A and A_bar, and whether stable A guarantees A_bar inside the unit circle (open question posed in exercises).

### 4 Exercises (one line)
State-transition matrix properties; shifted A(t); marginal stability and stability classification; norm-preserving dynamics; Bloch equation; ring oscillator linearization and limit cycle simulation; discrete-time stability proofs; BIBO in discrete time; zero-order-hold and Euler discretization.

## Chapter 5. State Feedback Control

### 5.A State feedback and controllability (A.1-A.10)
- **state-feedback**: measure the full state and feed back u = L x + v so the closed-loop matrix becomes A + B L, whose eigenvalues we try to place.
  - notation: L in R^{m x n} (gain; the book calls it L, not K), v new input (for feedforward, not considered yet), `A_cl = A + B L`, Figure 5.1.
  - formulas: `u = L x + v` (PLUS sign); closed loop `x' = (A + B L) x + B v`, `y = C x + D u`. Behavior is governed by eigenvalues of `A + B L`.
  - conditions: needs the whole state measured.
  - examples used: magnetically suspended ball linearization `A = [0 1; 195.9 0], B = [0; -16.1], C = [1 0]` at `(x1_eq, x2_eq, u_eq) = (0.1, 0, 1.212)` (Exercise 5.2); cruise control `m v' = -(1/2) rho a c v^2 + u/R` with m = 1700 kg, R = 0.3 m, a = 2.6 m^2, rho = 1.2 kg/m^3, c = 0.2, v_eq = 29 m/s, linearized `v~' = lambda v~ + beta u~`, proportional `u~ = L v~` targeting tau_cl = 5 s; adaptive cruise control `h' = v_L - v`... (headway `h' = v_L - v` presumably; the minus sign is detached in the conversion so the order is ambiguous; with `v' = -alpha v^2 + beta u`, v_L = 29 m/s, h_eq = 58 m, alpha = 1.84e-4, beta = 1.96e-3); mixing tank with cold and hot supplies, `T_C = 10`, `T_H = 90`, alpha = 3 m^2, beta = 0.155, h* = 1 m, T* = 25 degrees C; quadcopter with one propeller lost (state: roll rate, pitch rate, two axis components).
  - pitfalls: placing poles far left needs large control effort and can produce nonphysical behavior in the nonlinear model (negative flows, h <= 0).

- **eigenvalue-placement** (pole placement in controllable canonical form): with the controllable canonical pair (A_c, b_c), each entry of L sets one coefficient of the characteristic polynomial.
  - notation: `A_c, b_c`, alpha_i open-loop coefficients, gamma_i desired coefficients, poles p_i, `L_c = [l_0 l_1 ... l_{n-1}]`.
  - formulas: `det(sI - A_c) = s^n + alpha_{n-1} s^{n-1} + ... + alpha_0`. With `L = [l_0 ... l_{n-1}]`, `A_c + b_c L` keeps the canonical structure with bottom row `[-alpha_0 + l_0, ..., -alpha_{n-1} + l_{n-1}]`, char poly `s^n + (alpha_{n-1} - l_{n-1}) s^{n-1} + ... + (alpha_0 - l_0)`. Desired `(s - p_1)...(s - p_n) = s^n + gamma_{n-1} s^{n-1} + ... + gamma_0`. Choose `L_c = [(alpha_0 - gamma_0)  (alpha_1 - gamma_1) ... (alpha_{n-1} - gamma_{n-1})]`. (Note the book's text prints the char poly with minus signs in front of l's but the gain sign convention is A + bL; the result `L_c = alpha - gamma` is consistent.)
  - conditions: single input.
  - picture: the bottom row is a dial for each polynomial coefficient.

- **controllability**: the system is controllable iff the controllability matrix has rank n.
  - notation: `M = [B  AB  A^2 B ... A^{n-1} B]` (n x nm), controllability matrix; written `(A, B, *, *)`.
  - formulas: Definition 73: controllable iff `rank M = n`. Single input: M square, invertible. For canonical form M_c is anti-triangular with ones on the anti-diagonal. Does not depend on C, D.
  - conditions: rank test only (formal definition and other interpretations come later).
  - examples used: `A = [lambda_1 1; 0 lambda_2], b = [1; 0]`, `M = [1 lambda_1; 0 0]` rank 1: l can move lambda_1 (to `lambda_1 + l_1`) but lambda_2 is fixed because `A + bL = [lambda_1 + l_1, 1 + l_2; 0, lambda_2]`. Example 76: `A = [1 0; 0 a], b = [1; 1]`, controllable iff a != 1, `M = [1 1; 1 a]`.
  - picture: B pushes along columns of M; if columns of M fail to span R^n some direction is unreachable and its eigenvalue stays put.

- **canonical-form-transformation**: any controllable single-input pair can be brought to controllable canonical form by a similarity transformation built from the two controllability matrices.
  - formulas: Theorem 74: `A_c = T^{-1} A T, b_c = T^{-1} b` with `T = M M_c^{-1}`. Proof ideas: Cayley-Hamilton gives `A M = M Q` where Q is companion matrix with `-alpha` last column and ones below the diagonal, `A_c M_c = M_c Q`, and `M e_1 = b`.
  - picture: the controllability columns b, Ab, ..., A^{n-1}b form a basis in which A is a companion matrix.

- **single-input-pole-placement**: for controllable (A, b), L is found either through the canonical form or by matching coefficients directly.
  - formulas: Theorem 75: `L = L_c T^{-1}`, `T = M M_c^{-1}`, `L_c` as above, then `u = L x + v` gives desired characteristic polynomial. Direct method: write `A + bL` with unknown `l_1..l_n`, match coefficients of characteristic polynomial to desired, solve n equations; controllability guarantees solvability. Example 76 target poles -2, -3: `s^2 + 5s + 6`; characteristic polynomial `s^2 - (a + 1 + l_1 + l_2) s + (a + a l_1 + l_2)`; equations `a + 1 + l_1 + l_2 = -5`, `a + a l_1 + l_2 = 6`; the book solves `[1 1; a 1][l_1; l_2] = [-6 - a; 6 - a]` by inverting (final closed form is garbled in the conversion; solve it directly if needed).
  - conditions: controllable; direct method often avoids the detour of canonical form.

- **multi-input-pole-placement**: Heymann's Lemma reduces multi-input to single input by a preliminary feedback.
  - formulas: Lemma 77 (Heymann): for controllable (A,B) and `v in R^m` with `b = B v != 0`, there is `L_0 in R^{m x n}` with `(A + B L_0, b)` controllable (proof in Appendix D). Theorem 78: arbitrary eigenvalue assignment by `L = L_0 + v L_1` where `L_1` places poles for `(A + B L_0, b)`.
  - conditions: controllable (A,B).

- **pole-placement-software**: MATLAB `place` assigns eigenvalues of A - B K, so the book's convention requires passing -B.
  - formulas: `L = place(A, -B, poles)` gives `eig(A + B L) = poles`; or pass B and apply `u = -K x`.
  - pitfalls: `place` needs distinct poles (separate repeated poles slightly, e.g. -1, -1.000001, -1.0000002).

- **discrete-time-state-feedback**: same structure `A + B L` and same controllability condition, but eigenvalues must be placed inside the unit circle.
  - examples used: deadbeat (Exercise 5.7): `x_{k+1} = [1 1; 0 1] x_k + [0; 1] u_k`, place both eigenvalues at 0 so `A_cl^2 = 0` and `A_cl^n = 0` for n-th order, finite-time convergence; impossible with linear feedback in continuous time since e^{A_cl t} is never zero; requires large gains and is sensitive to noise and modeling error. Scalar integrator `x' = u` with sampling (Exercise 5.6): feedback `u = -gamma x` stabilizes continuous time for all gamma > 0 but the sampled version only for a limited range of gamma depending on T.
  - pitfalls: a continuous-time design implemented with sampling can destabilize if the sampling is slow.

### 5.B Kalman decomposition (B.1-B.4)
- **kalman-decomposition**: change coordinates to the range of the controllability matrix and the system splits into a controllable part and an uncontrollable part that evolves on its own.
  - notation: r = rank M, basis `t_1..t_r` of R(M) extended by `t_{r+1}..t_n`, `T = [t_1 ... t_r t_{r+1} ... t_n]`, `x_new = T^{-1} x`, blocks `A_11, A_12, A_22, B_1, C_1, C_2`.
  - formulas: Theorem 79: `A_new = T^{-1} A T = [A_11 A_12; 0 A_22]`, `B_new = T^{-1} B = [B_1; 0]`, `C_new = C T = [C_1 C_2]`, D unchanged; `(A_11, B_1, C_1, D)` is controllable and realizes the same H(s). Reduced `M_reduced = [B_1 A_11 B_1 ... A_11^{r-1} B_1]` has rank r. Proof: Cayley-Hamilton implies R(AM) is in R(M), so R(M) is A-invariant (zero block bottom-left); columns of B lie in R(M) (zero bottom of B).
  - conditions: not unique, depends on basis choice; structure is the same.
  - picture: Figure 5.2, input drives the controllable block, the uncontrollable block runs autonomously.
  - pitfalls: eigenvalues of A_22 do not appear among the poles of H(s) (explains pole-zero cancellation from Chapter 1).

- **controllability-eigenvalue-placement-iff** (necessity): uncontrollable eigenvalues can never be moved by state feedback.
  - formulas: `A_cl = T [A_11 + B_1 L_1, A_12 + B_1 L_2; 0, A_22] T^{-1}` where `L T = [L_1 L_2]`; eigenvalues of `A_cl` = eigenvalues of `A_11 + B_1 L_1` (freely assignable) together with eigenvalues of A_22 (fixed). Theorem 80: (A,B) controllable iff closed-loop eigenvalues can be assigned arbitrarily by state feedback.

- **stabilizability**: a system is stabilizable if some L makes A + BL stable, i.e. its uncontrollable eigenvalues are already stable.
  - notation: Definition 81 "stable" meaning negative real part (continuous time).
  - conditions: controllable implies stabilizable, not conversely.

### 5 Perspectives
Examples of control in daily life (flight control, cruise control, Boeing 737 MAX MCAS failure from faulty sensor, smartphone accelerometer as feedback, SpaceX landing); active control allows unstable designs for agility; Maynard Smith on unstable body plans in flying animals.

### 5 Exercises (one line)
Controllability of quadcopter with one propeller lost; stabilizing the magnetic ball (controllability, design, nonlinear simulation); cruise control and adaptive cruise control (equilibrium, linearize, design); mixing tank (linearize, controllable, pole placement, nonphysical behavior with fast poles); discretize versus not (integrator with zero-order hold); deadbeat control.

## Notation and conventions for these chapters

| symbol | meaning | convention |
|---|---|---|
| `x', x-dot` | time derivative | Continuous-time written `x'(t)` as `x-dot(t)`; formal `d/dt -> s` (Heaviside), not Laplace transform |
| `x_{k+1} = A x_k + B u_k` | discrete-time model | subscript k index; `y_k = C x_k + D u_k`; `x_k = A^k xi`; no z-transform in this range |
| `Sigma = [A B; C D]` | state space realization packed | `H(s) ~ [A B; C D]`; `H(s) = C (sI - A)^{-1} B + D` |
| n, m, p | numbers of states, inputs, outputs | `A in R^{n x n}, B in R^{n x m}, C in R^{p x n}, D in R^{p x m}` |
| `u = L x + v` | state feedback law | PLUS sign; gain is L (not K); `A_cl = A + B L`; MATLAB `place(A,-B,poles)` |
| `M = [B AB ... A^{n-1} B]` | controllability matrix | n x nm; controllable iff rank n; cols stacked horizontally; independent of C, D |
| `T = M M_c^{-1}` | transformation to controllable canonical form | `x_new = T^{-1} x`, `A_new = T^{-1} A T`, `B_new = T^{-1} B`, `C_new = C T` |
| controllable canonical form | companion form | ones on super-diagonal, bottom row `[-alpha_0 ... -alpha_{n-1}]`, `b = [0 ... 0 1]^T`, `C = [beta_0 ... beta_{n-1}]` (numerator coefficients in ascending order) |
| `chi_A(s)` | characteristic polynomial | `det(sI - A) = s^n + alpha_{n-1} s^{n-1} + ... + alpha_0` (monic; `a_k` in the I/O ODE, `alpha_k` for char poly) |
| `*` | adjoint | conjugate transpose, `A* = conj(A)^T`; for real A same as transpose; `adj` is the adjugate (different) |
| `<v, w>` | inner product | linear in the SECOND argument, conjugate-linear in the first; `<v,w> = v* w` on C^n |
| `j` | imaginary unit | `j = sqrt(-1)`; `e^{jwt} = cos(wt) + j sin(wt)`; w (omega) in rad/s |
| `H(s), H(jw)` | transfer function, frequency response | `|H(jw)|` plotted `20 log10` vs w on log axis |
| `zeta, w0` | damping ratio and natural frequency | `s^2 + 2 zeta w0 s + w0^2`; resonance peak for `zeta in (0, 1/sqrt(2))` |
| `x_eq, u_eq, y_eq` | equilibrium | written with superscript "eq"; `f(x_eq,u_eq) = 0` |
| `x~, u~, y~` | deviation variables | `x~ = x - x_eq` etc.; `x~' = A x~ + B u~` with `A = df/dx` at xi |
| `Spec(A)` | spectrum (eigenvalues with multiplicity) | `lambda in Spec(A)` |
| simple, semi-simple | distinct eigenvalues, n independent eigenvectors | simple implies semi-simple |
| `T^{-1} A T = Lambda` | diagonalization | columns of T are eigenvectors |
| `e^{At}` | matrix exponential | `T e^{Lambda t} T^{-1}` for simple A; `det(e^A) = e^{Tr A}` |
| `Phi(t, t0)` | state-transition matrix | `d/dt Phi = A(t) Phi`, `Phi(t0,t0) = I`; LTI: `e^{A(t - t0)}` |
| asymptotic stability (continuous) | all eigenvalues of A in open left half-plane | `Real(lambda) < 0`; such A is Hurwitz |
| asymptotic stability (discrete) | all eigenvalues strictly inside the unit circle | `|lambda| < 1` |
| marginal stability | bounded state | Real(lambda) <= 0 and Jordan blocks of size 1 on the imaginary axis |
| BIBO | bounded input bounded output | `h(t) = C e^{At} B`; asymptotic stability implies BIBO, not conversely |
| `(A, *, *, *)`, `(A,B,*,*)` | systems written with only relevant matrices | star marks irrelevant entries |
| `A_bar, B_bar` | zero-order-hold discretization | sampling period T; `x_k = x(kT)` |
| `rank + nullity = n` | rank-nullity | n = number of columns |
| `R(A), N(A), S^⊥` | range, null space, orthogonal complement | script R, script N |

## Where a visual would help most
1. **Eigenvalue location and mode shape (modes, internal-stability, discrete-time-systems).** Drag a point lambda in the complex plane (continuous: left/right of imaginary axis; discrete: inside/outside the unit circle, with a switch for time domain). A trace of Real(e^{lambda t}) (or lambda^k as a stem plot) updates, with a conjugate pair kept for real systems. Click: the sign of Real(lambda) is growth versus decay, Imag(lambda) is oscillation rate, and the stability boundary moves from the imaginary axis to the unit circle.
2. **Pole placement with L (state-feedback, eigenvalue-placement).** For a 2-state system (ball linearization with its 195.9 and -16.1) drag target poles in the s-plane and watch gains L and the closed-loop state trajectory update with u = Lx. Click: each target pole position fixes one coefficient of the characteristic polynomial, and far-left poles cost huge gains and control effort.
3. **Controllability rank test and the uncontrollable eigenvalue (controllability, kalman-decomposition).** Sliders on a, or on B direction, for a two-state example (Example 72 and Example 76 with a). Show columns b and Ab in the plane, shading their span, plus closed-loop eigenvalues as l changes. Click: when b and Ab align (a = 1) one eigenvalue freezes no matter what L is.
4. **Matrix exponential as a flow (matrix-exponential, solution-of-state-equations).** Drag the initial state in the plane and choose A (eigenvalues real, complex, repeated/Jordan); the trajectory e^{At} xi is drawn with eigenvector lines. Click: trajectories split along eigenvector directions, and a Jordan block adds a t e^{lambda t} drift.
5. **Second-order frequency response and resonance (frequency-response, transfer-function-model).** Drag zeta and w0 sliders and a frequency marker; show |H(jw)| on a log scale, pole positions in the s-plane, and a rotating phasor input and output. Click: pole positions near the imaginary axis (small zeta) create the resonance peak; peak frequency approaches w0 as zeta goes to 0.
6. **Linearization at an equilibrium (linearization, equilibrium).** Plot the ball's nonlinear force curve or phase portrait with a draggable equilibrium parameter beta; a tangent line (or the linear flow field) overlays, and an initial state slider shows linear vs nonlinear trajectories diverging far from beta. Click: the Jacobian gives the slope and the approximation fails away from the equilibrium; instability of the ball is a positive eigenvalue sqrt(19.6/beta).
7. **Projection as the closest point (projection, least-squares, orthogonality).** Drag a vector v in R^3 over a plane spanned by two draggable vectors b1, b2; show s-hat, the error v - s-hat, and the Gram system numbers. Click: the error is perpendicular to the subspace and any other point in the plane is farther (Pythagoras).
8. **Parametric resonance in the Mathieu equation (ltv-stability-pitfall).** Sliders for epsilon, mu, w0 and a simulated y(t) with the frozen eigenvalues of A(t) drawn moving in the left half-plane alongside the growing response. Click: eigenvalues of A(t) stay in the left half-plane at every instant yet y(t) grows when epsilon exceeds 2 mu at w0 = 1.
