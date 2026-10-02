#!/usr/bin/env python3
"""FT-01 calibration from gravimetric runs (ISO 4185 static weighing, standing start/stop).

Input CSV columns: run, pulses, time_s, mass_g   (optional: duty, note; or volume_l instead of mass_g)
mass_g is the NET mass in the bucket (gross - tare). The ESP32 'CAL <s> <duty%>' command
prints pulses and time_s for each run; rig_console.py writes them to runs/*_cal.csv.

  python cal_fit.py runs/20261003_101500_cal.csv --plot cal.png

Prints the Q2.2/Q2.3 tables, the fit (Q = a*f + b), R^2, max/average calibration error,
an uncertainty budget, and the SET commands to paste into the console.
"""
import argparse
import csv
import math
import sys

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 18: 2.101, 20: 2.086, 25: 2.060, 30: 2.042}


def t975(dof):
    if dof <= 0:
        return float("nan")
    keys = sorted(T975)
    for k in keys:
        if dof <= k:
            return T975[k]
    return 1.96


def load(path, rho, exclude):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if not r.get("pulses") or not r.get("time_s"):
                continue
            run = r.get("run", str(len(rows) + 1)).strip()
            if run in exclude:
                continue
            if r.get("mass_g", "").strip():
                vol = float(r["mass_g"]) / rho  # rho in g/L
            elif r.get("volume_l", "").strip():
                vol = float(r["volume_l"])
            else:
                print(f"run {run}: no mass_g/volume_l yet, skipped", file=sys.stderr)
                continue
            n, t = float(r["pulses"]), float(r["time_s"])
            rows.append({"run": run, "pulses": n, "t": t, "vol": vol, "f": n / t, "q": vol / t * 60.0,
                         "duty": r.get("duty", ""), "mass": r.get("mass_g", "")})
    return rows


def fit(rows):
    n = len(rows)
    fx = [r["f"] for r in rows]
    qy = [r["q"] for r in rows]
    fm, qm = sum(fx) / n, sum(qy) / n
    sxx = sum((x - fm) ** 2 for x in fx)
    sxy = sum((x - fm) * (y - qm) for x, y in zip(fx, qy))
    a = sxy / sxx
    b = qm - a * fm
    res = [y - (a * x + b) for x, y in zip(fx, qy)]
    ss_res = sum(e * e for e in res)
    ss_tot = sum((y - qm) ** 2 for y in qy)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    s = math.sqrt(ss_res / (n - 2)) if n > 2 else float("nan")
    se_a = s / math.sqrt(sxx)
    se_b = s * math.sqrt(1 / n + fm * fm / sxx)
    return {"a": a, "b": b, "r2": r2, "s": s, "se_a": se_a, "se_b": se_b, "fm": fm, "sxx": sxx, "n": n}


def write_certificate(args, rows, F, errs, kmean, kstd, pi, f3, worst):
    import datetime
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a, b = F["a"], F["b"]
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    fig.text(0.07, 0.955, "Calibration certificate", fontsize=18, weight="bold")
    fig.text(0.07, 0.932, "FT-01 flow transmitter (YF-S401 hall-effect turbine), installed in line L-202", fontsize=10)
    info = [
        ("Team", args.team or "-"), ("Date", datetime.date.today().isoformat()), ("Operator", args.operator or "-"),
        ("Method", "Static weighing after ISO 4185, standing start/stop; the ESP32 times each run"),
        ("Reference", args.scale), ("Medium", f"water, {args.water_temp or '-'} C, density {args.rho:g} g/L"),
        ("Installation", "in situ, final spool, P-02 pulsation present; spool frozen after calibration"),
    ]
    y = 0.905
    for k, v in info:
        fig.text(0.07, y, k, fontsize=9, weight="bold")
        fig.text(0.22, y, v, fontsize=9)
        y -= 0.018
    fig.text(0.07, y - 0.008, f"Result:  Q = {a:.6f} f {b:+.5f}   (Q in L/min, f in Hz)    R² = {F['r2']:.5f}", fontsize=11, weight="bold")
    y -= 0.03
    lines = [
        f"Max error {max(abs(e) for e in errs):.2f} %   ·   average error {sum(abs(e) for e in errs) / len(errs):.2f} %   ·   RMSE {F['s']:.4f} L/min",
        f"K = {kmean:.0f} ± {kstd:.0f} pulses/L (datasheet 5880, {(kmean / 5880 - 1) * 100:+.1f} %)   ·   a ± {F['se_a']:.6f}, b ± {F['se_b']:.5f} (1 SE)",
        f"At 3.00 L/min (f = {f3:.1f} Hz): ± {pi:.3f} L/min ({pi / 3 * 100:.2f} %), 95 % prediction interval; reference ≤ {worst:.2f} % (k = 2)",
    ]
    for ln in lines:
        fig.text(0.07, y, ln, fontsize=9)
        y -= 0.018
    ax = fig.add_axes([0.11, 0.42, 0.82, 0.235])
    fx = [r["f"] for r in rows]
    qy = [r["q"] for r in rows]
    hi = max(fx) * 1.08
    xs = [hi * i / 100 for i in range(101)]
    ax.plot(xs, [a * x + b for x in xs], lw=1.5, label="fit")
    ax.plot(xs, [x / 98 for x in xs], ":", lw=1, label="datasheet Q = f/98")
    ax.scatter(fx, qy, s=16, zorder=3, label="weighed runs")
    ax.set_xlabel("pulse frequency f (Hz)")
    ax.set_ylabel("actual flow Q (L/min)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    tax = fig.add_axes([0.07, 0.05, 0.86, 0.31])
    tax.axis("off")
    head = ["Run", "Pulses", "t (s)", "f (Hz)", "V (L)", "Q (L/min)", "Fit", "Error %"]
    body = [[r["run"], f"{r['pulses']:.0f}", f"{r['t']:.2f}", f"{r['f']:.2f}", f"{r['vol']:.4f}", f"{r['q']:.3f}",
             f"{a * r['f'] + b:.3f}", f"{e:+.2f}"] for r, e in zip(rows, errs)][:20]
    tbl = tax.table(cellText=body, colLabels=head, loc="upper center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.5)
    tbl.scale(1, 1.15)
    fig.text(0.07, 0.025, "Signed: ______________________ (operator)     ______________________ (checked)", fontsize=9)
    fig.savefig(args.certificate)
    print(f"certificate written to {args.certificate}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--rho", type=float, default=1000.0, help="water density, g/L (paper: 1000; 22 C: 997.8)")
    ap.add_argument("--u-scale-g", type=float, default=1.0, help="scale resolution, g")
    ap.add_argument("--u-lin", type=float, default=0.002, help="scale linearity, relative (0.002 = 0.2%%)")
    ap.add_argument("--u-time-s", type=float, default=0.05, help="start/stop timing uncertainty, s")
    ap.add_argument("--exclude", default="", help="comma-separated run ids to leave out")
    ap.add_argument("--plot", help="write a PNG of the fit and residuals")
    ap.add_argument("--certificate", help="write a one-page calibration certificate (PDF)")
    ap.add_argument("--team", default="", help="team name/ID for the certificate")
    ap.add_argument("--operator", default="", help="who ran the calibration")
    ap.add_argument("--water-temp", default="", help="water temperature, deg C (as measured)")
    ap.add_argument("--scale", default="1 g resolution, 5 kg digital scale", help="reference scale description")
    args = ap.parse_args()

    rows = load(args.csv, args.rho, set(x.strip() for x in args.exclude.split(",") if x.strip()))
    if len(rows) < 3:
        sys.exit("need at least 3 weighed runs")
    F = fit(rows)
    a, b = F["a"], F["b"]

    print("\nQ2.3  Trials (f = N/t, Q = V/t)")
    print("| Trial | Pulses | Time (s) | Frequency (Hz) | Collected volume (L) | Actual flow (L/min) | Fit (L/min) | Error (%) | K (pulses/L) |")
    print("|---|---|---|---|---|---|---|---|---|")
    errs = []
    for r in rows:
        qf = a * r["f"] + b
        e = (qf - r["q"]) / r["q"] * 100
        errs.append(e)
        k = r["pulses"] / r["vol"]
        print(f"| {r['run']} | {r['pulses']:.0f} | {r['t']:.2f} | {r['f']:.2f} | {r['vol']:.4f} | {r['q']:.3f} | {qf:.3f} | {e:+.2f} | {k:.0f} |")

    ks = [r["pulses"] / r["vol"] for r in rows]
    kmean = sum(ks) / len(ks)
    kstd = math.sqrt(sum((k - kmean) ** 2 for k in ks) / (len(ks) - 1))
    print("\nQ2.2  Calibration equation  Q = a*f + b   (Q in L/min, f in Hz)")
    print(f"| R^2 | {F['r2']:.5f} |")
    print(f"| a | {a:.6f} L/min per Hz  (+/- {F['se_a']:.6f} SE)  ->  {1 / a:.2f} Hz per L/min, {60 / a:.0f} pulses/L |")
    print(f"| b | {b:+.4f} L/min  (+/- {F['se_b']:.4f} SE) |")
    print(f"| Maximum calibration error | {max(abs(e) for e in errs):.2f} % |")
    print(f"| Average calibration error | {sum(abs(e) for e in errs) / len(errs):.2f} %  (RMSE {F['s']:.4f} L/min) |")
    print(f"\nDatasheet K = 5880 pulses/L (F = 98*Q). Measured K = {kmean:.0f} +/- {kstd:.0f} pulses/L "
          f"({(kmean / 5880 - 1) * 100:+.1f}% vs datasheet).")

    # Uncertainty of the reference flow (GUM, k = 2) per run, and of the fitted meter at 3 L/min.
    u_m = math.sqrt(2) * args.u_scale_g / math.sqrt(12)  # tare + gross readings
    print("\nReference uncertainty per run (k=2): ", end="")
    worst = 0
    for r in rows:
        m = r["vol"] * args.rho
        u_rel = math.sqrt((u_m / m) ** 2 + args.u_lin ** 2 + (args.u_time_s / r["t"]) ** 2 + 0.001 ** 2)
        worst = max(worst, 2 * u_rel * 100)
        print(f"{r['run']}:{2 * u_rel * 100:.2f}% ", end="")
    f3 = (3.0 - b) / a
    pi = t975(F["n"] - 2) * F["s"] * math.sqrt(1 + 1 / F["n"] + (f3 - F["fm"]) ** 2 / F["sxx"])
    print(f"\nAt 3.00 L/min (f = {f3:.1f} Hz) the fitted meter reads within +/- {pi:.3f} L/min "
          f"({pi / 3 * 100:.2f}%, 95% prediction interval); reference worst case {worst:.2f}%.")

    fcut = max(3.0, 0.8 * (0.3 - b) / a)
    print("\nPaste into rig_console:")
    print(f"SET a {a:.6f}\nSET b {b:.5f}\nSET fcut {fcut:.1f}\nSAVE")

    if args.certificate:
        write_certificate(args, rows, F, errs, kmean, kstd, pi, f3, worst)

    if args.plot:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fx = [r["f"] for r in rows]
        qy = [r["q"] for r in rows]
        lo, hi = 0, max(fx) * 1.08
        xs = [lo + (hi - lo) * i / 100 for i in range(101)]
        band = [t975(F["n"] - 2) * F["s"] * math.sqrt(1 + 1 / F["n"] + (x - F["fm"]) ** 2 / F["sxx"]) for x in xs]
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 7), gridspec_kw={"height_ratios": [3, 1.4]})
        ax1.fill_between(xs, [a * x + b - w for x, w in zip(xs, band)], [a * x + b + w for x, w in zip(xs, band)],
                         alpha=0.18, label="95% prediction band")
        ax1.plot(xs, [a * x + b for x in xs], lw=1.5, label=f"Q = {a:.5f} f {b:+.4f}   R² = {F['r2']:.4f}")
        ax1.plot(xs, [x / 98 for x in xs], ":", lw=1, label="datasheet Q = f/98")
        ax1.scatter(fx, qy, s=22, zorder=3, label="gravimetric runs")
        ax1.set_xlabel("FT-01 pulse frequency f (Hz)")
        ax1.set_ylabel("actual flow Q (L/min)")
        ax1.grid(alpha=0.3)
        ax1.legend(fontsize=8)
        ax2.axhspan(-2, 2, alpha=0.1)
        ax2.scatter(qy, errs, s=18)
        ax2.axhline(0, lw=0.8)
        ax2.set_xlabel("actual flow Q (L/min)")
        ax2.set_ylabel("fit error (%)")
        ax2.grid(alpha=0.3)
        fig.suptitle("FT-01 (YF-S401) in-situ gravimetric calibration")
        fig.tight_layout()
        fig.savefig(args.plot, dpi=160)
        print(f"plot written to {args.plot}")


if __name__ == "__main__":
    main()
