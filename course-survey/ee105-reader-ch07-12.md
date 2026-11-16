# EE 105 reader, chapters 7-12: concept notes

Source note: in the converted file almost every displayed equation is blank (only a few survive: Eq. 10.3, Eq. 11.4/11.5, Fig. 9.9 parameter box, a few figure labels). Formulas below are the standard forms that match the reader's symbols, signs and the surviving text clues. They are marked "(standard form, equation blank in conversion)" where the reader's own line is missing. Numeric values are the reader's unless marked "(my arithmetic)".

## Chapter 7. MOS Capacitor

### 7.2 MOS Capacitor Structure
- **mos-capacitor**: Two plates around a thin oxide, gate on top and a semiconductor body below; because the body is a semiconductor, charge on that plate can be depletion charge or an inversion sheet, so it is not a normal capacitor.
  - notation: G gate, B body; eps_ox = 3.9 eps_0, eps_s = 11.7 eps_0 (F/cm); t_ox (nm); x measured into the body, x = -t_ox at the gate, x = 0 at the oxide/Si interface; N_A (cm^-3)
  - typical values: t_ox ~ 1 nm in Fig. 7.1 (modern), 20 nm in the numeric example; N_A = 5e16 cm^-3; n+ poly gate potential ~ 550 mV if doping not given
  - approximations: poly-n+ gate treated as degenerately doped, so phi_gate = +550 mV
  - picture: sandwich of gate, SiO2, and silicon body. NMOS-C has a P-type body, PMOS-C an N-type body: the flavor is named for the carriers of the inversion layer, not the body doping.
  - pitfalls: "NMOS capacitor uses P-type substrate" is not a typo. Gate was metal until ~1970, then poly-Si, metal again after 2008. High-k stacks are used because oxide cannot be thinned further (leakage, breakdown).
- **mos-built-in-potential**: With gate shorted to body, the n+ gate sits above the p body by a built-in potential, like a PN junction, and that voltage splits across the oxide and a surface depletion region.
  - notation: phi_p (V, negative for P-type, = -(kT/q) ln(N_A/n_i)), phi_gate (V), phi_bi = phi_gate - phi_p (V)
  - formulas (standard form, equation blank in conversion): phi_p = -(kT/q) ln(N_A/n_i); phi_gate = +(kT/q) ln(N_D/n_i), about 550 mV for degenerate doping; phi_bi = phi_gate - phi_p
  - picture: a PN junction whose "N side" is the gate and whose field lines cross an oxide. In equilibrium gate carries + charge, body carries - depletion charge.
  - pitfalls: Contact potentials cancel around the loop, so a metal wire to the gate and body gives the same result as the poly wire in Fig. 7.3. Ohmic contact to body uses a p+ region.

### 7.3 MOS Regions of Operation
- **flatband-voltage**: The gate-body voltage that cancels the built-in potential so that charge and field are zero everywhere and the bands are flat.
  - notation: V_FB (V), Q_G(V_FB) = 0
  - formulas: V_FB = -phi_bi = -(phi_gate - phi_p) (standard form, equation blank)
  - typical values: example (my arithmetic, n_i = 1e10 cm^-3, kT/q = 26 mV): phi_p ~ -0.40 V, V_FB ~ -0.95 V
  - picture: bias the capacitor until it is "reset": no field, no depletion, no charge.
  - pitfalls: V_FB is negative for an NMOS-C with n+ gate.
- **mos-accumulation-depletion-inversion**: Sweeping V_GB up from very negative moves the body surface through accumulation, depletion and inversion; the body charge changes from holes to ionized acceptors to an electron sheet.
  - notation: V_GB (V), Q_G, Q_B = -Q_G (C/cm^2), x_dep or X_d (cm), V_ox, V_dep, Psi_s surface potential (V), Q_N inversion charge
  - formulas: accumulation V_GB < V_FB: Q_G = C_ox (V_GB - V_FB), Q_B = |Q_G| (holes at surface). Depletion V_GB > V_FB: Q_B = -q N_A X_d(V_GB), V_GB = V_FB + V_ox + V_dep. Inversion V_GB = V_T: surface electron density = N_A (equal to background ion density), Psi_s = -2 phi_p = 2|phi_p|.
  - approximations: depletion approximation (fully depleted, abrupt edge, uniform N_A); quasi-static (thermal generation has time to supply electrons)
  - picture: field lines leaving the gate must end on charge: holes at the surface, then ionized dopants spread through depth, then an electron sheet at the surface.
  - pitfalls: Depletion charge is not minority carriers; in depletion the gate pulls the surface potential up by an increasing drop across the depletion region. Past V_T depletion width stops growing and extra charge is inversion charge. After a fast step there is not time for generation, so the response comes from the depletion region.

### 7.4 MOS Device Threshold Voltage
- **threshold-voltage**: V_T is the gate-body voltage at which the surface goes from P-type to N-type, found by adding the flatband voltage, the surface potential 2|phi_p|, and the oxide drop needed to terminate the maximum depletion charge.
  - notation: V_T (V), V_Tn, phi_p (V), Q_B,max (C/cm^2), C_ox (F/cm^2)
  - formulas (standard form, equations blank): V_T = V_FB + 2|phi_p| + |Q_B,max|/C_ox; |Q_B,max| = sqrt(2 q eps_s N_A (2|phi_p|)); V_GB = V_ox + V_dep (KVL around the structure)
  - typical values: example, t_ox = 20 nm, N_A = 5e16 cm^-3: C_ox about 173 nF/cm^2 (my arithmetic); V_T about 0.5 V (my arithmetic)
  - approximations: zero inversion charge at the edge of inversion (inversion charge is small even though density is high); full depletion
  - picture: V_GB is split between two series drops, oxide and depletion region; V_T is the point where the second drop reaches 2|phi_p|.
  - pitfalls: Built-in voltage appears twice with opposite polarity in the loop and drops out.

### 7.5 Fields and Potential in Oxide/Substrate
- **mos-fields-potential**: Field is constant in the oxide, jumps down by eps_ox/eps_s (about 3.9/11.7, a factor of three) at the interface, then falls linearly to zero at the depletion edge; potential is linear in oxide and quadratic in the body.
  - notation: E_ox, E(x), phi(x), Psi_s = phi(0), phi_gate, x_dep
  - picture: field plot with a flat top in the oxide, a step down at x = 0, then a ramp to zero at x_dep; the potential is the integral of it.
  - pitfalls: The field discontinuity is from permittivity, not charge at the interface.

### 7.6 Charge-Voltage and Capacitance-Voltage Curves
- **mos-cv-curve**: The small-signal capacitance is the slope of the Q-V curve: C_ox in accumulation, a dip in depletion, and C_ox again in inversion (quasi-static).
  - notation: C (F/cm^2 or F), C_ox, C_dep, breakpoints V_FB and V_T
  - formulas: C_ox = eps_ox / t_ox; C_dep = eps_s / x_dep (standard form); depletion: C = C_ox in series with C_dep = C_ox C_dep / (C_ox + C_dep), x_dep evaluated at the operating point
  - picture: Q-V is linear, then sublinear in depletion, then linear again; C-V is flat, a valley, flat. Dashed curve shows the real smoothing.
  - pitfalls: Capacitance is small-signal (incremental). In inversion the depletion layer is "frozen" and does not appear in the small-signal circuit. Depletion capacitance is nonlinear because x_dep depends on bias.
- **mos-numerical-example**: Worked numbers for the capacitor.
  - typical values: P-type body, t_ox = 20 nm, N_A = 5e16 cm^-3, gate treated as +550 mV. Device in accumulation has the whole V_GB across the oxide, E_ox = V_ox / t_ox, body charge is holes.

## Chapter 8. MOSFET Device Physics

### 8.2 Device Layout and Cross Section
- **mosfet-structure**: A MOSFET is a MOS capacitor with two diffusions of the opposite doping type on either side of the gate; below threshold they are back-to-back diodes, above it the inversion channel joins them.
  - notation: G, B, S, D; W width (um), L channel length (um), L_min, t_ox, N_A, x_j junction depth
  - picture: planar cross-section: gate over a channel, n+ source and drain in a p substrate, with the top view setting W and L.
  - typical values: L down to 7 nm in digital, 22 nm for RF, about 1 um for power/automotive
  - pitfalls: Designer controls only W and L; x_j, t_ox, N_A are process parameters. Source and drain are physically the same: they are defined by bias and schematic. Larger W gives more current, shorter L gives a more conductive channel.
- **nmos-pmos-cmos**: NMOS sits in a P-type body with n+ S/D; PMOS sits in an N-type body (an n-well in CMOS) with p+ S/D; the body of NMOS goes to ground (lowest potential), the PMOS body to the supply (highest) so junctions stay reverse biased.
  - notation: symbols with arrow (analog use) vs bubble on PMOS gate (digital use); the arrow marks conventional current direction
  - pitfalls: Carriers in NMOS go S to D but current goes D to S. In PMOS holes go S to D and so does current. When the body is omitted from a schematic it is understood to be at ground (NMOS) or supply (PMOS).

### 8.3 NMOSFET Large Signal Models and Regions
- **mosfet-regions**: Cut-off, triode (including linear) and saturation, set by V_GS against V_T and V_DS against V_GS - V_T.
  - notation: V_GS, V_DS, V_GB, V_T, V_OV or V_od = V_GS - V_T, V_DS,sat = V_GS - V_T, I_DS
  - formulas: cut-off V_GS < V_T, I_DS = 0 (sub-threshold ignored); linear V_GS > V_T and V_DS << V_GS - V_T; triode V_GS > V_T and V_DS < V_GS - V_T; saturation V_GS > V_T and V_DS > V_GS - V_T = V_DS,sat
  - picture: I-V family: curves rise like a resistor, bend over, then go flat (a current source). Dashed line is the border V_DS = V_GS - V_T.
  - pitfalls: Sub-threshold current ignored on purpose (explained with BJT). In a BJT "saturation" means low V_CE, the opposite end of the curves from MOS saturation. Breakdown limits V_DS.
- **mosfet-iv-curves**: Two experiments: I_DS vs V_GS at fixed V_DS (zero, then a rise to linear-ish growth) and I_DS vs V_DS at fixed V_GS (a family).
  - picture: transfer curve with a threshold knee; output family, each curve labeled by V_GS.

### 8.4 Derivation of MOSFET I-V Curve
- **mosfet-linear-region**: With a uniform channel, current is charge per area times width times drift velocity, giving a voltage-controlled conductor.
  - notation: Q_N inversion charge per area (C/cm^2), W, v_y carrier velocity (cm/s), mu_n (cm^2/Vs), mu_n C_ox (A/V^2), G_DS (S), R_DS (ohm), R_square sheet resistance
  - formulas (standard form): I = W Q_N v_y; Q_N = -C_ox (V_GS - V_T); v_y = -mu_n E_y; E_y = V_DS / L; I_DS = mu_n C_ox (W/L)(V_GS - V_T) V_DS; G_DS = mu_n C_ox (W/L)(V_GS - V_T); R_DS = 1/G_DS = R_square L/W with R_square = 1/(mu_n C_ox (V_GS - V_T))
  - approximations: uniform channel and small V_DS
  - picture: channel as a sheet resistor whose sheet resistance falls with overdrive; V_GS tunes the resistor.
  - pitfalls: To get more conductance use higher mu, C_ox, overdrive or W/L.
- **mosfet-triode-square-law-derivation**: Inversion charge is largest at the source and smaller toward the drain, since the gate-to-channel voltage drops with channel potential; including this gives inverted parabolas in V_DS.
  - notation: V_ch(y) channel potential (V), V_GD = V_GS - V_DS, Q_N(y)
  - formulas (standard form): Q_N(y) = -C_ox (V_GS - V_ch(y) - V_T); I_DS = mu_n C_ox (W/L)[(V_GS - V_T) V_DS - V_DS^2/2]. Reader's first approach averages source and drain charge; second integrates I_DS dy = W mu_n C_ox (V_GS - V_ch - V_T) dV_ch from 0 to V_DS (equivalent result, called the less hand-wavy one).
  - approximations: threshold held constant along the channel (the body-effect variation with V_ch is ignored)
  - picture: two competing effects of larger V_DS: larger lateral field (more current) and less channel charge (less current); they bend the line into a parabola.
  - pitfalls: The triode formula peaks at V_DS = V_GS - V_T and then falls, which is not observed in a real device (Fig. 8.14 vs 8.15), hence the need for a saturation explanation.

### 8.5 Understanding Current Saturation (Pinch Off)
- **pinch-off**: When V_DS exceeds V_DS,sat = V_GS - V_T the channel charge goes to zero at the drain end; the excess V_DS - V_DS,sat drops across a short high-field region and carriers are swept through it, so current stays fixed.
  - notation: V_DS,sat, E_d,sat, E_d, V_DS - V_DS,sat
  - picture: water flows down a slope of fixed height then over a waterfall; slope sets flow, waterfall height does not.
  - pitfalls: The word "pinch-off" suggests zero current; current does not drop. Velocity saturation is a second, different mechanism that also flattens the curve in short devices.
- **square-law**: In saturation the current is set by the gate overdrive and not by the drain.
  - notation: I_DS,sat (A), V_OV, mu_n C_ox (A/V^2), W/L
  - formulas (standard form): I_DS = (1/2) mu_n C_ox (W/L)(V_GS - V_T)^2 [saturation, lambda = 0]; with CLM I_DS = (1/2) mu_n C_ox (W/L)(V_GS - V_T)^2 (1 + lambda V_DS). Obtained by setting V_DS = V_GS - V_T in the triode equation.
  - picture: ideal voltage-controlled current source (VCCS), the basic action of an amplifier.
  - pitfalls: Factor of 1/2 (kept in the reader's form).
- **channel-length-modulation**: Above V_DS,sat the pinch-off point moves toward the source, shrinking L to L - dL, so the current rises slowly with V_DS; modelled by lambda.
  - notation: lambda (V^-1), V_A = 1/lambda (V) "Early voltage" (the reader uses this name for MOS too), dL
  - formulas (standard form): I_D(L-dL) ~ I_D(L)(1 + dL/L) for dL << L; dL/L = lambda V_DS to first order; I_DS = I_D,sat (1 + lambda V_DS)
  - approximations: long channel, dL << L
  - picture: shorter effective channel, steeper current; saturated curves tilt upward and meet at -V_A on the V_DS axis.
  - pitfalls: lambda is called the Early voltage (inverse), after the BJT effect.
- **mosfet-region-summary**: Summary list of conditions and currents (cut-off I = 0; linear small V_DS; triode with square-law bracket; saturation with CLM).

### 8.6 The Complementary PMOS Device
- **pmos**: PMOS equations are the NMOS ones with all voltages and currents flipped; write with I_SD, V_SG, V_SD and |V_T| and the curves look right-side-up.
  - notation: I_SD (A), V_SG, V_SD (positive in forward active), V_T for PMOS is negative, use |V_T|; mu_p C_ox
  - formulas (standard form, equation blank): I_SD,sat = (1/2) mu_p C_ox (W/L)(V_SG - |V_T|)^2 (1 + lambda V_SD)
  - typical values: Fig. 8.19 curves with V_GS = -2, -3, -4 V; Fig. 8.20 with V_SG = 1 to 4 V
  - picture: Fig. 8.19 (V_DS, I_DS) is the NMOS plot rotated 180 degrees; Fig. 8.20 (V_SD, I_SD) is upright.
  - pitfalls: Keep the same polarity as NMOS and everything is upside down; define I_SD instead. Holes carry current S to D, same direction as the arrow.

## Chapter 9. MOS Transistor Small-Signal Models

### 9.2 Introduction to Amplifiers
- **common-source**: NMOS with source on the common node, gate as input, drain through R_D to V_DD as output; biased in saturation so a gate signal makes a drain current that makes a larger drain voltage.
  - notation: V_GS DC gate bias, v_s input signal, v_GS = V_GS + v_s, v_o output, R_D, V_DD (supply "rail")
  - picture: Fig. 9.4: a sine at input and an amplified, inverted sine at output (about +/-150 mV axis, gain 16). The DC is subtracted out.
  - pitfalls: Common-source gain is always inverting. Three topologies exist because each terminal can be common: CS, CG, CD.
- **mos-amplifier-vccs**: In saturation the drain current depends on V_GS and barely on V_DS, so the transistor is a transconductor G_m(V_GS) with output resistance R_o in parallel.

### 9.3 Operating Points
- **operating-point**: The DC bias (Q-point or quiescent point) fixes I_DS,Q, V_DS,Q and every small-signal parameter; the signal rides on top of it.
  - notation: V_GS,Q, I_DS,Q, V_DS,Q, V_GS (capital, DC), v_gs (lower, signal), v_GS (lower with capital subscript, total)
  - formulas: mid-rail design: V_DS,Q = V_DD/2; I_DS,Q = (V_DD - V_DS,Q)/R_D = V_DD/(2 R_D); I_DS,Q = (1/2) mu_n C_ox (W/L)(V_GS - V_T)^2; check V_DS,sat = V_GS - V_T < V_DS,Q
  - typical values: W = 40 um, L = 2 um, R_D = 25 kohm, mu_n C_ox = 100 uA/V^2, V_T = 1 V, V_DD = 5 V. Result: I_DS,Q = 100 uA, V_GS - V_T about 0.32 V (0.316), V_GS about 1.32 V, V_DS,sat 0.32 V < V_DS 2.5 V.
  - approximations: lambda ignored in the bias calculation
  - picture: marked point on the I-V curve; AC wiggles v_gs, i_ds, v_ds around it (Fig. 9.5, 9.6).
  - pitfalls: Mid-rail is a design choice, not a requirement (back-of-envelope max swing when V_DS,sat is small). Output can neither exceed V_DD nor go below V_GS - V_T and stay in saturation. Always check self-consistency (is it in saturation?).
- **small-signal-approximation**: Because I_DS is quadratic in V_GS, a small v_gs gives a linear change in i_ds; the quadratic term is dropped when v_gs << V_GS - V_T.
  - formulas: I_DS = (1/2) k (V_GS + v_gs - V_T)^2 = I_DS,Q (1 + v_gs/(V_GS - V_T))^2, expand (1+x)^2 = 1 + 2x + x^2, drop x^2 when x << 1. Then i_ds = 2 I_DS,Q v_gs/(V_GS - V_T)
  - approximations: x = v_gs/(V_GS - V_T) << 1; lambda and charge storage ignored in "hard way"
  - picture: tangent line to the I_DS vs V_GS parabola at the Q-point.
  - pitfalls: Small is defined relative to overdrive, not relative to V_DD.
- **cs-gain-hard-way**: Output vo = V_DD - I_DS R_D, expand the quadratic, bias terms cancel to leave v_o = -(2 I_DS,Q R_D/(V_GS - V_T)) v_s = -(V_DD/(V_GS - V_T)) v_s for mid-rail bias.
  - typical values: V_DD/(V_GS - V_T) = 5 V / 0.32 V gives gain of 16
  - pitfalls: To raise gain: higher V_DD, lower overdrive V_OD = V_GS - V_T. Gain is inverting.

### 9.4 Small-Signal Approach
- **small-signal-analysis-steps**: Five steps: find the DC point, get region and parameters, kill DC sources (shorts for voltage, opens for current), swap in the small-signal model, solve like any linear AC circuit.
  - notation: i_ds = g_m v_gs + g_o v_ds; I_DS = I_DS,Q + i_ds
  - picture: redraw circuit, combine R_D with r_o in parallel by inspection (Fig. 9.12).
  - pitfalls: DC supplies are AC grounds. Once the Q-point is chosen the small-signal parameters are fixed.
- **transconductance**: g_m is the slope of the I_DS vs V_GS curve at V_DS = V_DS,Q; it grows with overdrive and as sqrt(I_DS).
  - notation: g_m (S or mA/V) = dI_DS/dV_GS at Q
  - formulas (standard form): g_m = mu_n C_ox (W/L)(V_GS - V_T) = sqrt(2 mu_n C_ox (W/L) I_DS) = 2 I_DS/(V_GS - V_T)
  - typical values: example bias gives g_m = 2(100 uA)/0.316 V about 0.63 mS (my arithmetic)
  - picture: tangent slope on the transfer curve (Fig. 9.7).
  - pitfalls: The 2 I_DS/(V_GS - V_T) form is the one used to compare against specifications (it appears in the reader's parameter box).
- **output-resistance**: r_o = 1/g_o is the reciprocal slope of the saturated I_DS vs V_DS curve; set by lambda and the bias current.
  - formulas (standard form): g_o = dI_DS/dV_DS = lambda I_D,sat/(1+lambda V_DS) about lambda I_DS; r_o about 1/(lambda I_DS) = V_A/I_DS
  - approximations: lambda small, so (1 + lambda V_DS) about 1
  - picture: non-zero tilt of the flat part of the I-V curves (Fig. 9.8); r_o falls as the current is raised.
- **mos-small-signal-model**: Three-terminal model: a controlled current source g_m v_gs in parallel with r_o between drain and source; gate draws no current.
  - notation: v_gs (V), g_m v_gs (A), r_o (ohm), i_ds
  - picture: gate port is open (no current); output port has a current source and a resistor.
  - pitfalls: Common-source voltage gain A_v = -g_m (r_o || R_D); the reader notes this seems to disagree with the hard-way result until g_m is written in terms of bias (g_m R_D = V_DD/(V_GS - V_T) at mid-rail, r_o ignored).
- **intrinsic-gain**: Reader names A_0 = g_m r_o (the stage's maximum gain with no load) and uses it later in the CG input resistance.
  - formulas: A_0 = g_m r_o (standard), about 2/(lambda (V_GS - V_T)) (standard)

### 9.5 PMOS Amplifier and Small-Signal Model
- **pmos-small-signal**: The PMOS model is the NMOS model flipped: current source g_m v_sg points S to D, controlled by v_sg; the CS circuit with a PMOS is the same AC circuit as the NMOS one.
  - notation: v_sg, i_sd, V_SG
  - picture: wiggle test: raise the PMOS gate, inversion falls, current falls, model shows negative i_sd.
  - pitfalls: A PMOS with the source on V_DD is still "common source" since the supply is an AC ground. NMOS preferred (higher mu, higher g_m), but PMOS gives flipped bias in cascades and avoids large coupling capacitors.

### 9.6 What We've Ignored
- **second-order-effects-list**: Not yet in the model: body (back-gate), source/drain junction capacitance, gate capacitance, short-channel and velocity saturation, and weak/moderate inversion (still a transistor for AC signals).

## Chapter 10. Complete MOS Small-Signal Model

### 10.2 MOSFET Capacitance in Saturation
- **mos-capacitances**: Gate-source, gate-drain, drain-body and source-body capacitances; C_gs is the intrinsic channel part plus overlap, C_gd is only overlap and fringing in saturation, C_db and C_sb are reverse-biased junctions.
  - notation: C_gs, C_gd, C_db, C_sb (F), C_ov overlap, C_fringe, L_ov overlap length, C_j,A (area), C_j,sw (sidewall), junction area A = L_j W, perimeter P = 2 L_j + W
  - formulas: C_gd = C_ov + C_fringe = L_ov W C_ox + C_fringe (Eq. 10.3, survived). C_gs = (2/3) W L C_ox + C_ov (standard form; reader gives the factor 2/3 in prose). C_db, C_sb from area and perimeter terms with the PN-junction form C_j0/sqrt(1 + V_R/phi_0) (grading coefficient 1/2).
  - approximations: saturation: drain is cut off from the channel, so C_gd is overlap only; C_sb drops out if source and body are both AC grounded.
  - picture: wedge-shaped inversion charge gives 2/3 W L C_ox; overlap and fringing on both source and drain sides; five junction walls per diffusion.
  - pitfalls: Overlap capacitance is parasitic. L_ov << L so C_gd << C_gs. The inner junction face toward the channel is not counted in perimeter. Source and drain are symmetric in process; assignment comes from bias.
- **three-terminal-model-with-caps**: Fig. 10.5: C_gs from G to S, C_gd from G to D, C_db from D to the S/B node, with g_m v_gs and r_o; these produce poles and zeros that limit bandwidth.

### 10.3 Back-Gate Effect
- **body-effect**: The body acts as a second, weaker gate; raising source-to-body voltage V_SB raises V_T.
  - notation: V_SB = -V_BS (V), V_T0 zero-bias threshold (V), gamma (V^(1/2)), C_dep, C_ox
  - formulas (standard form, equations blank): V_T = V_T0 + gamma(sqrt(2|phi_p| + V_SB) - sqrt(2|phi_p|)); gamma = sqrt(2 q eps_s N_A)/C_ox. Charge: Q_N = -C_ox(V_GS - V_T) - C_dep V_BS... front gate acts through C_ox, back gate through C_dep.
  - picture: two gates on one channel, a strong front gate (C_ox) and a weak back gate (C_dep).
  - pitfalls: In most devices C_ox > C_dep. The body is usually tied to the source, which hides the effect.
- **back-gate-transconductance**: AC signal on the body gives a current via g_mb.
  - notation: g_mb (S), v_bs
  - formulas: g_mb = dI_DS/dV_BS = g_m (dV_T/dV_SB) in magnitude (standard form: g_mb = g_m gamma/(2 sqrt(2|phi_p| + V_SB))); the reader notes the guess g_mb = g_m C_dep/C_ox gives the same idea, and g_mb < g_m
- **mos-four-terminal-model**: i_ds = g_m v_gs + g_o v_ds + g_mb v_bs; two controlled sources (front and back) in parallel with r_o, plus capacitances C_gs, C_gd, C_db, C_sb. PMOS version uses v_sg, v_sb and i_sd.
  - picture: model without capacitors for low frequency, with capacitors for high frequency.

## Chapter 11. Bipolar Junction Transistors

### 11.2 Overview of BJT
- **bjt-structure**: An NPN or PNP sandwich with a thin, lightly-doped-relative-to-emitter base: emitter (heaviest doping), base (middle), collector (lightest).
  - notation: B, C, E; I_C, I_B, I_E (into the device in Fig. 11.5), V_BE, V_CE, V_CB; emitter area scales current
  - picture: two back-to-back diodes made useful because the base is thin, so electrons injected from the emitter reach the collector.
  - pitfalls: Collector and emitter cannot be swapped: reverse active has poor gain because doping is unsymmetrical. Lateral BJT in CMOS has base set by lithography, worse performance. Every MOS has parasitic BJTs.
- **bjt-operation**: Forward-biased BE junction injects electrons into the base; if the base is much shorter than the diffusion length they diffuse to the reverse-biased BC junction and are swept into the collector.
  - notation: alpha_F, beta_F (current gain), minority-carrier profiles n_pB(x), p_nE(x), p_nC(x); W_B base width, W_E
  - formulas: I_C = alpha_F I_E (magnitude); I_B = I_E - I_C; beta_F = alpha_F/(1 - alpha_F); I_C = beta_F I_B (Eq. 11.4)
  - typical values: beta_F = 200 typical; example "1 in 1000 recombines" gives alpha_F = 0.999 and beta_F = 999
  - approximations: negligible recombination gives linear minority-carrier profile in the base; with recombination the profile curves
  - picture: large arrow of electrons emitter to collector; smaller arrows for holes into the emitter and for recombination (Fig. 11.8).
  - pitfalls: Never design relying on a specific beta_F; datasheets give ranges. Base current has two parts: hole injection into the emitter and recombination in the base.
- **bjt-iv**: Two views: I_C vs V_CE at fixed V_BE (flat, exponential spacing) and at fixed I_B (flat, linearly spaced, gain beta_F). Regions: forward active, saturation (low V_CE, BC forward biased), reverse active, breakdown.
  - formulas: I_C = I_S exp(q V_BE / kT) (Eq. 11.5); I_C = beta_F I_B (Eq. 11.4)
  - typical values: Fig. 11.6 curves V_BE = 590 to 640 mV in 10 mV steps with I_C up to about 125 uA; Fig. 11.7 I_B = 100 to 500 nA; kT/q about 26 mV
  - picture: V_BE family curves are spaced exponentially; I_B family curves are spaced equally.
  - pitfalls: "Saturation" in a BJT means low V_CE, the opposite of MOS saturation (forward active). BJT is a VCCS in voltage terms and CCCS in current terms.

### 11.5 BJT Device Physics with Equations
- **bjt-currents-and-gain**: I_C from electron diffusion in the base gives I_C = I_S exp(V_BE/V_T); I_B from hole diffusion into the emitter; the ratio gives beta_F, set by doping and base width.
  - formulas (standard forms, equations blank): I_S = q A_E D_n n_i^2/(N_A W_B); beta_F = I_C/I_B proportional to (N_E/N_B)(D_n/D_p)(W_E/W_B)
  - picture: dope emitter high relative to base and make the base thin to maximize beta_F.

### 11.6 Large and Small-Signal Equivalent Circuits
- **ebers-moll**: Two diodes with controlled sources: I_F (BE diode), I_R (BC diode), alpha_F I_F into the collector, alpha_R I_R into the emitter; reciprocity alpha_F I_ES = alpha_R I_CS.
  - formulas: I_F, I_R diode currents; neglecting I_R in forward active: I_C = alpha_F I_F (standard form)
  - pitfalls: Model is symmetric in C and E, but the currents differ.
- **early-effect**: V_CE rise widens the BC depletion region, narrowing the base, and I_C rises.
  - formulas: I_C = I_S exp(V_BE/V_T)(1 + V_CE/V_A) (standard form); r_o about V_A/I_C
  - notation: V_A Early voltage (V)
  - pitfalls: The reader cross-refers to the MOS lambda as 1/V_A.
- **bjt-simple-models**: Forward active: V_BE = 0.7 V (battery), I_C = beta I_B. Saturation: V_BE = 0.7 V, V_CE = 0.1 V (V_CE,sat = difference of two diode on-voltages).
  - typical values: V_BE = 0.7 V, V_CE,sat = 0.1 V
- **bjt-small-signal-model**: Hybrid-pi: R_pi between B and E, g_m v_pi source from C to E, r_o, plus C_pi, C_mu (B-C), C_cs (collector-substrate).
  - notation: v_pi (or v_in in Fig. 11.14) (V), R_pi (ohm), g_m, r_o, C_pi, C_mu = C_j,bc(V_BC), C_cs, tau_F forward transit time
  - formulas (standard forms): g_m = I_C/(kT/q) = q I_C/kT; R_pi = beta_F/g_m = v_pi/i_b; r_o = V_A/I_C; C_pi = C_diffusion + 1.4 C_j,be0-like junction term (the reader states a factor 1.4 for forward-bias junction capacitance); C_diff = g_m tau_F
  - typical values: kT/q about 26 mV at room temperature; the 1.4 factor
  - picture: like the MOS model but with a base resistor, because a base current path exists.
  - pitfalls: At fixed bias current g_m,BJT >> g_m,MOS because V_OV >> kT/q in strong inversion; shrinking V_OV toward kT/q means biasing a MOS as a BJT (sub-threshold) and costs speed.

## Chapter 12. Single-Stage Amplifiers

### 12.2 Two-Port Amplifiers
- **amplifier-two-port**: An amplifier is a unilateral linear two-port: input resistance R_in, output resistance R_out, and one internal gain. Four forms (voltage, current, transconductance, transresistance).
  - notation: v_in, v_out, i_in, i_out, R_S source, R_L load, R_in, R_out, A_v (V/V), A_i (A/A), G_m (S), R_m or R (ohm), Thevenin/Norton one-ports
  - formulas: voltage amp: v_out = A_v v_in; current amp: i_out = A_i i_in; transconductor: i_out = G_m v_in; transresistor: v_out = R i_in
  - approximations: unilateral: forward gain g_m >> reverse path j omega C_gd (or C_mu); true at low frequency
  - picture: boxes with R_in at the left, a dependent source and R_out at the right.
  - pitfalls: Ideal voltage amp: R_in large, R_out small. Ideal current amp: R_in small, R_out large. Ideal G_m amp: R_in and R_out both large. Ideal R_m amp: both small.
- **input-output-resistance**: Find R_in with a test source at the input and the load connected; find R_out with a test source at the output and the source resistance connected.
  - formulas: R_in = v_x/i_x with load attached (convention); R_out = v_x/i_x with source resistance attached, independent sources off
  - pitfalls: A real amp is not perfectly unilateral, so the convention for what terminates the other port matters.

### 12.3 Single-Stage MOS Amplifier Family
- **ac-coupling-and-bias**: Large capacitors (C_inf) act as batteries/shorts at signal frequency; large resistors or chokes (L_big) apply DC bias without shorting the signal; together a bias-T. Mid-band: large caps shorted, small (parasitic) caps open.
  - picture: Bode curve with a flat pass-band between omega_LF and omega_HF.
  - pitfalls: AC-coupled amps have zero DC gain.
- **common-gate**: Input at the source, output at the drain, gate AC-grounded; behaves as a current buffer with low input resistance and high output resistance, and as a non-inverting voltage amplifier.
  - notation: I_Q bias current, V_bias,Q gate bias, R_S, R_D, R_L, i_s, i_out
  - formulas: DC: I_DS = I_Q, V_GS set by I_Q. A_i = i_out/i_s = 1 (short the output; the source current has no other path out) - i.e. unity "intrinsic" current gain. Input: R_in = 1/g_m approx (standard: R_in = (r_o + R_D||R_L)/(1 + g_m r_o) which reduces to 1/g_m for r_o >> R_D||R_L and g_m r_o >> 1). Output: R_out = R_D || (r_o + g_m r_o R_S) = R_D || (r_o(1 + g_m R_S)), simplified to R_D || (g_m r_o R_S) for R_S > 1/g_m. Voltage amp with R_S = 0: A_v = +g_m (R_D || R_L) (non-inverting, same g_m as CS); with source resistance: divider gives G_m,eff = g_m/(1 + g_m R_S) and A_v = g_m (R_D||R_L)/(1 + g_m R_S).
  - typical values: input match to 50 ohm or 75 ohm lines for RF
  - approximations: r_o >> R_D || R_L; g_m r_o >> 1 (good intrinsic gain A_0 = g_m r_o)
  - picture: current in at the source passes straight to the drain; source resistance in series with the transistor on the source side boosts R_out by 1 + g_m R_S, versus +R_S if placed on the drain side.
  - pitfalls: Bias V_bias,Q does not change the AC result; it is there to give the current source headroom. R_in of the CG depends weakly on R_L. A CS is not a current buffer (fails unity gain and low-R_in).
- **common-drain**: Gate in, source out, drain at the supply (AC ground); a voltage buffer ("source follower") with gain a bit below 1 and R_out about 1/g_m.
  - notation: I_Q, V_bias,Q, r_oc (current source output resistance), R_L, R_S
  - formulas: DC: I_DS = I_Q, V_GS from I_Q (positive), gate must sit about V_GS above the source plus current-source headroom. A_v = g_m (r_o||r_oc||R_L)/(1 + g_m (r_o||r_oc||R_L)) < 1 (standard form of the reader's Eq. 12.32; the exact algebra is blank). Output resistance: R_out = (1/g_m) || r_o || r_oc, about 1/g_m for r_o||r_oc >> 1/g_m.
  - approximations: gate draws no current, so R_in is high at low frequency; r_o, r_oc >> 1/g_m
  - picture: source voltage follows gate voltage; v_gs = v_s - v_out is a small difference.
  - pitfalls: Gain is below one but power gain exists. Larger I_Q gives larger g_m and lower R_out (g_m grows as sqrt(I_DS)). Often used as a driver for small R_L.
- **source-degeneration**: The source resistor boost factor (1 + g_m R_S) applies to drain output resistance and divides transconductance (shown through CG output resistance and CG voltage-divider arguments).
  - formulas: R_out = r_o + g_m r_o R_S + R_S (full), or r_o(1 + g_m R_S) approx; G_m,eff = g_m/(1 + g_m R_S)
  - pitfalls: A resistor on the drain side only adds R_S; on the source side it multiplies by (1 + g_m R_S). The reader says the reason needs feedback theory (later).

### 12.5 Impact of Body Effect
- **cd-body-effect**: With the body grounded (not tied to the source), v_bs = -v_out, so the back-gate generator g_mb v_bs adds to the output conductance; gain falls and R_out falls.
  - formulas (standard form): A_v = g_m (R_L||r_o) / (1 + (g_m + g_mb)(R_L||r_o)) (reader's equation is blank; effect is g_m replaced by g_m + g_mb in the denominator only); R_out about 1/(g_m + g_mb)
  - pitfalls: Deep N-well (triple well) removes the effect but costs area and process cost. In a CS amplifier with source at ground v_bs = 0 so no effect.

### 12.6 Chapter Summary
- **amplifier-topology-summary**: CS = transconductance amp (high R_in, high R_out); CG = current buffer (low R_in = 1/g_m, high R_out); CD = voltage buffer (high R_in, R_out = 1/g_m, gain a bit below 1). BJT equivalents: CE, CB, CC.

## Notation and conventions for these chapters

| symbol | meaning | unit | sign convention |
|---|---|---|---|
| V_GB, V_GS, V_DS | gate-body, gate-source, drain-source (large signal) | V | NMOS: all positive in forward active, current I_DS flows D to S inside the device |
| V_SG, V_SD, I_SD | PMOS counterparts | V, A | Positive for forward-active PMOS; I_SD flows S to D (same as hole flow) |
| V_T | threshold voltage (NMOS positive) | V | PMOS: V_T is negative, write |V_T| in equations |
| V_FB | flat-band voltage | V | = -phi_bi, negative for n+ poly on P body |
| phi_p | P-type body potential relative to intrinsic | V | negative: phi_p = -(kT/q) ln(N_A/n_i); 2|phi_p| is the surface potential at inversion |
| V_OV = V_od = V_GS - V_T = V_DS,sat | overdrive / saturation voltage | V | positive in saturation |
| mu_n C_ox | process transconductance parameter | A/V^2 | typical 100 uA/V^2 |
| W, L | width, length | um | W/L aspect ratio |
| lambda, V_A = 1/lambda | CLM parameter, Early voltage | V^-1, V | positive |
| gamma | body-effect coefficient | V^(1/2) | positive |
| I_DS,Q, V_GS,Q, V_DS,Q | Q-point values | A, V | capital + Q subscript |
| v_gs, i_ds, v_ds, v_o, v_s | small-signal | V, A | lowercase symbol, lowercase subscript |
| v_GS, i_DS | total instantaneous | V, A | lowercase symbol, UPPERCASE subscript; v_GS = V_GS + v_gs, I_DS = I_DS,Q + i_ds |
| V_GS, I_DS | DC / large-signal bias | V, A | uppercase symbol, uppercase subscript |
| g_m | transconductance dI_DS/dV_GS | S | positive; g_m = 2 I_DS/(V_GS - V_T) |
| g_mb | back-gate transconductance | S | g_mb < g_m, driven by v_bs |
| g_o = 1/r_o | output conductance | S | about lambda I_DS |
| C_gs, C_gd, C_db, C_sb | MOS small-signal capacitances | F | C_gs about (2/3) W L C_ox + overlap in saturation |
| I_C, I_B, I_E | BJT terminal currents | A | into the device (Fig. 11.5) |
| V_BE, V_CE, V_BC | BJT junction voltages | V | NPN forward active: V_BE about 0.7 V, V_BC < 0 |
| alpha_F, beta_F | common-base and common-emitter current gain | -, - | beta_F typically 200 |
| V_T (BJT context) vs kT/q | the reader writes kT/q (26 mV) for thermal voltage | V | careful: V_T in the MOS chapters means threshold |
| R_pi, g_m, r_o, C_pi, C_mu | hybrid-pi elements | ohm, S, ohm, F | R_pi = beta_F/g_m |
| R_in, R_out, A_v, A_i, G_m | two-port parameters | ohm, V/V, A/A, S | Measured with load attached (R_in) and source resistance attached (R_out) |
| A_0 = g_m r_o | intrinsic gain | V/V | |
| R_S, R_D, R_L | source, drain, load resistance | ohm | |
| j | imaginary unit | | j omega C_gd form used in the unilateral argument |

Case rules: uppercase symbol with uppercase subscript = DC/bias; lowercase symbol with lowercase subscript = small signal; lowercase symbol with uppercase subscript = total; the "Q" subscript marks bias-point values. Reader uses "V_DS,sat" for the saturation boundary and sometimes the name "V_od".

## Where a visual would help most

1. **MOS-C band/charge versus gate voltage (accumulation, depletion, inversion)**. Drag V_GB; show charge layers (holes, depletion width, electron sheet), field and potential plots, and a marker on the Q-V and C-V curves. What should click: the depletion width stops growing at V_T because the next charge goes to the surface.
2. **C-V curve with oxide thickness and doping sliders**. Change t_ox and N_A; V_FB, V_T and the valley depth move. What should click: the valley is C_ox in series with C_dep.
3. **MOSFET channel pinch-off picture linked to the I-V family**. Drag V_DS at a fixed V_GS; watch the channel taper, pinch off at V_DS = V_GS - V_T, and the operating point slide along its curve. What should click: V_DS above V_DS,sat only moves the pinch-off point, so current barely changes.
4. **Triode vs saturation parabola**. Overlay the inverted parabola and the clipped flat line; toggle lambda. What should click: saturation is the peak of the parabola held flat, lambda tilts it.
5. **Common-source Q-point and load line**. Drag V_GS,Q, R_D, V_DD; the load line, Q-point, output swing and clipping limits move; sinusoid in and out. What should click: gain is about V_DD/V_OV at mid-rail and shrinks when swing runs into V_DS,sat or V_DD.
6. **Tangent line to the square law = small-signal model**. Drag the Q-point along the I_DS vs V_GS parabola and amplitude of v_gs; the tangent slope g_m and the error from the dropped x^2 term appear. What should click: small means v_gs << V_OV.
7. **Body effect / back gate**. Drag V_SB; V_T shifts and the second gate (C_dep) shows. What should click: body is a weak second gate, so g_mb < g_m, and source followers lose gain.
8. **Single-stage topologies: R_S, R_L, g_m sliders for CS, CG, CD**. Show R_in, R_out, gain and the two-port equivalent. What should click: source degeneration multiplies R_out by (1 + g_m R_S), CG is low-R_in, CD output looks like 1/g_m.

(BJT exponential vs MOS square-law g_m at equal I_C is also a good one if there is room: drag I_C, watch g_m = I_C/26 mV versus 2 I_D/V_OV.)
