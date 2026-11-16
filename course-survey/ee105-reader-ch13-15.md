# EE 105 reader, chapters 13-15: concept notes

Source: ee105_reader_v3 copy.md, lines 6880-8488. Caveat: every display equation in this range was dropped by the conversion (blank gaps). Formulas below are the standard forms that the surrounding text names or implies (checked against the visible text and the few inline equations); where the reader's own number or wording is visible it is quoted as such. Items marked [reconstructed] come from the derivation the text describes, not from a visible equation.

## Chapter 13. Current Mirrors and Biasing

### 13.2 High Load Impedance in Amplifiers
- **current-source-load**: A high-gain stage needs a large load impedance Z_L, and a transistor in saturation with fixed V_GS is a usable stand-in for an ideal current source.
  - notation: Z_L load impedance (ohm); R_L (ohm); V_DD (V); V_OD = V_GS - V_T (V), also V_od, V_D,sat; I_CS (A); V_bias,Q (V); r_o (ohm)
  - formulas: saturation needs V_DS > V_OD (BJT: V_CE > V_CE,sat); resistor load limits R_L by I_D*R_L < V_DD - V_OD [reconstructed]; ideal current source has infinite resistance, so gain is then limited only by the transistor
  - typical values: IC resistors are hundreds to thousands of ohm per square; thin-oxide nanoscale supply about 1 V; I/O devices 2.5 V or 3.3 V; plot axes show I_DS up to 6 (mA) and V_DS up to 5 V
  - approximations: transistor as current source holds while it stays in saturation; the slope from r_o is the small leftover dependence on V_DS
  - picture: I_DS vs V_DS family; operating point sits where the load line meets the curve; raising R_L drags the point into triode.
  - pitfalls: a big resistor costs area, matching, current handling and above all DC drop (headroom), so "just use a bigger R_L" fails.

### 13.2.5 Process / temperature variation, diode-connected device
- **bias-reference**: Fixing V_GS from a model gives an unpredictable current (V_T drifts with temperature, devices vary), so one transistor generates V_GS for its neighbour.
  - notation: V_GS (V); V_T (V); V_OD (V); I_DS (A)
  - formulas: diode connected: V_DS = V_GS = V_D,sat + V_T, so never in triode; V_GS is the inverse function of I_DS = (1/2) mu C_ox (W/L) (V_GS - V_T)^2 [reconstructed]; at very small current V_GS is about V_T
  - approximations: matched neighbouring (inter-digitated) devices share V_T and process
  - picture: Rectifying I-V curve (I_DS vs V_GS, nonzero only for V_GS above V_T), quadratic not exponential like a PN diode.
  - pitfalls: two arbitrary transistors are not matched; only adjacent or interleaved ones are.

### 13.3 The Basic Current Mirror
- **current-mirror**: Two transistors with equal V_GS carry (nearly) equal drain current, so the input current is copied to the output for small and large signals.
  - notation: I_in, I_out (A); M1 diode-connected, M2 output device; V_GS1, V_GS2 (V); V_out (V); R_oc output resistance of the mirror (ohm); N scaling ratio; W_U unit width; lambda (1/V)
  - formulas: I_out/I_in = (W/L)_2 / (W/L)_1 = N (same V_GS, same V_T) [reconstructed]; with lambda = 0 the currents are exactly equal; R_oc = r_o2 (small-signal)
  - approximations: I_out = N*I_in needs M2 in saturation and lambda small; diode side is low impedance (1/g_m), output side is high impedance
  - picture: Diode side is a low-Z V_GS reference exported to a high-Z output side that behaves as a current source.
  - pitfalls: mirror accuracy is only as good as the match and the V_DS difference (V_out vs V_GS1 through channel-length modulation).
- **mirror-scaling-ratio**: Scale the output by replicating unit transistors (width), not by changing L, because V_T and other parameters vary with L.
  - notation: N ratio; W_U unit width; I_out = N I_in
  - formulas: (W/L)_2 = N (W/L)_1, realised as N parallel unit devices
  - typical values: 4:1 mirror drawn with five unit elements (one diode, four output fingers)
  - approximations: if N is very large, scale both W and L
  - picture: Layout of fingers abutted with shared source/drain for matching.
  - pitfalls: scaling L spoils matching.
- **small-signal-diode-connected**: Shorting gate to drain turns the MOS into a conductance 1/g_m (parallel r_o).
  - notation: g_m (S); r_o (ohm); C_gs, C_gd (F)
  - formulas: R_diode = (1/g_m) || r_o, about 1/g_m
  - picture: g_m generator controlled by its own terminal voltage equals a resistor.
- **current-mirror-output-resistance**: With a DC reference current, M1 gives v_gs = 0 so g_m2 v_gs2 = 0 and the output sees only r_o2.
  - formulas: R_oc = v_t / i_t = r_o2
  - picture: Test source at M2 drain; controlled source switched off; only r_o remains.

### 13.4 Improved Current Source: The Cascode Mirror
- **source-degeneration-mirror**: A resistor R_s in the source of the output device multiplies output resistance by about g_m R_s (not adds R_s as it would in the drain).
  - notation: R_s (ohm); R_eq Thevenin resistance of the input side; v_gs = -v_Rs
  - formulas: R_out = r_o (1 + g_m R_s) + R_s [reconstructed from "boosted by (1 + g_m R_s)"]; for scaled output I_out = N I_in, R_s is N times smaller to keep V_S the same (I_in R_s,1 = I_out R_s,2)
  - approximations: boost g_m R_s large
  - picture: Output current flows through R_s, creates v_gs of opposite sign and fights the change in current.
  - pitfalls: costs headroom by I_out R_s.
- **cascode-mirror**: Stacking M3/M4 on M1/M2 holds V_DS2 nearly constant as well as V_GS2, so r_o1 acts as the degeneration of M4 and R_out is about g_m r_o times larger.
  - notation: M1, M2 bottom, M3, M4 top; r_o (ohm); g_m (S); V_min (V); V_OD (V)
  - formulas: R_out = r_o4 + r_o2 + g_m4 r_o4 r_o2, about g_m r_o^2 [reconstructed from "R_S = r_o1 as seen by M4"]
  - approximations: all devices same V_T and size, so same V_OD
  - picture: Two stacked transistors; lower pair is a mirror, upper pair clamps the lower device's V_DS.
- **output-swing**: The cascode costs headroom; the minimum output voltage rises from V_OD (simple mirror) to V_T + 2 V_OD, and a high-swing bias reduces this to 2 V_OD.
  - notation: V_min (V), V_GS4 = V_T + V_OD; V_OD (V)
  - formulas: simple mirror V_min = V_OD; with R_s: V_OD + I_out R_s; cascode V_min = V_GS1 + V_OD4... = V_T + 2 V_OD; high-swing: bias M4 gate at V_T + 2 V_OD, so V_min = 2 V_OD [reconstructed]
  - typical values: high-swing bias made by scaling the bias device down by 4x (W/L x 1/4), which doubles its overdrive
  - picture: Bar stack showing minimum V_out growing as each transistor is added.
  - pitfalls: bias gate of top device is tied to V_GS1+V_GS3 in the plain cascode mirror, wasting a V_T.

### 13.5 Current Sources and Sinks
- **mirror-sink-source-duality**: NMOS mirrors sink current to ground, PMOS mirrors source it from V_DD; same r_o, scaling and cascode versions.
  - notation: I_ref (A); I_in, I_out
  - picture: Mirror dual, with one precision I_ref feeding many scaled copies, NMOS and PMOS.
  - pitfalls: "current source" is loosely used for both; NMOS only sinks.

### 13.6 Source Follower with Real Current Source
- **common-drain** (biased by mirror): The follower's current source is replaced by a mirror modelled as r_oc, which enters the effective load.
  - notation: R_S source resistance (ohm); R_L (ohm); I_Q bias current (A); V_bias,Q (V); r_oc (ohm); R_L,eff (ohm); G_v
  - formulas: R_L,eff = R_L || r_o || r_oc; G_v = v_out/v_s = g_m R_L,eff / (1 + g_m R_L,eff)
  - approximations: DC level of the previous stage only has to be large enough; V_bias,Q must keep mirror out of triode
  - picture: Follower AC schematic with the mirror shown as a resistor r_oc to ground at the source node.

### 13.7 Generation of Current References
- **bias-reference** (resistor reference): I_ref = (V_DD - V_GS1)/R_M, so it depends on supply, V_T and temperature.
  - notation: R_M (ohm); V_GS,1 (V)
  - formulas: I_in = (V_DD - V_GS,1)/R_M; V_GS,1 depends weakly on I_ref, so solve iteratively or with the square law
  - pitfalls: simple but supply and temperature dependent; on-chip resistors vary absolutely.
- **constant-gm-reference**: A loop of two mirrors with devices differing by 4x in W makes I_D independent of V_DD and V_T and ties g_m to 1/R_S.
  - notation: M1, M2 PMOS equal; M3 (x1), M4 (x4) NMOS; R_S (ohm); V_OD (V); I_D4 (A)
  - formulas: I_D3 = I_D4; V_Rs = V_GS3 - V_GS4 = V_OD3 - V_OD4 (V_T cancels); M3 is 1/4 the width, so V_OD3 = 2 V_OD4; I_D4 = V_OD4 / R_S, and with I_D = (1/2) k (W/L) V_OD^2, I_D4 = 2 / (k (W/L)_4 R_S^2) (1 - 1/2)^2 = ... [reconstructed]; reader's caption: g_m = 1/R_S
  - approximations: square-law devices; matched mirrors; text says "all transistors biased with this current have constant g_m"
  - picture: Current loops itself to a value fixed by R_S and a 4:1 width ratio; the supply drops out.
  - pitfalls: the reader says g_m = 1/R_S; with my reconstruction g_m of the 1x device (M3) is 1/R_S and g_m4 is 2/R_S, so confirm which device when specifying. Also the circuit has a second, zero-current stable state (start-up circuit not covered).

## Chapter 14. Frequency Response of Amplifiers

### 14.2 General considerations
- **amplifier-frequency-response**: Number of poles equals number of independent energy-storage elements; zeros depend on the chosen input and output ports.
  - notation: C_in, C_out (F); R_s, R_in, R_out (ohm); omega_p (rad/s)
  - formulas: input pole omega_in = 1 / ((R_s || R_in) C_in); output pole omega_out = 1 / (R_out C_out); gain = G_m (R_out) at mid-band with the two poles [reconstructed]
  - approximations: independent poles when each capacitor sits at its own node (no coupling capacitor)
  - picture: A transconductance amplifier whose input node and output node are two separate RC low-pass filters.
  - pitfalls: coupling capacitors (C_gd) break the "by inspection" method.

### 14.3 MOS parasitic capacitors
- **mos-capacitances**: In saturation the MOS has C_gs, C_gd, C_db, C_sb (junction plus overlap and fringe) that sit around the g_m source.
  - notation: C_gs, C_gd, C_db, C_sb (F); C_ox; C_sg,ov, C_dg,ov; L_ov; q_ch(v_gs)
  - picture: Cross-section with channel charge, overlap regions and depletion regions labeled with each capacitor.
  - pitfalls: C_sb is grounded at both ends in the CS stage, so it is ignored.

### 14.4 Common-source frequency response, bandpass shape
- **amplifier-frequency-response** (passband): AC-coupled amplifiers have a band-pass: coupling and bypass capacitors set a low cutoff, device capacitors set the high cutoff; DC-coupled amplifiers are low-pass only.
  - notation: omega_LF, omega_HF (rad/s); C_Large coupling/bypass (F); R_deg (ohm); |G(j omega)| in dB
  - typical values: Bode plot spans roughly 100 to 10^8 rad/s, mid-band gain about 40 dB, with low-corner about 100 and high-corner about 10^5 (reading from the axis labels)
  - approximations: large capacitors are shorts mid-band; small capacitors are open mid-band
  - picture: Band-pass Bode plot with the three regions and which capacitors rule each.
  - pitfalls: R_deg is bypassed so that it sets the bias but not the AC gain.

### 14.5 Common-source brute force
- **common-source** (full transfer function): Nodal analysis with C_gs, C_gd gives a second-order transfer function plus a right-half-plane zero from C_gd feed-through; with C_db and C_L it is cubic.
  - notation: R_L' = r_o || R_L (ohm); s = j omega; C_L (F)
  - formulas: DC gain A_0 = -g_m R_L'; zero at omega_z = g_m / C_gd (positive, from feed-through) [reconstructed]; widely separated poles approximation: omega_p1 << omega_p2 gives omega_p1 about 1 / [R_s (C_gs + C_gd (1 + g_m R_L')) + R_L' C_gd]
  - approximations: omega_p1 << omega_p2 (dominant pole); C_db + C_L neglected at this step
  - picture: Feed-forward current through C_gd opposes g_m, cancelling the gain at high frequency.
  - pitfalls: algebra gives little insight; use Miller or OCTC instead.

### 14.6 The Miller theorem
- **miller-effect**: A feedback impedance Z_F across an amplifier of gain A looks like Z_F/(1-A) to ground at the input; for a capacitor it multiplies by (1 - A).
  - notation: Z_F (ohm); A (voltage gain, negative for inverting); C_M (F)
  - formulas: Z_M = Z_F / (1 - A); C_M = C (1 - A); for CS: C_M = C_gd (1 - A_v) = C_gd (1 + g_m R_L')
  - approximations: use the low-frequency gain for A; amplifier input impedance assumed infinite; valid when Z_F does not itself change A much
  - picture: Inverting gain makes the capacitor's far end swing opposite and large, so it draws a large current from the input.
  - pitfalls: Miller is a trick that uses an estimate of A that the capacitor itself affects.

### 14.7 Common source with Miller
- **common-source** (Miller approach): Replace C_gd by C_M at the input; the input pole is 1/[R_s (C_gs + C_M)].
  - notation: C_in = C_gs + C_gd (1 + g_m R_L')
  - formulas: tau_in = R_s [C_gs + C_gd (1 + g_m R_L')]; omega_p1 = 1/tau_in
  - typical values: C_Miller about 100 C_gd for a gain near -100 (reader's example)
  - approximations: A_v,Cgd = -g_m R_L' (low-frequency value); close to the brute-force result except for the last term
  - picture: Two decoupled RC nodes, input with a large Miller capacitor, output with C_db.
  - pitfalls: raising gain lowers the input pole, the gain-bandwidth trade-off.

### 14.8 Common drain
- **common-drain**: The capacitor C_gs across a follower sees a gain just under +1, so it is bootstrapped and almost disappears.
  - notation: A_v,Cgs = g_m (r_o || r_oc) / (1 + g_m (r_o || r_oc)) (positive, below 1)
  - formulas: C_M = C_gs (1 - A_v) = C_gs / (1 + g_m (r_o || r_oc)); input pole 1/(R_s [C_gd + C_M]) is very high
  - approximations: second term small when g_m (r_o || r_oc) is large
  - picture: Both ends of C_gs move together, so almost no current flows in it.
  - pitfalls: the input pole is not the follower's limit; the model/approximations break down first. C_gd at the input does not get multiplied.
- **miller-effect** (summary): CS has C_Miller about 100 C_gd (harmful); CD has gain slightly below 1 and positive (negligible).

### 14.9 Common gate
- **common-gate**: Both C_gs and C_gd are grounded at one end, so there is no Miller effect and the stage is broadband.
  - notation: r_o coupling input to output; G_s = 1/R_s; g_o = 1/r_o; C_L' = C_gd + C_db + C_L (F)
  - formulas: input pole omega_in = (g_m + G_s) / C_gs, i.e. 1/[(R_s || 1/g_m) C_gs], lower-bounded by about g_m/C_gs which is omega_T; output pole omega_out = 1/(R_L C_L')
  - approximations: g_o = 0 (g_m r_o >> 1, so g_m >> g_o); DC gain with g_o neglected is g_m R_L / (1 + g_m R_s) [reconstructed]
  - picture: A low-impedance input node and a separate output RC with no cap bridging them.
  - pitfalls: r_o is the only coupling element; ignoring it is justified because it always adds to much larger conductances.

### 14.10 Device unity-gain frequency
- **transit-frequency**: f_T is where the short-circuit current gain of the transistor falls to 1, about g_m / (2 pi (C_gs + C_gd)).
  - notation: f_T (Hz); omega_T = 2 pi f_T (rad/s); i_out/i_s = A_i
  - formulas: A_i(s) = (g_m - s C_gd) / (s (C_gs + C_gd)) approx g_m / (s (C_gs + C_gd)); omega_T = g_m / (C_gs + C_gd); square law: omega_T = (3/2) mu V_OV / L^2 approx 3 mu (V_GS - V_T) / (2 L^2) [reconstructed]; channel field V_DS,ch / L with velocity mu E: omega_T about 1/(carrier transit time)
  - typical values: L < 100 nm gives f_T > 100 GHz; amplifiers designed for hundreds of MHz
  - approximations: g_m dominates the C_gd feed-through; C_db and r_o neglected
  - picture: Current gain falls 20 dB per decade, hitting 0 dB at f_T; f_T is roughly 1/transit time through the channel.
  - pitfalls: f_T is an upper bound; practical gain-bandwidth is below it.

### 14.11 OCTC
- **open-circuit-time-constants**: Dominant pole is estimated as the inverse of the sum of tau_i = R_Ci C_i, where R_Ci is the resistance across each capacitor with all other capacitors open.
  - notation: b_1 (s); R_Ci (ohm); tau_i (s); omega_1 (rad/s)
  - formulas: H(s) = 1/(1 + b_1 s + b_2 s^2 + ...); omega_1 about 1/b_1; b_1 = sum_i R_Ci C_i
  - approximations: no zeros; omega_1 << min(omega_2,...,omega_n)
  - picture: Each capacitor sees its own Thevenin resistance; the biggest tau (not biggest C) limits bandwidth.
  - pitfalls: independent sources are zeroed (voltage shorted, current opened) when finding R_Ci; omit other capacitors, don't short them.

### 14.12 OCTC applied to CS
- **open-circuit-time-constants** (CS example): R_Cgs = R_s; R_Cgd = R_s + R_L' + g_m R_s R_L'; R_Cdb(+C_L) = R_L'.
  - formulas: b_1 = R_s C_gs + [R_s (1 + g_m R_L') + R_L'] C_gd + R_L' (C_db + C_L) [reconstructed]; approximately R_s [C_gs + C_gd (1 + g_m R_L')] + R_L' (C_gd + C_db + C_L)
  - approximations: first term equals the Miller input time constant, second term equals the Miller output time constant
  - picture: Three capacitors, three resistances, one sum; the C_gd term is the Miller-sized one.
  - pitfalls: with many capacitors it is clunky; if one tau is about 100x the rest, keep just that one.
- **dominant-pole**: A high-impedance node is often designed in on purpose, and capacitance is added there to compensate (pointer to Sec. 17.9).
  - approximations: keep only tau larger than the others by about 100x

## Chapter 15. Multi-Stage Amplifiers

### 15.2 The need for multi-stage amplifiers
- **multistage-amplifier**: Cascade stages to get more gain, better bandwidth through isolation, impedance matching, level shifting and DC coupling.
  - notation: g_m r_o intrinsic gain
  - typical values: g_m r_o about 100 at L = 1 um; about 10 at 28 nm
  - picture: Fig. 15.2 chart of single-stage types with two-port models (CS g_m amp, CG current buffer, CD voltage buffer), to be "committed to memory".
  - pitfalls: more gain is not always better; buffers decouple high-Z nodes from large capacitive loads.

### 15.3 Input and output impedance
- **input-output-resistance**: Ideal amplifier types have input and output resistance (voltage: inf, 0; current: 0, inf; transconductance: inf, inf; transresistance: 0, 0), so a good cascade drives a high-Z input from a low-Z output.
  - notation: R_in, R_out (ohm)
  - approximations: "voltage matching" (low-Z source into high-Z load) or "current matching" (the opposite)
  - pitfalls: voltage amp driving a current amp loads badly, but voltage amp driving a transconductance amp is fine.
- **amplifier-two-port**: A cascade of unilateral stages is one two-port with R_in of stage 1 and R_out of stage 2.
- **interstage-loading**: Cascading must not disturb either stage's DC bias point (otherwise AC-coupling capacitors are needed).

### 15.4 Common-source cascades
- **multistage-amplifier** (two CS stages): Low-frequency gain is the product of stages, A_v = A_v1 A_v2 with A_vk = -g_mk (r_ok || r_ock); R_in = R_in,1; R_out = R_out,2.
  - notation: r_o1 || r_oc1, r_o2 || r_oc2 (ohm); C_M1, C_M2 (F); tau_1 = C_M1 R_s; tau_2 = C_M2 (r_o1 || r_oc1)
  - formulas: C_M1 = C_gs1 + C_gd1 (1 + g_m1 (r_o1 || r_oc1)); C_M2 = C_gs2 + C_db1 + C_gd2 (1 + g_m2 (r_o2 || r_oc2))
  - approximations: Miller with low-frequency gains; three independent nodes (input, intermediate, output)
  - picture: Six capacitors reduce to three RC nodes; the intermediate node (high R times large Miller C) is the killer.
  - pitfalls: poles close together give very poor bandwidth; keep R_s low.
- **bandwidth-extension-buffer**: A source follower between CS stages presents 1/g_m to the first stage and does not load it (bootstrapped C_gs), so the intermediate time constant collapses.
  - formulas: follower input C_in about C_gd (C_gs bootstrapped); tau at follower output about C/g_m (small)
  - picture: Fig. 15.7/15.8: CS, then CD, then CS, with the follower isolating the Miller capacitor from a high-Z node.
  - pitfalls: R_s still needs to stay low.

### 15.5 CS with capacitive load
- **common-source** (capacitive load): With a large C_L the output pole 1/((R_D || r_o) C_L) dominates; a source follower buffer between the gain stage and C_L extends bandwidth more cheaply than raising g_m or lowering R_D.
  - notation: R_in = R_B1 || R_B2 (ohm); C_L (F); C_Large coupling and bypass
  - formulas: tau_in = (R_s || R_in) [C_gs + C_gd (1 + g_m (R_D || r_o))]; tau_out about (R_D || r_o) C_L when C_L >> C_gs, C_gd, C_db [reconstructed]
  - approximations: C_L >> parasitics
  - picture: Output RC dominated by the load capacitor; the follower puts 1/g_m in front of it.
  - pitfalls: lowering R_D loses gain; recovering it with g_m costs power.

### 15.6 Cascode
- **cascode**: A CS stage (M1) with a CG stage (M2) stacked on it has the same g_m as a single device, output resistance boosted by about g_m r_o, and little Miller effect.
  - notation: g_m1, g_m2 (S); r_o1, r_o2 (ohm); R_D (ohm); I_bias (A); V_bias (V); nodes g (gate), i (internal drain of M1), o (output); C_i, C_o (F); R_s,2 = r_o1
  - formulas: CG two-port: R_in = 1/g_m, output current source with R_D || (r_o2 + g_m r_o2 r_o1); gain with R_D load -g_m1 R_D (when R_D << g_m r_o^2) [reconstructed]; with ideal current source load gain is about -g_m (g_m r_o^2) = -(g_m r_o)^2 [reconstructed from "substantially higher than single transistor"]
  - typical values: internal gain A_vi = -g_m1 / g_m2 = -1 for equal devices
  - approximations: R_D throws away gain; cascode input C_M = C_gd1 (1 + 1) = 2 C_gd1 (small)
  - picture: A "supercharged" transistor: M2 shields M1's drain, so M1's drain barely swings.
  - pitfalls: costs voltage headroom; M2's C_gd is grounded so it is not Miller-multiplied; intermediate node has low impedance 1/g_m2 so it is fast.
- **cascode-mirror** (as active load): Use a cascode current-mirror load in place of the ideal current source so that R_out is not limited by r_oc.
  - picture: NMOS cascode with PMOS cascode load, M1-M4 stacked, bias1..bias3 gates.
- **output-swing** (design example): the cascode amp with cascode load has four stacked V_d,sat devices.
  - formulas: A_v = -g_m1 R_out, R_out = (g_m r_o^2) / 2 (NMOS cascode || PMOS cascode load); need |A_v| = 5000
  - typical values: g_m1 = 1 mS; R_out = 5 Mohm; each cascode r_out = 10 Mohm; so r_o = 100 kohm [reconstructed from g_m r_o^2 = 10 Mohm with equal g_m, r_o]; k = mu C_ox = 100 uA/V^2; lambda = 0.1 V^-1; I_D = 1/(lambda r_o) = 100 uA; W/L = g_m^2 / (2 k I_D) = 50; V_d,sat = V_OD = 2 I_D / g_m = 0.2 V; four devices, so V_DD,min = V_swing + 0.8 V (for 0.4 V swing, 1.2 V)
  - approximations: all g_m and r_o equal; long-channel V_d,sat = V_GS - V_T
  - picture: Voltage stack: 4 x V_d,sat of 0.2 V eaten from the supply, leaving the rest for output swing.
  - pitfalls: undetermined DC output level because M1 fights M4 to set the current; need a feedback circuit (common-mode feedback) to set mid-rail; g_m chosen early because of bandwidth needs in op-amps.

### 15.7 Big circuit, folded cascode
- **folded-cascode**: Find the signal path, treat diode-connected and fixed-V_GS devices as DC levels (AC ground or current source) and see an NMOS CS followed by a PMOS CG; this is the folded cascode.
  - notation: M1..M8; M2 (NMOS CS input), M3 (PMOS CG); M1, M4 current sources (open circuit in AC); V_G1, V_G3, V_G4; R_S, R_L, C
  - formulas: I_D2 = I_M1 - I_M4 (M4 sets M3's current, M1 supplies the rest to M2); gain from M2 g_m times the load resistance seen at v_o [reconstructed]
  - approximations: M3 input conductance about g_m3 much larger than g_o1, so no AC current goes to M1; breaks if R_L is very large; M1 is not mirrored into M5 because M1 is not diode-connected
  - picture: A cascode folded down; M1 current is divided between M2 and M3 (current divider).
  - pitfalls: folding lowers headroom and shifts the DC level; same v_gs does not mean mirrored current unless the device is diode-connected.

## Notation and conventions for these chapters

| symbol | meaning | unit | sign convention |
|---|---|---|---|
| V_OD, V_od, V_D,sat | overdrive V_GS - V_T (long channel) | V | positive; saturation needs V_DS > V_OD (BJT V_CE > V_CE,sat) |
| I_in, I_out, I_ref, I_Q | mirror input, output, reference, bias currents | A | I_out flows into the output device drain (NMOS sinks to ground, PMOS sources from V_DD) |
| N | mirror ratio, I_out/I_in = (W/L)_2/(W/L)_1 | none | N > 1 scales up; scale W, not L |
| r_o, r_oc | transistor output resistance (about 1/(lambda I_D)); output resistance of a mirror/bias current source | ohm | positive |
| R_L,eff | R_L || r_o || r_oc | ohm | |
| R_s | source resistance of signal source (Ch 14-15); also degeneration resistor in Ch 13 | ohm | context-dependent: same symbol, two roles |
| R_deg | bias degeneration resistor, bypassed at AC | ohm | |
| R_L' | r_o || R_L (CS) | ohm | |
| A_v, G_v | voltage gain v_out/v_s | V/V | negative for CS, slightly below +1 for CD |
| C_M | Miller-equivalent capacitance C(1 - A_v) | F | A_v negative increases C |
| C_gs, C_gd, C_db, C_sb | MOS capacitances | F | C_gd couples input and output in CS |
| C_Large | coupling or bypass capacitor treated as an AC short | F | |
| tau_i = R_Ci C_i; b_1 = sum tau_i | open-circuit time constants | s | |
| omega_p, omega_z, omega_LF, omega_HF | pole, zero and band edges | rad/s | omega = 2 pi f; zero from C_gd at g_m/C_gd |
| omega_T = 2 pi f_T | current-gain unity frequency, about g_m/(C_gs + C_gd) | rad/s (Hz) | |
| g_m, 1/g_m | transconductance; CG/CD resistance | S, ohm | |
| s = j omega | complex frequency | rad/s | j is the imaginary unit |
| V_min | minimum output voltage keeping the mirror in saturation | V | V_OD, I R_s + V_OD, V_T + 2 V_OD, or 2 V_OD |
| R_in, R_out | input and output resistance of a stage or cascade | ohm | cascade R_in = R_in,1, R_out = R_out,2 |
| R_B1 || R_B2 | bias divider resistors, included in R_in | ohm | |
| lambda | channel-length-modulation parameter | 1/V | reader's example 0.1 V^-1 |
| k = mu C_ox | process transconductance parameter | A/V^2 | reader's example 100 uA/V^2 |

## Where a visual would help most

1. **Cascode vs simple mirror headroom and R_out**: drag V_out and bias gate voltages; I_D vs V_DS curve moves with V_min marker for simple, degenerate, cascode, high-swing. Click: output resistance rises by g_m r_o at the price of an extra V_T + V_OD of minimum voltage.
2. **Miller multiplication of C_gd**: drag the gain A_v (or g_m, R_L') and watch the input capacitance C_M and input pole move on a Bode plot. Click: a CS gain of -100 makes a 1 fF C_gd look like 101 fF, and a CD gain just below +1 makes C_gs nearly vanish.
3. **Dominant pole by OCTC**: drag the individual capacitors and resistors on a CS amplifier; bars show tau_i, a Bode plot shows sum. Click: the largest tau, not the largest C, sets the bandwidth.
4. **f_T and channel transit time**: drag L, V_OD, mobility; see f_T, current-gain curve crossing 0 dB, and a carrier crossing the channel. Click: f_T is about the inverse of transit time, and shorter L raises it as 1/L^2.
5. **CS cascade vs buffered cascade vs cascode**: drag R_s, C_L, whether a follower is inserted, and see three node poles on one Bode plot. Click: the intermediate high-R, Miller-boosted node kills bandwidth, and either a follower or a cascode takes it out.
6. **Constant-g_m reference**: drag V_DD, temperature (V_T) and R_S; see I_D, V_OV and g_m. Click: I_D and g_m do not move with V_DD or V_T, only with R_S.
7. **Mirror ratio and mismatch**: drag N, lambda and the V_out difference; see I_out vs I_in and error from channel-length modulation. Click: mirror holds as long as M2 stays saturated, with an error of about lambda delta V_DS.
8. **Cascode design budget (headroom stack)**: drag g_m, gain target, k and lambda; see r_o, I_D, W/L, V_OD, and a stacked voltage bar of four V_d,sat. Click: a gain of 5000 forces 4 x 0.2 V of headroom, so a 1.2 V supply leaves only 0.4 V of swing.
