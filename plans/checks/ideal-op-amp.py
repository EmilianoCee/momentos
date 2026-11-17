"""Reference script for plans/ideal-op-amp.md. Standard library only.

The op-amp: v_out = A (v+ - v-), no current into either input, no output resistance, and v_out held
between -Vsat and +Vsat when the rails are on. R1 and R2 as in the plan:
  inverting      v_in -> R1 -> node (- input) -> R2 -> v_out, + input grounded
  non-inverting  v_in -> + input; v_out -> R2 -> node (- input) -> R1 -> ground
  follower       v_in -> + input; v_out wired straight to the - input
"Swapped" exchanges the two input pins, which turns the feedback positive.
Prints the plan's check cases as one JSON list.
"""
import json


def beta(top, R1, R2):
    return 1.0 if top == "follower" else R1 / (R1 + R2)


def ideal_gain(top, R1, R2):
    return {"inverting": -R2 / R1, "non-inverting": 1 + R2 / R1, "follower": 1.0}[top]


def closed_gain(top, R1, R2, A):
    b = beta(top, R1, R2)
    if top == "inverting":
        # v- = (R2 v_in + R1 v_out)/(R1 + R2) and v_out = -A v-
        return -(R2 / (R1 + R2)) * A / (1 + A * b)
    return A / (1 + A * b)


def gain_error_pct(top, R1, R2, A):
    return 100 * (closed_gain(top, R1, R2, A) - ideal_gain(top, R1, R2)) / ideal_gain(top, R1, R2)


def nodes(top, R1, R2, vin, vout):
    """the voltages at the feedback node and at the other input pin's wire, for a given v_out"""
    if top == "inverting":
        fb = (R2 * vin + R1 * vout) / (R1 + R2)
        return fb, 0.0          # feedback node, the grounded side
    if top == "non-inverting":
        return R1 * vout / (R1 + R2), vin
    return vout, vin


def currents(top, R1, R2, vin, vout, fb):
    # inverting: i1 from v_in into the node through R1, i2 from the node to v_out through R2
    # non-inverting: i2 from v_out into the node through R2, i1 from the node to ground through R1
    if top == "inverting":
        return (vin - fb) / R1, (fb - vout) / R2
    if top == "non-inverting":
        return fb / R1, (vout - fb) / R2
    return 0.0, 0.0


def solve(top, R1, R2, A, vin, Vsat, clip, swapped):
    if not swapped:
        vout = closed_gain(top, R1, R2, A) * vin
        sat = clip and abs(vout) > Vsat
        if sat:
            vout = Vsat if vout > 0 else -Vsat
        fb, other = nodes(top, R1, R2, vin, vout)
        vplus, vminus = other, fb
    else:
        # positive feedback: the linear balance is unstable. Starting from v_out = 0 the output runs the
        # way the input difference pushes it, and the feedback pushes it further, to a rail.
        fb0, other0 = nodes(top, R1, R2, vin, 0.0)
        push = fb0 - other0          # v+ - v- at v_out = 0, with v+ now on the feedback node
        vout = 0.0 if push == 0 else (Vsat if push > 0 else -Vsat)
        sat = push != 0
        fb, other = nodes(top, R1, R2, vin, vout)
        vplus, vminus = fb, other
    i1, i2 = currents(top, R1, R2, vin, vout, fb)
    return {"vout": vout, "vplus": vplus, "vminus": vminus, "vdiff": vplus - vminus, "i1": i1, "i2": i2,
            "saturated": sat}


cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("idealGain", ["inverting", 1000, 10000], ideal_gain("inverting", 1000, 10000), "", "typical",
     "inverting, R1 = 1 kΩ, R2 = 10 kΩ: the ideal gain is −R2/R1 = −10")
case("idealGain", ["non-inverting", 1000, 10000], ideal_gain("non-inverting", 1000, 10000), "", "typical",
     "non-inverting, R1 = 1 kΩ, R2 = 10 kΩ: the ideal gain is 1 + R2/R1 = 11")
case("beta", ["non-inverting", 1000, 10000], beta("non-inverting", 1000, 10000), "", "typical",
     "R1 = 1 kΩ to ground and R2 = 10 kΩ from the output: a fraction 1/11 of v_out is fed back")
case("closedGain", ["inverting", 1000, 10000, 100000], closed_gain("inverting", 1000, 10000, 1e5), "", "typical",
     "inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is −9.9989, a hair short of −10")
case("closedGain", ["non-inverting", 1000, 10000, 100000], closed_gain("non-inverting", 1000, 10000, 1e5), "", "typical",
     "non-inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is 10.9988, a hair short of 11")
case("closedGain", ["follower", 1000, 10000, 1000], closed_gain("follower", 1000, 10000, 1000), "", "typical",
     "follower with A = 1000 (R1 and R2 unused): the gain is 1000/1001 = 0.999")
case("gainErrorPct", ["inverting", 1000, 10000, 100000], gain_error_pct("inverting", 1000, 10000, 1e5), "%", "typical",
     "inverting, 1 kΩ and 10 kΩ, A = 10⁵: the gain is 0.011% short, which is 1/(1 + Aβ) with Aβ = 9091")
case("solve", ["inverting", 1000, 10000, 100000, 0.5, 12, True, False],
     solve("inverting", 1000, 10000, 1e5, 0.5, 12, True, False), "V, A", "typical",
     "inverting, 1 kΩ and 10 kΩ, A = 10⁵, v_in = 0.5 V: v_out = −4.9995 V, the − input sits 50 µV above ground, and 0.5 mA flows through both resistors")
case("solve", ["non-inverting", 1000, 10000, 100000, 0.5, 12, True, False],
     solve("non-inverting", 1000, 10000, 1e5, 0.5, 12, True, False), "V, A", "typical",
     "non-inverting, 1 kΩ and 10 kΩ, A = 10⁵, v_in = 0.5 V: v_out = 5.4994 V and the two inputs differ by 55 µV")
case("solve", ["inverting", 1000, 10000, 100000, 0, 12, True, False],
     solve("inverting", 1000, 10000, 1e5, 0, 12, True, False), "V, A", "limit-zero",
     "inverting with v_in = 0 V: everything sits at 0 V and no current flows")
case("gainErrorPct", ["inverting", 1000, 10000, 10], gain_error_pct("inverting", 1000, 10000, 10), "%", "limit-zero",
     "inverting, 1 kΩ and 10 kΩ, with a small A = 10: the gain is −4.76, 52% short of −10. The virtual short needs a large A")
case("closedGain", ["inverting", 1000, 10000, 1e9], closed_gain("inverting", 1000, 10000, 1e9), "", "limit-infinity",
     "inverting, 1 kΩ and 10 kΩ, A = 10⁹: the gain is −10 to eight figures. The resistors alone set it")
case("solve", ["inverting", 1000, 10000, 1e9, 0.5, 12, True, False],
     solve("inverting", 1000, 10000, 1e9, 0.5, 12, True, False), "V, A", "limit-infinity",
     "the same with v_in = 0.5 V: the input difference has shrunk to 5 nV", tol=1e-12)
case("solve", ["inverting", 1000, 10000, 100000, 2, 12, True, False],
     solve("inverting", 1000, 10000, 1e5, 2, 12, True, False), "V, A", "breaks",
     "inverting, gain −10, v_in = 2 V asks for −20 V but the rail stops it at −12 V: the − input is pulled to 0.727 V and the virtual short is gone")
case("solve", ["non-inverting", 1000, 10000, 100000, 0.5, 12, True, True],
     solve("non-inverting", 1000, 10000, 1e5, 0.5, 12, True, True), "V, A", "sign",
     "non-inverting with its inputs swapped, v_in = 0.5 V: the feedback is positive and the output slams to −12 V, with 1.59 V between the inputs")
case("solve", ["inverting", 1000, 10000, 100000, 0.5, 12, True, True],
     solve("inverting", 1000, 10000, 1e5, 0.5, 12, True, True), "V, A", "sign",
     "inverting with its inputs swapped, v_in = 0.5 V: the output slams to +12 V, not to the −5 V the resistors ask for")
case("solve", ["inverting", 1000, 10000, 100000, 2, 12, False, False],
     solve("inverting", 1000, 10000, 1e5, 2, 12, False, False), "V, A", "other",
     "the same as the clipped case with the rails off: v_out = −19.998 V and the inputs differ by 200 µV")

print(json.dumps(cases, ensure_ascii=False))
