"""Reference script for plans/pn-junction.md. Standard library only.

An abrupt silicon pn junction: p side for x < 0 doped N_A, n side for x > 0 doped N_D, the junction at x = 0.
Course constants: kT/q = 0.026 V, n_i = 1e10 cm^-3, eps_s = 11.7 eps_0 with eps_0 = 8.854e-14 F/cm, q = 1.602e-19 C.
V_D is the applied voltage, p side minus n side (positive is forward). Units: cm, V, C, F, A.

The depletion approximation: the region -x_p < x < x_n holds only ions, rho = -q N_A on the p side and +q N_D on the
n side, and the neutral regions have no field. Gauss's law (dE/dx = rho/eps) from E = 0 at -x_p:
  E(x) = -q N_A (x + x_p)/eps        for -x_p < x <= 0
  E(x) = -q N_D (x_n - x)/eps        for 0 < x < x_n
E continuous at 0 gives N_A x_p = N_D x_n. The potential, measured from the neutral p side, phi = -integral of E:
  phi(x) = q N_A (x + x_p)^2 / (2 eps)              p part
  phi(x) = V - q N_D (x_n - x)^2 / (2 eps)          n part, with V = phi_bi - V_D the total step
Continuity at 0: q N_A x_p^2/(2 eps) + q N_D x_n^2/(2 eps) = V, which with N_A x_p = N_D x_n gives
  W = x_p + x_n = sqrt(2 eps V (1/N_A + 1/N_D) / q)
phi_bi = (kT/q) ln(N_A N_D / n_i^2): the n side's potential from intrinsic minus the p side's.
Equilibrium carriers (V_D = 0), Boltzmann: p(x) = N_A exp(-phi/(kT/q)), n(x) = N_D exp(-(phi_bi - phi)/(kT/q)).
Hole currents at equilibrium, with D_p = r mu_p for a chosen ratio r (in V):
  drift = q mu_p p E,   diffusion = -q D_p dp/dx = -q r mu_p p E/(kT/q)   (since dp/dx = p E/(kT/q))
so drift + diffusion = 0 exactly when r = kT/q: the Einstein relation.
mu_p is the Caughey-Thomas fit (Arora, 300 K) at the p side's doping N_A, the same fit as the drift-and-mobility tool.
Prints the plan's check cases as one JSON list.
"""
import json
import math

Q = 1.602e-19
EPS = 11.7 * 8.854e-14
VT = 0.026
NI = 1e10
FIT = {"n": (88.0, 1252.0, 1.26e17, 0.88), "p": (54.3, 407.0, 2.35e17, 0.88)}


def mobility(carrier, N):
    mn, d, nref, a = FIT[carrier]
    return mn + d / (1 + (N / nref) ** a)


def built_in(NA, ND):
    return VT * math.log(NA * ND / (NI * NI))


def widths(NA, ND, VD):
    V = built_in(NA, ND) - VD
    if V <= 0:
        return {"xp": 0.0, "xn": 0.0, "W": 0.0}
    W = math.sqrt(2 * EPS * V * (1 / NA + 1 / ND) / Q)
    return {"xp": W * ND / (NA + ND), "xn": W * NA / (NA + ND), "W": W}


def field_at(NA, ND, VD, x):
    w = widths(NA, ND, VD)
    if -w["xp"] < x <= 0:
        return -Q * NA * (x + w["xp"]) / EPS
    if 0 < x < w["xn"]:
        return -Q * ND * (w["xn"] - x) / EPS
    return 0.0


def peak_field(NA, ND, VD):
    return field_at(NA, ND, VD, 0.0)


def potential_at(NA, ND, VD, x):
    w = widths(NA, ND, VD)
    V = max(built_in(NA, ND) - VD, 0.0)
    if x <= -w["xp"]:
        return 0.0
    if x <= 0:
        return Q * NA * (x + w["xp"]) ** 2 / (2 * EPS)
    if x < w["xn"]:
        return V - Q * ND * (w["xn"] - x) ** 2 / (2 * EPS)
    return V


def charge_per_area(NA, ND, VD):
    return Q * NA * widths(NA, ND, VD)["xp"]


def junction_cap(NA, ND, VD):
    W = widths(NA, ND, VD)["W"]
    return math.inf if W == 0 else EPS / W


def carriers_at(NA, ND, x):
    phi = potential_at(NA, ND, 0.0, x)
    pbi = built_in(NA, ND)
    return {"n": ND * math.exp(-(pbi - phi) / VT), "p": NA * math.exp(-phi / VT)}


def hole_currents(NA, ND, x, ratio):
    mu = mobility("p", NA)
    p = carriers_at(NA, ND, x)["p"]
    E = field_at(NA, ND, 0.0, x)
    drift = Q * mu * p * E
    diffusion = -Q * ratio * mu * p * E / VT
    return {"drift": drift, "diffusion": diffusion, "net": drift + diffusion}


# checks against limits worked out by hand
NA, ND = 1e18, 1e17
w = widths(NA, ND, 0)
assert abs(NA * w["xp"] - ND * w["xn"]) / (ND * w["xn"]) < 1e-12
assert abs(potential_at(NA, ND, 0, w["xn"] * 0.999999999) - built_in(NA, ND)) < 1e-6
# the potential is continuous at the junction
assert abs(potential_at(NA, ND, 0, 0) - potential_at(NA, ND, 0, 1e-15)) < 1e-6
# the field is minus the slope of the potential
h = 1e-9
for x in (-0.5 * w["xp"], 0.3 * w["xn"]):
    slope = (potential_at(NA, ND, 0, x + h) - potential_at(NA, ND, 0, x - h)) / (2 * h)
    assert abs(slope + field_at(NA, ND, 0, x)) / abs(slope) < 1e-6
# capacitance is the slope of the charge: C_j = -dQ/dV_D... dQ/d(phi_bi - V_D)
dv = 1e-6
dq = charge_per_area(NA, ND, -1 - dv) - charge_per_area(NA, ND, -1 + dv)
assert abs(dq / (2 * dv) - junction_cap(NA, ND, -1)) / junction_cap(NA, ND, -1) < 1e-6
# the carriers meet the doping at the edges
assert abs(carriers_at(NA, ND, -w["xp"])["p"] - NA) < 1
assert abs(carriers_at(NA, ND, w["xn"])["n"] - ND) / ND < 1e-9
# Einstein: the hole drift and diffusion cancel when D/mu = kT/q
hc = hole_currents(NA, ND, -0.3 * w["xp"], VT)
assert abs(hc["net"]) < 1e-9 * abs(hc["drift"])
# 1/C^2 is a straight line in V_D that meets zero at phi_bi
c1, c2 = junction_cap(NA, ND, -1), junction_cap(NA, ND, -3)
slope = (1 / c1 ** 2 - 1 / c2 ** 2) / 2
assert abs(-1 - (1 / c1 ** 2) / slope - built_in(NA, ND)) < 1e-6

cases = []


def special(v):
    if isinstance(v, float) and math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    if isinstance(v, dict):
        return {k: special(x) for k, x in v.items()}
    return v


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": special(value), "tol": tol, "units": units, "tag": tag, "note": note})


xp0, xn0 = w["xp"], w["xn"]
case("builtIn", [1e18, 1e17], built_in(1e18, 1e17), "V", "typical",
     "N_A = 10¹⁸ and N_D = 10¹⁷ cm⁻³: φ_bi = (26 mV)·ln(10³⁵/10²⁰) = 0.898 V")
case("builtIn", [1e18, 1e18], built_in(1e18, 1e18), "V", "typical",
     "N_D raised tenfold to 10¹⁸ cm⁻³: φ_bi rises by one decade's 59.9 mV, to 0.958 V")
case("widths", [1e18, 1e17, 0], widths(1e18, 1e17, 0), "cm", "typical",
     "at equilibrium: x_p = 10.3 nm, x_n = 103 nm, W = 113 nm; ten times the doping, a tenth of the depth")
case("widths", [1e18, 1e17, -3], widths(1e18, 1e17, -3), "cm", "typical",
     "3 V of reverse bias: the step grows from 0.898 V to 3.898 V, 4.34 times, so every width grows √4.34 = 2.08 times, to W = 235 nm")
case("widths", [1e18, 1e17, 0.897], widths(1e18, 1e17, 0.897), "cm", "limit-zero",
     "V_D = 0.897 V, 1 mV short of φ_bi: the depletion region has shrunk to 3.8 nm; the approximation has long since stopped meaning anything")
case("widths", [1e19, 1e15, 0], widths(1e19, 1e15, 0), "cm", "limit-infinity",
     "a one-sided junction, N_A = 10¹⁹ and N_D = 10¹⁵ cm⁻³: W = 1.04 µm, all but 0.1 nm of it on the lightly doped n side")
case("peakField", [1e18, 1e17, 0], peak_field(1e18, 1e17, 0), "V/cm", "sign",
     "at equilibrium the field peaks at the junction at −1.59×10⁵ V/cm: negative, pointing from the n side to the p side")
case("peakField", [1e18, 1e17, -20], peak_field(1e18, 1e17, -20), "V/cm", "breaks",
     "20 V of reverse bias: the model gives −7.67×10⁵ V/cm, but silicon doped like this breaks down by avalanche near 4×10⁵ V/cm, and the model knows nothing of it")
case("fieldAt", [1e18, 1e17, 0, 5e-06], field_at(1e18, 1e17, 0, 5e-06), "V/cm", "typical",
     "50 nm into the n side, about halfway across it: the field has fallen linearly to −8.16×10⁴ V/cm")
case("potentialAt", [1e18, 1e17, 0, 0], potential_at(1e18, 1e17, 0, 0), "V", "typical",
     "at the junction itself: only 0.0816 V of the 0.898 V step has happened; the lightly doped n side holds the rest, 91 %, in proportion to its depth")
case("chargePerArea", [1e18, 1e17, 0], charge_per_area(1e18, 1e17, 0), "C/cm²", "typical",
     "at equilibrium each side holds |Q| = qN_A x_p = qN_D x_n = 165 nC/cm² of bare ions")
case("junctionCap", [1e18, 1e17, 0], junction_cap(1e18, 1e17, 0), "F/cm²", "typical",
     "at equilibrium: C_j0 = ε_s/W = 91.7 nF/cm², 9.17 pF for a 100 µm × 100 µm junction")
case("junctionCap", [1e18, 1e17, -3], junction_cap(1e18, 1e17, -3), "F/cm²", "typical",
     "3 V of reverse bias: the plates are 2.08 times further apart, so C_j falls to 44.0 nF/cm²")
case("carriersAt", [1e18, 1e17, 0], carriers_at(1e18, 1e17, 0), "cm⁻³", "typical",
     "at the junction, in equilibrium: p = 4.33×10¹⁶ and n = 2.31×10³ cm⁻³; their product is still n_i²")
case("carriersAt", [1e18, 1e17, 5.13e-06], carriers_at(1e18, 1e17, 5.13e-06), "cm⁻³", "typical",
     "halfway into the n side's depletion: n = 3.81×10¹³ and p = 2.63×10⁶ cm⁻³, both far below the 10¹⁷ cm⁻³ of ions; the region really is nearly empty of carriers")
case("carriersAt", [1e18, 1e17, -9.3e-07], carriers_at(1e18, 1e17, -9.3e-07), "cm⁻³", "breaks",
     "1 nm inside the p edge of the 'depleted' region: holes are still at 9.72×10¹⁷ cm⁻³, 97 % of N_A; the real edge is smeared over a few nm, not a sharp box")
case("mobility", ["p", 1e18], mobility("p", 1e18), "cm²/(V·s)", "typical",
     "holes in p-type silicon at 10¹⁸ cm⁻³: μ_p = 143 cm²/(V·s), the drift tool's fit")
case("holeCurrents", [1e18, 1e17, -3e-07, 0.026], hole_currents(1e18, 1e17, -3e-07, 0.026), "A/cm²", "limit-zero",
     "at equilibrium 3 nm into the p side's depletion, with D_p/μ_p = kT/q: hole diffusion of +5.35×10⁵ A/cm² toward n, drift of −5.35×10⁵ A/cm² back, net zero")
case("holeCurrents", [1e18, 1e17, -3e-07, 0.03], hole_currents(1e18, 1e17, -3e-07, 0.03), "A/cm²", "other",
     "the same point with D_p/μ_p set to 30 mV instead of 26 mV: a net hole current of 8.23×10⁴ A/cm² would flow with nothing connected, so D/μ must equal kT/q")

print(json.dumps(cases, ensure_ascii=False))
