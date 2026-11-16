# EE 105 reader, chapters 16-18: concept notes

Source: ee105_reader_v3 copy.md, lines 8489-10561. Almost every displayed equation is missing from the conversion (only the surrounding text, a few inline symbols and some figure labels survive). Where a formula below is marked "(reconstructed)", the text names the result in words and the form is the standard one consistent with that text; it is not read off the page. Where the text gives the formula in symbols, it is recorded as written. The reader's own equation numbers that appear in the text are noted where useful.

## Chapter 16. Differential Amplifiers

### 16.2 Motivation for Differential Operation
- **differential-vs-single-ended**: A differential signal rides on two wires with equal and opposite halves, self-referenced, so interference that hits both wires equally (common-mode) drops out of the difference.
  - notation: v_dm (differential-mode, V), v_cm (common-mode, V), v_noise
  - approximations: noise is rejected only if the circuit is balanced and the pickup is purely common-mode
  - picture: two wires, signal +v_dm/2 and -v_dm/2 on top of a shared v_cm; noise lifts both together.
  - pitfalls: in a single-ended system noise is indistinguishable from signal. Needs tight matching, so it favors ICs (matched, interdigitated devices; transistors are "free", resistors and capacitors are not). Differential stages also let you cascade without coupling or bypass capacitors.

### 16.3 Birth of Symmetric Source-Coupled Pair
- **gm-differential-transconductance-goal**: The goal is an output current set by (v+ - v-), i.e. a differential transconductance Gm, with high output impedance and little loading on the inputs.
  - notation: Gm (A/V), v+ , v-, R_D (ohm), R_S (ohm)
  - formulas: common-source from v-: v_o = -gm R_D v-; common-gate from v+: v_o,CG = +gm R_D v+ (eq 16.3); superposition: v_o = gm R_D (v+ - v-) (eq 16.4)
  - picture: a common-source and a common-gate stage in one transistor give opposite-phase gains that subtract.
  - pitfalls: gain looks symmetric only for ideal voltage drive.
- **input-impedance-asymmetry-fix**: The common-gate side has low input impedance, about 1/gm, so with a source resistance R_s it loses gain by voltage division while the common-source side does not; a buffer helps only to the extent its own output impedance (1/gm,buff for a source follower) is small.
  - notation: 1/gm (ohm), gm,buff (S)
  - formulas: CG input impedance ~ 1/gm; follower output impedance 1/gm,buff
  - picture: add a follower in front of the CG side; the follower's 1/gm,buff then degenerates the CS side.
  - pitfalls: burning more power in the buffer shrinks but never removes the mismatch.
- **symmetric-pair-by-matching-gm**: Setting gm,buff = gm makes both sides lose exactly a factor 1/2 (CS side by degeneration with 1/gm, CG side by division at the buffer), so both inputs are high impedance with matched gain; replacing R_S and the follower's source with one tail current source I_Q gives the symmetric differential pair.
  - notation: M1, M2, I_Q (A), v_o- , v_o+ (V)
  - formulas: single-sided gain is halved (the page equations are missing; each side is -gm R_D/2 magnitude); differential output v_o = v_o+ - v_o-; differential gain follows from the two opposite outputs
  - picture: two source followers and two common-source stages merged: each transistor is both amplifier and buffer for the other.
  - pitfalls: R_S in the early figure is only for bias.

### 16.4 Differential Operation
- **diffpair-dc-bias**: With equal gate DC voltages, symmetry forces I_Q to split in half, so V_GS, V_OD and drain voltage are fixed regardless of the input common-mode DC level; the source node moves instead.
  - notation: I_Q (A), V_GS, V_OD (V), V_D (V), V_DC,input
  - formulas: I_D1 = I_D2 = I_Q/2; V_D = V_DD - (I_Q/2) R_D; differential DC output is 0 V
  - typical values: Fig 16.8: supplies +3.3 V and -3.3 V, R_D = 10 kohm, I_Q = 0.2 mA, so drains sit at 2.3 V (1 V drop); input DC swept (0 V, 1 V, 2 V), source node moves -0.7 V, 0.3 V, 1.3 V (V_GS about 0.7 V inferred)
  - approximations: valid only while the tail current source keeps enough headroom (at least one V_OD for a transistor source)
  - picture: sweep the input DC; the source node slides, drains and currents do not.
  - pitfalls: "too good to be true" only if the tail source is squashed. Enables DC-coupled cascades without AC coupling capacitors (Fig 16.9).
- **diffpair-large-signal-steering**: M1 and M2 compete for I_Q; the one with larger v_GS gets more current, giving a smooth, odd, S-shaped steering curve that is linear near zero and saturates completely at |v_id| = sqrt(2) V_OD.
  - notation: v_id = v_GS1 - v_GS2 (V), i_D1, i_D2 (A), V_OD (V) at quiescent point (I_Q/2 each)
  - formulas: i_D1 + i_D2 = I_Q; square-law i_D = (k/2)(v_GS - V_T)^2; steering form (eq 16.23, reconstructed): i_D1 = I_Q/2 + (I_Q/2)(v_id/V_OD) sqrt(1 - (v_id/(2V_OD))^2), i_D2 = I_Q - i_D1; at v_id = +sqrt(2) V_OD, i_D1 = I_Q and M2 off; at -sqrt(2) V_OD the reverse. Derivation (Sec 16.8): subtract sqrt(i_D)s, square, use i_D2 = I_Q - i_D1, solve the quadratic.
  - typical values: Fig 16.12 curves for V_OD = 0.1, 0.2, 0.3, 0.4 V, v_id axis about -0.4 to 0.4 V
  - approximations: square-law MOS, matched V_T, matched devices, tail source ideal
  - picture: two normalized current curves versus v_id crossing at I_Q/2; larger V_OD widens the linear range.
  - pitfalls: larger V_OD buys linear range but lowers gm for the same current.
- **diffpair-small-signal-gm**: Near v_id = 0 the current deviation is linear, with per-transistor slope gm; because each device sees v_id/2, the difference current is gm v_id even though the source node floats.
  - notation: gm (S), g_m = I_Q/V_OD for I_Q/2 per device (follows from the text's V_OD definition), i_d = gm (v_id/2)
  - formulas: i_D1 = I_Q/2 + gm v_id/2; i_D2 = I_Q/2 - gm v_id/2; gm evaluated at bias I_Q/2; slope of the steering curve at the origin is the pair's Gm
  - picture: v_id is dropped across two series transistors, so it splits in half; each looks like an ordinary common-source stage.

### 16.5 Small-Signal Differential Circuits
- **common-mode-differential-mode**: Any pair of inputs v1, v2 is an invertible mix of an average (common-mode) and a difference (differential-mode); symmetry gives even excitation for common-mode and odd for differential-mode.
  - notation: v_CM, v_DM (V); v_cm, v_dm in small-signal figures
  - formulas: v1 = v_CM + v_DM/2; v2 = v_CM - v_DM/2; v_CM = (v1 + v2)/2 (eq 16.33, "the average"); v_DM = v1 - v2 (eq 16.34); the 2x2 matrix is invertible, so you can go back and forth
  - picture: draw each input as a point on a line; v_CM is the midpoint, v_DM the gap.
  - pitfalls: the AC part of v_CM is interference to be rejected; the DC part of v_CM is just the bias.
- **half-circuit**: For pure differential drive the tail node is a virtual ground (no capacitor needed) so cut at the middle and ground it; for pure common-mode drive no current crosses the middle, so cut the middle open, leaving a floating source.
  - notation: v_dm/2 per side, R_CS (tail output resistance, ohm), 2R_CS per half
  - formulas: DM half-circuit = common-source amplifier with grounded source; CM half-circuit = common-source with source resistance 2R_CS (a resistor split in parallel becomes two resistors of twice the value)
  - picture: a vertical cut: grounded for odd drive, open for even drive; the two halves are different circuits.
  - pitfalls: the DM and CM half-circuits differ, hence different gains. DM virtual ground holds even if the tail has finite impedance.
- **differential-mode-gain**: The DM half-circuit is a plain CS stage, so everything known about CS amplifiers transfers.
  - notation: A_DM (V/V), v_o = v_o+ - v_o-, DC bias I_D = I_Q/2 with gates at V_CM
  - formulas: A_DM = v_o / v_dm = -gm R_D (reconstructed from the CS half-circuit; page equation missing; ideal tail). With active load, A_DM = -gm (r_o,N || r_o,P) (the text says "simply given by").
  - approximations: transistor r_o ignored unless stated
  - picture: v_o+ = -gm R_D v_dm/2 and v_o- = +gm R_D v_dm/2, difference doubles it.
- **common-mode-gain-tail-resistance**: With an ideal tail the CM half-circuit is a source follower with v_gs = 0, so the CM output current is zero and rejection is infinite; with a real tail R_CS the stage is a source-degenerated amplifier and has small CM gain.
  - notation: A_CM (V/V), R_CS (ohm), A_CM->DM
  - formulas: A_CM = -gm R_D / (1 + 2 gm R_CS) (reconstructed: degenerated CS with source resistance 2R_CS, per output); differential output for CM input is zero when perfectly matched
  - approximations: gain made small by raising R_CS relative to R_D, but lowering R_D also lowers A_DM
  - picture: source follows the gate so v_gs stays 0 and no signal current is made.
  - pitfalls: a CM signal can still rail the amplifier; any mismatch or single-ended output turns CM into DM, and then the two cannot be told apart. DM-to-CM conversion exists but is of less concern.

### 16.5.9 Current-Source Loads
- **active-load-and-cascode-diffpair**: Replacing R_D by current-source loads saves area and headroom; cascoding both the pair and the load raises output resistance and gain at a cost in swing.
  - notation: M1/M2 pair, M3/M4 load (PMOS), cascode devices M5-M8, r_o, gm
  - formulas: A_DM (plain active load) = -gm (r_oN || r_oP) (reconstructed); cascode: R_out,N ~ gm r_o^2 (reconstructed; text says "from our knowledge of cascodes"); equal NMOS and PMOS impedances so R_out = (gm r_o^2)/2; max gain ~ gm * gm r_o^2 / 2 = (gm r_o)^2/2 (reconstructed)
  - approximations: assumes equal N and P cascode impedances
  - pitfalls: triple cascode loses unacceptable headroom.

### 16.6 Common-Mode Rejection Ratio and DC Offsets
- **cmrr**: CMRR is the ratio of wanted differential gain to unwanted common-mode (to differential) gain; a matched balanced amp has A_CM->DM = 0 and infinite CMRR.
  - notation: CMRR (dimensionless or dB), A_DM, A_CM->DM
  - formulas: CMRR = A_DM / A_CM->DM (reconstructed; expressed in dB as 20 log10 of the ratio)
  - typical values: biomedical measurements need 70-100 dB CMRR to reject 50/60 Hz mains compared with micro-volt sensor signals
  - pitfalls: A_CM->DM is "identically zero" only with differential outputs and zero mismatch.
- **cmrr-from-rd-mismatch**: If one R_D is larger by delta R_D, CM input produces a differential output proportional to delta R_D / R_D, so CMRR depends on resistor matching and on R_CS.
  - notation: delta R_D (ohm), R_D, R_CS
  - formulas: A_CM->DM ~ (delta R_D / R_D) * gm R_D /(1 + 2 gm R_CS) (reconstructed); CMRR ~ 2 gm R_CS * R_D/delta R_D (reconstructed, large gm R_CS)
  - approximations: small mismatch; gm R_CS >> 1 for the simplified form
- **cmrr-from-gm-mismatch**: Threshold, W, L and C_ox (t_ox) mismatch between M1 and M2 makes delta gm; CMRR again needs a high R_CS and good matching, which layout (interdigitation, unit cells) targets.
  - notation: delta gm (S), gm, V_T, W, L, C_ox, t_ox
  - formulas: CMRR ~ 2 gm R_CS * gm/delta gm (reconstructed; page equation missing)
- **input-referred-offset**: With inputs tied to the same V_CM the output is not exactly balanced; the input-referred offset V_OS is the DC the input would need to null it, equal to output DC offset divided by gain.
  - notation: V_O (output DC offset, V), V_OS (V), A_DM
  - formulas: V_OS = V_O / A_DM; for R_D mismatch: V_O = (I_Q/2) delta R_D, A_DM = gm R_D, so V_OS = (V_OD/2)(delta R_D / R_D) (the eq 16.65 text shows the chain V_OD/2 * delta R_D/R_D)
  - approximations: bias current still splits evenly because source and drain nodes are decoupled and transistors are matched
  - picture: tie both inputs together, read the output offset, then slide a source at the input until it zeroes.
  - pitfalls: larger V_OD means larger input offset for the same delta R_D/R_D.

### 16.7 Current Mirror Load
- **single-ended-output-penalty**: Taking just one drain of a differential pair gives half the gain and converts all of the common-mode gain into a single-ended signal that cannot be separated from the wanted one, wrecking CMRR.
  - picture: use one drain only; CM response now shows up at the output.
- **current-mirror-load-diffamp**: A current mirror load (M3 diode-connected, M4 mirrors) subtracts the M1 current from the M2 current at the output, so the two opposite-phase currents add and the single-ended Gm equals gm.
  - notation: G_m (S), i_o (short-circuit output current, A), M1/M2 pair, M3/M4 PMOS mirror, i_d1 = -i_d2 = i
  - formulas: output current = 2 i (M1's current mirrored plus M2's); G_m = i_o / v_dm; G_m = gm1,2 (twice the single-ended-without-mirror value gm/2); R_out = r_o2 || r_o4; A_DM = G_m R_out = gm (r_o2 || r_o4) (reconstructed from the text)
  - approximations: impedance at M1's drain ~ 1/gm3 (diode dominated); assumes equal DC currents in M1/M2 and in M3/M4; half-circuit with virtual ground is accurate despite asymmetry because i_D depends on v_GS, weakly on v_DS
  - picture: left side's current is copied across to the right; load sees the difference of two opposite currents.
  - pitfalls: circuit is not fully symmetric; the analysis leans on gate-controlled currents.
- **mirror-load-cm-gain**: Mirror error from finite r_o makes a small residual current delta i that becomes a differential output for common-mode input; since gm r_o >> 1 it is tiny, giving a far better CMRR than a plain single-output pair.
  - notation: delta i (A), A_CM->DM, v_o,dm
  - formulas: delta i = i_d4 - i_d2 (small); i_d1 from a degenerated-CS gm_eff with R_CS; CMRR for mirror load is much larger than single-output without mirror (page formula missing; scales roughly with gm R_CS-type factors)
  - approximations: here the usual 1/gm3 << r_o shortcut is deliberately not used because the quantity is small
  - pitfalls: dropping 1/gm3 vs r_o terms would discard the whole effect.

### 16.8 Appendix: Large Signal Derivation Steps
- **large-signal-derivation**: Subtract and square the sqrt(i_D) relations to get a linear v_GS1 - v_GS2 = v_id, use i_D2 = I_Q - i_D1, solve the resulting quadratic for i_D1, and factor out I_Q using V_OD to reach eq 16.23.
  - formulas: sqrt(i_D1) - sqrt(i_D2) proportional to v_id; (sqrt(i_D1) - sqrt(i_D2))^2 squared again leaves a quadratic in i_D1

## Chapter 17. Op-Amp Feedback and Frequency Response

### 17.2 Introduction to Feedback
- **feedback**: A feedback system measures its output, subtracts a fraction from the input to form an error, and amplifies the error; the closed-loop response then depends mainly on the feedback network.
  - notation: s_in, s_out, s_err, G (forward gain), f (feedback factor), T = G f (loop gain)
  - formulas: s_err = s_in - f s_out (eq 17.1); s_out = G s_err; closed loop s_out/s_in = G/(1 + G f) = G/(1 + T); for G f >> 1, s_out/s_in -> 1/f (eq 17.8)
  - approximations: G f >> 1; delay around loop neglected (electronic delay vanishingly small, though G's phase response acts as delay)
  - picture: cruise control: desired minus measured speed times K_p drives the engine, blind to engine details.
  - pitfalls: the equation looks circular (output depends on output); resolve by imagining a tiny delay.
- **ideal-opamp-circuits (non-inverting as feedback)**: In the non-inverting amplifier the resistor divider is the feedback box and the op-amp input forms the error.
  - notation: f = R1/(R1 + R2); G ~ 1 + R2/R1 = 1/f
  - formulas: closed-loop gain ~ 1/f = 1 + R2/R1
  - approximations: the Golden Rules are the limit of infinite gain: the error goes to zero and the product 0 times infinity is resolved by the limit; for finite gain the error is nearly zero
- **feedback-history**: Harold Black (1927, ferry to Bell Labs) saw that negative feedback improves linearity (and, in his flash, positive boosts gain).

### 17.3 Why Feedback?
- **feedback-precision-linearization**: A huge, nonlinear, drifting open-loop gain is fine because the amplifier only processes the tiny error signal, so the closed loop is linear and set by a resistor ratio.
  - typical values: gain of 1 million on a 5 V supply saturates for inputs above about 5 uV; ratio of resistors tracks temperature and aging
  - picture: high-gain curvy transfer curve inside, low-gain straight line outside (Fig 17.6b).
- **loop-gain**: Loop gain T = G f is the gain around the broken loop; precision needs T large, not just G.
  - formulas: closed loop = G/(1 + T), T = G f
  - pitfalls: for the inverting amplifier the loop is harder to see: input attenuated by g and feedback f, both at most 1.
- **feedback-noise-distortion-rejection**: Noise or distortion injected at the output (or inside the forward path) is divided by 1 + T.
  - formulas: s_out = (G s_in + s_noise)/(1 + T) for noise added at the forward block's output, reduced by 1/(1 + T) for T >> 1 (reconstructed from text "rejected by 1/(1+T)")
- **positive-feedback**: With the output added back, s_out = G/(1 - T) times input for T < 1 (geometric series), gain can be boosted but T near 1 is hard to control.
  - formulas: sum of geometric series 1 + T + T^2 + ... = 1/(1 - T) valid for |T| < 1; T = 1 - epsilon gives arbitrarily large gain
  - picture: infinite copies circulating the loop and adding to the output.
  - pitfalls: T > 1 gives oscillation or railing. Positive feedback is for hysteresis and memory (SRAM cell = two CMOS inverters).

### 17.4 Circuit Models for Op-Amps
- **opamp-linear-imperfections**: Linear imperfections: finite A0, finite R_i, nonzero R_o, finite bandwidth; non-linear ones (slew, swing, offset, bias currents, noise, distortion) come in Chapter 18.
- **vcvs-opamp-model**: Simplest model: output = A v_in through R_out; captures finite gain and R_out but no frequency dependence.
  - notation: A (V/V), R_out (ohm), v_in
- **general-amplifier-model**: Z_in(j omega), Z_out(j omega), G_v(j omega) is general but gives no insight.
- **physical-opamp-ota-model**: An op-amp is an input G_m cell (a differential pair) driving a high impedance node R_x || C_x, then a unity buffer; the single dominant pole and DC gain live at that node.
  - notation: G_m (S), R_x (ohm), C_x (F), A0 = G_m R_x, buffer gain 1, R_out after the buffer, C_in, C_out
  - formulas: output current I_out = G_m (v+ - v-); A0 = G_m R_x
  - picture: transconductor into a parallel R and C, then a follower; remove R_x and the DC gain is infinite (an integrator).
  - pitfalls: without R_out, C_out does not affect the transfer function (an ideal buffer drives any load). OTA = op-amp minus its triangle's buffer; realized as a differential pair with a high-impedance mirror load, outputs a current so needs a buffer for a resistive load.

### 17.5 Gain/Bandwidth Trade-off
- **dominant-pole / single-pole-opamp**: The open-loop op-amp is one pole with DC gain G0 = G_m R_x and corner set by R_x C_x.
  - notation: G0 (V/V), omega_-3dB (rad/s), tau = 1/omega_-3dB (s), omega_u (rad/s)
  - formulas: G(j omega) = G0 / (1 + j omega tau) (reconstructed; page equation missing); omega_-3dB = 1/(R_x C_x); GBW = omega_u = G0 omega_-3dB = G_m / C_x (independent of G0 and R_x)
  - approximations: for omega >> omega_-3dB, |G| ~ omega_u / omega (so unity at omega_u = G0 omega_-3dB)
  - picture: magnitude plot -20 dB/decade line; the 3 dB corner and the unity-gain crossing.
- **gain-bandwidth-tradeoff**: With feedback the gain drops by (1 + T) and the bandwidth rises by (1 + T), so the product is fixed; closed-loop bandwidth is f times omega_u.
  - notation: T = G0 f, omega_0 = closed-loop -3 dB frequency (rad/s)
  - formulas: closed loop = [G0/(1+T)] / (1 + j omega tau/(1+T)) (reconstructed); omega_0 = (1 + T) omega_-3dB; DC gain G0/(1+T); GBW = omega_u = G_m/C_x; closed-loop bandwidth ~ f omega_u
  - typical values: Fig 17.18 unity follower (f = 1, 100 ohm resistor drawn) has omega_0 = omega_u = GBW; figures label G0 = 40 dB, with -20 dB/decade slope
  - approximations: T >> 1 so (1 + T) ~ T
  - picture: closed-loop curve is a flat shelf at G0/(1+T) running out to (1+T)*omega_-3dB, then riding the same open-loop line.
  - pitfalls: step response is faster by (1 + T). Unity gain keeps the full GBW; infinite DC gain model gives the same GBW.
- **gbw-capacitive-load**: Driving a capacitor C_L with the bare OTA, bandwidth is set by combined internal and load capacitance.
  - formulas: pole ~ G... 1/(R_x (C_x + C_L)) (the page equation is missing; the figure shows C_x and C_L in parallel)
- **feedback-lowers-node-impedance (why feedback broadbands)**: In unity feedback the dependent source's control voltage equals the output node voltage, so as seen by C_x it is a resistor 1/G_m, not R_x; the bandwidth is G_m/C_x, not 1/(R_x C_x).
  - notation: Z_out of the transconductor = infinity if the control voltage is held at zero, = 1/G_m if the control is shorted to the output node
  - formulas: R_x replaced by R_x || 1/G_m ~ 1/G_m; gain to the node ~ 1 for unity feedback; bandwidth = G_m/C_x; with factor f: node impedance ~ R_x/(1 + A0 f), closed-loop gain ~ A0/(1 + A0 f), bandwidth ~ (1 + A0 f)/(R_x C_x)
  - picture: the feedback turns a current source into a resistor, like a MOS diode seeing 1/gm instead of r_o.
  - pitfalls: "if you said 1/(R_x C_x), think again" because of the dependent source.

### 17.6 Inverting Amplifier and Feedback
- **inverting-amp-loop-gain**: In the inverting amplifier the input is also applied at the inverting terminal, so there are two divider factors: feedback f from output and input attenuation g, and the loop gain is A f.
  - notation: R_S (source resistor, ohm), R_F or R_1/R_2 (feedback resistor), f = R_S/(R_S + R_F) (reconstructed), g = R_F/(R_S + R_F) (reconstructed), A (op-amp gain), loop break at V-
  - formulas: V- = g v_s + f v_o (superposition of two dividers); v_o = -A V-... closed loop = -(g A)/(1 + A f) = -(R_F/R_S) times A f/(1 + A f) after A f >> 1 -> -g/f = -R_F/R_S
  - approximations: A f >> 1
  - pitfalls: both g and f are at most 1; signal attenuated before the amplifier.
- **inverting-amp-gbw**: The inverting amp's closed-loop GBW is g times that of the non-inverting amp because DC gain falls by g while bandwidth still extends by (1 + A0 f).
  - formulas: GBW_inv = g * GBW; so a loss versus the non-inverting follower case
  - pitfalls: it is really a current-to-voltage (transresistance) amplifier (Norton transform of v_s with R_S): output is converted to current by the feedback resistor and subtracted from the input current at the inverting node, so the voltage-feedback analysis only approximately matches.

### 17.8 Effect of Feedback on Input/Output Impedance
- **feedback-impedance**: For voltage-amp (series-shunt) feedback, loop gain raises input impedance and lowers output impedance, both by 1 + A f.
  - notation: R_in, R_out (open-loop, ohm), Z_in,fb, Z_out,fb, v_err, test source v_x, current i_x
  - formulas: Z_in,fb ~ R_in (1 + A f) (reconstructed); Z_out,fb ~ R_out/(1 + A f) (reconstructed; Fig 17.26 label R_out/(1 + A0 f))
  - approximations: R_out ignored when computing input impedance, R_in ignored when computing output impedance (results still hold if kept)
  - picture: tie a test source to the port, find i_x; the loop forces v_err to fight the test source.
  - pitfalls: this is why op-amps are used at gain 1 (high Z in, low Z out).
- **impedance-vs-frequency**: The improvement exists only while loop gain does: Z_out,fb is R_out/(1 + A0 f) at low frequency, rises (pole/zero) above omega_0 and returns to R_out beyond omega_0 (1 + A0 f).
  - notation: omega_0, omega_u-like corner omega_0(1 + A0 f)
  - picture: Bode of |Z_out,fb|: flat low value, rising +20 dB/decade, flattening at R_out.

### 17.9 Feedback and Stability
- **stability-phase-margin**: A single pole lags at most 90 deg; non-dominant poles add phase and can bring the total to 180 deg, turning negative feedback into positive; stability needs |T| < 1 when the phase of T reaches 180 deg, measured as phase margin (60 deg or more in a good design).
  - notation: phase of G(j omega), omega_x with T(j omega_x) = -1, non-dominant poles
  - formulas: single-pole phase = -arctan(omega tau); two poles: -40 dB/decade and -180 deg asymptote; oscillation condition T(j omega_x) = G(j omega_x) f = -1
  - typical values: phase margin target >= 60 deg; Fig 17.27/17.28 axes span 10 to 10^5 rad/s
  - approximations: non-dominant poles must be well above omega_u so the 180 deg point falls where |T| < 1
  - picture: |G| bends from -20 to -40 dB/decade while phase slides from -90 deg toward -180 deg.
  - pitfalls: at T = -1 closed loop gain is infinite and any noise regenerates; this is how oscillators work. Compensation is deferred to an advanced course.

## Chapter 18. Non-Ideal Operational Amplifiers

### 18.2 Offset Voltage and Currents
- **opamp-offset**: Shorted inputs give a nonzero (even railed) output due to mismatched pair devices and loads; model as an ideal op-amp with a voltage source V_OS at either input, shifting the transfer curve left or right.
  - notation: V_OS (V; datasheet value is usually a standard deviation), V_sup (supply rails)
  - formulas: shifted transfer curve; V_OS random in sign
  - typical values: Fig 18.2 transfer curve plotted over +/-10 mV input, +/-1.5 V output
  - picture: the input-output curve slides sideways by V_OS, crossing zero output at nonzero input.
  - pitfalls: sign is random, so the source can sit on either terminal. Trimming: offset-null pins with a potentiometer whose wiper goes to the negative supply (LM741); ICs use internal calibration.
- **opamp-bias-current**: Bipolar inputs need a small DC base current; model as current sources I_B1, I_B2 at the inputs; the average is the bias current and the difference is the input offset current.
  - notation: I_B1, I_B2 (A), I_B = (I_B1 + I_B2)/2, I_OS = I_B1 - I_B2 (reconstructed sign convention; text says "difference")
  - typical values: bias about 100 nA, offset current about 10 nA (order of magnitude smaller)
  - approximations: I_B = I_C/beta, offset arises from beta variation
  - pitfalls: it is a DC current, not an AC current and not due to input impedance. Darlington input pair reduces it.
- **bias-current-output-offset**: In the inverting amplifier with R_3 = 0, the output offset is V_o = I_B1 R_2 (the figure label), since V- is a virtual ground and no current goes through R_1.
  - formulas: V_o = I_B1 R_2 (Fig 18.6)
  - pitfalls: limits how small R_2 can be (small R_2 needs a higher-power op-amp).
- **bias-current-compensation-r3**: A resistor R_3 from the non-inverting input to ground, chosen equal to R_1 || R_2 = R_1 R_2/(R_1 + R_2), cancels the systematic offset without changing AC behaviour; residual output is I_OS R_2.
  - formulas: R_3 = R_1 R_2/(R_1 + R_2) (the text writes R_3 = R_2/(1 + R_2/R_1)), V_o = 0 for I_B1 = I_B2; with offset current V_o = I_OS R_2
  - picture: the same I_B drops equal voltage at both inputs, so they cancel.

### 18.3 Op-Amp Frequency Response
- **closed-loop-inverting-bandwidth**: With a single-pole A(j omega) = A0/(1 + j omega/omega_-3dB) in an inverting stage, closed-loop gain is about -R_2/R_1 with bandwidth omega_0 = (1 + A0 f) omega_-3dB, and GBW stays nearly unchanged.
  - notation: A0, omega_-3dB, omega_u = A0 omega_-3dB (also written omega_t in figure), omega_0
  - formulas: finite-gain inverting transfer function A-dependent (page equations missing); for A >> 1, -R_2/R_1; GBW ~ omega_u
  - pitfalls: result differs slightly from the non-inverting analysis because the inverting amp is a transresistance amplifier.

### 18.4 Voltage Swing and Slewing
- **output-swing**: Output cannot exceed the supply rails (often it cannot reach them) and a maximum output current clips it; clipping causes distortion.
  - typical values: Fig 18.10 uses +10 V and -10 V rails; Fig 18.11 shows a sine clipped
  - pitfalls: clipping happens when input times gain exceeds the supplies; avoid in linear applications.
- **slew-rate**: Slew rate SR is the maximum rate of change of the output, a non-linear limit that distorts the waveform, unlike bandwidth, which is linear and does not change the shape of a sinusoid.
  - notation: SR (V/s, data sheets use V/us), V_i (step amplitude, V), omega_u
  - formulas: SR = max |dV_o/dt|; unity-gain linear step: V_o = V_i (1 - e^(-t omega_u)) with tau = 1/omega_u; initial slope = V_i omega_u; slews if V_i omega_u > SR; no slewing if V_sm,i omega_u <= SR
  - picture: ideal exponential versus straight-line ramp that hands over to exponential when the slope drops below SR.
  - pitfalls: a smaller step avoids slewing, so slewing depends on amplitude.
- **slew-rate-origin**: The input G_m stage can only supply a maximum current I_max, so a large input step charges C_x at a constant rate.
  - notation: I_max (A), C_x (F), G_m
  - formulas: SR = I_max / C_x; I_o = G_m (v+ - v-) clips at +/-I_max (Fig 18.16, axis +/-1 mA over +/-3 V); linear settling resumes when error shrinks back into the linear range
  - picture: transconductor curve flat for large input, so constant current into a capacitor gives a ramp.
  - pitfalls: a buffer with limited DC current can slew too. R_x ignored.
- **full-power-bandwidth**: For a sine of amplitude V_o,max, slewing starts at f_max where max slope omega V_o,max equals SR.
  - formulas: v_o = V_o,max sin(omega t); slope max = omega V_o,max <= SR; f_max = SR/(2 pi V_o,max) (reconstructed); can be far below the unity-gain frequency
  - pitfalls: depends on output amplitude; smaller amplitude pushes it up.

### 18.5 Noise and Distortion
- **distortion**: Distortion comes from clipping, slewing, group delay in bandwidth limits, and curvature (S shape) of the input-output curve; a Taylor expansion shows squaring gives a 2nd harmonic and cubing gives fundamental plus 3rd harmonic.
  - formulas: i = a0 + a1 v + a2 v^2 + a3 v^3 (Taylor); cos^2 = (1 + cos 2 omega t)/2; cos^3 = (3 cos omega t + cos 3 omega t)/4 (the text cites the trig identity)
  - approximations: small portion of the curve is modeled by a short Taylor series
  - picture: sine in, S-shaped curve, flattened-peaks sine out.
  - pitfalls: with negative feedback the input swing is small, so harmonics are tiny but visible on a spectrum analyzer; intermodulation also arises (deferred).
- **noise**: Shorted inputs show a small random flat-spectrum (white) signal from thermodynamic origin; model as input noise voltage and current sources, specified per root hertz and integrated over bandwidth.
  - notation: e_n or v_eq (V/sqrt(Hz)), i_eq (A/sqrt(Hz)), k (Boltzmann), T (K), delta f (Hz), SNR
  - formulas: noise = spectral density times sqrt(bandwidth); resistor noise current i_n^2 = 4kT delta f / R and voltage v_n^2 = 4kT R delta f (reconstructed; text names k, delta f, T)
  - typical values: rule of thumb: 1 kohm resistor integrates to about 4 uV over 1 MHz
  - pitfalls: low-noise designs use small feedback resistors; signal must stay well above noise. Unlike offset, noise is an AC statistical quantity.

### 18.6 Datasheets
- **datasheet-reading**: Example op-amp ADA4891 (CMOS) lists the specs from this chapter.
  - typical values: GBW 240 MHz; slew rate 170 V/us; DC offset 2 mV; open-loop DC gain 66 dB; input impedance 5 Gohm; input common-mode range -Vs - 0.3 V to +Vs - 0.8 V; CMRR 88 dB; small-signal bandwidth 240 MHz at G = +1 and 90 MHz at G = +2 (from the garbled table); fastest parts 3.8 GHz and near 1 GV/s at tens of mA; lowest-power parts under 1 uA but slow.
  - pitfalls: the datasheet table text is OCR-garbled; only values quoted in the prose are reliable.

## Appendices A, B, C
- **geometric-series**: Sum of r^n converges to 1/(1 - r) for |r| < 1, diverges otherwise (used for positive feedback).
- **taylor-series**: Coefficients from the nth derivative at x = a: c_n = f^(n)(a)/n!; Maclaurin when a = 0 (used for distortion).
- **linear-independence-sin-cos**: a sin x + b cos x = 0 forces a = b = 0 (set x = pi/2, then x = 0). The definitions say alpha_i in Z (integers), apparently a typo for real numbers.
- **common-drain-output-resistance**: KCL at v_x shows R_x = 1/(1/r_o + 1/r_oc + g_m) = (r_o || r_oc) || (1/g_m), confirming eq 12.34.
  - notation: r_oc (current-source output resistance below the source, ohm), r_o, g_m, v_x, i_x
  - picture: the output node sees three paths to ground in parallel: r_o, r_oc and 1/gm.

## Notation and conventions for these chapters

| symbol | meaning | unit | sign convention |
|---|---|---|---|
| v1, v2 / v+, v- | the two input terminals | V | v_id or v_dm = v1 - v2 = v+ - v-; positive steers I_Q into M1 |
| v_CM, v_cm | common-mode input (average of the two) | V | (v1 + v2)/2; DC part is bias, AC part is interference |
| v_DM, v_dm, v_id | differential-mode input | V | v1 - v2; each side sees +/- v_dm/2 |
| v_o+, v_o-, v_o | single outputs and differential output | V | v_o = v_o+ - v_o- |
| I_Q | tail current | A | splits to I_Q/2 per device at balance |
| V_OD (V_od) | overdrive at the I_Q/2 bias point | V | full steering at v_id = +/- sqrt(2) V_OD |
| gm, G_m | per-transistor or OTA transconductance | S | G_m (capital) is the differential or OTA transconductance; gm, small, is a single device |
| R_CS | tail current-source output resistance | ohm | splits into 2 R_CS per half-circuit |
| A_DM, A_CM, A_CM->DM | differential, common-mode and CM-to-DM conversion gain | V/V | CMRR = A_DM / A_CM->DM |
| V_OS, V_O | input-referred offset, output DC offset | V | V_OS = V_O / A_DM; sign random |
| s_in, s_err, s_out, G, f, T | feedback block diagram signals | V/V | s_err = s_in - f s_out; T = G f |
| f | feedback factor (fraction of output fed back) | none | non-inverting: R1/(R1 + R2); inverting: R_S/(R_S + R_F) (reconstructed) |
| g | input attenuation in inverting amp | none | R_F/(R_S + R_F) (reconstructed); GBW_inv = g GBW |
| A, A0, G0 | open-loop gain (A0 or G0 at DC) | V/V | A0 = G_m R_x |
| omega_-3dB, omega_u (omega_t), omega_0 | open-loop corner, unity-gain frequency, closed-loop corner | rad/s | omega_u = A0 omega_-3dB = G_m/C_x; omega_0 = (1 + T) omega_-3dB |
| tau | time constant | s | tau = 1/omega_-3dB (open loop) |
| GBW | gain-bandwidth product | rad/s or Hz | equals omega_u; closed-loop BW = f omega_u |
| R_x, C_x | high-impedance node resistance and capacitance | ohm, F | dominant pole 1/(R_x C_x) |
| I_B1, I_B2, I_B, I_OS | input bias, average, offset currents | A | I_B = average; I_OS = difference; flows into the inputs (bipolar) |
| SR | slew rate | V/s | SR = I_max/C_x; datasheets use V/us |
| omega_x | frequency where T = -1 | rad/s | phase margin measured at |T| = 1 against 180 deg |
| j | imaginary unit | none | used throughout (G(j omega)) |

## Where a visual would help most

1. **Differential-pair steering curve (diffpair-large-signal-steering)**: drag v_id and the overdrive V_OD (0.1 to 0.4 V) and I_Q. Two current bars, i_D1 and i_D2, and the S-curve marker move; the linear window widens. Click: current is conserved and handed over smoothly, saturating exactly at +/- sqrt(2) V_OD, with slope gm = I_Q/V_OD at the centre.
2. **Common-mode versus differential drive and half-circuit cut (common-mode-differential-mode, half-circuit)**: drag v1 and v2 handles (or v_CM and v_DM) and toggle R_CS from infinite to finite. The tail node voltage and drain waveforms move. Click: the tail node does not move for DM drive (virtual ground) and follows the gate for CM drive.
3. **CMRR and mismatch (cmrr)**: sliders for delta R_D/R_D, delta gm/gm and R_CS. A_CM->DM and CMRR in dB update, with a 60 Hz common-mode interferer riding on a small signal in a time-domain view. Click: CMRR is limited by the product of tail resistance and matching, not by the pair gain alone.
4. **Current-mirror load, single-ended output (current-mirror-load-diffamp)**: drag v_dm and r_o. Arrows for i, the mirrored copy and the 2i output current update, with the CM case showing the small residual delta i. Click: the mirror turns two opposite currents into one doubled current and cancels common-mode almost entirely.
5. **Feedback broadbanding (gain-bandwidth-tradeoff)**: drag the feedback factor f (or R2/R1) and A0. Open-loop single-pole Bode and closed-loop Bode move together; GBW is marked. Click: closed-loop gain times bandwidth stays pinned to the same line G_m/C_x as f changes.
6. **Phase margin and a second pole (stability-phase-margin)**: drag the second pole frequency and f. Magnitude and phase Bode, the T = 1 crossing, and a step response ringing change. Click: moving the non-dominant pole past omega_u shrinks the ringing and pushes phase margin toward 90 deg; near 60 deg is a good compromise.
7. **Slew rate versus bandwidth (slew-rate, full-power-bandwidth)**: drag step size or sine amplitude and frequency, SR and omega_u. Output waveform changes between exponential, ramp-then-exponential and a triangle-like distorted sine. Click: bandwidth limits distort nothing in shape, slew limits do, and f_max falls as 1/amplitude.
8. **Input bias current and R_3 compensation (opamp-bias-current)**: drag I_B, I_OS, R_1, R_2 and R_3. The inverting-input node voltage and output offset update. Click: choosing R_3 = R_1 || R_2 cancels the I_B term and leaves only I_OS R_2.
