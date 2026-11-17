"""Reference script for plans/small-signal-analysis.md. Standard library only.

An NMOS with k = mu_n C_ox W/L (A/V^2), threshold VT (V) and channel-length modulation lambda (1/V):
  cut-off    V_GS <= VT:                    I_D = 0
  saturation V_DS >= V_OV = V_GS - VT:      I_D = (k/2) V_OV^2 (1 + lambda V_DS)
  triode     0 <= V_DS < V_OV:              I_D = k (V_OV V_DS - V_DS^2/2) (1 + lambda V_DS)
The common-source stage: V_DD through R_D to the drain, the source grounded, V_GS on the gate.
Prints the plan's check cases as one JSON list.
"""
import json
import math


def drain_current(k, VT, lam, VGS, VDS):
    vov = VGS - VT
    if vov <= 0:
        return 0.0
    if VDS >= vov:
        return 0.5 * k * vov * vov * (1 + lam * VDS)
    return k * (vov * VDS - 0.5 * VDS * VDS) * (1 + lam * VDS)


def bias_point(k, VT, lam, VGS, VDD, RD):
    vov = VGS - VT
    if vov <= 0:
        return {"ID": 0.0, "VDS": VDD, "VOV": vov, "region": "cut-off"}
    # saturation: I = a (1 + lam (VDD - I RD)) with a = k vov^2 / 2, solved for I
    a = 0.5 * k * vov * vov
    I = a * (1 + lam * VDD) / (1 + a * lam * RD)
    VDS = VDD - I * RD
    if VDS >= vov:
        return {"ID": I, "VDS": VDS, "VOV": vov, "region": "saturation"}
    # triode: the load line (VDD - V)/RD meets the triode curve somewhere in 0 < V < vov; bisect on V
    lo, hi = 0.0, vov
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (VDD - mid) / RD - drain_current(k, VT, lam, VGS, mid) > 0:
            lo = mid
        else:
            hi = mid
    VDS = 0.5 * (lo + hi)
    return {"ID": (VDD - VDS) / RD, "VDS": VDS, "VOV": vov, "region": "triode"}


def gm(k, VT, lam, VGS, VDS):
    vov = VGS - VT
    if vov <= 0:
        return 0.0
    if VDS >= vov:
        return k * vov * (1 + lam * VDS)
    return k * VDS * (1 + lam * VDS)


def ro(lam, ID):
    return math.inf if lam * ID == 0 else 1 / (lam * ID)


def gain(gm_, ro_, RD):
    par = RD if math.isinf(ro_) else ro_ * RD / (ro_ + RD)
    return -gm_ * par


def hd2_rule(VOV, vhat):
    return vhat / (4 * VOV)


def harmonics(k, VT, lam, VGS, VDS, vhat):
    """the drain-current wiggle for v_gs = vhat sin(theta) at fixed V_DS: amplitudes of its fundamental and
    second harmonic, from a 256-point discrete Fourier sum"""
    N = 256
    I0 = drain_current(k, VT, lam, VGS, VDS)
    s1 = c1 = s2 = c2 = 0.0
    for n in range(N):
        th = 2 * math.pi * n / N
        i = drain_current(k, VT, lam, VGS + vhat * math.sin(th), VDS) - I0
        s1 += i * math.sin(th)
        c1 += i * math.cos(th)
        s2 += i * math.sin(2 * th)
        c2 += i * math.cos(2 * th)
    a1 = 2 / N * math.hypot(s1, c1)
    a2 = 2 / N * math.hypot(s2, c2)
    return {"a1": a1, "a2": a2, "ratio": 0.0 if a1 == 0 else a2 / a1}


def swing(k, VT, lam, VGS, VDS, vhat):
    """the drain current's rise at v_gs = +vhat and its fall at v_gs = -vhat, exact, at fixed V_DS"""
    I0 = drain_current(k, VT, lam, VGS, VDS)
    return {"up": drain_current(k, VT, lam, VGS + vhat, VDS) - I0,
            "down": I0 - drain_current(k, VT, lam, VGS - vhat, VDS)}


# checks of the closed forms against limits and slopes
K, VT, LAM = 2e-3, 0.5, 0.1
assert abs(gm(K, VT, 0, 0.8, 2) - 2 * drain_current(K, VT, 0, 0.8, 2) / 0.3) < 1e-15
h = 1e-6
assert abs((drain_current(K, VT, LAM, 0.8 + h, 2) - drain_current(K, VT, LAM, 0.8 - h, 2)) / (2 * h) - gm(K, VT, LAM, 0.8, 2)) < 1e-9
bp = bias_point(K, VT, LAM, 0.8, 3, 1e4)
assert abs(bp["ID"] - drain_current(K, VT, LAM, 0.8, bp["VDS"])) < 1e-15
bp = bias_point(K, VT, LAM, 1.1, 3, 1e4)
assert abs(bp["ID"] - drain_current(K, VT, LAM, 1.1, bp["VDS"])) < 1e-12
assert abs(harmonics(K, VT, 0, 0.8, 2, 0.03)["ratio"] - hd2_rule(0.3, 0.03)) < 1e-12

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    if isinstance(value, float) and math.isinf(value):
        value = "Infinity"
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("drainCurrent", [2e-3, 0.5, 0, 0.8, 2], drain_current(2e-3, 0.5, 0, 0.8, 2), "A", "typical",
     "k = 2 mA/V², V_T = 0.5 V, no λ, V_GS = 0.8 V (V_OV = 0.3 V), saturated: I_D = ½·2 mA/V²·(0.3 V)² = 90 µA", tol=1e-12)
case("drainCurrent", [2e-3, 0.5, 0.1, 0.8, 2], drain_current(2e-3, 0.5, 0.1, 0.8, 2), "A", "typical",
     "the same with λ = 0.1 /V at V_DS = 2 V: 90 µA × 1.2 = 108 µA", tol=1e-12)
case("drainCurrent", [2e-3, 0.5, 0, 1.0, 0.1], drain_current(2e-3, 0.5, 0, 1.0, 0.1), "A", "typical",
     "triode: V_OV = 0.5 V but V_DS = 0.1 V: I_D = 2 mA/V²·(0.5·0.1 − 0.005) V² = 90 µA", tol=1e-12)
case("drainCurrent", [2e-3, 0.5, 0.1, 0.4, 2], drain_current(2e-3, 0.5, 0.1, 0.4, 2), "A", "limit-zero",
     "V_GS = 0.4 V is below V_T = 0.5 V: cut off, no current", tol=1e-12)
case("biasPoint", [2e-3, 0.5, 0.1, 0.8, 3, 10000], bias_point(2e-3, 0.5, 0.1, 0.8, 3, 1e4), "A, V", "typical",
     "W/L = 10 (k = 2 mA/V²), V_GS = 0.8 V, V_DD = 3 V, R_D = 10 kΩ, λ = 0.1 /V: I_D = 107 µA, V_DS = 1.93 V, saturated", tol=1e-12)
case("biasPoint", [2e-3, 0.5, 0.1, 1.1, 3, 10000], bias_point(2e-3, 0.5, 0.1, 1.1, 3, 1e4), "A, V", "breaks",
     "the same stage with V_GS = 1.1 V: the drain falls to 0.289 V, below V_OV = 0.6 V. The transistor is in triode and the saturation model no longer holds", tol=1e-12)
case("gm", [2e-3, 0.5, 0, 0.8, 2], gm(2e-3, 0.5, 0, 0.8, 2), "S", "typical",
     "k = 2 mA/V² at V_OV = 0.3 V, no λ: g_m = k·V_OV = 0.6 mS, which is also 2·90 µA/0.3 V", tol=1e-12)
case("gm", [2e-3, 0.5, 0, 1.1, 2], gm(2e-3, 0.5, 0, 1.1, 2), "S", "typical",
     "the same transistor at V_OV = 0.6 V: g_m doubles to 1.2 mS. g_m belongs to the bias point, not to the transistor", tol=1e-12)
case("gm", [2e-3, 0.5, 0.1, 0.8, 1.9267], gm(2e-3, 0.5, 0.1, 0.8, 1.9267), "S", "typical",
     "with λ = 0.1 /V at the stage's V_DS = 1.93 V: g_m = 0.6 mS × 1.193 = 0.716 mS", tol=1e-12)
case("gm", [2e-3, 0.5, 0.1, 0.45, 2], gm(2e-3, 0.5, 0.1, 0.45, 2), "S", "limit-zero",
     "V_GS below V_T: no current and no slope, g_m = 0", tol=1e-12)
case("ro", [0.1, 0.0001], ro(0.1, 1e-4), "Ω", "typical",
     "λ = 0.1 /V at I_D = 100 µA: r_o = 1/(λ·I_D) = 100 kΩ")
case("ro", [0, 0.0001], ro(0, 1e-4), "Ω", "limit-infinity",
     "with λ = 0 the drain current ignores V_DS: r_o is infinite, an ideal current source")
case("gain", [0.0006, "Infinity", 10000], gain(6e-4, math.inf, 1e4), "", "limit-infinity",
     "g_m = 0.6 mS into R_D = 10 kΩ with r_o infinite: A_v = −g_m·R_D = −6")
case("gain", [0.0007156, 93170, 10000], gain(7.156e-4, 93170, 1e4), "", "typical",
     "g_m = 0.716 mS, r_o = 93.2 kΩ, R_D = 10 kΩ: A_v = −g_m (r_o ∥ R_D) = −6.46")
case("hd2Rule", [0.3, 0.03], hd2_rule(0.3, 0.03), "", "typical",
     "v̂ = 30 mV on V_OV = 0.3 V: the second harmonic is v̂/(4·V_OV) = 2.5% of the fundamental")
case("harmonics", [2e-3, 0.5, 0, 0.8, 2, 0.03], harmonics(2e-3, 0.5, 0, 0.8, 2, 0.03), "A, A, ratio", "typical",
     "the same, from the curve itself: a fundamental of g_m·v̂ = 18 µA and a second harmonic of 0.45 µA, 2.5%", tol=1e-12)
case("harmonics", [2e-3, 0.5, 0, 0.8, 2, 0.001], harmonics(2e-3, 0.5, 0, 0.8, 2, 0.001), "A, A, ratio", "limit-zero",
     "v̂ = 1 mV on V_OV = 0.3 V: the second harmonic is 0.083% of the fundamental. Small means small next to V_OV", tol=1e-12)
case("harmonics", [2e-3, 0.5, 0, 0.8, 2, 0.5], harmonics(2e-3, 0.5, 0, 0.8, 2, 0.5), "A, A, ratio", "breaks",
     "v̂ = 0.5 V on V_OV = 0.3 V: the transistor cuts off for part of every cycle and the second harmonic is 37% of the fundamental; the rule v̂/(4V_OV) would say 42%", tol=1e-12)
case("swing", [2e-3, 0.5, 0, 0.8, 2, 0.3], swing(2e-3, 0.5, 0, 0.8, 2, 0.3), "A", "breaks",
     "v̂ = V_OV = 0.3 V: the current rises 270 µA and falls 90 µA, while the tangent g_m·v̂ = 180 µA predicts the same both ways", tol=1e-12)
case("swing", [2e-3, 0.5, 0, 0.8, 2, 0.01], swing(2e-3, 0.5, 0, 0.8, 2, 0.01), "A", "sign",
     "v̂ = 10 mV: up 6.1 µA and down 5.9 µA, within 2% of g_m·v̂ = 6 µA. The rise is always the larger: the curve bends up", tol=1e-12)

print(json.dumps(cases, ensure_ascii=False))
