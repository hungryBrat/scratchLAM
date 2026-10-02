#!/usr/bin/env python3
"""Assembles the build-book artifact page and the downloadable build kit.

  python build_page.py  ->  out/hardware_hustle_build_book.html, out/kit/* (published), out/kit/*.zip (local only)
"""
import html
import json
import os
import re
import zipfile

import content as C
import diagrams as D
import export_plan_md as X

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")

CHECKS = [
    {"title": "Requirements coverage (every line of the paper)", "items": [
        ["rq-pid", "Q1.1 labelled P&amp;ID: pumps, throttling valve (BV-02), FT-01, flow direction, tanks, sump, tube sizes, measurement points (page 4 and video 0:30)"],
        ["rq-c1path", "Case 1 path exactly as specified: TK-01 → on/off valve → P-01 → sump → P-02 → FT-01 → TK-01 (single take)"],
        ["rq-duties", "P-01 at 50% and P-02 at 100%, or the raised P-01 duty explained with the measured data (decision log)"],
        ["rq-cal", "FT-01 calibrated and shown (certificate; Q2.2)"],
        ["rq-pour", "External fluid into the sump: P-01 stops, P-02 keeps running, P-01 restarts by itself (single take)"],
        ["rq-trend", "Flow against time in mL/s, total litres returned to TK-01, and screenshots in L/min"],
        ["rq-code", "Code shared: link written in the PDF (page 3 and appendix) and on the video's last card; opens logged out"],
        ["rq-switch", "Case 1 started with the on/off switch, on camera"],
        ["rq-tee", "Case 2 flush through the equal tee, with the on/off valve shut to isolate TK-01"],
        ["rq-bv01", "BV-01 opened before P-03 starts, and it is the only manual action"],
        ["rq-3pumps", "All three pumps running together during the flush (console duties visible)"],
        ["rq-onego", "Case 1 and Case 2 in a single go, with no other intervention"],
        ["rq-stop", "System stops as soon as the flush tank finishes (event latency read out)"],
        ["rq-video", "Challenge Video 10–12 min (MP4): every component identified, flow direction spoken, both cases shown"],
        ["rq-journey", "Journey Video 3–4 min (MP4): real build footage, each member on camera"],
        ["rq-hand", "Solution handwritten in blue or black ink, scanned to one PDF"],
        ["rq-photos", "Photographs of the completed setup with components identified (appendix of the PDF)"],
        ["rq-finalpid", "Final P&amp;ID block diagram submitted"],
        ["rq-q12", "Q1.2: runs at about 1, 3 and 6 L/min (or the measured maximum) compared with the theoretical velocity"],
        ["rq-q21", "Q2.1: flow at BV-02 25/50/70(75)/100% (plus 30 and 40%), table and graph"],
        ["rq-q22", "Q2.2: R², a, b, maximum and average calibration error"],
        ["rq-q23", "Q2.3: at least 5 flow conditions with pulses, time, frequency, volume and actual flow"],
        ["rq-q31", "Q3.1: residence time calculated, plus the four sub-answers"],
        ["rq-q32", "Q3.2: conditions A–E diagnosed; the hardest case and the extra information needed"],
        ["rq-p2", "Page 2 bullets: commissioned, characterised, FT-01 on the DAQ, valve effect analysed against time, 3 L/min held, graphs justify decisions"],
        ["rq-ids", "Team ID and team name on every page"],
    ]},
    {"title": "Laptop readiness (every laptop, before M1)", "items": [
        ["lp-driver", "USB driver installed (CP210x or CH340); the ESP32 shows up as a COM port"],
        ["lp-python", "Python 3.10+ and <code>pip install -r tools/requirements.txt</code> done"],
        ["lp-replay", "<code>rig_console.py --replay tools/samples/simulated_take_telemetry.csv</code> plays the simulated practice take"],
        ["lp-ide", "Arduino IDE 2 with esp32 core 2.0.17 (Boards Manager, pick that version; never 3.3 or later, whose touch driver changes the LSL-03 scale), board NodeMCU-32S; hold BOOT if upload stalls at “Connecting”"],
        ["lp-port", "Only one program holds the COM port: close the Serial Monitor before starting the console"],
        ["lp-power", "Sleep and screen saver off, charger in, notifications muted"],
        ["lp-obs", "OBS scene ready: camera plus the console window, test-recorded for 1 min"],
    ]},
    {"title": "Power-off check (kit sheet)", "items": [
        ["po-smps", "SMPS input wiring checked; PE bonded; terminal cover on"],
        ["po-mains", "No mains anywhere near the PCB"],
        ["po-pol", "12 V polarity at the PCB input checked with the DMM"],
        ["po-fuse", "Fuse F3 rating read and ≥ 15 A"],
        ["po-drv", "IBT-2 harness checked: GND, EN, PWM; VCC fed from 3V3"],
        ["po-sov", "D4184 wiring checked; flyback diode across the SOV coil"],
        ["po-ft", "FT-01 wiring and divider checked; signal ≤ 3.3 V"],
        ["po-float", "Float switch wiring checked; open = high"],
        ["po-gnd", "Common 0 V between the PCB and every IBT-2"],
        ["po-short", "No exposed conductors; loose wires tied; PCB in the drip tray on a raised board"],
    ]},
    {"title": "M1 bench bring-up", "items": [
        ["m1-float", "LS-01 connected (or FSW jumpered to GND) before any pump test: an open float input blocks P-01 and P-03"],
        ["m1-pins", "<code>PINS</code>: switch, float, ZSO and FT read correctly (G34 and G35 confirmed)"],
        ["m1-spin", "Each pump spins at 30%, pumping from IN to OUT"],
        ["m1-stagger", "Three pumps started together: no ESP32 reset"],
        ["m1-is", "IS gains g1–g3 calibrated against the DMM and saved"],
        ["m1-ft", "FT-01 output scoped; clean edges at G14; glitch count flat with pumps on"],
        ["m1-p1", "P-01 duty table filled in; d1 chosen and saved"],
        ["m1-touch", "LSL-03 probe reads clearly different in water and out of water (<code>PINS</code>)"],
    ]},
    {"title": "M2 hydraulic commissioning", "items": [
        ["m2-tags", "Every component tagged; flow arrows on every line"],
        ["m2-dip", "Dip tubes clipped at the rims and weighted"],
        ["m2-spool", "FT-01 horizontal, arrow along the flow, straight runs in place"],
        ["m2-leak1", "10 min at 3 L/min: no wet tissue anywhere"],
        ["m2-leak2", "2 min at BV-02 25%: no wet tissue anywhere"],
        ["m2-air", "No bubbles visible in the FT-01 spool"],
        ["m2-trip", "LS-01 trip volume measured on the scale"],
        ["m2-max", "Maximum loop flow recorded (duty map at 100%, BV-02 open)"],
        ["m2-p2map", "P-02 at 100% mapped against the BV-02 dial with IT-02; switch cycling noted; M2 checkpoint rule applied"],
        ["m2-is", "Every IS channel under 1,100 mV at the 30% dial point; clamp diodes fitted"],
    ]},
    {"title": "M3 calibration", "items": [
        ["m3-freeze", "FT-01 spool frozen: nothing moves near it from here"],
        ["m3-runs", "15 weighed runs entered in the workbench, each ≥ 1.5 kg; water temperature logged"],
        ["m3-timing", "Start-stop check at 3 L/min: one 180 s run against three 60 s runs agree within 0.5%"],
        ["m3-r2", "Maximum error ≤ 3% and repeats within ±1%; R² reported"],
        ["m3-set", "SET a, b, fcut, then SAVE"],
        ["m3-verify", "Verification at the exact Case 1 setting (d2 and BV-02 trim) within ±2% of the scale"],
    ]},
    {"title": "M4 and M5 acceptance", "items": [
        ["m4-r1", "Case 1 pass 1 (pour → P-01 stop ≤ 1.5 s → restart)"],
        ["m4-r2", "Case 1 pass 2"],
        ["m4-r3", "Case 1 pass 3"],
        ["m5-touch", "<code>TOUCHCAL EMPTY</code> done with the probe dry; i3dry set midway between wet and dry"],
        ["m5-r1", "Case 1 → Case 2 single go, pass 1"],
        ["m5-r2", "Single go, pass 2"],
        ["m5-r3", "Single go, pass 3; detection latency ≤ 1.0 s in the log"],
    ]},
    {"title": "M7 submission", "items": [
        ["m7-reh", "Three rehearsals done"],
        ["m7-take", "Single take recorded, with the console capture"],
        ["m7-video", "Challenge Video exported as MP4, 10:00–12:00 by the file's own duration, every component named, flow direction spoken"],
        ["m7-journey", "Journey Video exported as MP4, 3:00–4:00"],
        ["m7-photos", "Photos annotated with P&amp;ID tags, printed on the appendix pages"],
        ["m7-pid", "Final P&amp;ID drawn by hand on page 4"],
        ["m7-paper", "Every table and answer handwritten in blue or black ink with measured data; scanned to one PDF and read page by page"],
        ["m7-code", "Code package downloaded from the final revision (sheet 11), results filled in its README, link in the submission"],
        ["m7-check", "Second person checked everything against paper pages 1–3"],
        ["m7-up", "All three files uploaded on the portal by 16:00 (a saved submission cannot be changed)"],
    ]},
]

README = """# Hardware Hustle build kit

LAM Research Challenge 3.0, Stage 2. Firmware, bench tools and the printable P&ID.

## Bring-up order
1. Flash the bare ESP32 over USB, with no 12 V connected:
   - PlatformIO: `cd firmware/lam_flow_rig && pio run -t upload`
   - Arduino IDE 2: open `firmware/lam_flow_rig/lam_flow_rig.ino` (it compiles `src/main.cpp`; there is one copy
     of the code). Boards Manager: esp32 by Espressif, version 2.0.17. Board "NodeMCU-32S".
2. Start the console (step 4) or a serial monitor at 115200. The console prints `fw=1.1`. Type `PINS` and press the
   switch: `button` should read 0 while it is pressed. Close any serial monitor before starting the console.
3. Run the power-off checklist, then apply 12 V. `MANUAL`, then `P 1 30`, then `P 1 0`, and the same for pumps 2 and 3.
4. Start the console: `pip install -r tools/requirements.txt`, then `python tools/rig_console.py --port COM5`
   (on Linux: `/dev/ttyUSB0`). It logs to `runs/<stamp>_*.csv`, including the parameters in force (`_params.csv`).
   Type `SHOT` to save a screenshot; it also saves them after the float event, at the end of Case 1, with three
   pumps flushing, and at the automatic stop (`runs/<stamp>_shotNN_*.png`).

## Printables (print at 100%, no fit to page)
`print/tag_labels.svg` (equipment tags and flow-direction flags), `print/bv02_dial.svg` (valve position dial),
`print/pid.svg` (P&ID, A3).

## Daily commands
START / STOP / RESET · MANUAL · P n duty · SOV 0|1 · CAL seconds duty · FIC · SET key value · GET · SAVE ·
MARK text · TOUCHCAL EMPTY|WET · IZERO · ZERO · LEARN · BURST · PINS · NEXT (rehearsal only)

## Telemetry (10 Hz)
D,t_ms,state,q_lpm,q_mls,f_hz,v_tot_l,v_c1_l,v_c2_l,d1,d2,d3,i1_a,i2_a,i3_a,lsh,sov,zso,touch,diag,alarms,sp,ft_duty_pct,glitches
Events: E,t_ms,TAG,text.  Calibration: C,t_ms,run,pulses,time_s,f_hz,duty.

## Practice data
`tools/samples/simulated_take_*.csv` come from the simulator. Use them to practise `rig_console.py --replay`
and `analyze_run.py trend` before the rig is ready. They are not measurements: never put them in the video or the paper.

## Calibration certificate
`python tools/cal_fit.py runs/<stamp>_cal.csv --certificate ft01_certificate.pdf --team "<team>" --operator "<name>" --water-temp 24`

## Simulator (run after any firmware change)
From `firmware/lam_flow_rig`: `g++ -std=gnu++14 -O2 -Itest/mock test/sim_rig.cpp -o sim_rig && ./sim_rig`
(Linux, macOS, WSL or MinGW). It compiles the unchanged firmware against a tank model and plays the
single take plus four failure cases; every line must say PASS.

## Analysis
- `python tools/cal_fit.py runs/<stamp>_cal.csv --plot cal.png`: Q2.2/Q2.3 tables, R², errors, SET lines
- `python tools/analyze_run.py valve <telemetry> <events>`: Task 2 table and plots
- `python tools/analyze_run.py trend <telemetry> <events>`: flow (mL/s, L/min) and litres against time
- `python tools/analyze_run.py dutymap|step|burst ...`: FIC feed-forward, tuning, pulsation
- `python tools/theory.py --id 5.0 --measured 1.0 3.0 4.8`: Q1.2 and Q3.1 tables

Firmware 1.1 compiles without warnings on Arduino-ESP32 core 2.0.17 (PlatformIO espressif32 7.0.1, and arduino-cli
with the Arduino IDE layout) and on core 3.1.3.
"""

SHARE_README = """# Automated three-pump flow rig: controller and analysis code

LAM Research Challenge 3.0, Stage 2 (Hardware Hustle). Team [Team ID] · [Team name]

ESP32 firmware and laptop tools for our liquid-flow rig. Case 1 transfers process fluid with automatic sump level
protection and a calibrated, totalising flow measurement. Case 2 flushes the line through the equal tee and shuts the
system down by itself when the flush tank runs dry. All results were measured on the physical rig.

## Files
| Path | Contents |
|---|---|
| `firmware/lam_flow_rig/src/main.cpp` | The controller (C++, Arduino-ESP32 core 2.0.17; also builds on 3.1.3) |
| `firmware/lam_flow_rig/platformio.ini` | PlatformIO build: `pio run -t upload` |
| `firmware/lam_flow_rig/lam_flow_rig.ino` | Arduino IDE entry point; the IDE compiles `src/main.cpp` |
| `tools/rig_console.py` | Live trends in L/min and mL/s, CSV logging, commands, screenshots |
| `tools/cal_fit.py` | FT-01 calibration: Q = a·f + b by least squares, R², errors, uncertainty, certificate |
| `tools/analyze_run.py` | Valve position against flow, flow-time trends, step response, pulsation |
| `tools/theory.py` | Velocity, Reynolds number and residence-time calculations |
| `docs/` | P&ID, sequence state machine, power distribution |

## How the controller works
- **Scan cycle.** Inputs, interlocks and sequence logic run every 10 ms, flow every 100 ms, and telemetry streams
  at 10 Hz over USB. Wi-Fi stays off.
- **Flow measurement.** An interrupt timestamps every FT-01 pulse and rejects edges closer than 0.8 ms as noise.
  Frequency is computed reciprocally from real pulse timestamps over about 0.5 s, so there is no ±1-count
  quantisation. Flow is Q = a·f + b (our calibration), set to zero below the cutoff fcut. The totalisers add
  a·ΔN/60 + b·Δt/60 litres every 100 ms, so every pulse counts, for the whole run, Case 1 and Case 2.
- **Case 1.** One press of the on/off switch opens SOV-01, runs P-02 at 100% and P-01 at duty d1. When LS-01 reads
  high (debounced), P-01 stops and SOV-01 closes while P-02 keeps draining the sump. Once the level clears, P-01
  restarts by itself.
- **Case 2.** After Case 1, SOV-01 closes to isolate the 10 L tank and the LED asks the operator to open BV-01. Then
  P-01, P-02 and P-03 run together. The flush ends when the LSL-03 probe at the flush-tank pickup reads dry, or
  P-03's current shows it running dry, with a timeout as the last backstop. Every output then turns off and stays off.
- **Interlocks.** I-1: sump high or a broken float wire stops P-01 and P-03 and closes SOV-01; it can never be
  bypassed. I-2: P-03 runs only into a running P-01 with SOV-01 closed. I-3: SOV-01 stays closed while P-03 runs.
  I-4: P-02 trips on no-flow (dry running or a blocked discharge). At boot or brown-out every output starts low, and
  the normally closed SOV-01 shuts.
- **Diagnostics.** Flow, pump current and pump command are compared with a learned baseline to name the likely
  cause: restriction, blocked discharge, suction loss, pump failure, FT-01 signal failure or unstable flow. These are
  the conditions of Q3.2.
- **Commands.** START, STOP, MANUAL, P n duty, SOV 0/1, CAL seconds duty, FIC, SET / GET / SAVE, MARK, PINS.
  Parameters are stored in flash.

## Build and run
1. `cd firmware/lam_flow_rig && pio run -t upload`, or open `lam_flow_rig.ino` in the Arduino IDE (board NodeMCU-32S,
   esp32 core 2.0.17).
2. `pip install -r tools/requirements.txt`
3. `python tools/rig_console.py --port COM5` (Linux: `/dev/ttyUSB0`). Logs are written to `runs/`.
4. `python tools/cal_fit.py runs/<stamp>_cal.csv --plot cal.png`

## Results measured on our rig
- Calibration: a = ____ L/min per Hz, b = ____ L/min, R² = ____, maximum error ____ %, average error ____ %
- Case 1: mean flow ____ L/min over ____ min; P-01 stopped ____ s after LS-01 tripped
- Case 2: all pumps off ____ s after the flush tank ran dry
"""


def esc_attr(s):
    return s.replace('"', "&quot;")


def findings():
    out = []
    for f, d, srcs in C.FINDINGS:
        links = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' if u else t for t, u in srcs)
        out.append(f'    <div class="finding"><div>{f}</div><div class="arrow" aria-hidden="true">→</div>'
                   f'<div><span class="dec">{d}</span><span class="src">Source: {links}</span></div></div>')
    return "\n".join(out)


def milestones():
    out = []
    for m in C.MILESTONES:
        chips = f'<span class="chip{" crit" if m["crit"] else ""}">{"critical path" if m["crit"] else "off critical path"}</span>' \
                f'<span class="chip">owner {m["owner"]}</span><span class="chip">{m["when"]}</span>'
        rows = f'<dt>Do</dt><dd>{m["do"]}</dd><dt>Done when</dt><dd>{m["done"]}</dd>'
        if m.get("retires"):
            rows += f'<dt>Retires</dt><dd>{m["retires"]}</dd>'
        rows += f'<dt>Estimate</dt><dd>{m["est"]}</dd>'
        out.append(f'    <article class="ms"><header><span class="id">{m["id"]}</span><h3>{m["title"]}</h3></header>'
                   f'<div class="chips">{chips}</div><dl>{rows}</dl></article>')
    return "\n".join(out)


def runsheet():
    cells = ['<div class="hd">Lane</div>'] + [f'<div class="hd">{b}</div>' for b in C.BLOCKS]
    for lane, tasks in C.LANES:
        cells.append(f'<div class="lane">{lane}</div>')
        cells += [f"<div>{t}</div>" for t in tasks]
    return "\n".join("      " + c for c in cells)


def rows(data, num_cols=()):
    out = []
    for r in data:
        tds = "".join(f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>" for i, c in enumerate(r))
        out.append(f"        <tr>{tds}</tr>")
    return "\n".join(out)


def code_rows(data):
    return "\n".join(f"        <tr><td><code>{a}</code></td><td>{b}</td></tr>" for a, b in data)


def team():
    out = []
    for r in C.TEAM:
        owns = "".join(f'<li><a href="{a}">{t}</a></li>' for a, t in r["owns"])
        steps = "".join(f'<div class="citem"><input type="checkbox" id="c-{i}" data-chk="{i}"><label for="c-{i}">{t}</label>'
                        f'<span class="who"></span></div>' for i, t in r["first"])
        out.append(f'    <article class="role" id="role-{r["code"]}"><header><span class="id">{r["code"]}</span><h3>{r["role"]}</h3></header>'
                   f'<div class="field"><label for="rn-{r["code"]}">Name</label><input type="text" class="rolename" id="rn-{r["code"]}" '
                   f'data-role="{r["code"]}" placeholder="Who has this role?" autocomplete="off" maxlength="60"></div>'
                   f'<p class="fit">Best fit: {r["fit"]}</p><h4>Owns in this book</h4><ul>{owns}</ul>'
                   f'<h4>Milestones</h4><p>{r["ms"]}</p><h4>First steps · Fri 08–10</h4><div>{steps}</div>'
                   f'<h4>Hands over</h4><p>{r["hands"]}</p></article>')
    return "\n".join(out)


def bench():
    return "\n".join(f'        <tr><td>{what}</td><td class="small">{how}</td><td class="small">{when} · {who}</td>'
                     f'<td><input type="text" data-bench="{i}" aria-label="{esc_attr(what)}" maxlength="300" autocomplete="off"></td>'
                     f'<td class="who" data-bench-who="{i}"></td></tr>' for i, what, how, when, who in C.BENCH)


def build():
    os.makedirs(os.path.join(OUT, "kit"), exist_ok=True)
    tpl = open(os.path.join(HERE, "page_template.html"), encoding="utf-8").read()
    script = open(os.path.join(HERE, "page_script.js"), encoding="utf-8").read()
    script = script.replace("{{CHECKS}}", json.dumps(CHECKS, ensure_ascii=False))
    repl = {
        "{{REV}}": C.REV,
        "{{OBJECTIVE}}": C.OBJECTIVE,
        "{{DONE_WHEN}}": C.DONE_WHEN,
        "{{NOT_DOING}}": "\n".join(f"        <li>{x}</li>" for x in C.NOT_DOING),
        "{{CONSTRAINTS}}": "\n".join(f"        <li>{x}</li>" for x in C.CONSTRAINTS),
        "{{FINDINGS}}": findings(),
        "{{MILESTONES}}": milestones(),
        "{{RUNSHEET}}": runsheet(),
        "{{CHECKPOINTS}}": "\n".join(f"        <li>{c}</li>" for c in C.CHECKPOINTS),
        "{{TEAM_NOTE}}": C.TEAM_NOTE,
        "{{TEAM}}": team(),
        "{{ORG_MSG}}": html.escape(C.ORG_MSG),
        "{{ORG_MSG2}}": html.escape(C.ORG_MSG2),
        "{{JOURNEY}}": "\n".join(f"        <li>{x}</li>" for x in C.JOURNEY),
        "{{SUBMIT}}": "\n".join(f"        <li>{x}</li>" for x in C.SUBMIT),
        "{{PARTS}}": rows(C.PARTS, num_cols=(1,)),
        "{{PARTS_NOTE}}": C.PARTS_NOTE,
        "{{BENCH}}": bench(),
        "{{PID}}": D.pid(),
        "{{POWER}}": D.power(),
        "{{WIRING}}": D.wiring(),
        "{{GLOSSARY}}": "\n".join(f"        <tr><td><code>{a}</code></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in C.GLOSSARY),
        "{{COND}}": D.conditioning(),
        "{{STATES}}": D.states(),
        "{{LINELIST}}": rows(C.LINELIST),
        "{{IOLIST}}": "\n".join(f"        <tr><td><code>{a}</code></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>"
                                for a, b, c, d, e in C.IOLIST),
        "{{INTERLOCKS}}": rows(C.INTERLOCKS),
        "{{FDI}}": "\n".join(f"        <tr><td><code>{a}</code></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>"
                             for a, b, c, d, e, f in C.FDI),
        "{{COMMANDS}}": code_rows(C.COMMANDS),
        "{{PARAMS}}": "\n".join(f'        <tr><td><code>{a}</code></td><td class="num">{b}</td><td>{c}</td></tr>' for a, b, c in C.PARAMS),
        "{{Q32}}": rows(C.Q32),
        "{{STORY}}": rows(C.STORY),
        "{{OPENQ}}": rows(C.OPENQ),
        "{{LADDER}}": "\n".join(f"        <li><span>{x}</span></li>" for x in C.LADDER),
        "{{TRIGGERS}}": "\n".join(f"          <li>{x}</li>" for x in C.TRIGGERS),
        "{{CHANGELOG}}": rows(C.CHANGELOG),
        "{{FITTINGS}}": rows(C.FITTINGS),
        "{{FIRSTWATER}}": "\n".join(f"      <li>{x}</li>" for x in C.FIRSTWATER),
        "{{RESET}}": "\n".join(f"        <li>{x}</li>" for x in C.RESET),
        "{{RUNSCRIPT}}": rows(C.RUNSCRIPT),
        "{{ABORT}}": C.ABORT,
        "{{WIN_SOURCES}}": " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in C.WIN_SOURCES),
        "{{WIN_PILLARS}}": rows(C.WIN_PILLARS),
        "{{WIN_LOSE}}": "\n".join(f"        <li>{x}</li>" for x in C.WIN_LOSE),
        "{{WIN_VOCAB}}": rows(C.WIN_VOCAB),
        "{{FINALE}}": "\n".join(f"      <li>{x}</li>" for x in C.FINALE),
        "{{DECISIONS}}": rows(C.DECISIONS),
        "{{Q2TEXT}}": "\n".join(f"      <dt>{a}</dt><dd>{b}</dd>" for a, b in C.Q2TEXT),
        "{{SIMRESULTS}}": "\n".join(f'        <tr><td>{a}</td><td>{b}</td><td><span class="pill ok">{c}</span></td></tr>' for a, b, c in C.SIMRESULTS),
        "{{SCRIPT}}": script,
    }
    for k, v in repl.items():
        assert k in tpl, k
        tpl = tpl.replace(k, v)
    assert "{{" not in tpl, tpl[tpl.index("{{"):tpl.index("{{") + 40]
    page = os.path.join(OUT, "hardware_hustle_build_book.html")
    open(page, "w", encoding="utf-8").write(tpl)

    pid_svg = D.standalone(D.pid(), "LAM Stage 2 rig P&ID")
    open(os.path.join(OUT, "kit", "pid.svg"), "w", encoding="utf-8").write(pid_svg)

    kit = os.path.join(OUT, "kit")
    fw = os.path.join(ROOT, "firmware", "lam_flow_rig")
    files = {  # archive path -> (published name, content)
        "README.md": ("README.md", README),
        "firmware/lam_flow_rig/platformio.ini": ("platformio.ini.txt", open(os.path.join(fw, "platformio.ini")).read()),
        "firmware/lam_flow_rig/src/main.cpp": ("main.cpp.txt", open(os.path.join(fw, "src", "main.cpp")).read()),
        "firmware/lam_flow_rig/lam_flow_rig.ino": ("lam_flow_rig.ino.txt", open(os.path.join(fw, "lam_flow_rig.ino")).read()),
        "tools/requirements.txt": ("requirements.txt", "pyserial>=3.5\nmatplotlib>=3.6\nnumpy>=1.24\n"),
        "templates/cal_runs.csv": ("cal_runs.csv", "run,pulses,time_s,f_hz,duty,mass_g,note\n"),
        "print/pid.svg": ("pid.svg", pid_svg),
        "print/wiring.svg": ("wiring.svg", D.standalone(D.wiring(), "Firmware connection diagram E-01")),
        "print/tag_labels.svg": ("tag_labels.svg", D.labels_sheet(C.TAGS, C.LINEFLAGS)),
        "print/bv02_dial.svg": ("bv02_dial.svg", D.dial_sheet()),
        "docs/power.svg": ("power.svg", D.standalone(D.power(), "Power distribution")),
        "docs/states.svg": ("states.svg", D.standalone(D.states(), "Sequence state machine")),
    }
    for t in ("rig_console.py", "cal_fit.py", "analyze_run.py", "theory.py"):
        files[f"tools/{t}"] = (f"{t}.txt", open(os.path.join(ROOT, "tools", t)).read())
    for smp in ("simulated_take_telemetry.csv", "simulated_take_events.csv"):
        files[f"tools/samples/{smp}"] = (smp, open(os.path.join(ROOT, "tools", "samples", smp)).read())
    tdir = os.path.join(fw, "test")
    files["firmware/lam_flow_rig/test/sim_rig.cpp"] = ("sim_rig.cpp.txt", open(os.path.join(tdir, "sim_rig.cpp")).read())
    for h in ("Arduino.h", "Preferences.h", "esp_arduino_version.h", "esp_system.h", "esp_timer.h"):
        files[f"firmware/lam_flow_rig/test/mock/{h}"] = (f"mock_{h}.txt", open(os.path.join(tdir, "mock", h)).read())
    files["firmware/lam_flow_rig/test/mock/soc/gpio_reg.h"] = ("mock_gpio_reg.h.txt", open(os.path.join(tdir, "mock", "soc", "gpio_reg.h")).read())
    manifest = {}
    for arc, (pub, text) in files.items():
        manifest[arc] = "kit/" + pub
        if text is not None:
            open(os.path.join(kit, pub), "w", encoding="utf-8").write(text)
    json.dump(manifest, open(os.path.join(kit, "manifest.json"), "w"), indent=1)

    open(os.path.join(kit, "SHARE_README.md"), "w", encoding="utf-8").write(SHARE_README)
    share = {"README.md": "kit/SHARE_README.md", "docs/pid.svg": "kit/pid.svg", "docs/states.svg": "kit/states.svg",
             "docs/power.svg": "kit/power.svg", "docs/wiring.svg": "kit/wiring.svg"}
    for arc in ("firmware/lam_flow_rig/src/main.cpp", "firmware/lam_flow_rig/platformio.ini",
                "firmware/lam_flow_rig/lam_flow_rig.ino", "tools/requirements.txt", "tools/rig_console.py",
                "tools/cal_fit.py", "tools/analyze_run.py", "tools/theory.py"):
        share[arc] = manifest[arc]
    json.dump(share, open(os.path.join(kit, "share_manifest.json"), "w"), indent=1)

    for name, man in (("hh-build-kit.zip", manifest), ("lam-flow-rig-code.zip", share)):  # local copies; not published
        zpath = os.path.join(kit, name)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for arc, pub in man.items():
                z.write(os.path.join(OUT, pub), arc)
        print("zip :", len(man), "files;", zpath, f"{os.path.getsize(zpath) / 1024:.0f} KB")
    print("page:", page, f"{os.path.getsize(page) / 1024:.0f} KB")


def md(html):
    t = re.sub(r"<code>(.*?)</code>", r"`\1`", html)
    t = re.sub(r"<strong>(.*?)</strong>", r"**\1**", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def export_markdown():
    L = [f"# LAM Stage 2 flow rig: roadmap (rev {C.REV})", "",
         f"**Objective:** {md(C.OBJECTIVE)}", f"**Done when:** {md(C.DONE_WHEN)}",
         "**Not doing:** " + " ".join(f"({i + 1}) {md(x)}" for i, x in enumerate(C.NOT_DOING)),
         "**Constraints:** " + " ".join(md(x) for x in C.CONSTRAINTS), "", "---", "", "## Ground truth", ""]
    for f, d, _ in C.FINDINGS:
        L.append(f"- {md(f)} → {md(d)}")
    L += ["", "---", "", "## Critical path", "",
          "Roughly 2.5 days. M1 → M2 → M3 → M4 → M5 → M7; M6 runs alongside and can slip.", ""]
    for m in C.MILESTONES:
        L += [f"### {m['id']} — {md(m['title'])}  ({m['owner']}, {m['when']})",
              f"- **Do:** {md(m['do'])}", f"- **Done when:** {md(m['done'])}"]
        if m.get("retires"):
            L.append(f"- **Retires:** {md(m['retires'])}")
        L += [f"- **Est:** {m['est']}", ""]
    L += ["---", "", "## Team", "", md(C.TEAM_NOTE), ""]
    for r in C.TEAM:
        L += [f"### {r['code']} · {r['role']}", f"- **Owns:** " + "; ".join(md(t) for _, t in r["owns"]),
              f"- **Milestones:** {md(r['ms'])}", "- **First steps (Fri 08–10):**"]
        L += [f"  - [ ] {md(t)}" for _, t in r["first"]]
        L += [f"- **Hands over:** {md(r['hands'])}", ""]
    L += ["---", "", "## Parallel & lead-time", "", "**Buy today:**"]
    L += [f"- {md(a)} × {b}: {md(c)} ({md(d)})" for a, b, c, d in C.PARTS] + ["", md(C.PARTS_NOTE), "",
          "**Organiser message:**", "", "```", C.ORG_MSG, "```", "",
          "**Follow-up message (Rev F):**", "", "```", C.ORG_MSG2, "```"]
    L += ["", "**Off critical path:** M6 (evidence pack): fault demos, FIC, burst, dye transit.",
          "**Contention:** one rig and one scale. Book rig time in the run sheet; batch the scale work.", "",
          "## Checkpoints", ""] + [f"- {md(x)}" for x in C.CHECKPOINTS]
    L += ["", "## Open questions", "", "| Question | Resolved by | When | If bad |", "|---|---|---|---|"]
    L += [f"| {md(a)} | {md(b)} | {c} | {md(d)} |" for a, b, c, d in C.OPENQ]
    L += ["", "## Descope ladder", ""] + [f"{i + 1}. {md(x)}" for i, x in enumerate(C.LADDER)]
    L += ["", "**Floor:** Case 1 and Case 2 automated to spec, FT-01 calibrated (Q = af + b, R²), P&ID, 10–12 min Challenge Video, 3–4 min Journey Video, handwritten paper.",
          "**Kill rule:** if Case 1 is not passing by Sat 14:00, stop every extra until it does.", "",
          "## Replan triggers", ""] + [f"- {md(x)}" for x in C.TRIGGERS]
    L += ["", "## Changelog", ""] + [f"- Rev {a}: {md(c)}" for a, b, c in C.CHANGELOG]
    path = os.path.join(HERE, "ROADMAP.md")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("md  :", path)


ARTIFACT_URL = "https://claude.ai/artifact/GDvmoMtX1gnrWGFqVeGuy9"

PLAN_PREAMBLE = """# LAM Stage 2 (Hardware Hustle): full build plan

Generated {stamp} by `plan/build_page.py` from build book Rev {rev}. Do not edit this file by hand. Edit
`plan/content.py` (data), `plan/page_template.html` (static text) or `plan/diagrams.py`, then run
`python plan/build_page.py`, which rebuilds the page, the kit, `plan/ROADMAP.md` and this file.

## Quick context for a new session
- **Task:** LAM Research Challenge 3.0, Stage 2 "Hardware Hustle". Build an ESP32-automated three-pump flow rig
  from the kit; upload on the LRC portal a 10–12 min Challenge Video (MP4), a 3–4 min Journey Video (MP4) and the
  handwritten paper scanned to one PDF (with the P&ID, photos, plots and code link inside). Upload by
  Sun 4 Oct 2026 18:00 IST (team target 16:00). 25 of 50 teams advance to an offline Grand Finale.
- **Hard rule:** real data only ("no simulations, no shortcuts"). The simulator is a firmware test tool and its
  output must never appear in the video, photos or paper.
- **Inputs:** the question paper (`1790306239938-STAGE_2_Question_Paper_Lam_Research_Challenge_3.0.pdf`) and kit photos
  (`WhatsApp Image 2026-10-01 at *.jpeg`) sit next to this file.
- **Live build book:** {url} (private; the owner shares it with the team). Its database holds the team's real data;
  read it with the ArtifactData tool before tuning anything: `bench` (bench readings, ids `b-*`), `cal_runs`
  (weighed calibration runs), `checks` (ticks; first steps are `fs-*`), `team` (names on the four roles).
- **Republish after a rebuild:** Artifact publish with `url` = the link above, `file_path` =
  `plan/out/hardware_hustle_build_book.html`, and `files` = every file in `plan/out/kit/` except the `.zip` files and
  `sample_take_*`, each published as `kit/<name>`. Omit `capabilities` (db, user with profile scope, downloads carry over).
- **After any firmware change:** `pio run` in `firmware/lam_flow_rig` (zero warnings), then the simulator
  (`g++ -std=gnu++14 -O2 -Itest/mock test/sim_rig.cpp -o sim_rig && ./sim_rig` must print ALL PASS), then rebuild
  and republish so the kit and the judges' code package carry the new firmware.

## File map
| Path | What it is |
|---|---|
| `firmware/lam_flow_rig/src/main.cpp` | The controller (single source; firmware {fw}) |
| `firmware/lam_flow_rig/platformio.ini`, `lam_flow_rig.ino` | PlatformIO build; Arduino IDE entry stub (core 2.0.17) |
| `firmware/lam_flow_rig/test/` | Software-in-the-loop simulator and mock headers (never evidence) |
| `tools/rig_console.py` | Live trends, logging to `runs/`, commands, screenshots |
| `tools/cal_fit.py`, `analyze_run.py`, `theory.py` | Calibration fit and certificate; valve, trend, duty-map, step and burst plots; Q1.2/Q3.1 tables |
| `tools/samples/` | Simulated practice take (practice only) |
| `plan/content.py`, `page_template.html`, `page_script.js`, `diagrams.py` | Build-book sources |
| `plan/build_page.py`, `plan/export_plan_md.py` | Build the page, kit, zips, ROADMAP.md and this file |
| `plan/out/` | Built page; `kit/` holds the published kit files and the local zips |
"""


def fw_version():
    m = re.search(r'FW_VERSION = "([^"]+)"', open(os.path.join(ROOT, "firmware", "lam_flow_rig", "src", "main.cpp")).read())
    return m.group(1) if m else "?"


def export_plan():
    page = open(os.path.join(OUT, "hardware_hustle_build_book.html"), encoding="utf-8").read()
    pre = PLAN_PREAMBLE.format(stamp=X.stamp(), rev=C.REV, url=ARTIFACT_URL, fw=fw_version())
    path = os.path.join(ROOT, "BUILD_PLAN.md")
    text = X.write(page, CHECKS, path, pre, {"velocity": X.velocity_table(os.path.join(ROOT, "tools"))})
    print("plan:", path, f"{len(text) / 1024:.0f} KB")


if __name__ == "__main__":
    build()
    export_markdown()
    export_plan()
