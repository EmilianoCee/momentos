"""Reference script for plans/diode-current.md. Standard library only.

A silicon pn diode: p side doped N_A, n side doped N_D, each neutral region W long from its depletion edge to an ohmic
contact, minority lifetime tau for both carriers, area A. Course constants: kT/q = 0.026 V, n_i = 1e10 cm^-3,
q = 1.602e-19 C. V_D is the p side minus the n side. Units: cm, s, V, A, C, F.

Diffusion constants from the Einstein relation and the drift tool's mobility fit, each at the doping the minority
carrier moves through: D_n = (kT/q) mu_n(N_A), D_p = (kT/q) mu_p(N_D). Diffusion length L = sqrt(D tau).

Forward bias lowers the barrier, so the minority density at each depletion edge rises by e^(V_D/(kT/q)):
  excess at the edge  d0 = (n_i^2/N) (e^(V_D/(kT/q)) - 1)       N the doping of that side
In the neutral region there is no field; the excess diffuses and recombines: D d''(x) = d/tau, with d(0) = d0 at the
edge and d(W) = 0 at the contact:
  d(x) = d0 sinh((W - x)/L) / sinh(W/L) = d0 (e^(-x/L) - e^(-(2W - x)/L)) / (1 - e^(-2W/L))
The current is diffusion at the edge, q D |d'(0)| = q D d0 coth(W/L)/L. Summing both sides:
  I = I_S (e^(V_D/(kT/q)) - 1),   I_S = q A n_i^2 [ D_n coth(W/L_n)/(N_A L_n) + D_p coth(W/L_p)/(N_D L_p) ]
Short (W << L): coth(W/L)/L -> 1/W, a straight-line profile. Long (W >> L): coth -> 1, the profile e^(-x/L).
Stored minority charge: q A integral of d = q A d0 L tanh(W/(2L)) per side; C_d = dQ/dV_D.
Prints the plan's check cases as one JSON list.
"""
import json
import math

Q = 1.602e-19
VT = 0.026
NI = 1e10
FIT = {"n": (88.0, 1252.0, 1.26e17, 0.88), "p": (54.3, 407.0, 2.35e17, 0.88)}


def mobility(carrier, N):
    mn, d, nref, a = FIT[carrier]
    return mn + d / (1 + (N / nref) ** a)


def diffusivity(carrier, N):
    return VT * mobility(carrier, N)


def diffusion_length(D, tau):
    return math.sqrt(D * tau)


def excess_at(N, VD, L, W, x):
    if x < 0 or x >= W:
        return 0.0
    d0 = NI * NI / N * math.expm1(VD / VT)
    return d0 * (math.exp(-x / L) - math.exp(-(2 * W - x) / L)) / (1 - math.exp(-2 * W / L))


def coth(z):
    return 1 / math.tanh(z)


def saturation_current(NA, ND, W, tau, A):
    Dn, Dp = diffusivity("n", NA), diffusivity("p", ND)
    Ln, Lp = diffusion_length(Dn, tau), diffusion_length(Dp, tau)
    In = Q * A * NI * NI * Dn * coth(W / Ln) / (NA * Ln)
    Ip = Q * A * NI * NI * Dp * coth(W / Lp) / (ND * Lp)
    return {"IS": In + Ip, "In": In, "Ip": Ip}


def diode_current(IS, VD):
    return IS * math.expm1(VD / VT)


def conductance(IS, VD):
    gd = IS * math.exp(VD / VT) / VT
    return {"gd": gd, "rd": 1 / gd}


def stored_charge(NA, ND, W, tau, A, VD):
    Dn, Dp = diffusivity("n", NA), diffusivity("p", ND)
    Ln, Lp = diffusion_length(Dn, tau), diffusion_length(Dp, tau)
    f = math.expm1(VD / VT)
    return Q * A * NI * NI * f * (Ln * math.tanh(W / (2 * Ln)) / NA + Lp * math.tanh(W / (2 * Lp)) / ND)


def diffusion_cap(NA, ND, W, tau, A, VD):
    Dn, Dp = diffusivity("n", NA), diffusivity("p", ND)
    Ln, Lp = diffusion_length(Dn, tau), diffusion_length(Dp, tau)
    return Q * A * NI * NI * math.exp(VD / VT) / VT * (Ln * math.tanh(W / (2 * Ln)) / NA + Lp * math.tanh(W / (2 * Lp)) / ND)


def transit_time(NA, ND, W, tau, A, VD):
    return stored_charge(NA, ND, W, tau, A, VD) / diode_current(saturation_current(NA, ND, W, tau, A)["IS"], VD)


def injection_ratio(NA, ND, VD):
    """the larger of the two edge excesses as a fraction of the doping it must stay well below"""
    f = math.expm1(VD / VT)
    return max(NI * NI / NA * f / NA, NI * NI / ND * f / ND)


NA, ND, A = 1e18, 1e17, 1e-4
# checks against limits worked out by hand
Dp = diffusivity("p", ND)
Lp = diffusion_length(Dp, 1e-6)
W = 1e-4
# the current from the profile's slope matches the closed form
h = 1e-9
slope = (excess_at(ND, 0.6, Lp, W, h) - excess_at(ND, 0.6, Lp, W, 0)) / h
assert abs(Q * A * Dp * -slope / (saturation_current(NA, ND, W, 1e-6, A)["Ip"] * math.expm1(0.6 / VT)) - 1) < 1e-4
# the profile solves D d'' = d/tau
x, hh = 0.4 * W, 1e-7
d2 = (excess_at(ND, 0.6, Lp, W, x + hh) - 2 * excess_at(ND, 0.6, Lp, W, x) + excess_at(ND, 0.6, Lp, W, x - hh)) / hh ** 2
assert abs(Dp * d2 / (excess_at(ND, 0.6, Lp, W, x) / 1e-6) - 1) < 1e-3
# short diode: the straight line, and the textbook I_S with W in place of L
short = saturation_current(NA, ND, 1e-5, 1e-3, A)["IS"]
textbook = Q * A * NI * NI * (diffusivity("n", NA) / (NA * 1e-5) + Dp / (ND * 1e-5))
assert abs(short / textbook - 1) < 1e-3
# long diode: the current no longer depends on W
assert abs(saturation_current(NA, ND, 1e-2, 1e-9, A)["IS"] / saturation_current(NA, ND, 5e-3, 1e-9, A)["IS"] - 1) < 1e-12
# ten times the current every 59.9 mV
assert abs(diode_current(1e-15, 0.7 + VT * math.log(10)) / diode_current(1e-15, 0.7) - 10) < 1e-6
# short diode transit time is W^2/(2D) when one side dominates
t = transit_time(1e20, ND, 1e-5, 1e-3, A, 0.6)
assert abs(t / (1e-10 / (2 * Dp)) - 1) < 1e-2
# C_d is the slope of the stored charge
dv = 1e-7
assert abs((stored_charge(NA, ND, W, 1e-6, A, 0.6 + dv) - stored_charge(NA, ND, W, 1e-6, A, 0.6 - dv)) / (2 * dv)
           / diffusion_cap(NA, ND, W, 1e-6, A, 0.6) - 1) < 1e-6

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


IS0 = saturation_current(NA, ND, 1e-4, 1e-6, A)["IS"]
case("diffusivity", ["p", 1e17], diffusivity("p", 1e17), "cm²/s", "typical",
     "holes crossing n-type silicon at 10¹⁷ cm⁻³: D_p = (kT/q)·μ_p = 26 mV × 331 = 8.60 cm²/s")
case("diffusivity", ["n", 1e18], diffusivity("n", 1e18), "cm²/s", "typical",
     "electrons crossing p-type silicon at 10¹⁸ cm⁻³: D_n = 26 mV × 262 = 6.81 cm²/s")
case("diffusionLength", [8.6, 1e-6], diffusion_length(8.6, 1e-6), "cm", "typical",
     "D = 8.6 cm²/s and τ = 1 µs: L = √(Dτ) = 29.3 µm, how far a hole gets before it recombines")
case("excessAt", [1e17, 0.6, 0.00293, 0.0001, 5e-05], excess_at(1e17, 0.6, 0.00293, 1e-4, 5e-5), "cm⁻³", "typical",
     "n side at 10¹⁷ cm⁻³, V_D = 0.6 V, L = 29.3 µm, W = 1 µm, halfway to the contact: 5.26×10¹² cm⁻³, about half the edge's 1.05×10¹³; a short region gives a straight line")
case("excessAt", [1e17, 0.6, 9.3e-05, 0.01, 9.3e-05], excess_at(1e17, 0.6, 9.3e-05, 1e-2, 9.3e-05), "cm⁻³", "typical",
     "the same edge with L = 0.93 µm and W = 100 µm, one diffusion length in: 3.87×10¹² cm⁻³, the edge value over e")
case("excessAt", [1e17, -0.3, 0.00293, 0.0001, 0], excess_at(1e17, -0.3, 0.00293, 1e-4, 0), "cm⁻³", "sign",
     "reverse bias, V_D = −0.3 V, at the edge: −1.00×10³ cm⁻³, a deficit; the edge is emptied of its few minority holes, p_n0 = n_i²/N_D")
case("saturationCurrent", [1e18, 1e17, 0.0001, 1e-6, 0.0001], saturation_current(1e18, 1e17, 1e-4, 1e-6, A), "A", "typical",
     "N_A = 10¹⁸, N_D = 10¹⁷ cm⁻³, W = 1 µm, τ = 1 µs, A = 100 µm × 100 µm: I_S = 1.49×10⁻¹⁵ A, 93 % of it holes injected into the lightly doped n side")
case("saturationCurrent", [1e18, 1e17, 0.01, 1e-9, 0.0001], saturation_current(1e18, 1e17, 1e-2, 1e-9, A), "A", "limit-infinity",
     "W = 100 µm with τ = 1 ns (L_p = 0.93 µm): a long diode; I_S = 1.62×10⁻¹⁵ A, set by L instead of W, and making W longer still changes nothing")
case("diodeCurrent", [IS0, 0.65], diode_current(IS0, 0.65), "A", "typical",
     "I_S = 1.49 fA at V_D = 0.65 V: I_D = 107 µA")
case("diodeCurrent", [IS0, 0.7099], diode_current(IS0, 0.7099), "A", "typical",
     "59.9 mV more, V_D = 0.7099 V: I_D = 1.07 mA, ten times as much")
case("diodeCurrent", [IS0, 0], diode_current(IS0, 0), "A", "limit-zero",
     "V_D = 0: no current; diffusion over the barrier and drift down it cancel")
case("diodeCurrent", [IS0, -0.3], diode_current(IS0, -0.3), "A", "sign",
     "V_D = −0.3 V: I_D = −1.49×10⁻¹⁵ A, essentially −I_S; more reverse voltage changes nothing")
case("conductance", [IS0, 0.7099], conductance(IS0, 0.7099), "S, Ω", "typical",
     "at 1.07 mA: g_d = I_D/(kT/q) = 41.3 mS, so r_d = 24.2 Ω; the tangent to the exponential")
case("storedCharge", [1e18, 1e17, 0.0001, 1e-6, 0.0001, 0.7099], stored_charge(1e18, 1e17, 1e-4, 1e-6, A, 0.7099), "C", "typical",
     "at 1.07 mA with W = 1 µm: Q_s = 6.35×10⁻¹³ C of minority carriers waiting in the neutral regions")
case("diffusionCap", [1e18, 1e17, 0.0001, 1e-6, 0.0001, 0.7099], diffusion_cap(1e18, 1e17, 1e-4, 1e-6, A, 0.7099), "F", "typical",
     "at 1.07 mA: C_d = dQ_s/dV_D = 24.4 pF, and it grows in proportion to the current")
case("transitTime", [1e18, 1e17, 0.0001, 1e-6, 0.0001, 0.7099], transit_time(1e18, 1e17, 1e-4, 1e-6, A, 0.7099), "s", "typical",
     "Q_s/I_D = 592 ps: about W²/(2D_p) = 581 ps, the time a hole takes to diffuse across 1 µm")
case("injectionRatio", [1e18, 1e17, 0.65], injection_ratio(1e18, 1e17, 0.65), "", "typical",
     "V_D = 0.65 V: the hole excess at the edge is 7.2×10¹³ cm⁻³ against N_D = 10¹⁷ cm⁻³, 0.072 %; low-level injection holds")
case("injectionRatio", [1e18, 1e17, 0.85], injection_ratio(1e18, 1e17, 0.85), "", "breaks",
     "V_D = 0.85 V: the injected holes, 1.58×10¹⁷ cm⁻³, outnumber the donors; the edge law and I_S·e^(V_D/(kT/q)) both fail, and the real current grows more slowly")

print(json.dumps(cases, ensure_ascii=False))
