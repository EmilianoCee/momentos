"""Reference script for plans/carriers-and-doping.md. Standard library only.

Silicon, in the course's units: cm, V, eV, K. The course's constants at 300 K: kT/q = 26 mV, n_i = 1e10 cm^-3,
E_g = 1.12 eV. Away from 300 K:
  kT/q   = 0.026 V * T / 300 K
  n_i(T) = 1e10 cm^-3 * (T/300)^1.5 * exp(E_g/(2 * 0.026 eV) - E_g/(2 kT))
which is sqrt(N_c N_v) exp(-E_g/2kT) with N_c N_v proportional to T^3, scaled so that n_i(300 K) = 1e10 cm^-3.
E_g is held at 1.12 eV at every temperature, and E_i is taken at mid-gap.
Every dopant is ionised. Charge neutrality with mass action, net doping N = N_D - N_A:
  n - p = N,  n p = n_i^2   =>   n = N/2 + sqrt((N/2)^2 + n_i^2)  (for N >= 0; the hole formula mirrors it)
The Fermi level from intrinsic, Boltzmann statistics: E_F - E_i = kT ln(n/n_i) = -kT ln(p/n_i).
Prints the plan's check cases as one JSON list.
"""
import json
import math

EG = 1.12            # eV
VT300 = 0.026        # kT/q at 300 K, V
NI300 = 1e10         # cm^-3


def thermal_voltage(T):
    return VT300 * T / 300.0


def intrinsic(T):
    return NI300 * (T / 300.0) ** 1.5 * math.exp(EG / (2 * VT300) - EG / (2 * thermal_voltage(T)))


def carriers(ND, NA, T):
    ni = intrinsic(T)
    net = ND - NA
    half = abs(net) / 2
    maj = half + math.sqrt(half * half + ni * ni)
    mino = ni * ni / maj
    n, p = (maj, mino) if net >= 0 else (mino, maj)
    if n >= 100 * p:
        kind = "n-type"
    elif p >= 100 * n:
        kind = "p-type"
    else:
        kind = "nearly intrinsic"
    return {"n": n, "p": p, "kind": kind}


def fermi_level(ND, NA, T):
    """E_F - E_i in eV: positive for n-type, negative for p-type"""
    c = carriers(ND, NA, T)
    return thermal_voltage(T) * math.log(c["n"] / intrinsic(T))


def edge_margin(ND, NA, T):
    """how far E_F sits inside the gap from the nearer band edge, eV; Boltzmann statistics need at least 3kT"""
    return EG / 2 - abs(fermi_level(ND, NA, T))


def per_decade(T):
    """the shift of E_F for a tenfold change of the majority density, eV"""
    return thermal_voltage(T) * math.log(10)


# checks against limits worked out by hand
assert abs(intrinsic(300) - 1e10) < 1e-3
c = carriers(1e16, 0, 300)
assert abs(c["n"] * c["p"] - 1e20) / 1e20 < 1e-12
assert abs(fermi_level(1e17, 0, 300) - fermi_level(1e16, 0, 300) - per_decade(300)) < 1e-6
assert abs(fermi_level(0, 1e16, 300) + fermi_level(1e16, 0, 300)) < 1e-12
assert carriers(0, 0, 300)["kind"] == "nearly intrinsic"
# n_i doubles in roughly 9 K near room temperature
assert 8 < math.log(2) / (1.5 / 300 + EG / (2 * VT300 * 300)) < 10

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("thermalVoltage", [300], thermal_voltage(300), "V", "typical",
     "T = 300 K: kT/q = 26 mV, the course's value")
case("intrinsic", [300], intrinsic(300), "cm⁻³", "typical",
     "T = 300 K: n_i = 1.00×10¹⁰ cm⁻³, the course's value")
case("intrinsic", [309], intrinsic(309), "cm⁻³", "typical",
     "T = 309 K, 9 K warmer: n_i = 1.96×10¹⁰ cm⁻³, about double; the gap is crossed by a Boltzmann factor e^(−E_g/2kT)")
case("intrinsic", [200], intrinsic(200), "cm⁻³", "limit-zero",
     "T = 200 K: n_i = 1.14×10⁵ cm⁻³, five decades down; toward 0 K it goes to zero and pure silicon stops conducting")
case("carriers", [1e16, 0, 300], carriers(1e16, 0, 300), "cm⁻³", "typical",
     "N_D = 10¹⁶ cm⁻³ at 300 K: n = 1.00×10¹⁶ cm⁻³, p = n_i²/n = 1.00×10⁴ cm⁻³; six decades up for electrons, six down for holes")
case("carriers", [4e16, 1e17, 300], carriers(4e16, 1e17, 300), "cm⁻³", "typical",
     "N_D = 4×10¹⁶ and N_A = 10¹⁷ cm⁻³: p-type, p = 6.00×10¹⁶ cm⁻³ (the difference), n = 1.67×10³ cm⁻³")
case("carriers", [1e16, 1e16, 300], carriers(1e16, 1e16, 300), "cm⁻³", "typical",
     "N_D = N_A = 10¹⁶ cm⁻³: the two cancel and n = p = n_i, though the crystal is full of ions")
case("carriers", [0, 0, 300], carriers(0, 0, 300), "cm⁻³", "limit-zero",
     "no dopants at 300 K: n = p = n_i = 10¹⁰ cm⁻³")
case("carriers", [1e16, 0, 700], carriers(1e16, 0, 700), "cm⁻³", "limit-infinity",
     "N_D = 10¹⁶ cm⁻³ at 700 K: n_i = 7.9×10¹⁵ cm⁻³ has caught up with the doping; n = 1.43×10¹⁶, p = 4.34×10¹⁵ cm⁻³, nearly intrinsic")
case("fermiLevel", [1e16, 0, 300], fermi_level(1e16, 0, 300), "eV", "typical",
     "N_D = 10¹⁶ cm⁻³ at 300 K: E_F sits 0.359 eV above E_i, 6 decades × 59.9 meV")
case("fermiLevel", [0, 1e16, 300], fermi_level(0, 1e16, 300), "eV", "sign",
     "N_A = 10¹⁶ cm⁻³ at 300 K: E_F sits 0.359 eV below E_i; p-type puts it below the middle")
case("fermiLevel", [1e17, 0, 300], fermi_level(1e17, 0, 300), "eV", "typical",
     "N_D = 10¹⁷ cm⁻³: ten times the doping raises E_F by one step of 59.9 meV, to 0.419 eV")
case("perDecade", [300], per_decade(300), "eV", "typical",
     "T = 300 K: (kT/q)·ln 10 = 59.9 mV per decade of density")
case("edgeMargin", [1e16, 0, 300], edge_margin(1e16, 0, 300), "eV", "typical",
     "N_D = 10¹⁶ cm⁻³: E_F is 0.201 eV below the conduction band edge, far more than 3kT = 78 meV, so Boltzmann statistics hold")
case("edgeMargin", [1e19, 0, 300], edge_margin(1e19, 0, 300), "eV", "breaks",
     "N_D = 10¹⁹ cm⁻³: E_F is only 21 meV below the edge, under 3kT; the silicon is nearly degenerate and n = n_i e^((E_F−E_i)/kT) no longer holds")

print(json.dumps(cases, ensure_ascii=False))
