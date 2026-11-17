"""Reference script for plans/bode-plot.md. Standard library only.

H(s) = K * s^m * prod(1 + s/z) / prod(1 + s/p), with every pole at s = -p and every zero at s = -z
(p, z > 0, in rad/s). m is the number of zeros at the origin. Prints the plan's check cases as one JSON list.
"""
import cmath
import json
import math


def omega_rc(R, C):
    return 1.0 / (R * C)


def omega_rl(R, L):
    return R / L


def rad_to_hz(w):
    return w / (2 * math.pi)


def circuit_system(kind, R, X):
    wc = omega_rc(R, X) if kind.startswith("rc") else omega_rl(R, X)
    if kind.endswith("low"):
        return {"gain": 1.0, "origin": 0, "poles": [wc], "zeros": []}
    return {"gain": 1.0 / wc, "origin": 1, "poles": [wc], "zeros": []}


def H(sys, w):
    s = 1j * w
    h = sys["gain"] * s ** sys["origin"]
    for z in sys["zeros"]:
        h *= 1 + s / z
    for p in sys["poles"]:
        h /= 1 + s / p
    return h


def mag(sys, w):
    return abs(H(sys, w))


def mag_db(sys, w):
    return 20 * math.log10(mag(sys, w))


def phase_deg(sys, w):
    # summed term by term so that three poles reach -270 degrees instead of wrapping
    deg = 90.0 * sys["origin"]
    for z in sys["zeros"]:
        deg += math.degrees(math.atan(w / z))
    for p in sys["poles"]:
        deg -= math.degrees(math.atan(w / p))
    return deg


def asym_db(sys, w):
    db = 20 * math.log10(sys["gain"]) + 20 * sys["origin"] * math.log10(w)
    for z in sys["zeros"]:
        db += max(0.0, 20 * math.log10(w / z))
    for p in sys["poles"]:
        db -= max(0.0, 20 * math.log10(w / p))
    return db


def ramp(w, c):
    # 0 below c/10, 1 above 10c, a straight line in log w between
    return min(1.0, max(0.0, (math.log10(w / c) + 1) / 2))


def asym_phase_deg(sys, w):
    deg = 90.0 * sys["origin"]
    for z in sys["zeros"]:
        deg += 90 * ramp(w, z)
    for p in sys["poles"]:
        deg -= 90 * ramp(w, p)
    return deg


def delay_sec(sys, w):
    return -math.radians(phase_deg(sys, w)) / w


def output_at(sys, w, t):
    # the steady-state output, in volts, for the input sin(wt) of amplitude 1 V
    return mag(sys, w) * math.sin(w * t + math.radians(phase_deg(sys, w)))


# a check that the closed forms agree with the complex number itself where the angle does not wrap
for test_w in (1.0, 37.0, 1000.0, 5e4):
    one = {"gain": 1.0, "origin": 0, "poles": [1000.0], "zeros": []}
    assert abs(phase_deg(one, test_w) - math.degrees(cmath.phase(H(one, test_w)))) < 1e-9

LP = {"gain": 1, "origin": 0, "poles": [1000], "zeros": []}
HP = {"gain": 0.001, "origin": 1, "poles": [1000], "zeros": []}
TWO = {"gain": 1, "origin": 0, "poles": [100, 10000], "zeros": []}
DOUBLE = {"gain": 1, "origin": 0, "poles": [1000, 1000], "zeros": []}
LEADLAG = {"gain": 1, "origin": 0, "poles": [100], "zeros": [10000]}
THREE = {"gain": 1, "origin": 0, "poles": [100, 10000, 1000000], "zeros": []}

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("omegaRC", [1000, 1e-6], omega_rc(1000, 1e-6), "rad/s", "typical",
     "R = 1 kΩ and C = 1 µF put the corner at 1/(RC) = 1000 rad/s")
case("radToHz", [1000], rad_to_hz(1000), "Hz", "typical",
     "1000 rad/s is 1000/(2π) = 159.2 Hz, not 1000 Hz")
case("omegaRL", [1000, 0.1], omega_rl(1000, 0.1), "rad/s", "typical",
     "R = 1 kΩ and L = 100 mH put the corner at R/L = 10 000 rad/s")
case("circuitSystem", ["rc-low", 1000, 1e-6], circuit_system("rc-low", 1000, 1e-6), "", "typical",
     "RC low-pass, 1 kΩ and 1 µF: H(s) = 1/(1 + s/1000), one pole at 1000 rad/s")
case("circuitSystem", ["rl-high", 1000, 0.1], circuit_system("rl-high", 1000, 0.1), "", "typical",
     "RL high-pass, 1 kΩ and 100 mH: H(s) = (s/10 000)/(1 + s/10 000), a zero at the origin and a pole at 10 000 rad/s")
case("mag", [LP, 1000], mag(LP, 1000), "", "typical",
     "one pole at 1000 rad/s, at ω = 1000 rad/s: |H| = 1/√2 = 0.707 of the input amplitude, half the power")
case("magDb", [LP, 1000], mag_db(LP, 1000), "dB", "typical",
     "the same point in decibels: −3.01 dB")
case("phaseDeg", [LP, 1000], phase_deg(LP, 1000), "°", "typical",
     "one pole at 1000 rad/s, at ω = 1000 rad/s: the phase is −45°, not −90°")
case("delaySec", [LP, 1000], delay_sec(LP, 1000), "s", "typical",
     "−45° at 1000 rad/s is a delay of (π/4)/1000 = 0.785 ms")
case("outputAt", [LP, 1000, 3 * math.pi / 4 / 1000], output_at(LP, 1000, 3 * math.pi / 4 / 1000), "V", "typical",
     "input sin(ωt) of 1 V at 1000 rad/s through one pole at 1000 rad/s: at t = 2.356 ms the output is at its peak, 0.707 V, 0.785 ms after the input's peak at 1.571 ms")
case("magDb", [LP, 1], mag_db(LP, 1), "dB", "limit-zero",
     "one pole at 1000 rad/s, at ω = 1 rad/s, three decades below: |H| is 1 to within 0.000004 dB")
case("phaseDeg", [LP, 1], phase_deg(LP, 1), "°", "limit-zero",
     "the same point: the phase is only −0.057°")
case("magDb", [LP, 1e7], mag_db(LP, 1e7), "dB", "limit-infinity",
     "one pole at 1000 rad/s, at ω = 10⁷ rad/s, four decades above: −80 dB, falling 20 dB per decade")
case("phaseDeg", [LP, 1e7], phase_deg(LP, 1e7), "°", "limit-infinity",
     "the same point: the phase has nearly finished its turn, at −89.994°")
case("asymDb", [LP, 1000], asym_db(LP, 1000), "dB", "breaks",
     "the straight-line sketch says 0 dB at the corner of a pole at 1000 rad/s; the true value is −3.01 dB")
case("magDb", [DOUBLE, 1000], mag_db(DOUBLE, 1000), "dB", "breaks",
     "two poles both at 1000 rad/s: the sketch still says 0 dB at the corner, the curve is at −6.02 dB")
case("asymPhaseDeg", [LP, 100], asym_phase_deg(LP, 100), "°", "breaks",
     "the three-segment phase sketch says 0° a decade below a pole at 1000 rad/s; the true phase there is −5.71°")
case("phaseDeg", [LP, 100], phase_deg(LP, 100), "°", "breaks",
     "the true phase a decade below the pole at 1000 rad/s, at 100 rad/s: −5.71°")
case("phaseDeg", [HP, 1000], phase_deg(HP, 1000), "°", "sign",
     "RC high-pass with its corner at 1000 rad/s: at the corner the output leads by +45°")
case("delaySec", [HP, 1000], delay_sec(HP, 1000), "s", "sign",
     "a lead of 45° at 1000 rad/s is a negative delay: the output peaks 0.785 ms before the input")
case("magDb", [HP, 1000], mag_db(HP, 1000), "dB", "typical",
     "the high-pass is also −3.01 dB at its corner")
case("asymDb", [TWO, 1000], asym_db(TWO, 1000), "dB", "typical",
     "poles at 100 rad/s and 10 000 rad/s, at 1000 rad/s: the sketch is one decade down a −20 dB/decade line, −20 dB")
case("magDb", [TWO, 1000], mag_db(TWO, 1000), "dB", "typical",
     "the same point on the true curve: −20.09 dB, close to the sketch because both corners are a decade away")
case("phaseDeg", [TWO, 1000], phase_deg(TWO, 1000), "°", "typical",
     "the same point: −84.29° from the first pole and −5.71° from the second, −90° in all")
case("asymPhaseDeg", [TWO, 1000], asym_phase_deg(TWO, 1000), "°", "typical",
     "the phase sketch at the same point: −90° from the first pole and 0° from the second")
case("asymDb", [LEADLAG, 1e5], asym_db(LEADLAG, 1e5), "dB", "typical",
     "a pole at 100 rad/s and a zero at 10 000 rad/s, at 10⁵ rad/s: −60 dB from the pole plus 20 dB from the zero, −40 dB, and the line is flat again")
case("phaseDeg", [THREE, 1e7], phase_deg(THREE, 1e7), "°", "limit-infinity",
     "poles at 100, 10⁴ and 10⁶ rad/s, at 10⁷ rad/s: the phase has gone past −180°, to −264.23°")

print(json.dumps(cases, ensure_ascii=False))
