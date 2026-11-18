"""Reference script for plans/current-mirror.md. Standard library only.

An NMOS mirror. M1 is diode-connected (gate tied to drain) and carries I_REF; M2 has n times M1's W/L, the same V_GS,
and its drain on a voltage V_out. The square law with channel-length modulation in both regions, as in the other EE 105
tools: k = mu_n C_ox W/L in A/V^2, V_T in V, lam in 1/V.
  saturation  I = (k/2) V_OV^2 (1 + lam V_DS)        triode  I = k (V_OV V_DS - V_DS^2/2)(1 + lam V_DS)
Prints the plan's check cases as one JSON list.
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


def vgs_for_current(k, VT, lam, I):
    """the V_GS a diode-connected transistor settles at to carry I (V_DS = V_GS): bisection on [VT, VT + 10]"""
    lo, hi = VT, VT + 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if drain_current(k, VT, lam, mid, mid) < I:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def output_resistance(lam, I, VDS):
    """the slope of the saturated law, (1 + lam V_DS)/(lam I); infinite when lam I = 0"""
    return math.inf if lam * I == 0 else (1 + lam * VDS) / (lam * I)


def mirror(k1, VT, lam, Iref, n, Vout):
    vgs = vgs_for_current(k1, VT, lam, Iref)
    vov = vgs - VT
    iout = drain_current(n * k1, VT, lam, vgs, Vout)
    region = "saturation" if Vout >= vov else "triode"
    return {"VGS": vgs, "VOV": vov, "Iout": iout, "region": region, "error": iout / (n * Iref) - 1,
            "ro": output_resistance(lam, iout, Vout) if region == "saturation" else None}


def diode_resistance(k1, VT, lam, Iref):
    """small-signal resistance of the diode-connected M1: 1/g_m in parallel with r_o"""
    vgs = vgs_for_current(k1, VT, lam, Iref)
    gm = k1 * (vgs - VT) * (1 + lam * vgs)
    ro = output_resistance(lam, Iref, vgs)
    g = gm + (0 if math.isinf(ro) else 1 / ro)
    return 1 / g


def load_gain(kind, I, VOVamp, lam, VDD):
    """common-source gain at a bias current I, with an amplifying transistor at overdrive VOVamp:
    g_m = 2I/VOVamp, r_o = 1/(lam I). kind "resistor": R_D = (VDD/2)/I, so the output sits at mid-supply.
    kind "mirror": the load is a current source of output resistance 1/(lam I)."""
    gm = 2 * I / VOVamp
    ro = math.inf if lam == 0 else 1 / (lam * I)
    load = (VDD / 2) / I if kind == "resistor" else ro
    if math.isinf(ro) and math.isinf(load):
        return -math.inf
    if math.isinf(ro):
        par = load
    elif math.isinf(load):
        par = ro
    else:
        par = ro * load / (ro + load)
    return -gm * par


K1, VT = 2e-3, 0.5
# checks: M1 carries exactly I_REF; M2 copies it exactly when its drain sits at V_GS
v = vgs_for_current(K1, VT, 0.1, 1e-4)
assert abs(drain_current(K1, VT, 0.1, v, v) - 1e-4) < 1e-16
assert abs(mirror(K1, VT, 0.1, 1e-4, 1, v)["error"]) < 1e-12
assert abs(mirror(K1, VT, 0.1, 1e-4, 3, v)["Iout"] - 3e-4) < 1e-15

cases = []


def special(v):
    """JSON has no infinities: write them as the strings the tool tests read back"""
    if isinstance(v, float) and math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    if isinstance(v, dict):
        return {k: special(x) for k, x in v.items()}
    return v


def case(fn, args, value, units, tag, note, tol=1e-9):
    value = special(value)
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("vgsForCurrent", [K1, VT, 0, 1e-4], vgs_for_current(K1, VT, 0, 1e-4), "V", "typical",
     "k = 2 mA/V², V_T = 0.5 V, no λ, I_REF = 100 µA: the diode settles at V_GS = 0.5 + √(2I/k) = 0.816 V", tol=1e-12)
case("vgsForCurrent", [K1, VT, 0.1, 1e-4], vgs_for_current(K1, VT, 0.1, 1e-4), "V", "typical",
     "the same with λ = 0.1 /V: 0.804 V, a little lower, because its own V_DS = V_GS adds a few percent of current", tol=1e-12)
case("vgsForCurrent", [K1, VT, 0.1, 1e-9], vgs_for_current(K1, VT, 0.1, 1e-9), "V", "limit-zero",
     "1 nA: V_GS is barely above V_T, 0.501 V; the square law's tail, where real transistors are subthreshold", tol=1e-12)
case("mirror", [K1, VT, 0.1, 1e-4, 1, 1.5], mirror(K1, VT, 0.1, 1e-4, 1, 1.5), "V, A", "typical",
     "a 1:1 mirror, I_REF = 100 µA, λ = 0.1 /V, V_out = 1.5 V: I_out = 106 µA, 6.4 % high, because M2's drain sits 0.7 V above M1's", tol=1e-12)
case("mirror", [K1, VT, 0.1, 1e-4, 1, 0.804], mirror(K1, VT, 0.1, 1e-4, 1, 0.804), "V, A", "typical",
     "V_out = 0.804 V, almost exactly V_GS: the copy is within 0.003 %", tol=1e-12)
case("mirror", [K1, VT, 0.1, 1e-4, 3, 1.5], mirror(K1, VT, 0.1, 1e-4, 3, 1.5), "V, A", "typical",
     "M2 three times as wide: I_out = 319 µA, three times the copy, with the same 6.4 % error", tol=1e-12)
case("mirror", [K1, VT, 0, 1e-4, 1, 3], mirror(K1, VT, 0, 1e-4, 1, 3), "V, A", "limit-infinity",
     "λ = 0: the copy is exact at any V_out above V_OV, here 3 V, and r_o is infinite", tol=1e-12)
case("mirror", [K1, VT, 0.1, 1e-4, 1, 0.15], mirror(K1, VT, 0.1, 1e-4, 1, 0.15), "V, A", "breaks",
     "V_out = 0.15 V, below V_OV = 0.304 V: M2 is in triode and gives 69.8 µA, 30 % short; the mirror has stopped being a current source", tol=1e-12)
case("outputResistance", [0.1, 1e-4, 1.5], output_resistance(0.1, 1e-4, 1.5), "Ω", "typical",
     "λ = 0.1 /V at 100 µA and V_DS = 1.5 V: r_o = (1 + λV_DS)/(λI) = 115 kΩ; 1/(λI) alone gives 100 kΩ")
case("outputResistance", [0, 1e-4, 1.5], output_resistance(0, 1e-4, 1.5), "Ω", "limit-infinity",
     "λ = 0: an ideal current source, infinite output resistance")
case("diodeResistance", [K1, VT, 0.1, 1e-4], diode_resistance(K1, VT, 0.1, 1e-4), "Ω", "typical",
     "the diode-connected M1 at 100 µA: 1/g_m ∥ r_o = 1.50 kΩ, close to 1/g_m; a small resistance, not the 8 kΩ of V_GS/I_REF")
case("loadGain", ["resistor", 1e-4, 0.2, 0.1, 3], load_gain("resistor", 1e-4, 0.2, 0.1, 3), "", "typical",
     "a common-source stage at 100 µA with V_OV = 0.2 V and R_D = 15 kΩ (the drain at mid-supply on 3 V): A_v = −13.0")
case("loadGain", ["mirror", 1e-4, 0.2, 0.1, 3], load_gain("mirror", 1e-4, 0.2, 0.1, 3), "", "typical",
     "the same stage with a mirror load of r_o = 100 kΩ: A_v = −g_m(r_o ∥ r_o) = −1/(λV_OV) = −50")
case("loadGain", ["mirror", 1e-3, 0.2, 0.1, 3], load_gain("mirror", 1e-3, 0.2, 0.1, 3), "", "sign",
     "ten times the current with the mirror load: still −50. g_m grows with I and r_o falls with it; the gain does not care")
case("loadGain", ["mirror", 1e-4, 0.2, 0, 3], load_gain("mirror", 1e-4, 0.2, 0, 3), "", "limit-infinity",
     "λ = 0 with a mirror load: the gain would be infinite; in a real circuit the next stage's input or the transistors' r_o set it")

print(json.dumps(cases, ensure_ascii=False))
