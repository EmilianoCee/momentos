"""Reference script for plans/mosfet-channel.md. Standard library only.

A long-channel NMOS with no channel-length modulation, in cm, s, V, A, F. The channel runs from the source (x = 0) to
the drain (x = 1, as a fraction of L). With V_OV = V_GS - V_T and V_e = min(V_DS, V_OV) (the drain voltage the channel
actually sees before it pinches off):
  F = V_OV V_e - V_e^2/2
  I_D = mu C_ox (W/L) F
  V(x) = V_OV - sqrt(V_OV^2 - 2 x F)               the channel's voltage above the source
  Q(x) = C_ox (V_OV - V(x)) = C_ox sqrt(V_OV^2 - 2 x F)   the electron charge per area (a magnitude)
  E(x) = dV/dx = F / (L sqrt(V_OV^2 - 2 x F))           the field along the channel, V/cm
Every slice carries the same current: W Q(x) mu E(x) = I_D. Prints the plan's check cases as one JSON list.
"""
import json
import math


def v_ov(VGS, VT):
    return VGS - VT


def region(VGS, VDS, VT):
    vov = VGS - VT
    if vov <= 0:
        return "cut-off"
    return "triode" if VDS < vov else "saturation"


def drain_current(k, VT, VGS, VDS):
    vov = VGS - VT
    if vov <= 0:
        return 0.0
    ve = min(VDS, vov)
    return k * (vov * ve - ve * ve / 2)


def _F(VGS, VT, VDS):
    vov = VGS - VT
    ve = min(VDS, vov)
    return vov, vov * ve - ve * ve / 2


def channel_v(VGS, VT, VDS, x):
    vov, F = _F(VGS, VT, VDS)
    if vov <= 0:
        return 0.0
    return vov - math.sqrt(max(0.0, vov * vov - 2 * x * F))


def channel_charge(Cox, VGS, VT, VDS, x):
    vov, F = _F(VGS, VT, VDS)
    if vov <= 0:
        return 0.0
    return Cox * math.sqrt(max(0.0, vov * vov - 2 * x * F))


def channel_field(VGS, VT, VDS, L, x):
    vov, F = _F(VGS, VT, VDS)
    if vov <= 0 or F == 0:
        return 0.0
    r = vov * vov - 2 * x * F
    return math.inf if r <= 0 else F / (L * math.sqrt(r))


def current_at(mu, Cox, W, L, VGS, VT, VDS, x):
    """W Q(x) mu E(x): the current through the slice at x, from drift alone"""
    E = channel_field(VGS, VT, VDS, L, x)
    Q = channel_charge(Cox, VGS, VT, VDS, x)
    if math.isinf(E):
        return math.nan
    return W * Q * mu * E


def speed_at(mu, VGS, VT, VDS, L, x):
    """the electrons' drift speed mu E(x), cm/s"""
    return mu * channel_field(VGS, VT, VDS, L, x)


def on_resistance(k, VGS, VT):
    """deep triode, V_DS much smaller than V_OV: R = 1/(k V_OV)"""
    vov = VGS - VT
    return math.inf if vov <= 0 else 1 / (k * vov)


MU, COX, L = 400.0, 5e-7, 1e-4            # cm^2/(V s), F/cm^2, cm (1 um)
K10 = MU * COX * 10                        # W/L = 10: 2 mA/V^2

# checks: the drift current is the same in every slice and equals I_D; the triode and saturation formulas meet at V_OV
for vds in (0.1, 0.3, 0.5, 0.9):
    for x in (0.0, 0.4, 0.8):
        assert abs(current_at(MU, COX, 10 * L, L, 1.0, 0.5, vds, x) - drain_current(K10, 0.5, 1.0, vds)) < 1e-15
assert abs(drain_current(K10, 0.5, 1.0, 0.5) - K10 / 2 * 0.25) < 1e-18

cases = []


def case(fn, args, value, units, tag, note, tol=1e-9):
    if isinstance(value, float) and math.isinf(value):
        value = "Infinity"
    cases.append({"fn": fn, "args": args, "expect": value, "tol": tol, "units": units, "tag": tag, "note": note})


case("region", [1.0, 0.2, 0.5], region(1.0, 0.2, 0.5), "", "typical",
     "V_GS = 1 V, V_T = 0.5 V, V_DS = 0.2 V: V_DS < V_OV = 0.5 V, triode")
case("region", [1.0, 0.8, 0.5], region(1.0, 0.8, 0.5), "", "typical",
     "the same with V_DS = 0.8 V: V_DS ≥ V_OV, saturation")
case("region", [0.4, 1.0, 0.5], region(0.4, 1.0, 0.5), "", "typical",
     "V_GS = 0.4 V below V_T = 0.5 V: cut-off, whatever V_DS")
case("drainCurrent", [0.002, 0.5, 1.0, 0.2], drain_current(0.002, 0.5, 1.0, 0.2), "A", "typical",
     "k = μ_nC_ox·W/L = 2 mA/V², V_OV = 0.5 V, V_DS = 0.2 V: I_D = k(V_OV·V_DS − V_DS²/2) = 160 µA", tol=1e-15)
case("drainCurrent", [0.002, 0.5, 1.0, 0.8], drain_current(0.002, 0.5, 1.0, 0.8), "A", "typical",
     "V_DS = 0.8 V, past V_OV: I_D = (k/2)·V_OV² = 250 µA, the square law", tol=1e-15)
case("drainCurrent", [0.002, 0.5, 1.5, 2.0], drain_current(0.002, 0.5, 1.5, 2.0), "A", "typical",
     "double the overdrive to 1 V (saturated): I_D = 1 mA, four times as much", tol=1e-15)
case("drainCurrent", [0.002, 0.5, 1.0, 0.001], drain_current(0.002, 0.5, 1.0, 0.001), "A", "limit-zero",
     "V_DS = 1 mV: I_D = 0.999 µA, almost exactly k·V_OV·V_DS: the channel is a resistor of 1/(k·V_OV) = 1 kΩ", tol=1e-15)
case("onResistance", [0.002, 1.0, 0.5], on_resistance(0.002, 1.0, 0.5), "Ω", "limit-zero",
     "that resistance: 1/(2 mA/V² × 0.5 V) = 1 kΩ, set by the gate")
case("drainCurrent", [0.002, 0.5, 1.0, 5.0], drain_current(0.002, 0.5, 1.0, 5.0), "A", "limit-infinity",
     "V_DS = 5 V, far past pinch-off: still 250 µA. Without channel-length modulation the current ignores the drain", tol=1e-15)
case("channelCharge", [5e-7, 1.0, 0.5, 0.2, 0], channel_charge(5e-7, 1.0, 0.5, 0.2, 0), "C/cm²", "typical",
     "at the source, the channel charge is C_ox·V_OV = 5×10⁻⁷ F/cm² × 0.5 V = 250 nC/cm²", tol=1e-15)
case("channelCharge", [5e-7, 1.0, 0.5, 0.2, 1], channel_charge(5e-7, 1.0, 0.5, 0.2, 1), "C/cm²", "typical",
     "at the drain, with V_DS = 0.2 V: C_ox(V_OV − V_DS) = 150 nC/cm²; the sheet is thinner where the gate-to-channel voltage is smaller", tol=1e-15)
case("channelV", [1.0, 0.5, 0.2, 0.5], channel_v(1.0, 0.5, 0.2, 0.5), "V", "typical",
     "halfway along that channel the voltage is 0.088 V, less than half of 0.2 V: the field is weaker near the source, where the sheet is thick")
case("channelField", [1.0, 0.5, 0.2, 0.0001, 0.5], channel_field(1.0, 0.5, 0.2, 1e-4, 0.5), "V/cm", "typical",
     "the field halfway along a 1 µm channel at V_DS = 0.2 V: 1.94 kV/cm")
case("speedAt", [400, 1.0, 0.5, 0.2, 0.0001, 0.5], speed_at(400, 1.0, 0.5, 0.2, 1e-4, 0.5), "cm/s", "typical",
     "the electrons there drift at μE = 400 cm²/V·s × 1.94 kV/cm = 7.76×10⁵ cm/s")
case("currentAt", [400, 5e-7, 0.001, 0.0001, 1.0, 0.5, 0.2, 0.5], current_at(400, 5e-7, 1e-3, 1e-4, 1.0, 0.5, 0.2, 0.5), "A", "other",
     "drift in that slice: W·Q·μ·E = 10 µm × 206 nC/cm² × 400 cm²/V·s × 1.94 kV/cm = 160 µA, the drain current", tol=1e-15)
case("currentAt", [400, 5e-7, 0.001, 0.0001, 1.0, 0.5, 0.2, 0.9], current_at(400, 5e-7, 1e-3, 1e-4, 1.0, 0.5, 0.2, 0.9), "A", "other",
     "near the drain the sheet is thinner and the field stronger, and the product is again 160 µA", tol=1e-15)
case("channelCharge", [5e-7, 1.0, 0.5, 0.8, 1], channel_charge(5e-7, 1.0, 0.5, 0.8, 1), "C/cm²", "typical",
     "in saturation the charge at the drain end is zero: the channel has pinched off", tol=1e-15)
case("channelField", [1.0, 0.5, 0.8, 0.0001, 1], channel_field(1.0, 0.5, 0.8, 1e-4, 1), "V/cm", "breaks",
     "at the pinch-off point the model's field is infinite, and μE would pass any speed; real electrons stop near 10⁷ cm/s and cross a short high-field gap")
case("channelField", [1.0, 0.5, 0.8, 0.0001, 0.99], channel_field(1.0, 0.5, 0.8, 1e-4, 0.99), "V/cm", "breaks",
     "just 10 nm before it the field is already 25 kV/cm: μE = 10⁷ cm/s, at velocity saturation")

print(json.dumps(cases, ensure_ascii=False))
