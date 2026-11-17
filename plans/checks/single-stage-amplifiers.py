"""Reference script for plans/single-stage-amplifiers.md. Standard library only.

One NMOS, three ways to connect it. p = { k, VT, lam, VDD, R, VB } in A/V^2, V, 1/V, V, ohms, V.
  cs  common source: v_IN on the gate, source grounded, R from V_DD to the drain; output at the drain
  cg  common gate:   gate held at VB, v_IN (an ideal voltage source) on the source, R from V_DD to the drain;
                     output at the drain
  cd  common drain (source follower): v_IN on the gate, drain on V_DD, R from the source to ground;
                     output at the source
The body is tied to the source, so there is no body effect. Prints the plan's check cases as one JSON list.
"""
import json
import math


def drain_current(k, VT, lam, VGS, VDS):
    vov = VGS - VT
    if vov <= 0 or VDS <= 0:
        return 0.0
    if VDS >= vov:
        return 0.5 * k * vov * vov * (1 + lam * VDS)
    return k * (vov * VDS - 0.5 * VDS * VDS) * (1 + lam * VDS)


def terminals(stage, p, vin, vout):
    """V_GS and V_DS for an input and an output voltage"""
    if stage == "cs":
        return vin, vout
    if stage == "cg":
        return p["VB"] - vin, vout - vin
    return vin - vout, p["VDD"] - vout


def mismatch(stage, p, vin, v):
    """current the resistor carries minus current the transistor carries, at output v; it falls as v rises"""
    VGS, VDS = terminals(stage, p, vin, v)
    I = drain_current(p["k"], p["VT"], p["lam"], VGS, VDS)
    if stage == "cd":
        return I - v / p["R"]
    return (p["VDD"] - v) / p["R"] - I


def solve_out(stage, p, vin):
    lo = vin if stage == "cg" else 0.0
    hi = p["VDD"]
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if mismatch(stage, p, vin, mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def region_of(VGS, VDS, VT):
    if VGS - VT <= 0:
        return "cut-off"
    return "saturation" if VDS >= VGS - VT else "triode"


def bias(stage, p, vin):
    vout = solve_out(stage, p, vin)
    VGS, VDS = terminals(stage, p, vin, vout)
    return {"vout": vout, "ID": drain_current(p["k"], p["VT"], p["lam"], VGS, VDS), "VGS": VGS, "VDS": VDS,
            "VOV": VGS - p["VT"], "region": region_of(VGS, VDS, p["VT"])}


def gm(k, VT, lam, VGS, VDS):
    vov = VGS - VT
    if vov <= 0:
        return 0.0
    if VDS >= vov:
        return k * vov * (1 + lam * VDS)
    return k * VDS * (1 + lam * VDS)


def ro(lam, ID, VDS):
    # the exact slope of the saturated law: dI/dV_DS = lam I / (1 + lam V_DS)
    return math.inf if lam * ID == 0 else (1 + lam * VDS) / (lam * ID)


def par(a, b):
    if math.isinf(a):
        return b
    if math.isinf(b):
        return a
    return a * b / (a + b)


def small_signal(stage, g, r, R):
    if stage == "cs":
        return {"Av": -g * par(r, R), "Rin": "Infinity", "Rout": par(r, R)}
    if stage == "cg":
        if math.isinf(r):
            return {"Av": g * R, "Rin": 1 / g, "Rout": R}
        return {"Av": (1 + g * r) * R / (R + r), "Rin": (r + R) / (1 + g * r), "Rout": par(r, R)}
    rr = par(r, R)
    Av = 1.0 if math.isinf(rr) else g * rr / (1 + g * rr)
    return {"Av": Av, "Rin": "Infinity", "Rout": par(1 / g, rr)}


def slope(stage, p, vin):
    h = 1e-4
    return (solve_out(stage, p, vin + h) - solve_out(stage, p, vin - h)) / (2 * h)


def sat_range(stage, p):
    """the input interval over which the transistor is saturated, and the output interval it maps to"""
    N = 600
    reg = lambda v: bias(stage, p, v)["region"]
    xs = [p["VDD"] * i / N for i in range(N + 1)]
    sat = [reg(x) == "saturation" for x in xs]
    if not any(sat):
        return None
    first = sat.index(True)
    last = N - sat[::-1].index(True)

    def edge(a, b):
        # a is outside saturation, b inside (or the reverse); bisect for the boundary
        inside_b = reg(b) == "saturation"
        for _ in range(60):
            m = 0.5 * (a + b)
            if (reg(m) == "saturation") == inside_b:
                b = m
            else:
                a = m
        return 0.5 * (a + b)

    lo = xs[0] if first == 0 else edge(xs[first - 1], xs[first])
    hi = xs[N] if last == N else edge(xs[last + 1], xs[last])
    o1, o2 = solve_out(stage, p, lo), solve_out(stage, p, hi)
    return {"inLo": lo, "inHi": hi, "outLo": min(o1, o2), "outHi": max(o1, o2)}


def room(stage, p, vin):
    """how far the output can move down and up from its bias before the transistor leaves saturation"""
    v = solve_out(stage, p, vin)
    s = sat_range(stage, p)
    return {"down": v - s["outLo"], "up": s["outHi"] - v}


def intrinsic_gain(g, r):
    return g * r


P = {"k": 0.002, "VT": 0.5, "lam": 0.1, "VDD": 3, "R": 10000, "VB": 1.2}
P0 = dict(P, lam=0)


def model_at(stage, p, vin):
    b = bias(stage, p, vin)
    g = gm(p["k"], p["VT"], p["lam"], b["VGS"], b["VDS"])
    r = ro(p["lam"], b["ID"], b["VDS"])
    return b, g, r, small_signal(stage, g, r, p["R"])


# the small-signal gain must be the slope of the large-signal curve, in every stage
for st, v in (("cs", 0.8), ("cg", 0.3), ("cd", 1.5)):
    b, g, r, ss = model_at(st, P, v)
    assert b["region"] == "saturation"
    assert abs(slope(st, P, v) - ss["Av"]) < 1e-5 * max(1, abs(ss["Av"])), (st, slope(st, P, v), ss["Av"])

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    if isinstance(value, float) and math.isinf(value):
        value = "Infinity"
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


bcs, gcs, rcs, sscs = model_at("cs", P, 0.8)
bcg, gcg, rcg, sscg = model_at("cg", P, 0.3)
bcd, gcd, rcd, sscd = model_at("cd", P, 1.5)

case("solveOut", ["cs", P, 0.8], solve_out("cs", P, 0.8), "V", "typical",
     "common source, W/L = 10 (k = 2 mA/V²), λ = 0.1 /V, R_D = 10 kΩ, V_DD = 3 V, v_IN = 0.8 V: the drain sits at 1.93 V", tol=1e-12)
case("bias", ["cg", P, 0.3], bcg, "V, A", "typical",
     "common gate, gate at 1.2 V, source driven to 0.3 V: V_GS = 0.9 V, I_D = 175 µA, the drain at 1.25 V, saturated", tol=1e-12)
case("bias", ["cd", P, 1.5], bcd, "V, A", "typical",
     "source follower, R_S = 10 kΩ, gate at 1.5 V: the source sits at 0.752 V, one V_GS = 0.748 V below the gate, with 75.2 µA", tol=1e-12)
case("gm", [0.002, 0.5, 0.1, bcs["VGS"], bcs["VDS"]], gcs, "S", "typical",
     "the common-source bias: g_m = k·V_OV·(1 + λV_DS) = 0.716 mS", tol=1e-12)
case("ro", [0.1, bcs["ID"], bcs["VDS"]], rcs, "Ω", "typical",
     "the common-source bias: r_o = (1 + λV_DS)/(λI_D) = 111 kΩ; the usual 1/(λI_D) gives 93.2 kΩ")
case("smallSignal", ["cs", gcs, rcs, 10000], sscs, "", "typical",
     "common source: A_v = −g_m (r_o ∥ R_D) = −6.57, R_in infinite, R_out = r_o ∥ R_D = 9.17 kΩ")
case("slope", ["cs", P, 0.8], slope("cs", P, 0.8), "", "typical",
     "the slope of the large-signal curve at the same bias: −6.57, the small-signal gain", tol=1e-7)
case("smallSignal", ["cg", gcg, rcg, 10000], sscg, "", "sign",
     "common gate at its bias (g_m = 0.876 mS, r_o = 62.5 kΩ): A_v = +7.69, no inversion; R_in = 1.30 kΩ, near 1/g_m = 1.14 kΩ; R_out = 8.62 kΩ")
case("slope", ["cg", P, 0.3], slope("cg", P, 0.3), "", "sign",
     "the slope of the common-gate curve: positive, +7.69. Raising the source lowers V_GS, so less current and a higher drain", tol=1e-7)
case("smallSignal", ["cd", gcd, rcd, 10000], sscd, "", "typical",
     "source follower at its bias (g_m = 0.607 mS, r_o = 163 kΩ): A_v = 0.851, under 1; R_out = 1/g_m ∥ r_o ∥ R_S = 1.40 kΩ, near 1/g_m = 1.65 kΩ")
case("intrinsicGain", [gcs, rcs], intrinsic_gain(gcs, rcs), "", "typical",
     "common-source bias: g_m·r_o = 79.5, the ceiling on this transistor's gain at this bias, whatever R_D")
case("solveOut", ["cs", P, 0.4], solve_out("cs", P, 0.4), "V", "limit-zero",
     "common source with v_IN = 0.4 V, below V_T = 0.5 V: no current, the drain sits at V_DD = 3 V", tol=1e-12)
case("smallSignal", ["cg", 0.001, "Infinity", 10000], small_signal("cg", 1e-3, math.inf, 1e4), "", "limit-infinity",
     "common gate with r_o infinite, g_m = 1 mS, R_D = 10 kΩ: R_in = 1/g_m = 1 kΩ exactly, A_v = g_m·R_D = 10")
case("smallSignal", ["cd", 0.001, "Infinity", "Infinity"], small_signal("cd", 1e-3, math.inf, math.inf), "", "limit-infinity",
     "follower with r_o and R_S both infinite: A_v = 1 exactly and R_out = 1/g_m = 1 kΩ")
case("smallSignal", ["cs", 0.001, 100000, "Infinity"], small_signal("cs", 1e-3, 1e5, math.inf), "", "limit-infinity",
     "common source with R_D → ∞ (an ideal current-source load), g_m = 1 mS, r_o = 100 kΩ: the gain is the intrinsic gain, −100")
case("solveOut", ["cs", P, 1.1], solve_out("cs", P, 1.1), "V", "breaks",
     "common source pushed 0.3 V above its 0.8 V bias: the tangent predicts 1.93 − 6.57·0.3 = −0.04 V, below ground; the curve says 0.289 V, in triode", tol=1e-12)
case("satRange", ["cs", P], sat_range("cs", P), "V", "typical",
     "common source: saturated for v_IN from 0.5 V to 0.989 V, where v_OUT = v_IN − V_T = 0.489 V; the output can sit anywhere from 0.489 V to 3 V", tol=1e-9)
case("satRange", ["cd", P], sat_range("cd", P), "V", "typical",
     "follower: saturated over the whole input range above V_T, so its output runs from 0 V to 2.07 V at v_IN = 3 V", tol=1e-9)
case("satRange", ["cs", dict(P, R=100000)], sat_range("cs", dict(P, R=100000)), "V", "other",
     "common source with R_D = 100 kΩ: the saturated input window shrinks from 0.489 V wide to 0.167 V wide; the steeper curve crosses the same output range in a narrower input range", tol=1e-9)
case("room", ["cs", P, 0.8], room("cs", P, 0.8), "V", "typical",
     "common source at v_IN = 0.8 V: the output can fall 1.44 V before triode and rise 1.07 V before it reaches V_DD, so a symmetric swing is at most 1.07 V", tol=1e-9)
case("room", ["cs", dict(P, R=20000), 0.8], room("cs", dict(P, R=20000), 0.8), "V", "typical",
     "the same bias with R_D = 20 kΩ: the gain grows from −6.57 to −11.2, but the drain drops to 1.02 V and the room below shrinks from 1.44 V to 0.66 V", tol=1e-9)
case("room", ["cs", dict(P, R=40000), 0.8], room("cs", dict(P, R=40000), 0.8), "V", "breaks",
     "R_D = 40 kΩ at the same bias: the drain falls to 0.158 V, below the edge of saturation (the room below is negative): the transistor is in triode", tol=1e-9)
case("slope", ["cs", dict(P, R=40000), 0.8], slope("cs", dict(P, R=40000), 0.8), "", "breaks",
     "there the curve's slope is only −1.01: more R_D bought less gain, because the transistor left saturation", tol=1e-7)

print(json.dumps(cases, ensure_ascii=False))
