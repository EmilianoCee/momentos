# Survey: CS 70, EECS 16A, EECS 16B (research date 2026-11-15)

Headline: the 16A/16B sequence has been restructured. The old "Designing Information Devices and Systems I/II" content is split. 16A is now signals, dynamics, information (linear algebra heavy). The circuits half became a separate course, EE 64 (catalog code ELENG 64, formerly EL ENG 16B), "Introduction to Circuits & Devices". The EECS dept page still also carries an "EECS 16B. Introduction to Circuits & Devices" listing with the same title. No Fall 2026 course website was found for EE 64 / 16B; the eecs16b.org site is a stale Spring 2024 snapshot.

## CS 70: Discrete Mathematics and Probability Theory
- Catalog: 4 units. Prerequisites: sophomore-level mathematical maturity, plus programming experience like CS 3 or AP CS A. The course covers logic, induction, infinity and undecidability, modular arithmetic and cryptography, polynomials and error-correcting codes, and then discrete and some continuous probability, with applications such as load balancing and Bayesian inference. Fall 2026: TuTh 3:30-4:59 PM, Li Ka Shing 245 (Hug, Sabin).
- Sources (all fetched 2026-11-15):
  - https://eecs70.org : Fall 2026 weekly schedule (below); no textbook listed.
  - https://www2.eecs.berkeley.edu/Courses/CS70 : title, units, prerequisites, description, Fall 2026 and Spring 2027 times.
  - Failed: none. No separate catalog page fetched for CS 70 (undergraduate.catalog.berkeley.edu not queried for it).
- Outline (Fall 2026, eecs70.org): W0 direct proofs. W1 propositional logic, proof techniques I and II. W2 induction, modular arithmetic. W3 Euclid/FLT/CRT, RSA. W4 polynomials, secret sharing and error-correcting codes. W5 graphs I, II. W6 stable matching, countability. W7 computability, midterm 10/15. W8 counting, intro discrete probability. W9 conditional probability, combinations of events. W10 random variables, expectation, linearity. W11 variance, covariance. W12 concentration inequalities, continuous probability. W13 Gaussian, CLT. W14 Markov chains, text generation. W15 RRR. W16 final 12/18.
- Topic candidates:
  1. direct proof: start from what you know, chain implications to the claim.
  2. propositional logic: statements are true or false and connectives are truth tables.
  3. quantifiers: "for all" is a claim about every item, "there exists" about one; negation swaps them.
  4. proof by contrapositive: proving not-Q implies not-P proves P implies Q.
  5. proof by contradiction: assume the claim fails and follow it to something impossible.
  6. proof by cases: split the world into pieces that cover everything.
  7. induction: knock over the first domino, show each knocks the next.
  8. strong induction: assume all earlier cases, not just the previous one.
  9. well-ordering: any non-empty set of naturals has a least member.
  10. modular arithmetic: numbers on a clock; only the remainder matters.
  11. modular inverse: the number that undoes multiplication on the clock, if it exists.
  12. gcd and Euclid: repeated remainders shrink a pair until one number is the common divisor.
  13. extended Euclid: run the steps backward to write gcd as a combination.
  14. Fermat's little theorem: raising to p-1 on a prime clock lands on 1.
  15. Chinese remainder theorem: remainders mod coprime numbers fix a number mod their product.
  16. RSA: multiplying primes is easy, undoing it is hard, and a modular exponent is the trapdoor.
  17. polynomial degree and roots: a degree d polynomial has at most d roots.
  18. interpolation: d+1 points pin down one degree-d polynomial.
  19. secret sharing: a secret is a polynomial value; fewer than d+1 shares reveal nothing.
  20. error-correcting codes: send extra points so the polynomial survives lost or flipped ones.
  21. graphs: dots and links; degree, paths, connectivity.
  22. Euler tours and planarity: edge-counting rules decide what can be traced or drawn flat.
  23. trees: connected with no cycles; n nodes, n-1 edges.
  24. hypercube: bit strings as corners, edges flip one bit.
  25. stable matching: propose and reject until nobody wants to defect.
  26. countability: a set is countable if you can list it.
  27. diagonalization: build an element that differs from the k-th listed item in place k.
  28. halting problem: no program can decide for every program whether it stops.
  29. counting by rule of product: independent choices multiply.
  30. combinations: choosing k from n ignores order; divide the ordered count.
  31. stars and bars: place dividers among items to count ways to split.
  32. inclusion-exclusion: add, subtract overlaps, add back.
  33. sample space and events: list every outcome; an event is a subset.
  34. conditional probability: shrink the sample space to what you know happened.
  35. Bayes rule: flip a conditional using the base rate.
  36. independence: learning one event tells you nothing about the other.
  37. union bound: the chance of any of several events is at most the sum.
  38. random variable: a number attached to each outcome.
  39. expectation: the balance point of the distribution.
  40. linearity of expectation: averages add, even when variables depend on each other.
  41. common distributions: uniform, Bernoulli, binomial, geometric, Poisson each model one counting story.
  42. variance: the average squared distance from the mean.
  43. covariance: do two variables move together.
  44. Markov inequality: a non-negative variable rarely exceeds many times its mean.
  45. Chebyshev inequality: far from the mean is rare, measured in standard deviations.
  46. law of large numbers: sample averages settle on the mean.
  47. continuous density: probability is area under a curve, not height.
  48. Gaussian: the bell curve set by mean and variance.
  49. central limit theorem: sums of many small independent pieces look Gaussian.
  50. Markov chain: the next state depends only on the current one.
  51. stationary distribution: the mix that the chain leaves unchanged.
  52. hitting time and mixing: how long until you reach a state, or forget the start.
- Changes worth knowing: none found. Title and number unchanged. Instructors alternate by term.

## EECS 16A: official title varies by source
Exact title on EECS dept page and course site: "Foundations of Signals, Dynamical Systems, and Information Processing". Exact title on the Berkeley undergraduate catalog: "Introduction to Signals, Dynamics, and Information". Old title (stale dept page): "Designing Information Devices and Systems I".
- Catalog: 4 units. Prerequisites: MATH 54 (dept page). The catalog page shows "Complete all" but its fetch did not name the courses. Formerly: EL ENG 16A. The course introduces signals, systems, optimization, controls and machine learning on a linear algebra base. It starts with a short linear algebra review, then signal processing, linear systems, feedback control, optimization and basic machine learning.
- Sources (fetched 2026-11-15):
  - https://eecs16a.org : Spring 2026 schedule (the newest the site showed), lecture topics, notes 1-8.
  - https://eecs16a.org/policies : course framing (signals, dynamical systems, data analysis, ML); no prerequisites or restructure explanation.
  - https://www2.eecs.berkeley.edu/Courses/EECS16A : title, 4 units, MATH 54, description, Fall and Summer formats.
  - https://undergraduate.catalog.berkeley.edu/courses/1063272 : catalog title, formerly EL ENG 16A, description.
  - https://www2.eecs.berkeley.edu/Courses/EE16A : stale old page (old title, prerequisites Math 1A/1B and CS 61A).
  - Search snippet only (not fetched): https://www2.eecs.berkeley.edu/Courses/ELENG16A/index.html
  - Failed: https://eecs16a.org/schedule (404). No Fall 2026 site found.
- Outline (Spring 2026, eecs16a.org; Fall 2026 outline not found): vectors and signals; vector spaces, inner products; Cauchy-Schwarz, triangle inequality; periodicity, complex exponentials, Euler; DTFS (three lectures); least squares; adjacency matrices, PageRank; eigenanalysis; change of basis; spring break; intro SVD; SVD/PCA; input-output models of DT-LTI systems (four lectures); state-space DT-LTI; CT-LTI; demos and applications. Exams 2/10 and 3/19. Textbook: course Notes 1-8; VMLS (Boyd and Vandenberghe) as an extra resource only.
- Topic candidates:
  1. vector: a list of numbers that can be a point, an arrow or a signal.
  2. signal as vector: sampling a waveform gives a point in a high-dimensional space.
  3. inner product: multiply entries and add; large when two vectors line up.
  4. norm: the length of a vector, the square root of its own inner product.
  5. Cauchy-Schwarz: the inner product never beats the product of lengths.
  6. triangle inequality: going direct is never longer than going via a detour.
  7. correlation as angle: the normalised inner product is the cosine of the angle.
  8. matched filtering: slide a template over a signal; the peak marks where it fits.
  9. vector space and span: everything you can reach by scaling and adding.
  10. linear independence: no vector in the set is a combination of the others.
  11. basis and dimension: the smallest set that reaches the whole space.
  12. matrix as map: a matrix sends input vectors to output vectors, linearly.
  13. null space and range: what the map kills and what it can reach.
  14. periodicity: a signal that repeats after N samples.
  15. complex exponential: a point circling the unit circle at a set rate.
  16. Euler formula: cosine and sine are the shadows of that circling point.
  17. DTFS: any periodic signal is a sum of a few spinning exponentials.
  18. Fourier coefficient as projection: each coefficient is an inner product with one exponential.
  19. orthogonal basis: perpendicular directions make coordinates independent.
  20. least squares: the closest point in a subspace, found by dropping a perpendicular.
  21. normal equations: the error must be perpendicular to every column of A.
  22. overdetermined systems: more equations than unknowns means fit, not solve.
  23. graphs as matrices: an adjacency matrix records who links to whom.
  24. PageRank: rank is the long-run share of a random surfer's time.
  25. eigenvector: a direction the matrix only stretches.
  26. eigenvalue: the stretch factor for that direction.
  27. diagonalisation and change of basis: pick the eigen-directions and the matrix becomes independent scalings.
  28. powers of a matrix: eigenvalues decide whether repeated application grows or dies.
  29. SVD: any matrix is a rotation, a stretch along axes, and another rotation.
  30. singular values: how much the matrix stretches along each axis.
  31. low-rank approximation: keep the big singular values, drop the rest.
  32. PCA: the directions of greatest spread in data are the top singular vectors.
  33. DT-LTI system: output is a linear, time-invariant function of input.
  34. impulse response: what the system does to a single kick, which fixes everything else.
  35. convolution: each input sample adds a scaled, shifted copy of the impulse response.
  36. state-space model: the state holds what the system remembers; the next state is A times it plus B times input.
  37. stability: all eigenvalues of A inside the unit circle means the state decays.
  38. CT-LTI system: the same ideas with derivatives, where eigenvalues need negative real part.
  39. feedback control: measure the output and feed it back to reshape eigenvalues.
  40. optimisation and gradient descent: walk downhill on a cost surface (listed in catalog; topic placement unknown for the Spring 2026 site).
  41. classification as a linear model (catalog lists basic ML; exact site coverage not seen).
- Changes worth knowing: (a) title changed from "Designing Information Devices and Systems I" to "Foundations of Signals, Dynamical Systems, and Information Processing" (dept/site) or "Introduction to Signals, Dynamics, and Information" (catalog). (b) Prerequisite now MATH 54 (was Math 1A/1B and CS 61A). (c) Content moved away from circuits toward linear algebra, signals, state-space, SVD/PCA and ML. Circuits left 16A. (d) No page explaining the restructure was found. Items 40-41 are the catalog's words, not confirmed lectures.

## EECS 16B / EE 64: Introduction to Circuits & Devices
Exact title: "Introduction to Circuits & Devices". Dept pages list it both as "EECS 16B" and as "EE 64". Catalog code is ELENG 64, formerly EL ENG 16B. Old title (Spring 2024 site, stale dept page): "Designing Information Devices and Systems II".
- Catalog: 4 units. Prerequisite: MATH 54 (Physics 89 accepted as alternative per EE 64 enrollment notes); the catalog page says "Complete all" without naming courses in the fetched text. The course teaches how to predict real electronic behavior with mathematical models and circuit analysis: time and frequency domains, phasors, Kirchhoff's laws, RLC circuits, op-amp signal processors, feedback and circuit models for non-electronic domains. Fall 2026: TuTh 14:00-15:29, Stanley 105 (Murch, Muller). Spring 2027: TuTh 08:00-09:29 (Kante, Dutta).
- Sources (fetched 2026-11-15):
  - https://www2.eecs.berkeley.edu/Courses/EE64 : title, units, prerequisites, description, Fall 2026 and Spring 2027 times.
  - https://undergraduate.catalog.berkeley.edu/courses/1063282 : ELENG 64, formerly EL ENG 16B, description.
  - https://www2.eecs.berkeley.edu/Courses/EECS16B : "EECS 16B. Introduction to Circuits & Devices", MATH 54, Summer/Fall.
  - https://eecs16b.org/ and https://eecs16b.org : Spring 2024 snapshot only (old content).
  - https://www2.eecs.berkeley.edu/Courses/EE16B/ : stale old page (prerequisite EE 16A).
  - Search only (not fetched): https://www2.eecs.berkeley.edu/Scheduling/EE/schedule-draft.html (draft Fall 2026 listing of Muller, Murch, Dutta).
  - Failed or absent: no Fall 2026 or 2025 course website for EE 64 / new 16B found.
- Outline: no current outline found. The only official outline is the OLD course, Spring 2024 (eecs16b.org): capacitors, RC, first-order ODEs; inductors, RL; CMOS transistors, DACs/ADCs; RLC and second-order ODEs; impedance, frequency domain, transfer functions; Bode plots, poles and zeros; state space, vector ODEs; natural and forced response; discrete time, hybrid systems, system ID; stability, feedback control, controllability; Gram-Schmidt, spectral theorem, minimum-energy control; SVD, PCA; linearisation. Much of the later half (state space, controllability, SVD/PCA) appears to have moved to the new 16A. Textbook: course notes 01-17 and lab notes 0-8.
- Topic candidates (from the catalog description, plus the old Spring 2024 outline where marked; the new course's actual order is unknown):
  1. voltage and current: voltage is the push between two points, current is the flow through one.
  2. KCL: current in equals current out at every node.
  3. KVL: voltage drops around any loop sum to zero.
  4. resistor and Ohm's law: current proportional to voltage, slope 1/R.
  5. series and parallel: series adds resistance, parallel adds conductance.
  6. voltage divider: a loaded ratio of resistances sets the output.
  7. node analysis: write KCL at each node and solve for voltages.
  8. superposition and Thevenin: a linear network looks like one source and one resistor from outside.
  9. capacitor: stores charge; current is C times how fast voltage changes.
  10. inductor: stores flux; voltage is L times how fast current changes.
  11. RC step response: voltage climbs to its target along an exponential with time constant RC.
  12. first-order ODE: the rate of change is proportional to the distance from the target.
  13. RLC circuit: two storage elements can trade energy back and forth and ring.
  14. second-order response: damping decides between ringing and slow settling.
  15. complex numbers as rotation: multiplying by j turns a phasor a quarter turn.
  16. phasor: a sinusoid at known frequency reduces to one complex number.
  17. impedance: resistance generalised to capacitors and inductors, R, 1/(jwC), jwL.
  18. frequency response: how gain and phase change as the input frequency sweeps.
  19. transfer function: output over input as a function of s or jw.
  20. poles and zeros: the roots that shape the response.
  21. Bode plot: gain and phase on log axes, with straight-line asymptotes.
  22. low-pass and high-pass filters: RC arrangements that pass one end of the spectrum.
  23. op-amp ideal model: with feedback, the two inputs sit at equal voltage.
  24. inverting and non-inverting amplifier: the gain is a ratio of two resistors.
  25. op-amp integrator and filters: put a capacitor in the feedback path to get dynamics.
  26. feedback: sending output back to the input trades gain for accuracy and speed.
  27. stability of feedback: feedback with too much phase lag turns into oscillation.
  28. diode: a one-way valve with a knee near 0.7 V (from memory, not verified; assumed within "physical examples of devices").
  29. MOSFET as switch and amplifier: gate voltage controls channel current (old 16B covered CMOS; new coverage not verified).
  30. ADC and DAC: turn voltage into numbers and back (old 16B; new coverage not verified).
  31. circuit models for non-electronic systems: mass-spring-damper and heat flow map onto RLC (catalog line).
  32. state-space view of RLC circuits: capacitor voltage and inductor current as the state (old 16B; new coverage not verified).
- Changes worth knowing: (a) renumbered in the catalog to ELENG 64 (formerly EL ENG 16B). (b) Title changed from "Designing Information Devices and Systems II" to "Introduction to Circuits & Devices". (c) Prerequisite changed from EE 16A to MATH 54 (or Physics 89). (d) Content narrowed to circuits and devices; state-space, SVD and PCA no longer appear in the catalog description. (e) Enrollment: students starting Summer 2026 or later need an enrollment permission form for Spring 2027. (f) The dept still lists the same course as "EECS 16B" and "EE 64" on two pages, so naming is mid-transition. The 16A and 16B dept pages say Fall and Summer only (no Spring), while the EE 64 page lists Spring 2027.
