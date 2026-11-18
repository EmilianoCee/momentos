"""Reference script for plans/mos-capacitor.md. Standard library only.

An NMOS capacitor: a gate of n+ or p+ polysilicon on an oxide t_ox thick (cm) over a p-type body with N_A acceptors
(cm^-3). Units: cm, F, C, V. kT/q = 0.026 V and n_i = 1e10 cm^-3, as in the course's examples.
  phi_p = -(kT/q) ln(N_A/n_i)          (negative for p-type)
  phi_gate = +0.55 V (n+ poly) or -0.55 V (p+ poly)
  V_FB = phi_p - phi_gate
  C_ox = eps_ox / t_ox,  |Q_B,max| = sqrt(2 q eps_si N_A 2|phi_p|)
  V_T = V_FB + 2|phi_p| + |Q_B,max|/C_ox
Body charges per area: holes positive, acceptor ions and electrons negative. The surface potential psi_s is measured
from the body's neutral bulk. Prints the plan's check cases as one JSON list.
"""
import json
import math

Q = 1.602e-19
KT = 0.026
NI = 1e10
EPS0 = 8.854e-14
EOX = 3.9 * EPS0
ESI = 11.7 * EPS0
PHI_GATE = {"n+": 0.55, "p+": -0.55}


def phi_p(NA):
    return -KT * math.log(NA / NI)


def flatband(gate, NA):
    return phi_p(NA) - PHI_GATE[gate]


def cox(tox):
    return EOX / tox


def qb_max(NA):
    return math.sqrt(2 * Q * ESI * NA * 2 * abs(phi_p(NA)))


def threshold(gate, NA, tox):
    return flatband(gate, NA) + 2 * abs(phi_p(NA)) + qb_max(NA) / cox(tox)


def surface(gate, NA, tox, VGB):
    """the state of the body surface at a gate-to-body voltage VGB"""
    vfb, vt, c = flatband(gate, NA), threshold(gate, NA, tox), cox(tox)
    two_phi = 2 * abs(phi_p(NA))
    if VGB <= vfb:
        return {"region": "accumulation", "psiS": 0.0, "xd": 0.0, "Qacc": c * (vfb - VGB), "Qdep": 0.0, "Qinv": 0.0,
                "Vox": VGB - vfb}
    if VGB <= vt:
        gamma = math.sqrt(2 * Q * ESI * NA) / c
        root = (-gamma + math.sqrt(gamma * gamma + 4 * (VGB - vfb))) / 2      # sqrt(psi_s)
        psi = root * root
        xd = math.sqrt(2 * ESI * psi / (Q * NA))
        return {"region": "depletion", "psiS": psi, "xd": xd, "Qacc": 0.0, "Qdep": -Q * NA * xd, "Qinv": 0.0,
                "Vox": gamma * root}
    xd = math.sqrt(2 * ESI * two_phi / (Q * NA))
    return {"region": "inversion", "psiS": two_phi, "xd": xd, "Qacc": 0.0, "Qdep": -qb_max(NA), "Qinv": -c * (VGB - vt),
            "Vox": VGB - vfb - two_phi}


def capacitance(gate, NA, tox, VGB, high):
    """small-signal capacitance per area, F/cm^2. high = True: measured too fast for the electrons to follow"""
    s, c = surface(gate, NA, tox, VGB), cox(tox)
    if s["region"] == "accumulation" or s["xd"] == 0:
        return c
    if s["region"] == "inversion" and not high:
        return c
    cdep = ESI / s["xd"]
    return c * cdep / (c + cdep)


def potential_at(gate, NA, tox, VGB, x):
    """the potential in the body at a depth x (cm) below the surface, relative to the neutral bulk:
    psi_s (1 - x/x_d)^2 inside the depletion region, 0 beyond it"""
    s = surface(gate, NA, tox, VGB)
    if s["xd"] == 0 or x >= s["xd"]:
        return 0.0
    return s["psiS"] * (1 - x / s["xd"]) ** 2


# checks: in depletion, V_GB - V_FB = V_ox + psi_s; at V_T the depletion and inversion formulas meet
for v in (-0.5, 0.0, 0.4):
    s = surface("n+", 5e16, 20e-7, v)
    assert abs(s["Vox"] + s["psiS"] - (v - flatband("n+", 5e16))) < 1e-12
vt = threshold("n+", 5e16, 20e-7)
a, b = surface("n+", 5e16, 20e-7, vt - 1e-9), surface("n+", 5e16, 20e-7, vt + 1e-9)
assert abs(a["psiS"] - b["psiS"]) < 1e-6 and abs(a["Qdep"] - b["Qdep"]) < 1e-12
# Gauss: the oxide field times eps_ox is the body charge
s = surface("n+", 5e16, 20e-7, 1.5)
assert abs(EOX * s["Vox"] / 20e-7 + s["Qdep"] + s["Qinv"]) < 1e-15

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("phiP", [5e16], phi_p(5e16), "V", "typical",
     "p-type body, N_A = 5×10¹⁶ cm⁻³: φ_p = −(26 mV)·ln(5×10⁶) = −0.401 V")
case("flatband", ["n+", 5e16], flatband("n+", 5e16), "V", "sign",
     "n+ poly gate (+0.55 V) on that body: V_FB = φ_p − φ_gate = −0.951 V, negative")
case("flatband", ["p+", 5e16], flatband("p+", 5e16), "V", "sign",
     "p+ poly gate (−0.55 V) on the same body: V_FB = +0.149 V")
case("cox", [20e-7], cox(20e-7), "F/cm²", "typical",
     "20 nm of oxide: C_ox = ε_ox/t_ox = 173 nF/cm²", tol=1e-15)
case("qbMax", [5e16], qb_max(5e16), "C/cm²", "typical",
     "N_A = 5×10¹⁶ cm⁻³ at the onset of inversion: |Q_B,max| = √(2qε_si N_A·2|φ_p|) = 115 nC/cm²", tol=1e-15)
case("threshold", ["n+", 5e16, 20e-7], threshold("n+", 5e16, 20e-7), "V", "typical",
     "n+ gate, N_A = 5×10¹⁶ cm⁻³, t_ox = 20 nm: V_T = −0.951 + 0.802 + 0.668 = 0.519 V")
case("threshold", ["n+", 5e17, 20e-7], threshold("n+", 5e17, 20e-7), "V", "typical",
     "ten times the doping: V_T rises to 2.18 V, mostly through the depletion charge the oxide must hold")
case("threshold", ["n+", 5e16, 5e-7], threshold("n+", 5e16, 5e-7), "V", "typical",
     "the same body with 5 nm of oxide: V_T falls to 0.018 V; a thinner oxide holds the same charge with less voltage")
case("surface", ["n+", 5e16, 20e-7, -2], surface("n+", 5e16, 20e-7, -2), "V, cm, C/cm²", "typical",
     "V_GB = −2 V, below V_FB: accumulation, 181 nC/cm² of holes at the surface, all of V_GB − V_FB across the oxide", tol=1e-12)
case("surface", ["n+", 5e16, 20e-7, 0], surface("n+", 5e16, 20e-7, 0), "V, cm, C/cm²", "typical",
     "V_GB = 0 V: depletion, the surface 0.450 V above the bulk, 108 nm of bare acceptors, 0.501 V across the oxide", tol=1e-12)
case("surface", ["n+", 5e16, 20e-7, 1.5], surface("n+", 5e16, 20e-7, 1.5), "V, cm, C/cm²", "typical",
     "V_GB = 1.5 V: inversion, ψ_s pinned at 2|φ_p| = 0.802 V, the depletion stopped at 144 nm, and 169 nC/cm² of electrons", tol=1e-12)
case("surface", ["n+", 5e16, 20e-7, -0.951], surface("n+", 5e16, 20e-7, -0.951), "V, cm, C/cm²", "limit-zero",
     "V_GB just above V_FB = −0.9512 V: almost no charge anywhere; the bands are nearly flat", tol=1e-9)
case("surface", ["n+", 5e16, 20e-7, 4], surface("n+", 5e16, 20e-7, 4), "V, cm, C/cm²", "limit-infinity",
     "V_GB = 4 V: the depletion has not grown past 144 nm; every extra volt adds C_ox·1 V = 173 nC/cm² of electrons", tol=1e-12)
case("surface", ["n+", 5e16, 20e-7, 0.519], surface("n+", 5e16, 20e-7, 0.519), "V, cm, C/cm²", "breaks",
     "at threshold the model says no electrons at all, though the surface is as n-type as the body is p-type (5×10¹⁶ cm⁻³ at the surface): the charge-sheet picture ignores the electrons below threshold", tol=1e-9)
case("capacitance", ["n+", 5e16, 20e-7, 0, False], capacitance("n+", 5e16, 20e-7, 0, False), "F/cm²", "typical",
     "in depletion at 0 V: C_ox in series with ε_si/x_d gives 61.7 nF/cm², 0.357 of C_ox", tol=1e-15)
case("capacitance", ["n+", 5e16, 20e-7, 2, True], capacitance("n+", 5e16, 20e-7, 2, True), "F/cm²", "typical",
     "in inversion at high frequency the electrons cannot follow: C stays at its minimum, 50.8 nF/cm²", tol=1e-15)
case("capacitance", ["n+", 5e16, 20e-7, 2, False], capacitance("n+", 5e16, 20e-7, 2, False), "F/cm²", "typical",
     "the same, measured slowly: the electron sheet answers at the surface and C is back to C_ox", tol=1e-15)
case("potentialAt", ["n+", 5e16, 20e-7, 0, 5.4e-6], potential_at("n+", 5e16, 20e-7, 0, 5.4e-6), "V", "typical",
     "at 0 V, 54 nm down, halfway through the 108 nm depletion region: the potential is a quarter of ψ_s, 0.112 V")

print(json.dumps(cases, ensure_ascii=False))
