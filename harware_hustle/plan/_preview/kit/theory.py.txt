#!/usr/bin/env python3
"""Hand-calculation tables for the answer sheet (Q1.2 and Q3.1) from first principles.

  python theory.py                          # paper values, 5.0 mm measured bore
  python theory.py --id 5.1 --measured 1.02 3.01 4.85 --length 2.4

v = Q/A, Re = rho*v*D/mu, Blasius f = 0.316 Re^-0.25 (smooth tube, Re < 1e5),
dp/L = f*rho*v^2/(2D), transport time over L = L/v, residence time tau = V/Q.
"""
import argparse
import math

RHO, MU = 1000.0, 1e-3


def row(q_lpm, d_mm, length_m):
    q = q_lpm / 60000.0
    d = d_mm / 1000.0
    area = math.pi * d * d / 4
    v = q / area
    re = RHO * v * d / MU
    regime = "laminar" if re < 2300 else "transitional" if re < 4000 else "turbulent, near transition" if re < 6000 else "turbulent"
    f = 64 / re if re < 2300 else 0.316 * re ** -0.25
    dpl = f * RHO * v * v / (2 * d)
    return v, re, regime, dpl, length_m / v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nominal", type=float, default=8.0, help="'pipe diameter' given in the paper, mm (it is the OD)")
    ap.add_argument("--id", type=float, default=5.0, help="measured bore of the 8x5 PU tube, mm")
    ap.add_argument("--flows", type=float, nargs="+", default=[1.0, 3.0, 6.0])
    ap.add_argument("--measured", type=float, nargs="*", help="FT-01 calibrated flows achieved, L/min (same order)")
    ap.add_argument("--length", type=float, default=1.0, help="tube length for transit time / pressure drop, m")
    a = ap.parse_args()

    print(f"\nQ1.2  Theoretical velocity: paper bore {a.nominal} mm vs measured bore {a.id} mm "
          f"(area ratio {(a.nominal / a.id) ** 2:.2f})")
    print("| Q target (L/min) | v @ 8 mm (m/s) | Re @ 8 mm | v @ ID (m/s) | Re @ ID | regime @ ID | dp per m @ ID (kPa/m) | "
          f"transit {a.length:g} m (s) | turbulent front speed 1.22v (m/s) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in a.flows:
        v8, re8, *_ = row(q, a.nominal, a.length)
        v, re, reg, dpl, tt = row(q, a.id, a.length)
        print(f"| {q:g} | {v8:.3f} | {re8:,.0f} | {v:.3f} | {re:,.0f} | {reg} | {dpl / 1000:.1f} | {tt:.2f} | {1.224 * v:.2f} |")
    if a.measured:
        print("\nMeasured operating points (calibrated FT-01, same bore):")
        print("| target | achieved (L/min) | v actual (m/s) | Re | dp per m (kPa/m) |\n|---|---|---|---|---|")
        for tq, mq in zip(a.flows, a.measured):
            v, re, reg, dpl, _ = row(mq, a.id, a.length)
            print(f"| {tq:g} | {mq:.3f} | {v:.3f} | {re:,.0f} ({reg}) | {dpl / 1000:.1f} |")

    print("\nQ3.1  Residence time tau = V/Q  (the paper prints Q/V; that ratio is the turnover rate in 1/min)")
    for v_l, q in ((0.5, 2.5), (1.0, 2.5), (0.5, 5.0)):
        print(f"  V = {v_l} L, Q = {q} L/min  ->  tau = {v_l / q:.2f} min = {v_l / q * 60:.0f} s   (Q/V = {q / v_l:.1f} /min)")

    print("\nFlush effectiveness of a well-mixed sump (CSTR washout): fraction of old fluid left = exp(-V_flush/V_sump)")
    for vs in (1.5, 2.0, 2.5, 3.0):
        print(f"  sump {vs:.1f} L, flush 4.2 L  ->  {math.exp(-4.2 / vs) * 100:.0f}% of the original fluid remains")

    print("\nSOV-01 (1/4\" brass, ~2.5 mm orifice, Cv ~0.23): dp = SG*(Q/Cv)^2 with Q in US gpm, dp in psi")
    for q in (1.0, 2.0, 3.0, 4.0):
        gpm = q / 3.785
        dp_psi = (gpm / 0.23) ** 2
        print(f"  {q:.0f} L/min -> {dp_psi:5.1f} psi = {dp_psi * 0.0689:.2f} bar across the valve on the P-01 suction")


if __name__ == "__main__":
    main()
