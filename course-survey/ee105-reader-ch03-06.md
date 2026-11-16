# EE 105 reader, chapters 3-6: concept notes

Source: ee105_reader_v3 copy.md, lines 2296-4495. Note on the source: almost every displayed equation was lost in the conversion (blank lines where the equation was). Formulas below are therefore RECONSTRUCTED from the surrounding prose, the symbols and numbers that survived, and the standard EE 105 form of each result. Where the reader's own text pins a convention down (for example "V_D < 0 is reverse bias", "potential referenced to intrinsic Si", "diode current flows P to N") I say so. Items marked (reconstructed) should be checked against the original PDF before a tool relies on a factor.

## Chapter 3. Introduction to Semiconductors

### 3.2 Conduction in an Ideal Metal "Gas"
- **conduction-in-metals**: a metal is a gas of free electrons that gain a little momentum from the field between collisions, then lose their memory of direction, so current is proportional to field (Ohm's law) instead of accelerating without limit.
  - notation: J current density (A/cm^2 or A/m^2); E field (V/cm); sigma conductivity (S/m); rho = 1/sigma resistivity; N carrier density (cm^-3); tau mean free time (s); M or m* effective mass
  - formulas: V = IR; J = sigma E; sigma = 1/rho; G = 1/R; for a rectangular bar I = J W t, E = V/L, so R = L/(sigma W t) (reconstructed); momentum gained in one free flight = q E t; random initial momenta average to zero so average momentum gain = q E tau; sigma = q N mu; with both carriers sigma = q(n mu_n + p mu_p) (reconstructed); sigma = N q^2 tau / m* (reconstructed)
  - typical values: sodium, one free electron per atom; mean free time back-calculated from measured conductivity is surprisingly long; electron thermal speed ~10^7 cm/s at room temperature (metal figure given as v*tau = 3x10^-7 cm vs ion spacing 3.8x10^-8 cm, so about 10 ions passed between collisions)
  - approximations: Ohm's law is the first term of a Taylor expansion of V(I), valid for small current, and the reader says the range is very large; gas model treats collisions as randomizing velocity
  - picture: stop-and-go freeway traffic: you accelerate only until the next stop, so you gain a bounded amount of speed, not an ever-growing one.
  - pitfalls: current proportional to force (velocity proportional to field) looks odd next to F = ma; the reader flags that the long mean free time puzzle (electron passing ~10 ions) needs quantum mechanics

- **scattering-mechanisms**: in a perfect periodic crystal an electron would not scatter at all (wave nature, effective mass); resistance comes only from lattice vibrations (phonons) and impurities that break the periodicity.
  - notation: m* effective mass (kg), tau mean relaxation time (s)
  - formulas: sigma depends on N, q, m*, tau (summary only)
  - picture: periodic row of atoms is transparent to the electron wave; a vibrating atom or a foreign atom is a bump that deflects it (Fig 3.2).
  - pitfalls: electron does not scatter just because it meets an atom

### 3.3 Introduction to Semiconductors
- **conductivity-vs-temperature**: metals get slightly worse conductors when hot, semiconductors get orders of magnitude better, because heat creates carriers in a semiconductor but only adds scattering in a metal.
  - typical values: copper 273 K 6.4x10^7 S/m, 373 K 4.46x10^6 S/m (reader's figures; listed as about 30% decrease for +100 degrees, which does not match the two numbers as printed, so treat as garbled); germanium 273 K 0.5 S/m, 500 K 833 S/m; pure water 291 K 4x10^-6 S/m; seawater 4 S/m
  - picture: a table of conductivities spanning many decades, with the temperature trend of germanium opposite to copper.
  - pitfalls: insulating pure water vs conductive seawater: the difference is free charges, not the material

- **crystal-structure-bond-model**: silicon atoms each share four valence electrons with four neighbours in a diamond lattice; at 0 K every electron is in a bond and nothing conducts.
  - notation: Si 14 electrons, crystal config 1s2 2s2 2p6 3(sp)^4; bond length 0.235 nm; lattice constant 5.43 angstrom (from figure label)
  - typical values: Si crystal density about 5x10^22 atoms/cm^3 (from Ch 4)
  - picture: flat 2D drawing of ions with double lines for bonds, each bond holding two electrons of opposite spin (Fig 3.9).
  - pitfalls: inner core electrons never take part in conduction (unless x-rays)

- **energy-bands**: allowed electron energies form bands separated by a forbidden gap; electrons in the valence band are bound, electrons in the conduction band move, and the size of the gap decides metal, semiconductor or insulator.
  - notation: E_g band gap (eV); valence band, conduction band; kT thermal energy (about 25 meV at room temperature)
  - typical values: insulator gap ~4-8 eV; semiconductor ~1 eV; metal: no gap or overlapping bands; kT about 25 meV
  - approximations: bands treated as continuous because many atoms split discrete levels into near-continuous bands; electron occupancy follows Boltzmann tail of Fermi-Dirac
  - picture: levels of isolated atoms split and merge into bands as atoms approach (Fig 3.6); a ladder with a forbidden gap and an electron hopping over it (Fig 3.7).
  - pitfalls: a 4 eV gap vs 25 meV thermal energy is effectively infinite, not just large

- **electrons-and-holes**: breaking a bond frees an electron and leaves a vacancy that behaves as a free positive particle, the hole; a full band carries no current, so the current of a nearly full band is that of the missing electrons acting as positive charges.
  - notation: n free electron concentration, p free hole concentration (cm^-3); effective mass differs for electrons and holes
  - formulas: partially filled band = full band minus removed electrons; full band current = 0, so the current equals that of the removed states with opposite sign (so positive charge)
  - picture: a bubble in a full bottle; a vacancy hopping down a row of bonds (Fig 3.11).
  - pitfalls: the hole is described as fictitious but behaves as real; electrons near the valence-band top have negative effective mass, which the reader leaves out

- **generation-recombination-equilibrium**: thermal generation of electron-hole pairs balances recombination, which is why n p stays fixed at a given temperature.
  - notation: G generation rate, R recombination rate (cm^-3 s^-1); k a proportionality constant
  - formulas: R = k n p; at equilibrium G_thermal = k n0 p0 (reconstructed)
  - picture: a crowd leaves and enters a room at equal rates; more people means more meetings.
  - pitfalls: optical generation is ignored in this section

### 3.4 Intrinsic Carrier Concentration
- **intrinsic-carriers**: in pure silicon every freed electron leaves a hole, so n0 = p0 = n_i, and n_i climbs exponentially with temperature and falls exponentially with band gap.
  - notation: n_i intrinsic carrier concentration (cm^-3); n0, p0 equilibrium concentrations; E_g (eV); k Boltzmann constant; T (K)
  - formulas: n0 = p0 = n_i; n_i^2 = (generation constant, a function of T only); n_i proportional to exp(-E_g/(2kT)) times a power of T (reconstructed; reader says generation goes as exp(-E_g/kT) "approximately")
  - typical values: n_i = 10^10 cm^-3 at 300 K (the reader's round number for silicon)
  - approximations: optical generation neglected
  - picture: classroom heights, normal distribution: only the tail above the wall height clears it; raising the wall cuts the count exponentially.
  - pitfalls: the reader defines n_i^2 as the constant because n_i^2 has units of concentration squared

- **mass-action-law**: in thermal equilibrium the product of electron and hole concentrations is the constant n_i^2, whatever the doping.
  - formulas: n p = n_i^2
  - typical values: n_i = 10^10 cm^-3 at 300 K
  - approximations: valid in thermal equilibrium only (Ch 6 relaxes it)
  - picture: see-saw: raise one carrier type and the other falls so the product stays fixed.
  - pitfalls: even with dopant adding electrons, n is not n_i + N_D, because recombination also rises

### 3.5 Doping with Impurities
- **doping**: adding group V atoms (P, As) donates one free electron each; adding group III atoms (B) accepts an electron and creates a free hole; each ionized dopant leaves behind an immobile charge.
  - notation: N_D donor concentration, N_A acceptor concentration (cm^-3); N_D^+, N_A^- ionized densities
  - formulas: charge neutrality p + N_D^+ = n + N_A^- (reconstructed); with only donors n = p + N_D; with mass action n^2 - N_D n - n_i^2 = 0, so n = N_D/2 + sqrt((N_D/2)^2 + n_i^2) (positive root only); for N_D >> n_i, n ~ N_D and p = n_i^2/N_D; likewise N-type: n0 ~ N_D, p0 = n_i^2/N_D; P-type: p0 ~ N_A, n0 = n_i^2/N_A
  - typical values: doping 10^14 to 10^18 cm^-3 in practice; unintentional impurities about 10^12 cm^-3; wafer purity about 1 part in 10^9; wafer thickness about 700 um
  - approximations: N_D >> n_i (n ~ N_D); all dopants ionized at room temperature (fails at low temperature, "freeze-out")
  - picture: donor sits in the lattice as a + ion with one electron to spare; acceptor takes an electron from a neighbour bond, making a - ion and a mobile hole (Figs 3.12, 3.13).
  - pitfalls: only the positive root of the quadratic is physical

- **compensation**: with both dopant types the larger one wins, and the material behaves as if doped by the difference.
  - formulas: N_D > N_A: n ~ N_D - N_A, p = n_i^2/n; N_A > N_D: p ~ N_A - N_D, n = n_i^2/p
  - approximations: |N_D - N_A| >> n_i
  - picture: donors and acceptors cancel pairwise (Fig 3.14).

### 3.6 Drift Currents
- **thermal-velocity-and-collisions**: carriers move randomly very fast, collide very often, and the field adds only a small drift on top.
  - notation: v_th thermal velocity (cm/s); tau_c time between collisions (s); lambda mean free path (cm)
  - formulas: (1/2) m v_th^2 ~ kT (kinetic = thermal energy); lambda = v_th tau_c
  - typical values: v_th ~ 10^7 cm/s; tau_c ~ 10^-13 s; so lambda ~ 10^-6 cm = 10 nm
  - picture: arrow of thermal speed with a small extra a*tau_c arrow added by the field (Fig 3.15).

- **drift-current**: field adds an average drift velocity proportional to E; with mobility mu this gives the Ohm's-law current of electrons and holes.
  - notation: v_d drift velocity (cm/s); mu_n, mu_p mobility (cm^2/V s); E (V/cm)
  - formulas: v_d = -mu_n E for electrons, v_d = +mu_p E for holes (sign: holes move with E, electrons against it); mu = q tau_c / m*; J_n,drift = q n mu_n E; J_p,drift = q p mu_p E; J_drift = q(n mu_n + p mu_p) E = sigma E
  - typical values: mu_n about 1000 cm^2/V s, mu_p about 400 cm^2/V s (reader's rounded values). Mobility-vs-doping figure labels 1400 and about 330 and 160 (axis labelled cm^2/Vs, doping on log axis 10^13 to 10^19 cm^-3)
  - approximations: mobility treated as constant in field (fails at high field, see velocity saturation, mentioned in 5.4.6)
  - picture: mobility falls as doping rises, because dopant ions are extra scattering sites (Fig 3.16).
  - pitfalls: electrons are faster because they are lighter; mobility depends on total N_D + N_A, not just majority type

### 3.7 Diffusion Currents
- **diffusion-current**: random thermal motion sends more carriers from the high-concentration side to the low side, so current flows down a concentration gradient with no field.
  - notation: D_n, D_p diffusion constants (cm^2/s); n(x), p(x) concentration (cm^-3); lambda mean free path
  - formulas: flux of electrons crossing x=0 = (1/2)(n(-lambda) - n(lambda)) v_th = -v_th lambda dn/dx (the factor 1/2: half move each way); J_n,diff = q D_n dn/dx (electrons flow down the gradient, charge is negative so current flows up the gradient); J_p,diff = -q D_p dp/dx; D = v_th lambda (up to a factor)
  - approximations: lambda small compared with variation scale, so a first-order Taylor expansion of n(x) works
  - picture: partition opened in a box: left chamber particles spread until each side is equally filled (Fig 3.17); two crowds crossing a line, the denser one sending more (Fig 3.19).
  - pitfalls: diffusion current direction for electrons is opposite to particle flow

- **einstein-relation**: the diffusion constant and mobility are both set by scattering, so their ratio is just the thermal voltage.
  - formulas: D/mu = kT/q = V_th (about 26 mV at 300 K)
  - typical values: V_th = kT/q ~ 26 mV at 300 K
  - picture: both D and mu are proportional to tau_c, so tau_c cancels in the ratio.

- **total-current-and-continuity-across-interface**: with both mechanisms present, drift and diffusion add; a uniform current through a conductivity step forces a field jump.
  - formulas: J_n = q n mu_n E + q D_n dn/dx; J_p = q p mu_p E - q D_p dp/dx; J = J_n + J_p; at an interface sigma1 E1 = sigma2 E2 so E1/E2 = sigma2/sigma1 (field inversely proportional to conductivity)
  - approximations: in resistors carrier density is uniform, so the diffusion term is nearly zero
  - picture: a series bar with two conductivities carrying one current; field is larger in the less conductive piece (Fig 3.20).

## Chapter 4. IC Resistors and Capacitors and Electrostatics

### 4.2 IC Fabrication: Si Substrate (and oxide, implantation)
- **ic-fabrication-flow**: grow oxide, spin photoresist, expose through a mask, etch windows, implant dopants, then anneal so dopants diffuse and bond into the crystal.
  - notation: SiO2 oxide; photoresist; HF etch; ion implantation; thermal diffusion
  - typical values: Si crystal density about 5x10^22 cm^-3; intended doping 10^14-10^18 cm^-3; unintended impurities ~10^12 cm^-3; wafer ~700 um thick
  - picture: six-step cross-section strip (a) to (f) of oxide, resist, UV, etch, implant, diffuse (Fig 4.1).
  - pitfalls: positive photoresist becomes etchable where exposed to UV

### 4.3 IC Resistors
- **ic-resistor**: a resistor is a doped slab whose thickness and doping are fixed by the process, and whose length and width are chosen by the designer.
  - notation: R (ohm); L length, W width, t thickness (cm or um); rho (ohm cm); sigma
  - formulas: I = J W t; E = V/L; R = rho L/(W t) = L/(sigma W t)
  - typical values: poly film example 10 ohm per square
  - picture: slab with current along L through cross-section W x t (Fig 4.4).
  - pitfalls: diffusion resistor must keep its pn junction to the substrate reverse biased (never negative relative to the P substrate), and there is a distributed capacitance to the substrate; poly resistor sits on oxide to cut that parasitic

- **sheet-resistance**: lump rho and t into R_sq so that resistance is R_sq times the number of squares L/W.
  - notation: R_sq (written R with a square symbol), unit ohm per square (ohm/sq, written ohm with a square), N squares = L/W
  - formulas: R_sq = rho/t; R = R_sq (L/W)
  - typical values: 10 ohm/sq (poly example)
  - approximations: uniform current in each square
  - picture: resistor cut into squares laid end to end; resistance is the count times R_sq (Figs 4.5, 4.6).
  - pitfalls: a square has the same R at any size (L = W)

- **layout-squares-correction**: current crowding at contacts and corners means those regions count as fewer than one square.
  - formulas: resistance = R_sq (N_straight + 0.65 per contact + 0.56 per corner) (rule of thumb)
  - typical values: contact (dog-bone) 0.65 square; 90-degree corner 0.56 square
  - picture: contact region where current spreads from a small via; corner where current hugs the inner track (Fig 4.6).

### 4.4 Review of Electrostatics
- **poisson-equation**: field lines diverge on charge, so the slope of E is the charge density over permittivity.
  - notation: rho charge density (C/cm^3); epsilon (F/cm) or epsilon_s for silicon; E (V/cm); phi potential (V)
  - formulas: dE/dx = rho/epsilon (1D); E(x) = E(x0) + (1/epsilon) integral of rho dx; E = -dphi/dx; Poisson 1D: d^2 phi/dx^2 = -rho/epsilon; 3D form div E = rho/epsilon
  - approximations: 1D, variations in y and z neglected
  - picture: charge-free region means E constant; uniform charge slab gives E rising linearly then flat (Fig 4.8).
  - pitfalls: sign: E points from + charge to - charge, phi decreases along E

- **electrostatics-gauss**: the net field leaving a closed surface equals enclosed charge over epsilon.
  - formulas: closed-surface integral of E dot dS = Q_enclosed/epsilon; via divergence theorem
  - picture: a box around positive charge, net field leaving it (Fig 4.7b).

- **potential-and-boundary-conditions**: potential is the integral of the field and must be continuous; the field may jump at an interface where there is surface charge or different permittivity.
  - formulas: phi(x2) - phi(x1) = -integral of E dx; epsilon1 E1 = epsilon2 E2 (no free surface charge)
  - picture: pillbox around an interface with height shrinking to zero (Fig 4.10).
  - pitfalls: an electron floats toward high potential because of its negative charge

### 4.5 IC Capacitors
- **ic-capacitor**: two overlapping plates (metal or poly, separated by thin oxide) give a parallel-plate capacitor whose plate charges are equal and opposite.
  - notation: C (F); Q (C); V_s source voltage; epsilon_ox, d oxide thickness; MIM = metal-insulator-metal
  - formulas: E = Q/(epsilon A) uniform in insulator; V = E d; Q = C V with C = epsilon A/d
  - picture: all charge sits as delta functions at the metal surfaces because field inside metal is zero (Fig 4.13).
  - pitfalls: bottom-plate parasitic capacitance to the substrate; poly/doped-Si plates are MOS caps (Ch 7)

- **nonlinear-capacitor-small-signal**: when charge is a nonlinear function of voltage, capacitance is defined incrementally at a bias point as the slope dQ/dV.
  - formulas: Q = f(V_s); Taylor: Q = f(V_s) + (df/dV)|_V_s v_s + ... ; C_small-signal = dQ/dV at V_s
  - approximations: small signal, signal much smaller than the bias
  - picture: Q-V curve with a tangent at the bias point; capacitance is the tangent slope (Fig 4.15).
  - pitfalls: no single C for a nonlinear device; reverse-biased pn is the example (Q depends on reverse bias)

## Chapter 5. PN Junctions in Equilibrium

### 5.3 Carrier Concentration and Potential
- **drift-diffusion-balance-in-equilibrium**: zero net current in equilibrium forces a field wherever there is a concentration gradient, and that field is a potential step.
  - formulas: J_n = q n mu_n E + q D_n dn/dx = 0, so E = -(V_th/n) dn/dx; dphi = -V_th dn/n (reconstructed, sign set by E = -dphi/dx), using D/mu = kT/q
  - picture: steady diffusion flux cancelled by an equal opposite drift flux.
  - pitfalls: the reader's footnote asks why not the sum of electron and hole currents: each carrier's current is zero separately in equilibrium

- **potential-vs-doping**: the potential of a doped region relative to intrinsic silicon is the thermal voltage times the log of its carrier ratio, so each decade of doping moves it by about 60 mV.
  - notation: phi_n, phi_p potential relative to intrinsic Si (V); V_th or V_T or phi_T = kT/q (V)
  - formulas: phi_n = V_th ln(n_n0/n_i) = V_th ln(N_D/n_i); phi_p = -V_th ln(p_p0/n_i) = -V_th ln(N_A/n_i); n = n_i exp(phi/V_th), p = n_i exp(-phi/V_th); np = n_i^2 holds; base-10 form: phi = (V_th ln 10) log10(N/n_i) about 60 mV per decade
  - typical values: V_th about 26 mV at 300 K; 60 mV per decade; example: P-type 10^16 cm^-3 holes is 6 decades above n_i = 10^10, so phi_p = -6 x 60 mV = -360 mV
  - approximations: N >> n_i
  - picture: ruler of doping decades on a log axis maps to linear potential; N-type above, P-type below intrinsic.
  - pitfalls: reference is intrinsic Si (the reader calls this customary and confusing); negative potential means P-type

### 5.4 PN-Junction in Equilibrium
- **pn-equilibrium**: when P and N are joined, majority carriers diffuse across, leave uncompensated ions, and build a field that drives a drift current exactly cancelling the diffusion current.
  - notation: x_p0, x_n0 depletion-region edges (first subscript region type, second subscript equilibrium); transition region = space-charge region; E_0 field
  - formulas: n and p change smoothly across the junction (finite field means no abrupt change); J_n,drift + J_n,diff = 0 and J_p,drift + J_p,diff = 0 separately
  - picture: panel sequence: initial diffusion, charge imbalance and field, final balance with drift opposite diffusion (Fig 5.2).
  - pitfalls: injected majority carriers become minority carriers on the other side and recombine, so they do not penetrate far

- **depletion-region**: the layer where free carriers are removed, leaving fixed ionized dopants whose charge sources the field.
  - notation: rho_0(x) = q(p0 - n0 + N_D - N_A) (Eq 5.18 in the reader); P side -x_p0 < x < 0, rho = -q N_A; N side 0 < x < x_n0, rho = +q N_D
  - formulas: depletion approximation: rho = -q N_A (P side), +q N_D (N side), 0 outside; dE/dx = rho/epsilon_s; E(x) = -(q N_A/epsilon_s)(x + x_p0) for -x_p0<x<0 and E(x) = -(q N_D/epsilon_s)(x_n0 - x) for 0<x<x_n0 (reconstructed; field negative, points from N to P, peak magnitude at x=0); E continuous at x=0 gives q N_A x_p0 = q N_D x_n0 (Eq 5.34); E_peak = q N_D x_n0 / epsilon_s
  - typical values: potential drop across junction about 0.7 V (varies with doping); 60 mV per decade means free carriers fall 10x for each 60 mV into the region
  - approximations: depletion approximation (free carriers set to zero in the depletion region and to equilibrium outside, E=0 in neutral regions): reader argues the error is small because carriers fall tenfold per 60 mV
  - picture: charge box (negative left, positive right), field triangle peaking at the junction, and a potential S-curve (Figs 5.3, 5.4).
  - pitfalls: depletion region is not symmetric; the more heavily doped side has the narrower depletion width; peak field is always at the metallurgical junction; charges on both sides must be equal and opposite (no net charge)

- **built-in-potential**: the potential difference across the junction in equilibrium is the thermal voltage times the log of the doping product over n_i squared.
  - notation: phi_bi or phi_0 (V); phi_n - phi_p
  - formulas: phi_bi = phi_n - phi_p = V_th ln(N_A N_D / n_i^2); potential across P side = q N_A x_p0^2/(2 epsilon_s), across N side = q N_D x_n0^2/(2 epsilon_s) (reconstructed), sum = phi_bi
  - typical values: about 0.7 V for typical doping
  - approximations: depletion approximation; N_A, N_D >> n_i
  - picture: S-shaped potential falling from the N side (high) to the P side (low).
  - pitfalls: do not confuse with a battery

- **depletion-width**: both depletion depths grow with sqrt of the potential and shrink on the more heavily doped side; the total width is the sum.
  - formulas: x_n0 = sqrt( (2 epsilon_s phi_bi / q) (N_A/(N_D(N_A+N_D))) ); x_p0 = sqrt( (2 epsilon_s phi_bi / q) (N_D/(N_A(N_A+N_D))) ); X_dep0 = x_n0 + x_p0 = sqrt( (2 epsilon_s phi_bi / q)(1/N_A + 1/N_D) ) (all reconstructed, standard abrupt-junction results; N_A x_p0 = N_D x_n0)
  - typical values: epsilon_s = 11.7 epsilon_0 for Si (epsilon_0 = 8.85x10^-14 F/cm)
  - approximations: abrupt junction, depletion approximation
  - picture: sanity check: if N_A >> N_D then x_p0 -> 0 and all width goes into the lightly doped N side.
  - pitfalls: reader notes carriers cross the region at velocity-saturated speed because of the high field (the example numbers did not survive)

- **contact-potential**: attaching a metal wire adds contact potentials that exactly cancel the built-in potential, so a PN junction is not a battery.
  - notation: phi_mn, phi_mp contact potentials; N_m about 10^22 cm^-3 (metal modeled as very heavily doped); work functions
  - formulas: KVL around the shorted loop: phi_bi + phi_mp-side + phi_mn-side = 0 (reconstructed); with the P region as reference, n-region potential = V_th ln(N_A N_D/n_i^2) = phi_bi, metal potential V_th ln(N_m ... ) terms cancel
  - picture: shorted diode loop where every junction has its own step and the sum is zero (Fig 5.5).
  - pitfalls: thermodynamic argument, a diode as a perfect ratchet is impossible; reference changes between sections (intrinsic Si vs P region)

### 5.5 Reverse Biased PN Junction
- **pn-reverse-bias**: with no current the whole reverse voltage drops across the depletion region, which widens to uncover more fixed charge.
  - notation: V_D diode voltage (positive for forward, negative for reverse; reader's convention); Fig 5.6 shows V_D polarity
  - formulas: replace phi_bi with (phi_bi - V_D) in the depletion widths; X_dep = X_dep0 sqrt(1 - V_D/phi_bi); x_n = x_n0 sqrt(1 - V_D/phi_bi), similarly x_p; Q = A q N_D x_n = A sqrt(2 q epsilon_s (N_A N_D/(N_A+N_D)) (phi_bi - V_D)) (reconstructed)
  - typical values: reader says only a very small leakage current flows (see saturation current, Ch 6)
  - approximations: depletion approximation; abrupt junction; no current (so no voltage drop in neutral regions)
  - picture: depletion region widening like a dielectric slab between two charged plates as reverse bias grows.
  - pitfalls: sign check: V_D < 0 makes the depletion regions grow

- **depletion-capacitance**: the junction stores charge nonlinearly, and its small-signal capacitance is that of a parallel-plate capacitor with the depletion width as the plate spacing.
  - notation: C_j (F or F/cm^2), C_j0 zero-bias value, epsilon_s
  - formulas: C_j = dQ/dV_D magnitude; C_j0 = epsilon_s/X_dep0 per unit area; C_j = epsilon_s/X_dep = C_j0 / sqrt(1 - V_D/phi_bi) (abrupt junction, exponent 1/2); general C_j = C_j0/(1 - V_D/phi_bi)^m, m=1/2 for abrupt (reader's Fig 5.7 labels the curve n = 1/2)
  - typical values: epsilon_s = 11.7 epsilon_0
  - approximations: small signal, |v_D/V_D| << 1; abrupt junction
  - picture: incremental charge appears at the depletion edges, so it behaves as if metal plates sat at the edges of the depletion region (Section 5.5.4).
  - pitfalls: reader's C = epsilon/d uses the width at the operating point

- **varactor**: a reverse-biased junction used as a voltage-controlled capacitor to tune an LC oscillator.
  - notation: V_c control voltage (reverse bias), C_2 DC blocking capacitor, L, C tank
  - formulas: C_j(V_c) = C_j0/sqrt(1 - V_c/phi_bi); tank resonance f = 1/(2 pi sqrt(L C)) (standard, reconstructed; not displayed in the surviving text)
  - picture: capacitance-vs-reverse-voltage curve and an LC tank with a varactor (Fig 5.7).
  - pitfalls: nonlinear C-V is handled by the feedback loop in a PLL

## Chapter 6. PN Junction Currents

### 6.2 Qualitative Overview of Diode Currents
- **pn-equilibrium-currents**: at zero bias a small diffusion current (carriers that climb the barrier) is balanced by an equally small minority-carrier drift current.
  - picture: two opposed arrows of equal size (Fig 6.1).
  - pitfalls: only minority carriers generated within a diffusion length of the junction contribute drift current

- **pn-reverse-bias**: (current view) reverse bias raises the barrier, cutting diffusion exponentially, while minority drift current stays fixed, leaving a small saturation current.
  - notation: I_S saturation current (A)
  - formulas: drift current independent of barrier height; diffusion current proportional to exp(V_D/V_th); net reverse current -> -I_S
  - picture: barrier higher, diffusion arrow shrinks, drift arrow unchanged (Fig 6.2).

- **pn-forward-bias**: forward bias lowers the barrier, diffusion current grows exponentially, drift stays fixed.
  - formulas: net current dominated by diffusion; exponential from Boltzmann tail
  - picture: barrier lower, big diffusion arrow, minority carriers injected (Fig 6.3).

- **diode-iv**: the diode characteristic is an exponential in forward bias that saturates to -I_S in reverse.
  - notation: I_D diode current (A, positive from P to N); V_D (V); I_S (A); V_T = kT/q
  - formulas: I_D = I_S (exp(V_D/V_T) - 1); I_S = q A n_i^2 (D_n/(N_A W_p) + D_p/(N_D W_n)) for short diode (reconstructed; text says "linear profile" case)
  - typical values: V_T about 26 mV; current plotted against V_D/V_T from -10 to 4 in Fig 6.4
  - approximations: low-level injection; neglect of generation in depletion region; ideal series resistance zero
  - picture: curve with flat -I_S on the left and an exponential wall on the right (Fig 6.4).
  - pitfalls: reader warns that practical diodes have series resistance in P and N regions that can dominate

- **ic-diode-structure**: a real IC diode sits in an N-well on a P substrate with P and N+ diffusions; the substrate must sit at the lowest potential so the parasitic well-substrate diode stays reverse biased.
  - picture: cross-section with N-well, P diffusion, N+ ohmic contact, P+ substrate tap, parasitic diode (Fig 6.5).
  - pitfalls: N+ needed for ohmic contact; the unwanted diode must be reverse biased for isolation

### 6.3 Carrier concentration in Non-Equilibrium
- **recombination-generation-centers**: in silicon most generation and recombination happens through mid-gap traps, releasing phonons, not photons.
  - picture: bands with a trap level in mid-gap (Fig 6.6b).
  - pitfalls: direct band-to-band recombination is unlikely in Si

- **excess-carrier-recombination**: an excess of minority carriers decays at a rate proportional to the excess, with a lifetime.
  - notation: delta p, delta n excess minority concentration (cm^-3); tau_p, tau_n minority carrier lifetime (s); c_p capture constant; N_T trap density
  - formulas: R_net = -delta p / tau_p with 1/tau_p = c_p N_T (hole in N-type); likewise electrons in P-type with tau_n; n p != n_i^2 out of equilibrium, R > G
  - typical values: lifetime from nanoseconds to microseconds depending on material quality
  - picture: recombination exceeds generation when excess is present, so excess relaxes toward zero.
  - pitfalls: generation rate is unchanged; only recombination rises

### 6.4 Current Continuity Equation
- **continuity-diffusion-equation**: balancing minority carrier flow in and out of a slab with recombination gives a diffusion equation with a natural length.
  - notation: L_p = sqrt(D_p tau_p) diffusion length (cm or um); J_p(x)
  - formulas: d(delta p)/dt = -(1/q) dJ_p/dx - delta p/tau_p (hole continuity, reconstructed); steady state with diffusion only: d^2(delta p)/dx^2 = delta p / L_p^2; solution delta p(x) = delta p(0) exp(-x/L_p) for excess injected at x=0 and decaying to 0 at infinity; J_p(x) = (q D_p/L_p) delta p(0) exp(-x/L_p)
  - approximations: steady state; minority carriers move by diffusion only (field zero in neutral region)
  - picture: injected minority carriers exponentially decay over a few L_p while majority carriers come in to supply the recombination (Figs 6.8, 6.9).
  - pitfalls: total current constant in x, with majority current making up the difference to the decaying minority current (J_total - J_p(x))

### 6.5 Forward Biased PN-junctions
- **minority-carrier-injection**: forward bias raises the minority concentration at each depletion edge by an exponential factor of V_D/V_T over equilibrium.
  - notation: p_n(x_n), n_p(-x_p) minority concentrations at depletion edges; p_n0 = n_i^2/N_D, n_p0 = n_i^2/N_A
  - formulas: Boltzmann law: p_n(x_n) = p_n0 exp(V_D/V_T); n_p(-x_p) = n_p0 exp(V_D/V_T); (depends on phi_bi - V_D barrier, reconstructed as N_A and N_D on the other side of the junction: p_n = N_A exp(-(phi_bi - V_D)/V_T)); excess = p_n0 (exp(V_D/V_T) - 1)
  - typical values: n_i = 10^10 cm^-3
  - approximations: low-level injection (injected minority << majority: p_n << N_D, n_p << N_A); reader notes the law was derived in equilibrium and extended to non-equilibrium here
  - picture: bands: lowering barrier by V_D lets exponentially more carriers cross.
  - pitfalls: subscript notation is confusing, N_A and N_D in the formulas refer to the other side of the junction; setting V_D=0 gives back equilibrium

- **minority-profile-long-and-short**: minority carriers decay exponentially (long diode) or fall in a straight line (short diode, no recombination).
  - notation: W_n, W_p widths of the neutral regions (cm); L_n, L_p diffusion lengths
  - formulas: long diode: delta p(x) = delta p(x_n) exp(-(x - x_n)/L_p); short diode (L >> W): linear profile, delta p(x) = delta p(x_n)(1 - (x-x_n)/(W_n - x_n))
  - approximations: short diode requires L_{n,p} >> W_{n,p} or very large tau; long diode requires W >> L
  - picture: exponentially decaying tails vs straight ramps to zero at the contact (Figs 6.10, 6.11).
  - pitfalls: no recombination means uniform current so profile slope constant

- **diode-diffusion-current**: total current is the sum of the electron and hole diffusion currents at the depletion edges, both adding in the same direction.
  - formulas: J_n = q D_n (n_p0 (exp(V_D/V_T) - 1))/W_p, J_p = q D_p (p_n0 (exp(V_D/V_T)-1))/W_n; I = A(J_n + J_p) = I_S (exp(V_D/V_T) - 1) (linear-profile case, reconstructed)
  - picture: electrons flow one way, holes the other, but opposite charge makes the currents add.
  - pitfalls: negative charge and opposite direction => electron and hole currents add in phase

- **boltzmann-exponential-picture**: lowering a barrier by a given voltage exponentially increases the number of carriers that clear it.
  - picture: students taller than a threshold, shaded area of a Gaussian grows exponentially as the threshold falls (Fig 6.12).

### 6.6 Diode Small Signal Model
- **diode-small-signal**: around a DC bias the exponential I-V is linear for small signals, so the diode looks like a conductance equal to I_D/V_T.
  - notation: v_d small signal voltage (V); i_d small signal current (A); g_d small signal conductance (S); r_d = 1/g_d; I_D, V_D DC bias
  - formulas: I_D + i_d = I_S exp((V_D + v_d)/V_T) ~ I_D (1 + v_d/V_T); i_d = g_d v_d; g_d = dI_D/dV_D = I_D/V_T (forward, I_D >> I_S)
  - typical values: V_T about 26 mV; so g_d about 1/(26 mV) per amp: 1 mA gives r_d about 26 ohm
  - approximations: |v_d| << kT/q (about 26 mV); forward bias
  - picture: tangent line to the exponential at the bias point (Taylor series, linear term).
  - pitfalls: components are nonlinear in operating point, linear only for fixed bias and small swings

- **diffusion-capacitance**: stored minority charge is proportional to current, so the incremental charge for an incremental voltage looks like a capacitance that grows with bias current.
  - notation: Q_s stored charge (C); tau_F forward transit time (s); C_d (the reader labels it C with a subscript in Fig 6.14; the symbol did not survive) diffusion capacitance (F); C_j junction (depletion) capacitance (F)
  - formulas: Q_s = tau_F I_D; C_d = dQ_s/dV_D = tau_F g_d = tau_F I_D/V_T; total forward small-signal C = C_j + C_d; forward C_j approx 2 C_j0 (reader says "approximation for forward bias", the figure of the factor is missing; 2 C_j0 is the standard EE 105 choice, so treat as reconstructed)
  - typical values: tau_F is either the transit time (short diode) or the minority lifetime (long diode); lifetimes ns to us
  - approximations: Q_s proportional to I_D whatever the profile shape (linear or exponential)
  - picture: when forward bias rises the minority profile lifts, and the area between the curves is extra stored charge (Fig 6.13).
  - pitfalls: unlike a resistor, a diode stores net charge because current is diffusion; turn-off is slow because the profiles cannot collapse instantly

- **diode-circuits**: the complete small-signal model of a forward-biased diode is g_d in parallel with C_j + C_d; the same device acts as a switch (low impedance on, high impedance off), for example sharing an antenna.
  - formulas: model = g_d || (C_j + C_d) (Fig 6.14)
  - picture: equivalent circuit with v_d across g_d, C_j, and C_d in parallel.
  - pitfalls: model only valid for small incremental signals around a fixed operating point

### 6.7 Photonic Applications
- **photodiode-solar-cell-led** (solar cell I-V): a solar cell is a diode with a light-generated current that shifts the I-V curve into the fourth quadrant, where V and I have opposite signs and the cell delivers power.
  - notation: I_sc short-circuit current (A); V_oc open-circuit voltage (V); P_max maximum power (W); G_L optical generation rate (cm^-3 s^-1); I_light, I_dark
  - formulas: I_D = I_S (exp(V_D/V_T) - 1) - I_sc (reconstructed sign: reader plots I_sc as negative current in the fourth quadrant); power extracted when I x V < 0
  - typical values: efficiency 10% to 30%; 1 m^2 gives 25 W average, 150 W peak
  - approximations: uniform illumination in the N region, thin P+ layer
  - picture: dark diode curve shifted down by I_sc; the rectangle I times V at the maximum-power point (Fig 6.16).
  - pitfalls: passive sign convention: generation shows as negative I x V

- **optical-generation-excess**: uniform illumination gives a steady excess minority density equal to generation rate times lifetime.
  - formulas: delta p = G_L tau_p; from continuity: 0 = G_L - delta p/tau_p (no x variation)
  - picture: 10 arrivals per minute with a 5-minute stay gives 50 people in the room on average.

- **short-circuit-current-collection**: only carriers photogenerated within about one diffusion length of the depletion edge reach the junction, so I_sc is about q A G_L L_p.
  - formulas: boundary condition delta p(x_n) = 0 at zero bias, delta p(far) = G_L tau_p; delta p(x) = G_L tau_p (1 - exp(-(x - x_n)/L_p)); I_sc = q A L_p G_L (reconstructed: reader gives only the statement in words)
  - approximations: uniform G_L (only approximate in practice)
  - picture: shaded strip of width L_p next to the junction where photons contribute (Fig 6.18).

- **open-circuit-voltage**: setting total current to zero gives V_oc logarithmic in I_sc/I_S, which rises with lifetime.
  - formulas: V_oc = V_T ln(I_sc/I_S + 1) approx V_T ln(I_sc/I_S) (exponential dominates)
  - picture: the dark curve crossing the I = I_sc line.
  - pitfalls: a large tau_p, meaning good material, is what raises V_oc

- **led-direct-bandgap**: LEDs are forward-biased direct-gap diodes where injected minority carriers recombine radiatively, emitting photons at the gap energy.
  - notation: E_g (eV); h, nu, lambda; alpha absorption coefficient (1/cm or 1/m)
  - formulas: h nu = hc/lambda = E_g; lambda (um) = 1.24 / E_g (eV) (reconstructed; Eq 6.47); light intensity decays as exp(-alpha x)
  - typical values (Table 6.1, E_g in eV and lambda in um): InAs 0.35, 3.51; InN 0.65, 1.91; InP 1.34, 0.92; GaAs 1.43, 0.87; GaP 2.26, 0.55; AlP 2.45, 0.51; GaN 3.40, 0.37; AlN 6.20, 0.20. The colour column in the table is garbled in places (it lists GaAs as red although 0.87 um is infrared; InP likewise)
  - approximations: photon absorbed only if E = hc/lambda > E_g
  - picture: E-k diagram, direct gap vertical jump with photon vs indirect gap needing a phonon for momentum (Fig 6.20).
  - pitfalls: silicon is indirect, so most recombination is trap-assisted and wasted as phonons; most LEDs use III-V direct-gap compounds

## Notation and conventions for these chapters

| symbol | meaning | unit | sign convention |
|---|---|---|---|
| q or e | electron charge magnitude (reader uses both) | C | positive number; electron charge is -q |
| n, p | free electron, free hole concentration | cm^-3 | positive; n0, p0 at equilibrium |
| n_i | intrinsic carrier concentration | cm^-3 | 10^10 at 300 K |
| N_D, N_A | donor, acceptor concentration | cm^-3 | N_D^+ and N_A^- are ionized densities |
| mu_n, mu_p | electron, hole mobility | cm^2/(V s) | positive; v_d = -mu_n E for electrons, +mu_p E for holes |
| D_n, D_p | diffusion constant | cm^2/s | D = mu kT/q |
| J | current density | A/cm^2 | J_n,diff = +q D_n dn/dx, J_p,diff = -q D_p dp/dx |
| E | electric field | V/cm | E = -dphi/dx; points from + to - |
| phi | electrostatic potential | V | referenced to intrinsic Si in 5.3; to the P region in 5.4.7 |
| phi_n, phi_p | doped-region potential vs intrinsic | V | phi_n > 0 (N-type), phi_p < 0 (P-type) |
| phi_bi | built-in potential | V | N side higher; about 0.7 V |
| V_th, V_T, phi_T | thermal voltage kT/q | V | about 26 mV at 300 K; about 60 mV per decade of n |
| V_D | diode voltage, P side minus N side | V | V_D > 0 forward, V_D < 0 reverse |
| I_D | diode current | A | positive from P to N through the diode |
| I_S | saturation current | A | reverse current is -I_S |
| x_p0, x_n0 | depletion edges in equilibrium | cm | P edge at -x_p0, N edge at +x_n0, junction at x = 0 |
| X_dep, X_dep0 | total depletion width (biased, zero bias) | cm | grows with reverse bias |
| epsilon_s | silicon permittivity | F/cm | 11.7 epsilon_0 |
| C_j, C_j0 | depletion (junction) capacitance, zero-bias value | F | decreases with reverse bias |
| tau_p, tau_n | minority carrier lifetime | s | ns to us |
| L_p, L_n | diffusion length sqrt(D tau) | cm | |
| tau_F | forward transit time or lifetime | s | Q_s = tau_F I_D |
| Q_s | stored minority charge | C | |
| g_d | diode small-signal conductance I_D/V_T | S | lowercase v_d, i_d for small signals |
| delta p, delta n | excess minority concentration | cm^-3 | zero in equilibrium |
| G, R, G_L | generation, recombination, optical generation rates | cm^-3 s^-1 | |
| R_sq | sheet resistance (written with a square symbol) | ohm/sq | R = R_sq L/W |
| I_sc, V_oc | short-circuit current, open-circuit voltage | A, V | solar cell operates where I V < 0 (fourth quadrant) |
| E_g | band gap | eV | about 1.1 eV for Si, 25 meV is kT |
| j | imaginary unit | | (not used in these chapters) |

## Where a visual would help most

1. **Doping vs potential vs carriers (potential-vs-doping, mass-action-law).** Drag N_D (or N_A) on a log slider from 10^10 to 10^18 cm^-3. Bars for n and p on a log axis move in opposite directions, and a ruler shows phi_n or phi_p about intrinsic. What should click: np stays pinned at n_i^2, and each decade of doping is the same 60 mV step.

2. **Drift versus diffusion balance in equilibrium (drift-diffusion-balance, pn-equilibrium).** Drag a concentration profile n(x) from flat to steep and watch a field E(x) and a potential step build to cancel the diffusion flux. What should click: a gradient forces a field, and the potential step is V_th times the log of the concentration ratio.

3. **Depletion region builder (depletion-region, depletion-width).** Sliders for N_A and N_D (log) and reverse bias V_D. The charge-density rectangles, the triangular field and the S-shaped potential redraw, with x_n, x_p and E_peak shown. What should click: equal charge on both sides forces the lightly doped side to be wider, and the field always peaks at the junction.

4. **Reverse-bias capacitor (depletion-capacitance, varactor).** Drag V_D from 0 to a large reverse bias; the depletion plates move apart and the C_j(V) curve gets a marker at the matching point, and an LC tank frequency readout shifts. What should click: C_j = epsilon_s/X_dep, and capacitance falls as 1/sqrt(1 - V_D/phi_bi).

5. **Barrier height and the exponential (pn-forward-bias, boltzmann-exponential-picture, diode-iv).** Drag V_D across the band-diagram barrier; show the Gaussian tail of carriers above the barrier and a live I-V point. What should click: 60 mV of barrier change is a 10x change in current, which is why the diode is a near-switch.

6. **Minority carrier profile (minority-profile-long-and-short, continuity-diffusion-equation).** Sliders for V_D, diffusion length L_p and neutral width W_n. Exponential or linear profile redraws, with the diffusion current slope shown. What should click: when L is much larger than W the profile straightens and I_S depends on 1/W; when L is much smaller it decays over L.

7. **Small-signal diode and its capacitances (diode-small-signal, diffusion-capacitance).** Drag the DC bias point along the exponential, with a small signal wiggle; show the tangent line, g_d = I_D/V_T, and bars for C_j and C_d. What should click: g_d and C_d both scale with bias current, so r_d falls and C_d rises together while C_j barely changes.

8. **Solar-cell I-V (photodiode-solar-cell-led).** Drag illumination G_L (or I_sc) and a load line; the dark curve shifts down, V_oc and I_sc markers move, and the max-power rectangle slides. What should click: I_sc scales with light, V_oc only logarithmically, and power comes from the fourth quadrant.
