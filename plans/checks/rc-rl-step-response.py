"""Reference script for plans/rc-rl-step-response.md. Standard library only.

The circuit: a two-way switch puts either V_S or ground on the left end of R1. R1 runs to the top of the store
(a capacitor C or an inductor L) whose other end is ground. R2, when present, sits across the store; None means
absent. The state x is v_C in volts or i_L in amperes. Prints the plan's check cases as one JSON list.
"""
import json
import math


def r_th(R1, R2):
    return R1 if R2 is None else R1 * R2 / (R1 + R2)


def v_th(VS, R1, R2):
    return VS if R2 is None else VS * R2 / (R1 + R2)


def tau(store, R1, R2, X):
    return r_th(R1, R2) * X if store == "C" else X / r_th(R1, R2)


def final_value(store, VS, R1, R2):
    # capacitor: open at t -> infinity, so it takes the Thevenin voltage
    # inductor: a short at t -> infinity, so it carries the Thevenin voltage over the Thevenin resistance
    return v_th(VS, R1, R2) if store == "C" else v_th(VS, R1, R2) / r_th(R1, R2)


def state_at(start, final, T, t):
    return final + (start - final) * math.exp(-t / T)


def tangent_at(start, final, T, t):
    return start + (final - start) * t / T


def fraction_done(n):
    return 1 - math.exp(-n)


def jump_at(store, VS, R1, R2, x):
    # capacitor: i_C into the top plate. inductor: v_L across it, top end positive.
    if store == "C":
        return (v_th(VS, R1, R2) - x) / r_th(R1, R2)
    return v_th(VS, R1, R2) - r_th(R1, R2) * x


def square_wave(store, VS, R1, R2, X, x0, half, t):
    # the source is VS for the first half period, 0 for the next, and so on
    T = tau(store, R1, R2, X)
    x, done = x0, 0.0
    k = 0
    while done + half <= t:
        x = state_at(x, final_value(store, VS if k % 2 == 0 else 0.0, R1, R2), T, half)
        done += half
        k += 1
    return state_at(x, final_value(store, VS if k % 2 == 0 else 0.0, R1, R2), T, t - done)


# a numerical check of the capacitor case against Euler steps of C dv/dt = (V_th - v)/R_th
v, dt = 0.0, 1e-8
for _ in range(100000):            # 1 ms
    v += dt * (v_th(5, 1000, 1000) - v) / (r_th(1000, 1000) * 1e-6)
assert abs(v - state_at(0, 2.5, 5e-4, 1e-3)) < 1e-4

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("tau", ["C", 1000, None, 1e-6], tau("C", 1000, None, 1e-6), "s", "typical",
     "R1 = 1 kΩ, C = 1 µF, no R2: τ = RC = 1 ms")
case("tau", ["C", 1000, 1000, 1e-6], tau("C", 1000, 1000, 1e-6), "s", "typical",
     "the same with R2 = 1 kΩ across C: the capacitor sees 1 kΩ ∥ 1 kΩ = 500 Ω, so τ = 0.5 ms, not 1 ms")
case("tau", ["L", 1000, None, 1], tau("L", 1000, None, 1), "s", "typical",
     "R1 = 1 kΩ, L = 1 H: τ = L/R = 1 ms")
case("tau", ["L", 1000, 1000, 1], tau("L", 1000, 1000, 1), "s", "typical",
     "the same with R2 = 1 kΩ across L: L/(500 Ω) = 2 ms. A smaller resistance makes the inductor slower")
case("rTh", [1000, 3000], r_th(1000, 3000), "Ω", "typical",
     "R1 = 1 kΩ in parallel with R2 = 3 kΩ: 750 Ω, what the store sees with the source turned off")
case("finalValue", ["C", 5, 1000, None], final_value("C", 5, 1000, None), "V", "typical",
     "V_S = 5 V through 1 kΩ into a capacitor: it ends at 5 V, an open circuit carrying no current")
case("finalValue", ["C", 5, 1000, 1000], final_value("C", 5, 1000, 1000), "V", "typical",
     "with R2 = 1 kΩ across it, the capacitor ends at the divider's 2.5 V, not at 5 V")
case("finalValue", ["L", 5, 1000, 1000], final_value("L", 5, 1000, 1000), "A", "typical",
     "V_S = 5 V, R1 = 1 kΩ, R2 = 1 kΩ across an inductor: it ends as a short carrying 5 V/1 kΩ = 5 mA, and R2 carries nothing")
case("stateAt", [0, 5, 0.001, 0.001], state_at(0, 5, 1e-3, 1e-3), "V", "typical",
     "from 0 V toward 5 V with τ = 1 ms, after 1 ms: 3.16 V, 63% of the way, not all of it")
case("fractionDone", [1], fraction_done(1), "", "typical",
     "after one τ, 63.2% of the change is done")
case("fractionDone", [5], fraction_done(5), "", "typical",
     "after five τ, 99.3% of the change is done")
case("stateAt", [0, 5, 0.001, 0], state_at(0, 5, 1e-3, 0), "V", "limit-zero",
     "at t = 0⁺ the capacitor is still at its start, 0 V: its voltage cannot jump")
case("jumpAt", ["C", 5, 1000, None, 0], jump_at("C", 5, 1000, None, 0), "A", "limit-zero",
     "at t = 0⁺, with v_C = 0 V, the capacitor acts as a 0 V source: i_C jumps from 0 to 5 V/1 kΩ = 5 mA")
case("jumpAt", ["L", 5, 1000, None, 0], jump_at("L", 5, 1000, None, 0), "V", "limit-zero",
     "at t = 0⁺, with i_L = 0 A, the inductor acts as a 0 A current source, an open circuit: v_L jumps to the full 5 V")
case("stateAt", [0, 5, 0.001, 0.02], state_at(0, 5, 1e-3, 0.02), "V", "limit-infinity",
     "after 20 τ the capacitor is at 5 V to within 0.00000001 V: the open-circuit picture")
case("jumpAt", ["C", 5, 1000, None, 5], jump_at("C", 5, 1000, None, 5), "A", "limit-infinity",
     "when v_C has reached 5 V the capacitor current is 0 A: an open circuit")
case("tangentAt", [0, 5, 0.001, 0.001], tangent_at(0, 5, 1e-3, 1e-3), "V", "breaks",
     "the tangent at t = 0⁺ reaches the final 5 V at t = τ = 1 ms; the curve itself is only at 3.16 V. Keeping the starting slope is wrong after the first few percent")
case("jumpAt", ["C", 0, 1000, None, 5], jump_at("C", 0, 1000, None, 5), "A", "sign",
     "the switch flips to ground with the capacitor at 5 V: i_C = −5 mA, the capacitor drives current back out through R1")
case("stateAt", [5, 0, 0.001, 0.001], state_at(5, 0, 1e-3, 1e-3), "V", "sign",
     "discharging from 5 V toward 0 V with τ = 1 ms: after 1 ms it is at 1.84 V, 63% of the way down")
case("squareWave", ["C", 5, 1000, None, 1e-6, 0, 0.001, 0.0015], square_wave("C", 5, 1000, None, 1e-6, 0, 1e-3, 1.5e-3), "V", "typical",
     "square wave with half period 1 ms = τ: charging for 1 ms reaches 3.16 V, then 0.5 ms toward 0 V leaves 1.92 V")
case("squareWave", ["C", 5, 1000, None, 1e-6, 0, 0.01, 0.01], square_wave("C", 5, 1000, None, 1e-6, 0, 1e-2, 1e-2), "V", "typical",
     "square wave with half period 10 ms = 10 τ: by the end of the first half the capacitor is at 5 V to within 0.0002 V")

print(json.dumps(cases, ensure_ascii=False))
