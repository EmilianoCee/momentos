"""Reference script for plans/drift-and-mobility.md. Standard library only.

Silicon at 300 K, units of the course: cm, s, V, A. n_i = 1e10 cm^-3, q = 1.602e-19 C, kT/q = 0.02585 V.
Mobility: a Caughey-Thomas fit with Arora's 300 K parameters, in cm^2/(V s), against the total ionised doping N:
  electrons  mu_n = 88   + 1252 / (1 + (N / 1.26e17)^0.88)
  holes      mu_p = 54.3 + 407  / (1 + (N / 2.35e17)^0.88)
Velocity saturation: v = mu E / (1 + (mu E / v_sat)^beta)^(1/beta), electrons v_sat = 1e7 cm/s, beta = 2;
holes v_sat = 8e6 cm/s, beta = 1.
Drude picture: tau_c = mu m*/q with conductivity masses 0.26 m0 (electrons) and 0.39 m0 (holes).
Prints the plan's check cases as one JSON list.
"""
import json
import math

Q = 1.602e-19
M0 = 9.109e-31
KT = 0.02585          # kT/q in V
NI = 1e10
MSTAR = {"n": 0.26 * M0, "p": 0.39 * M0}
FIT = {"n": (88.0, 1252.0, 1.26e17, 0.88), "p": (54.3, 407.0, 2.35e17, 0.88)}
VSAT = {"n": (1e7, 2.0), "p": (8e6, 1.0)}


def mobility(carrier, N):
    mn, d, nref, a = FIT[carrier]
    return mn + d / (1 + (N / nref) ** a)


def carriers(kind, N):
    """electron and hole densities, cm^-3, for N donors (kind "n") or acceptors (kind "p"), fully ionised"""
    maj = N / 2 + math.sqrt((N / 2) ** 2 + NI * NI)
    mino = NI * NI / maj
    return {"n": maj, "p": mino} if kind == "n" else {"n": mino, "p": maj}


def conductivity(kind, N):
    c = carriers(kind, N)
    return Q * (c["n"] * mobility("n", N) + c["p"] * mobility("p", N))


def resistivity(kind, N):
    return 1 / conductivity(kind, N)


def current_density(kind, N, E):
    return conductivity(kind, N) * E


def drift_velocity(carrier, N, E):
    """the plain law: mu E, in cm/s (magnitude)"""
    return mobility(carrier, N) * E


def velocity(carrier, N, E):
    """with velocity saturation, cm/s (magnitude)"""
    vs, b = VSAT[carrier]
    u = mobility(carrier, N) * E
    return u / (1 + (u / vs) ** b) ** (1 / b)


def collision_time(carrier, N):
    """mean time between collisions, s: tau = mu m* / q, with mu in m^2/(V s)"""
    return mobility(carrier, N) * 1e-4 * MSTAR[carrier] / Q


def thermal_velocity(carrier):
    """sqrt(3kT/m*), cm/s"""
    return math.sqrt(3 * KT * Q / MSTAR[carrier]) * 100


def bar_resistance(kind, N, L, W, t):
    """a bar L long, W wide, t thick, all in cm: R = rho L/(W t), ohms"""
    return resistivity(kind, N) * L / (W * t)


def sheet_resistance(kind, N, t):
    return resistivity(kind, N) / t


def step_carrier(c, a, dt, tau, vth, r1, r2, width, height):
    """one time step of the Drude picture, in nm and ps. c = {x, y, vx, vy, laps}. The field accelerates along x by a
    (nm/ps^2); a collision happens when r1 < 1 - exp(-dt/tau), and sends the carrier off at speed vth in the direction
    2 pi r2. x wraps round the box (laps counts the wraps, so the true distance is x + laps*width); y bounces."""
    vx, vy = c["vx"] + a * dt, c["vy"]
    if r1 < 1 - math.exp(-dt / tau):
        vx, vy = vth * math.cos(2 * math.pi * r2), vth * math.sin(2 * math.pi * r2)
    x, y, laps = c["x"] + vx * dt, c["y"] + vy * dt, c["laps"]
    while x >= width:
        x -= width
        laps += 1
    while x < 0:
        x += width
        laps -= 1
    if y < 0:
        y, vy = -y, -vy
    if y > height:
        y, vy = 2 * height - y, -vy
    return {"x": x, "y": y, "vx": vx, "vy": vy, "laps": laps}


def acceleration(carrier, E):
    """q E / m* along the field, in nm/ps^2, for E in V/cm; negative for electrons (they go against E)"""
    a = Q * E * 100 / MSTAR[carrier] * 1e-15
    return -a if carrier == "n" else a


# checks: the Drude mean velocity a*tau equals mu E; sigma*E equals q n mu E for a strongly n-type bar
for N in (1e15, 1e17):
    tau_ps = collision_time("n", N) * 1e12
    assert abs(abs(acceleration("n", 1000)) * tau_ps * 1e5 - drift_velocity("n", N, 1000)) < 1e-6 * drift_velocity("n", N, 1000)
assert abs(velocity("n", 1e14, 1) - drift_velocity("n", 1e14, 1)) < 1e-7 * drift_velocity("n", 1e14, 1)

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("mobility", ["n", 1e16], mobility("n", 1e16), "cm²/(V·s)", "typical",
     "electrons in silicon with 10¹⁶ cm⁻³ dopants: about 1220 cm²/(V·s)")
case("mobility", ["p", 1e16], mobility("p", 1e16), "cm²/(V·s)", "typical",
     "holes at the same doping: about 437 cm²/(V·s); electrons outrun them about 2.8 times")
case("mobility", ["n", 1e19], mobility("n", 1e19), "cm²/(V·s)", "typical",
     "electrons with 10¹⁹ cm⁻³ dopants: about 114 cm²/(V·s), a twelfth of the clean-crystal value: the ions scatter them")
case("mobility", ["n", 1e12], mobility("n", 1e12), "cm²/(V·s)", "limit-zero",
     "almost no dopants: the lattice alone scatters, μ_n → 88 + 1252 = 1340 cm²/(V·s)")
case("mobility", ["n", 1e22], mobility("n", 1e22), "cm²/(V·s)", "limit-infinity",
     "enormous doping: the fit's floor, close to 88 cm²/(V·s)")
case("carriers", ["n", 1e16], carriers("n", 1e16), "cm⁻³", "typical",
     "10¹⁶ cm⁻³ donors: n = 10¹⁶ cm⁻³ and p = n_i²/n = 10⁴ cm⁻³, twelve decades fewer")
case("carriers", ["p", 1e6], carriers("p", 1e6), "cm⁻³", "limit-zero",
     "10⁶ cm⁻³ acceptors, far below n_i = 10¹⁰ cm⁻³: n and p both stay near n_i; the doping barely registers")
case("resistivity", ["n", 1e16], resistivity("n", 1e16), "Ω·cm", "typical",
     "n-type, 10¹⁶ cm⁻³: ρ = 1/(q n μ_n) = 0.51 Ω·cm")
case("resistivity", ["n", 1e17], resistivity("n", 1e17), "Ω·cm", "typical",
     "ten times the doping: ρ = 0.0857 Ω·cm, only 6.4 times lower, because μ_n fell from 1218 to 777 cm²/(V·s)")
case("resistivity", ["p", 1e16], resistivity("p", 1e16), "Ω·cm", "typical",
     "p-type, 10¹⁶ cm⁻³: ρ = 1.43 Ω·cm, nearly three times the n-type bar's, because holes are slower")
case("currentDensity", ["n", 1e16, 1000], current_density("n", 1e16, 1000), "A/cm²", "typical",
     "n-type 10¹⁶ cm⁻³ in a field of 1 kV/cm: J = σE = 1.95 kA/cm²")
case("driftVelocity", ["n", 1e16, 1000], drift_velocity("n", 1e16, 1000), "cm/s", "typical",
     "electrons at 10¹⁶ cm⁻³ in 1 kV/cm: v = μE = 1.22×10⁶ cm/s, about a twentieth of their thermal speed")
case("thermalVelocity", ["n"], thermal_velocity("n"), "cm/s", "typical",
     "electrons at 300 K with m* = 0.26 m₀: √(3kT/m*) = 2.29×10⁷ cm/s, in random directions")
case("collisionTime", ["n", 1e16], collision_time("n", 1e16), "s", "typical",
     "electrons at 10¹⁶ cm⁻³: τ_c = μm*/q = 0.18 ps between collisions")
case("velocity", ["n", 1e16, 1000], velocity("n", 1e16, 1000), "cm/s", "typical",
     "at 1 kV/cm the saturating law gives 1.21×10⁶ cm/s, within 1% of μE")
case("velocity", ["n", 1e16, 100000], velocity("n", 1e16, 1e5), "cm/s", "breaks",
     "at 100 kV/cm μE would be 1.22×10⁸ cm/s; the electrons actually reach 9.97×10⁶ cm/s. v = μE no longer holds")
case("velocity", ["n", 1e16, 1e9], velocity("n", 1e16, 1e9), "cm/s", "limit-infinity",
     "an absurd field: the speed stops at v_sat = 10⁷ cm/s")
case("barResistance", ["n", 1e16, 0.01, 0.001, 0.0001], bar_resistance("n", 1e16, 0.01, 0.001, 0.0001), "Ω", "typical",
     "a bar 100 µm long, 10 µm wide, 1 µm thick, n-type 10¹⁶ cm⁻³: R = ρL/(Wt) = 51.1 kΩ")
case("sheetResistance", ["n", 1e16, 0.0001], sheet_resistance("n", 1e16, 1e-4), "Ω/□", "typical",
     "the same layer 1 µm thick: R_□ = ρ/t = 5.11 kΩ per square; the bar is 10 squares long")
case("acceleration", ["n", 1000], acceleration("n", 1000), "nm/ps²", "sign",
     "electrons in +1 kV/cm are pushed the other way: −67.6 nm/ps²")
case("stepCarrier", [{"x": 100, "y": 50, "vx": 0, "vy": 0, "laps": 0}, -67.6, 0.01, 0.18, 229, 0.9, 0.25, 600, 240],
     step_carrier({"x": 100, "y": 50, "vx": 0, "vy": 0, "laps": 0}, -67.6, 0.01, 0.18, 229, 0.9, 0.25, 600, 240), "nm, nm/ps", "sign",
     "an electron at rest, no collision this step (0.9 > 1 − e^(−0.01/0.18)): after 0.01 ps it moves −0.00676 nm, against the field")
case("stepCarrier", [{"x": 599, "y": 50, "vx": 200, "vy": 0, "laps": 3}, 0, 0.01, 0.18, 229, 0.01, 0.25, 600, 240],
     step_carrier({"x": 599, "y": 50, "vx": 200, "vy": 0, "laps": 3}, 0, 0.01, 0.18, 229, 0.01, 0.25, 600, 240), "nm, nm/ps", "other",
     "a collision (0.01 < 0.054) turns the carrier to point along +y at 229 nm/ps; it stays inside the box")

print(json.dumps(cases, ensure_ascii=False))
