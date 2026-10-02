#!/usr/bin/env python3
"""Live console for the LAM flow rig.

Logs every frame the ESP32 sends to runs/<stamp>_telemetry.csv (+ events, calibration,
parameter and burst files) and plots live trends. Type firmware commands in the terminal and
press Enter (START, STOP, MARK V50, CAL 60 80, SET a 0.0101, SAVE, ...).
SHOT saves a screenshot of the live plots; screenshots are also saved automatically after the
float event, at the end of Case 1, with three pumps flushing, and at the automatic stop.

  pip install pyserial matplotlib
  python rig_console.py --port COM5            # Windows
  python rig_console.py --port /dev/ttyUSB0    # Linux
  python rig_console.py --replay runs/x_telemetry.csv   # no hardware

The console does not reboot the ESP32 when it connects, so it can be restarted during a run.
"""
import argparse
import collections
import csv
import datetime as dt
import os
import queue
import sys
import threading
import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

WINDOW_S = 180
NUMERIC_SKIP = {"state", "diag"}


def stamp():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


class Store:
    def __init__(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        s = stamp()
        self.paths = {k: os.path.join(outdir, f"{s}_{k}.csv") for k in ("telemetry", "events", "cal", "params")}
        self.burst_path = os.path.join(outdir, f"{s}_burst.txt")
        self.outdir, self.stamp = outdir, s
        self.params = None
        self.shots = []  # (firmware t_ms when due, label)
        self.shot_req = None
        self.shot_n = 0
        self.fields = None
        self.tele = None
        self.events = open(self.paths["events"], "w", newline="")
        self.ev_w = csv.writer(self.events)
        self.ev_w.writerow(["host_time", "t_ms", "tag", "text"])
        self.cal = open(self.paths["cal"], "w", newline="")
        self.cal_w = csv.writer(self.cal)
        self.cal_w.writerow(["run", "pulses", "time_s", "f_hz", "duty", "mass_g", "note"])
        self.series = collections.defaultdict(lambda: collections.deque(maxlen=WINDOW_S * 10 + 50))
        self.last = {}
        self.recent_events = collections.deque(maxlen=5)
        self.t0 = None
        self.phase_start = {}  # "Case 1" / "Case 2" -> firmware t_ms when it began

    def header(self, fields):
        self.fields = fields
        if self.tele is None:
            self.tele = open(self.paths["telemetry"], "w", newline="")
            self.tele_w = csv.writer(self.tele)
            self.tele_w.writerow(["host_time"] + fields)

    def frame(self, values, host_time):
        if not self.fields or len(values) != len(self.fields):
            return
        self.tele_w.writerow([host_time] + values)
        row = dict(zip(self.fields, values))
        prev, st = self.last.get("state", ""), row.get("state", "")
        if st == "C1_START":
            self.phase_start.clear()
        if st == "C1_RUN" and "Case 1" not in self.phase_start:
            self.phase_start["Case 1"] = float(row["t_ms"])
        if st == "C2_ISOLATE" and prev != "C2_ISOLATE":
            self.phase_start["Case 2"] = float(row["t_ms"])
        if prev and st != prev:
            t_ms = float(row["t_ms"])
            if prev == "C1_HOLD_LSH" and st == "C1_RUN":
                self.shots.append((t_ms + 5000, "case1_float_event"))
            elif st == "C2_ISOLATE":
                self.shots.append((t_ms, "case1_complete"))
            elif st == "C2_FLUSH":
                self.shots.append((t_ms + 20000, "case2_three_pumps"))
            elif st == "COMPLETE":
                self.shots.append((t_ms + 3000, "case2_auto_stop"))
            elif st == "STOPPED":
                self.shots.append((t_ms + 1000, "stopped"))
        t = float(row["t_ms"]) / 1000.0
        if self.t0 is None or t < self.t0:
            self.t0 = t
            for d in self.series.values():
                d.clear()
        self.series["t"].append(t - self.t0)
        for k, v in row.items():
            if k in NUMERIC_SKIP or k == "t_ms":
                continue
            try:
                x = float(v)
            except ValueError:
                x = float("nan")
            self.series[k].append(float("nan") if k == "sp" and x == 0 else x)
        self.last = row

    def param(self, key, value, host_time):
        if self.params is None:
            self.params = open(self.paths["params"], "w", newline="")
            self.par_w = csv.writer(self.params)
            self.par_w.writerow(["host_time", "key", "value"])
        self.par_w.writerow([host_time, key, value])

    def shot(self, fig, label):
        self.shot_n += 1
        path = os.path.join(self.outdir, f"{self.stamp}_shot{self.shot_n:02d}_{label}.png")
        fig.savefig(path, dpi=110)
        print("screenshot:", path)

    def flush(self):
        for f in (self.tele, self.events, self.cal, self.params):
            if f:
                f.flush()


def reader(ser, q, stop):
    while not stop.is_set():
        try:
            raw = ser.readline()
        except Exception as e:  # unplugged cable, etc.
            q.put(("ERR", str(e)))
            time.sleep(1)
            continue
        if raw:
            q.put(("LINE", raw.decode("utf-8", "replace").strip()))


def replayer(path, q, stop, speed):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    fields = rows[0][1:]
    q.put(("LINE", "H," + ",".join(fields)))
    prev = None
    for r in rows[1:]:
        if stop.is_set():
            return
        t = float(r[1]) / 1000.0
        if prev is not None:
            time.sleep(max(0.0, (t - prev) / speed))
        prev = t
        q.put(("LINE", "D," + ",".join(r[1:])))


def keyboard(ser, store, stop):
    for line in sys.stdin:
        cmd = line.strip()
        if not cmd:
            continue
        if cmd.upper() == "SHOT":
            store.shot_req = "manual"
            continue
        if ser is None:
            print("(replay mode: command not sent)")
            continue
        ser.write((cmd + "\n").encode())
        store.ev_w.writerow([dt.datetime.now().isoformat(timespec="milliseconds"), "", "CMD", cmd])
        if stop.is_set():
            return


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--out", default="runs")
    ap.add_argument("--replay", help="telemetry CSV written by this tool")
    ap.add_argument("--speed", type=float, default=1.0, help="replay speed factor")
    ap.add_argument("--reset", action="store_true", help="reboot the ESP32 on connect (never during a run)")
    ap.add_argument("--target", type=float, default=3.0, help="target flow drawn on the trend, L/min (0 hides it)")
    args = ap.parse_args()
    if not args.port and not args.replay:
        ap.error("give --port or --replay")

    store = Store(args.out)
    q = queue.Queue()
    stop = threading.Event()
    ser = None
    if args.replay:
        threading.Thread(target=replayer, args=(args.replay, q, stop, args.speed), daemon=True).start()
    else:
        import serial  # pyserial

        # Opening a port normally pulses DTR/RTS, which resets an ESP32 dev board and would stop the
        # rig mid-run. Hold both lines low through the open; use --reset when a reboot is wanted.
        ser = serial.Serial()
        ser.port, ser.baudrate, ser.timeout = args.port, args.baud, 0.2
        ser.dtr = False
        ser.rts = False
        ser.open()
        if args.reset:  # RTS asserted with DTR released pulls EN low on the auto-reset circuit
            ser.rts = True
            time.sleep(0.1)
            ser.rts = False
            time.sleep(1.0)
        time.sleep(0.3)
        ser.write(b"HDR\nGET\n")
        threading.Thread(target=reader, args=(ser, q, stop), daemon=True).start()
    threading.Thread(target=keyboard, args=(ser, store, stop), daemon=True).start()
    print(f"logging to {store.paths['telemetry']}")

    plt.rcParams.update({"font.size": 9})
    fig, axes = plt.subplots(4, 1, figsize=(11, 8.5), sharex=True, gridspec_kw={"height_ratios": [3, 2, 2, 2]})
    ax_q, ax_v, ax_i, ax_d = axes
    lines = {
        "q_lpm": ax_q.plot([], [], lw=1.6, label="FT-01 flow (L/min)")[0],
        "sp": ax_q.plot([], [], "--", lw=1, label="FIC set point")[0],
        "v_tot_l": ax_v.plot([], [], lw=1.4, label="total (L)")[0],
        "v_c1_l": ax_v.plot([], [], lw=1, label="Case 1 (L)")[0],
        "v_c2_l": ax_v.plot([], [], lw=1, label="Case 2 (L)")[0],
        "i1_a": ax_i.plot([], [], lw=1, label="P-01")[0],
        "i2_a": ax_i.plot([], [], lw=1, label="P-02")[0],
        "i3_a": ax_i.plot([], [], lw=1, label="P-03")[0],
        "d1": ax_d.plot([], [], lw=1, label="P-01 duty")[0],
        "d2": ax_d.plot([], [], lw=1, label="P-02 duty")[0],
        "d3": ax_d.plot([], [], lw=1, label="P-03 duty")[0],
        "lsh": ax_d.step([], [], where="post", lw=1, label="LS-01 high")[0],
        "sov": ax_d.step([], [], where="post", lw=1, label="SOV-01 open")[0],
    }
    if args.target > 0:
        ax_q.axhspan(args.target - 0.1, args.target + 0.1, color="tab:green", alpha=0.12, lw=0,
                     label=f"target {args.target:.1f} ± 0.1 L/min")
    sec = ax_q.secondary_yaxis("right", functions=(lambda x: x * 1000 / 60, lambda x: x * 60 / 1000))
    sec.set_ylabel("mL/s")
    ax_q.set_ylabel("L/min")
    ax_v.set_ylabel("litres")
    ax_i.set_ylabel("pump current (A)")
    ax_d.set_ylabel("duty / state")
    ax_d.set_xlabel("time (s)")
    ax_d.set_ylim(-0.05, 1.15)
    for a in axes:
        a.grid(alpha=0.3)
        a.legend(loc="upper left", fontsize=7, ncol=5)
    title = fig.suptitle("waiting for data...", fontsize=10, family="monospace")
    ev_text = fig.text(0.01, 0.005, "", fontsize=7, family="monospace", va="bottom")
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))

    def drain():
        while True:
            try:
                kind, payload = q.get_nowait()
            except queue.Empty:
                return
            now = dt.datetime.now().isoformat(timespec="milliseconds")
            if kind == "ERR":
                print("serial error:", payload)
                continue
            parts = payload.split(",")
            tag = parts[0]
            if tag == "H":
                store.header(parts[1:])
            elif tag == "D":
                store.frame(parts[1:], now)
            elif tag == "E" and len(parts) >= 4:
                text = ",".join(parts[3:])

                store.ev_w.writerow([now, parts[1], parts[2], text])
                store.recent_events.append(f"{float(parts[1]) / 1000:8.1f}s {parts[2]:<11} {text}")
                print(f"[{parts[2]}] {text}")
            elif tag == "C" and len(parts) >= 7:
                store.cal_w.writerow([parts[2], parts[3], parts[4], parts[5], parts[6], "", ""])
                print(f"\n*** CAL run {parts[2]}: pulses={parts[3]} t={parts[4]} s f={parts[5]} Hz duty={parts[6]}"
                      f" -> weigh the bucket and enter the mass in {store.paths['cal']}\n")
            elif tag == "B":
                with open(store.burst_path, "a") as f:
                    f.write("\n".join(parts[1:]) + "\n")
            elif tag == "P" and len(parts) >= 3:
                store.param(parts[1], parts[2], now)
                print(payload)
            elif tag == "I":
                store.ev_w.writerow([now, "", "INFO", ",".join(parts[1:])])
                print(payload)

    def update(_):
        drain()
        s = store.series
        if not s["t"]:
            return list(lines.values())
        t = list(s["t"])
        for k, ln in lines.items():
            if k in s and len(s[k]) == len(t):
                ln.set_data(t, list(s[k]))
        tmax = t[-1]
        for a in axes:
            a.set_xlim(max(0, tmax - WINDOW_S), max(10, tmax))
        for a, keys in ((ax_q, ["q_lpm", "sp"]), (ax_v, ["v_tot_l", "v_c1_l", "v_c2_l"]), (ax_i, ["i1_a", "i2_a", "i3_a"])):
            vals = [v for k in keys for v in list(s[k])[-WINDOW_S * 10:] if v == v]
            if vals:
                lo, hi = min(vals), max(vals)
                if a is ax_q:
                    hi = max(hi, args.target + 0.1)
                a.set_ylim(min(0, lo), hi * 1.15 + 0.1)
        L = store.last
        st = L.get("state", "?")
        phase = "Case 2" if st.startswith("C2") or st == "COMPLETE" else "Case 1" if st.startswith("C1") else None
        clock = ""
        if phase in store.phase_start and "t_ms" in L and st != "COMPLETE":
            clock = f"  {phase} +{(float(L['t_ms']) - store.phase_start[phase]) / 1000:5.0f} s"
        title.set_text(
            f"{st:<14}{clock} flow {float(L.get('q_lpm', 0)):5.2f} L/min = {float(L.get('q_mls', 0)):5.1f} mL/s"
            f"   V {float(L.get('v_tot_l', 0)):6.3f} L   diag {L.get('diag', '?')}   alarms 0x{int(float(L.get('alarms', 0))):X}"
        )
        ev_text.set_text("\n".join(store.recent_events))
        t_now = float(L.get("t_ms", 0))
        due = [x for x in store.shots if x[0] <= t_now]
        store.shots = [x for x in store.shots if x[0] > t_now]
        if store.shot_req:
            due.append((t_now, store.shot_req))
            store.shot_req = None
        for _, label in due:
            store.shot(fig, label)
        store.flush()
        return list(lines.values())

    anim = FuncAnimation(fig, update, interval=200, cache_frame_data=False)  # noqa: F841 (kept alive)
    try:
        plt.show()
    finally:
        stop.set()
        store.flush()
        if ser:
            ser.close()


if __name__ == "__main__":
    main()
