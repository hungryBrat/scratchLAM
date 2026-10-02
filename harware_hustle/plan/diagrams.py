#!/usr/bin/env python3
"""Generates the engineering diagrams for the build book.

Each function returns inline SVG that is styled by the page CSS (theme-aware). `standalone()`
wraps a diagram with its own print stylesheet for a black-on-white file.
"""

FONT = "'JetBrains Mono', ui-monospace, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, cls="t", anchor="middle"):
        self.add(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>')

    def line(self, pts, cls="ln"):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.add(f'<path d="{d}" class="{cls}"/>')

    def arrow(self, x, y, direction, cls="fa"):
        s = 6
        p = {
            "r": f"M{x - s},{y - 5} L{x + s},{y} L{x - s},{y + 5} Z",
            "l": f"M{x + s},{y - 5} L{x - s},{y} L{x + s},{y + 5} Z",
            "u": f"M{x - 5},{y + s} L{x},{y - s} L{x + 5},{y + s} Z",
            "d": f"M{x - 5},{y - s} L{x},{y + s} L{x + 5},{y - s} Z",
        }[direction]
        self.add(f'<path d="{p}" class="{cls}"/>')

    def tank(self, x0, x1, top, bot, liquid, tag, sub, note=None, lx=None):
        self.add(f'<rect x="{x0}" y="{liquid}" width="{x1 - x0}" height="{bot - liquid}" class="liq"/>')
        self.add(f'<path d="M{x0},{top} V{bot} H{x1} V{top}" class="eq"/>')
        self.add(f'<path d="M{x0 - 8},{top} H{x0 + 8} M{x1 - 8},{top} H{x1 + 8}" class="eq"/>')
        cx = lx if lx is not None else (x0 + x1) / 2
        ty = liquid + (bot - liquid) / 2 - 4
        self.text(cx, ty, tag, "tb")
        self.text(cx, ty + 17, sub, "ts")
        if note:
            self.text(cx, ty + 32, note, "ts")

    def valve(self, cx, cy, tag, under=None, hand=True, actuator=None, horizontal=True):
        self.add(f'<path d="M{cx - 16},{cy - 11} L{cx},{cy} L{cx - 16},{cy + 11} Z M{cx + 16},{cy - 11} L{cx},{cy} '
                 f'L{cx + 16},{cy + 11} Z" class="vlv"/>')
        if hand:
            self.add(f'<path d="M{cx},{cy} V{cy - 18} M{cx - 10},{cy - 18} H{cx + 10}" class="eq"/>')
        if actuator:
            self.add(f'<path d="M{cx},{cy} V{cy - 26}" class="eq"/>')
            self.add(f'<rect x="{cx - 12}" y="{cy - 46}" width="24" height="20" class="box"/>')
            self.text(cx, cy - 31.5, "S", "tb")
        ty = cy - (56 if actuator else 26)
        self.text(cx, ty, tag, "tb")
        if under:
            self.text(cx, cy + 27, under, "ts")

    def pump(self, cx, cy, tag, sub, flow="r"):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="26" class="eq pumpfill"/>')
        if flow == "r":
            self.add(f'<path d="M{cx - 8},{cy - 11} L{cx + 12},{cy} L{cx - 8},{cy + 11} Z" class="fa"/>')
        else:
            self.add(f'<path d="M{cx + 8},{cy - 11} L{cx - 12},{cy} L{cx + 8},{cy + 11} Z" class="fa"/>')
        self.text(cx, cy + 45, tag, "tb")
        self.text(cx, cy + 61, sub, "ts")

    def bubble(self, cx, cy, top, num, io=None, io_side="r", r=19):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="bub"/>')
        self.add(f'<path d="M{cx - r},{cy} H{cx + r}" class="eq thin"/>')
        self.text(cx, cy - 4, top, "tbub")
        self.text(cx, cy + 13, num, "tbub")
        if io:
            if io_side == "r":
                self.text(cx + r + 5, cy + 4, io, "io", "start")
            elif io_side == "l":
                self.text(cx - r - 5, cy + 4, io, "io", "end")
            else:
                self.text(cx, cy + r + 14, io, "io")

    def render(self, cls="diagram"):
        body = "\n".join(self.parts)
        return (f'<svg class="{cls}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.label)}" '
                f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')


def pid():
    s = Svg(1280, 780, "P&ID: TK-01 feeds P-01 through SOV-01 and the equal tee into the sump TK-02; P-02 returns sump "
                       "fluid through BV-02 and FT-01 to TK-01; the flush tank TK-03 joins at the tee through BV-01 and P-03.")
    # tanks
    s.tank(70, 250, 120, 300, 175, "TK-01", "Process tank · 10 L", "on +0.3 m stand", lx=172)
    s.tank(980, 1160, 400, 600, 470, "TK-02", "Sump · 4.2 L")
    s.tank(70, 230, 480, 650, 520, "TK-03", "Flush tank · 4.2 L", "on +0.3 m stand", lx=162)

    # L-101 process suction: TK-01 dip tube -> SOV-01 -> TEE-01 -> P-01
    s.line([(88, 290), (88, 96), (40, 96), (40, 380), (164, 380)])
    s.line([(196, 380), (519, 380)])
    s.arrow(40, 240, "d")
    s.arrow(100, 380, "r")
    s.arrow(250, 380, "r")
    s.text(320, 372, "L-101 · 8×5 PU", "ts")
    s.valve(180, 380, "SOV-01", "NC · fail-closed", hand=False, actuator=True)
    s.text(200, 344, "G27", "io", "start")
    s.add('<circle cx="440" cy="380" r="5" class="dot"/>')
    s.text(452, 400, "TEE-01", "ts", "start")
    s.pump(545, 380, "P-01", "diaphragm · d1", "r")
    s.bubble(545, 318, "IT", "01", "G15")
    s.line([(545, 337), (545, 354)], "sig")

    # L-102 P-01 -> sump
    s.line([(571, 380), (1030, 380), (1030, 445)])
    s.arrow(800, 380, "r")
    s.arrow(1030, 425, "d")
    s.text(800, 372, "L-102 · 8×5 PU", "ts")

    # LS-01
    s.add('<path d="M1160,450 H1140" class="eq"/><circle cx="1133" cy="450" r="6" class="eq pumpfill"/>')
    s.line([(1160, 450), (1196, 450)], "sig")
    s.bubble(1216, 450, "LSH", "01", "G35", "b")
    s.text(1216, 500, "open = high", "ts")
    s.text(1216, 514, "fail-safe", "ts")

    # L-201 sump outlet -> BV-03 -> P-02 -> BV-02 -> FT-01 -> L-202 return
    s.line([(1120, 588), (1120, 250), (1076, 250)])
    s.arrow(1120, 330, "u")
    s.valve(1060, 250, "BV-03", "NO · isolation")
    s.line([(1044, 250), (976, 250)])
    s.arrow(1010, 250, "l")
    s.pump(950, 250, "P-02", "diaphragm · d2 = 100%", "l")
    s.bubble(950, 186, "IT", "02", "G36")
    s.line([(950, 205), (950, 224)], "sig")
    s.line([(924, 250), (836, 250)])
    s.arrow(880, 250, "l")
    s.valve(820, 250, "BV-02", "throttle · 0–90° dial")
    s.line([(804, 250), (716, 250)])
    s.arrow(760, 250, "l")
    s.add('<rect x="644" y="238" width="72" height="24" rx="3" class="box"/>')
    s.add('<circle cx="680" cy="250" r="7" class="eq thin"/><path d="M673,250 H687 M680,243 V257" class="eq thin"/>')
    s.line([(680, 238), (680, 214)], "eq")
    s.bubble(680, 194, "FT", "01", "G14 · ISR")
    s.text(680, 280, "≥10D in · ≥5D out", "ts")
    s.line([(644, 250), (330, 250), (330, 60), (200, 60), (200, 140)])
    s.arrow(480, 250, "l")
    s.arrow(330, 150, "u")
    s.arrow(265, 60, "l")
    s.arrow(200, 110, "d")
    s.text(480, 242, "L-202 return · 8×5 PU", "ts")
    s.text(265, 52, "free discharge above liquid", "ts")

    # L-301 flush: TK-03 -> BV-01 -> P-03 -> TEE-01
    s.line([(88, 640), (88, 460), (264, 460)])
    s.arrow(88, 560, "u")
    s.valve(280, 460, "", None)
    s.text(280, 492, "BV-01", "tb")
    s.text(280, 508, "manual", "ts")
    s.bubble(280, 400, "ZSO", "01", "G5", "l")
    s.line([(280, 419), (280, 442)], "sig")
    s.line([(296, 460), (354, 460)])
    s.pump(380, 460, "P-03", "diaphragm · d3", "r")
    s.bubble(380, 398, "IT", "03", "G39", "l")
    s.line([(380, 417), (380, 434)], "sig")
    s.line([(406, 460), (440, 460), (440, 385)])
    s.arrow(440, 425, "u")
    s.text(468, 470, "L-301", "ts", "start")

    # LSL-03 probe at the dip-tube inlet
    s.add('<circle cx="96" cy="634" r="4" class="probe"/>')
    s.line([(100, 634), (262, 634)], "sig")
    s.bubble(282, 634, "LSL", "03", "T0 · G4", "b")
    s.text(282, 682, "probe at dip-tube inlet", "ts")

    # controller block
    s.add('<rect x="380" y="548" width="440" height="200" rx="6" class="box"/>')
    s.text(600, 572, "UC-01 · ESP32 NodeMCU-32S (basic process control)", "tb")
    rows = [
        ("FQI-01", "Q = a·f + b, mL/s and L/min, totalised litres"),
        ("UY-01", "sequence: Case 1 → Case 2 → safe OFF"),
        ("FIC-01", "P-02 flow PI loop (optional mode)"),
        ("I-1", "LSH-01 high: stop P-01 + P-03, close SOV-01"),
        ("I-2", "P-03 only into running P-01, SOV-01 closed"),
        ("I-3", "SOV-01 held closed while P-03 runs"),
        ("I-4", "P-02 trip: dry run or blocked discharge"),
        ("HS-01", "start / stop switch on G34"),
    ]
    for k, (tag, desc) in enumerate(rows):
        y = 596 + k * 19
        s.text(396, y, tag, "io", "start")
        s.text(460, y, desc, "t", "start")

    # notes and legend
    notes = [
        "NOTES",
        "1  Dip tubes enter from the top; only LS-01 pierces a wall.",
        "2  FT-01 after BV-02: never sees the 8.25 bar cut-off.",
        "   (FT-01 rated 0.8 MPa)",
        "3  TK-01, TK-03 raised ~0.3 m: flooded pump suction.",
        "4  8×5 PU lines; 10×8 PU stubs at pump ports.",
        "5  BV-02 is the throttling (needle) valve: the kit has none.",
    ]
    for k, n in enumerate(notes):
        s.text(850, 636 + k * 19, n, "tb" if k == 0 else "t", "start")
    s.line([(40, 712), (90, 712)])
    s.text(98, 716, "process line, arrow = flow", "t", "start")
    s.line([(40, 736), (90, 736)], "sig")
    s.text(98, 740, "electrical signal", "t", "start")
    s.text(40, 762, "G14 = ESP32 GPIO wired to that instrument", "io", "start")
    return s.render("diagram pid")


def power():
    s = Svg(1180, 430, "Power distribution: mains reaches only the SMPS; 12 V enters the PCB through fuse F3 and the TVS, "
                       "feeds P1-P3 to the three IBT-2 drivers and P4 to the D4184 valve driver; the LM2596 makes 5 V.")

    def blk(x, y, w, h, title, sub=None, cls="box"):
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="{cls}"/>')
        s.text(x + w / 2, y + h / 2 - (6 if sub else -4), title, "tb")
        if sub:
            s.text(x + w / 2, y + h / 2 + 12, sub, "ts")

    def wire(pts):
        s.line(pts, "pw")
        x, y = pts[-1]
        px, py = pts[-2]
        d = "r" if x > px else "l" if x < px else ("d" if y > py else "u")
        off = {"r": (-6, 0), "l": (6, 0), "d": (0, -6), "u": (0, 6)}[d]
        s.arrow(x + off[0], y + off[1], d, "pa")

    blk(20, 30, 150, 52, "230 V AC mains", "3-core cord, PE bonded", "box hot")
    blk(20, 150, 150, 64, "SMPS", "12 V · 29 A")
    wire([(95, 82), (95, 150)])
    s.text(103, 120, "L · N · PE only here", "ts", "start")
    blk(280, 140, 240, 84, "PCB 12V INPUT", "fuse F3 ≥ 15 A · TVS · 1000 µF")
    wire([(170, 182), (280, 182)])
    s.text(225, 174, "16 AWG red/black", "ts")
    blk(580, 30, 150, 52, "P1 · P2 · P3", "12 V + 470 µF each")
    blk(580, 160, 150, 52, "P4 / P5", "12 V aux")
    blk(580, 290, 150, 52, "LM2596 buck", "5 V rail (VCC)")
    wire([(520, 160), (550, 160), (550, 56), (580, 56)])
    wire([(520, 186), (580, 186)])
    wire([(520, 210), (550, 210), (550, 316), (580, 316)])
    blk(790, 20, 170, 72, "IBT-2 × 3", "B+/B− 18 AWG from P1–P3")
    wire([(730, 56), (790, 56)])
    blk(1010, 20, 160, 72, "P-01 · P-02 · P-03", "M+/M− · 2.5–3.5 A each")
    wire([(960, 56), (1010, 56)])
    blk(790, 150, 170, 72, "D4184 MOSFET", "flyback diode on coil")
    wire([(730, 186), (790, 186)])
    blk(1010, 150, 160, 72, "SOV-01 coil", "12 V, normally closed")
    wire([(960, 186), (1010, 186)])
    blk(790, 280, 170, 72, "ESP32 5V pin", "on-board 3.3 V LDO")
    wire([(730, 316), (790, 316)])
    blk(1010, 280, 160, 72, "FT-01 red wire", "YF-S401 5 V supply")
    wire([(960, 316), (1010, 316)])
    s.text(875, 372, "3V3 → IBT-2 VCC (logic) ×3", "io")
    s.text(590, 410, "Starts are staggered ≥ 500 ms and ramped, so three pumps never draw inrush at once.", "t")
    return s.render("diagram power")


def wiring():
    """Every connection the firmware relies on: ESP32 pin -> PCB connector or add-on pad -> module -> rig device."""
    W = 1120
    s = Svg(W, 100, "Firmware connection diagram: each ESP32 GPIO used by the firmware, the PCB connector pin or "
                    "add-on-board pad it goes through, the interface module, and the device on the rig it drives or reads.")
    E0, E1, C0, C1, M0, M1, F0, F1 = 20, 250, 380, 530, 620, 800, 900, 1100
    zones, esp_rows = [], []

    def hop(x0, x1, y, d, cls="wire"):
        s.line([(x0, y), (x1, y)], cls)
        if cls != "gnd":
            s.arrow(x1 - 6 if d == "r" else x0 + 6, y, d, "pa" if cls == "pw" else "ta")

    def esp(y, gpio, role, pin):
        esp_rows.append((y, gpio, role, pin))

    def box(x0, x1, y0, y1, header=None, hcls="tb"):
        s.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="4" class="box"/>')
        if header:
            s.text((x0 + x1) / 2, y0 + 14, header, hcls)

    def pins(x, ys, labels, cls="t", anchor="start"):
        for y, lab in zip(ys, labels):
            if lab:
                s.text(x, y + 4, lab, cls, anchor)

    def field(ys, tag, subs):
        s.add(f'<rect x="{F0}" y="{ys[0] - 12}" width="{F1 - F0}" height="{ys[-1] - ys[0] + 24}" rx="4" class="box"/>')
        s.text(F0 + 10, ys[0] + 4, tag, "tb", "start")
        for y, sub in zip(ys[1:], subs):
            s.text(F0 + 10, y + 4, sub, "ts", "start")

    def band(T, bottom, title, shade):
        if shade:
            zones.append(f'<rect x="0" y="{T}" width="{W}" height="{bottom - T}" class="zone"/>')
        s.text(262, T + 16, title, "tb", "start")

    # column heads and legend
    for cx, head, sub in ((135, "U7 · ESP32 NodeMCU-32S", "GPIO · firmware role · socket pin"),
                          (455, "PCB connector", "or add-on board pad"),
                          (710, "Interface module", "driver or signal conditioning"),
                          (1000, "Device on the rig", "P&ID tag")):
        s.text(cx, 20, head, "tb")
        s.text(cx, 36, sub, "ts")
    ly = 56
    hop(380, 420, ly, "r")
    s.text(428, ly + 4, "signal, arrow = direction", "ts", "start")
    hop(600, 640, ly, "r", "pw")
    s.text(648, ly + 4, "power", "ts", "start")
    hop(700, 740, ly, "r", "gnd")
    s.text(748, ly + 4, "0 V (GND)", "ts", "start")
    s.text(840, ly + 4, "G14 = GPIO 14 · pin = U7 socket pin", "ts", "start")

    T = 72
    pumps = [
        (1, "U2", ("G33", "G32", "G26", "G13"), ("8", "7", "10", "15"), ("G15", "23", "IS1 · ADC2, Wi-Fi off"),
         "P-01 · transfer pump, TK-01 → sump", ("12 V diaphragm pump", "speed = duty d1")),
        (2, "U3", ("G19", "G18", "G17", "G16"), ("31", "30", "28", "27"), ("G36", "3", "IS2 · ADC1"),
         "P-02 · return pump, sump → FT-01 → TK-01", ("12 V diaphragm pump", "speed = duty d2")),
        (3, "U4", ("G25", "G23", "G22", "G21"), ("9", "37", "36", "33"), ("G39", "4", "IS3 · ADC1"),
         "P-03 · flush pump, TK-03 → tee", ("12 V diaphragm pump", "speed = duty d3")),
    ]
    for i, (n, hdr, gp, pn, (isg, ispin, isrole), title, subs) in enumerate(pumps):
        ys = [T + 52 + 20 * k for k in range(6)] + [T + 182]
        bottom = ys[6] + 22
        band(T, bottom, title, i % 2 == 0)
        roles = (f"R_PWM{n} · PWM 20 kHz", f"L_PWM{n} · held LOW", f"R_EN{n} · HIGH = run", f"L_EN{n} · HIGH = run")
        for k in range(4):
            esp(ys[k], gp[k], roles[k], pn[k])
            hop(E1, C0, ys[k], "r")
            hop(C1, M0, ys[k], "r")
        esp(ys[6], isg, isrole, ispin)
        box(C0, C1, T + 24, ys[5] + 12, f"{hdr} · 6-pin XH")
        pins(C0 + 8, ys[:6], (f"6  R_PWM{n}", f"5  L_PWM{n}", f"4  R_EN{n}", f"3  L_EN{n}", "2  GND", "1  VCC 5 V · open"))
        hop(C1, M0, ys[4], "r", "gnd")
        s.line([(572, ys[5]), (M0, ys[5])], "pw")
        s.arrow(M0 - 6, ys[5], "r", "pa")
        s.text(566, ys[5] + 4, "3V3", "pwt", "end")
        box(C0, C1, ys[6] - 13, ys[6] + 13)
        s.text((C0 + C1) / 2, ys[6] + 4, "add-on 10k/100n/BAT85", "ts")
        hop(C1, M0, ys[6], "l")
        hop(E1, C0, ys[6], "l")
        box(M0, M1, T + 24, ys[6] + 13, f"IBT-2 #{n}")
        pins(M0 + 8, ys, ("1  RPWM", "2  LPWM", "3  R_EN", "4  L_EN", "8  GND", "7  VCC", "5+6  IS, 3.3 kΩ to GND"))
        s.text(M1 - 8, ys[1] + 4, "M+ M−", "t", "end")
        s.text(M1 - 8, ys[4] + 4, f"B+ B− ← P{n} 12 V", "pwt", "end")
        hop(M1, F0, ys[1], "r")
        field(ys[:3], f"P-0{n}", subs)
        T = bottom

    # SOV-01
    ys = [T + 52 + 20 * k for k in range(3)]
    bottom = ys[2] + 22
    band(T, bottom, "SOV-01 · on/off valve on P-01 suction", True)
    esp(ys[0], "G27", "SOV · HIGH = open", "11")
    hop(E1, C0, ys[0], "r")
    box(C0, C1, T + 24, ys[2] + 12, "SOLENOID_VALVE")
    pins(C0 + 8, ys, ("1  SV", "2  V · 5 V", "3  G · GND"))
    hop(C1, M0, ys[0], "r")
    hop(C1, M0, ys[1], "r", "pw")
    hop(C1, M0, ys[2], "r", "gnd")
    box(M0, M1, T + 24, ys[2] + 12, "D4184 MOSFET")
    pins(M0 + 8, ys, ("SIG", "VCC (if fitted)", "GND"))
    s.text(M1 - 8, ys[0] + 4, "OUT+ OUT−", "t", "end")
    s.text(M1 - 8, ys[2] + 4, "VIN ← P4 12 V", "pwt", "end")
    hop(M1, F0, ys[0], "r")
    field(ys, "SOV-01", ("NC: shuts when unpowered", "12 V coil, flyback diode"))
    T = bottom

    # FT-01
    ys = [T + 52 + 20 * k for k in range(3)]
    bottom = ys[2] + 22
    band(T, bottom, "FT-01 · flow transmitter on the return line", False)
    esp(ys[0], "G14", "FT · pulses, interrupt", "12")
    hop(E1, C0, ys[0], "l")
    box(C0, C1, T + 24, ys[2] + 12, "FLOW_SENSOR")
    pins(C0 + 8, ys, ("1  S", "2  V · 5 V", "3  G · GND"))
    hop(C1, M0, ys[0], "l")
    box(M0, M1, ys[0] - 13, ys[0] + 13)
    s.text((M0 + M1) / 2, ys[0] + 4, "R1 10k / R2 20k: 5 → 3.3 V", "ts")
    hop(M1, F0, ys[0], "l")
    hop(C1, F0, ys[1], "r", "pw")
    hop(C1, F0, ys[2], "r", "gnd")
    s.add(f'<rect x="{F0}" y="{ys[0] - 12}" width="{F1 - F0}" height="64" rx="4" class="box"/>')
    pins(F0 + 10, ys, ("yellow · pulses", "red · 5 V", "black · 0 V"), "ts")
    s.text(F1 - 10, ys[0] + 4, "FT-01", "tb", "end")
    s.text(F1 - 10, ys[1] + 4, "YF-S401", "ts", "end")
    T = bottom

    # LS-01 and HS-01
    for gpio, pin, role, conn, c1, note, tag, sub, title, shade in (
            ("G35", "6", "FSW · HIGH = sump high", "FLOAT_SWITCH", "1  FSW · pull-up", "contact open = HIGH = stop P-01",
             "LS-01", "float switch in the sump", "LS-01 · sump high-level float", True),
            ("G34", "5", "SW · LOW = pressed", "ON/OFF_SWITCH", "1  SW · pull-up", "one press = START, next = STOP",
             "HS-01", "start / stop push button", "HS-01 · start / stop switch", False)):
        ys = [T + 52, T + 72]
        bottom = ys[1] + 22
        band(T, bottom, title, shade)
        esp(ys[0], gpio, role, pin)
        hop(E1, C0, ys[0], "l")
        box(C0, C1, T + 24, ys[1] + 12, conn)
        pins(C0 + 8, ys, (c1, "2  GND"))
        hop(C1, F0, ys[0], "l")
        hop(C1, F0, ys[1], "r", "gnd")
        s.text((M0 + M1) / 2, ys[0] - 6, note, "ts")
        field(ys, tag, (sub,))
        T = bottom

    # add-on pins: LSL-03 probe and ZSO-01
    ys = [T + 52, T + 72, T + 108, T + 128]
    bottom = ys[3] + 22
    band(T, bottom, "LSL-03 and ZSO-01 · soldered to unrouted socket pins", True)
    esp(ys[0], "G4", "T0 · touch, LSL-03", "26")
    esp(ys[2], "G5", "ZSO · LOW = BV-01 open", "29")
    box(C0, C1, T + 24, ys[3] + 12, "add-on board")
    pins(C0 + 8, ys, ("probe lead", "probe GND", "ZSO lead", "ZSO GND"))
    for k in (0, 2):
        hop(E1, C0, ys[k], "l")
        hop(C1, F0, ys[k], "l")
        hop(C1, F0, ys[k + 1], "r", "gnd")
    s.text((M0 + M1) / 2, ys[0] - 6, "TOUCHCAL EMPTY with the probe dry", "ts")
    s.text((M0 + M1) / 2, ys[2] - 6, "optional: SET bvmode 1", "ts")
    field(ys[:2], "LSL-03", ("bare wires at TK-03 dip tube",))
    field(ys[2:], "ZSO-01", ("closes when BV-01 is open",))
    T = bottom

    # board pins and supply
    ys = [T + 52 + 30 * k for k in range(4)]
    bottom = ys[3] + 24
    band(T, bottom, "On the ESP32 board, and the supply pins", False)
    for y, gpio, role, pin, target, d, cls in (
            (ys[0], "G2", "LED · fast blink = BV-01", "24", "on-board LED", "r", "wire"),
            (ys[1], "3V3", "3.3 V out, board LDO", "1", "IBT-2 VCC × 3", "r", "pw"),
            (ys[2], "5V", "5 V in", "19", "LM2596 5 V rail", "l", "pw"),
            (ys[3], "GND", "0 V", "14 · 32 · 38", "common 0 V", "r", "gnd")):
        esp(y, gpio, role, pin)
        hop(E1, C0, y, d, cls)
        box(C0, C1, y - 12, y + 12)
        s.text((C0 + C1) / 2, y + 4, target, "t")
    for k, txt in enumerate(("12 V: SMPS → PCB 12V INPUT (fuse F3 ≥ 15 A, TVS)",
                             "→ P1, P2, P3 to the IBT-2 B+/B− · P4 to the D4184 VIN",
                             "5 V: LM2596 → ESP32 5V pin, FT-01 red, SOLENOID_VALVE V",
                             "0 V is common to the PCB, every IBT-2 and the D4184")):
        s.text(M0, ys[k] + 4, txt, "pwt" if k < 3 else "ts", "start")
    T = bottom

    # ESP32 body and its pin rows, drawn under the wires
    body = [f'<rect x="{E0}" y="96" width="{E1 - E0}" height="{T - 104}" rx="6" class="box"/>']
    for y, gpio, role, pin in esp_rows:
        body.append(f'<text x="30" y="{y + 4}" class="io" text-anchor="start">{esc(gpio)}</text>')
        body.append(f'<text x="66" y="{y + 4}" class="ts" text-anchor="start">{esc(role)}</text>')
        body.append(f'<text x="242" y="{y + 4}" class="ts" text-anchor="end">{esc(pin)}</text>')
        body.append(f'<circle cx="{E1}" cy="{y}" r="3.5" class="dot"/>')
    s.parts = zones + body + s.parts
    s.h = T + 8
    return s.render("diagram wiring")


def conditioning():
    s = Svg(1180, 300, "Signal conditioning on the add-on board: the BTS7960 current-mirror output is loaded to about "
                       "2 kilo-ohms and fed through 10 kilo-ohms with 100 nF to an ADC pin; the flow sensor's 5 V pulse is "
                       "divided to 3.3 V before G14.")
    # current sense chain
    s.text(20, 26, "IS current sense (one per pump)", "tb", "start")
    s.add('<rect x="20" y="60" width="130" height="70" rx="5" class="box"/>')
    s.text(85, 90, "IBT-2", "tb")
    s.text(85, 107, "R_IS + L_IS tied", "ts")
    s.line([(150, 95), (260, 95)], "wire")
    s.add('<circle cx="200" cy="95" r="3.5" class="dot"/>')
    # onboard 5k and added 3.3k to ground
    s.line([(200, 95), (200, 150)], "wire")
    s.add('<rect x="190" y="150" width="20" height="44" class="res"/>')
    s.line([(200, 194), (200, 230)], "wire")
    s.add('<path d="M188,230 H212 M192,236 H208 M196,242 H204" class="wire"/>')
    s.text(218, 172, "3.3 kΩ ∥ on-board 5 kΩ", "ts", "start")
    s.text(218, 188, "≈ 2.0 kΩ → 0.24 V/A", "io", "start")
    s.add('<rect x="260" y="85" width="56" height="20" class="res"/>')
    s.text(288, 75, "10 kΩ", "ts")
    s.line([(316, 95), (470, 95)], "wire")
    s.add('<circle cx="430" cy="95" r="3.5" class="dot"/>')
    s.line([(430, 95), (430, 140)], "wire")
    s.add('<path d="M416,140 H444 M416,148 H444" class="wire"/>')
    s.line([(430, 148), (430, 178)], "wire")
    s.add('<path d="M418,178 H442 M422,184 H438 M426,190 H434" class="wire"/>')
    s.text(452, 148, "100 nF", "ts", "start")
    s.add('<rect x="470" y="70" width="150" height="50" rx="5" class="box"/>')
    s.text(545, 92, "G15 · G36 · G39", "io")
    s.text(545, 108, "ADC, 2.5 dB atten.", "ts")
    s.text(20, 268, "Fault current (≈4.5 mA) into 2 kΩ stays ≤ 9 V; 10 kΩ keeps pin injection < 0.6 mA.", "t", "start")
    s.text(20, 288, "10 kΩ + 100 nF (160 Hz) averages the 20 kHz PWM: reading = supply current.", "t", "start")

    # FT-01 level shift
    x0 = 660
    s.text(x0, 26, "FT-01 pulse level shift", "tb", "start")
    s.add(f'<rect x="{x0}" y="60" width="140" height="70" rx="5" class="box"/>')
    s.text(x0 + 70, 90, "YF-S401", "tb")
    s.text(x0 + 70, 107, "yellow: 0 / >4.5 V", "ts")
    s.line([(x0 + 140, 95), (x0 + 190, 95)], "wire")
    s.add(f'<rect x="{x0 + 190}" y="85" width="56" height="20" class="res"/>')
    s.text(x0 + 218, 75, "R1", "ts")
    s.line([(x0 + 246, 95), (x0 + 360, 95)], "wire")
    s.add(f'<circle cx="{x0 + 300}" cy="95" r="3.5" class="dot"/>')
    s.line([(x0 + 300, 95), (x0 + 300, 140)], "wire")
    s.add(f'<rect x="{x0 + 290}" y="140" width="20" height="44" class="res"/>')
    s.text(x0 + 318, 166, "R2", "ts", "start")
    s.line([(x0 + 300, 184), (x0 + 300, 210)], "wire")
    s.add(f'<path d="M{x0 + 288},210 H{x0 + 312} M{x0 + 292},216 H{x0 + 308} M{x0 + 296},222 H{x0 + 304}" class="wire"/>')
    s.add(f'<rect x="{x0 + 360}" y="70" width="140" height="50" rx="5" class="box"/>')
    s.text(x0 + 430, 92, "FLOW_SENSOR S", "io")
    s.text(x0 + 430, 108, "→ G14 interrupt", "ts")
    s.text(x0 + 250, 240, "push-pull output: R1 10 kΩ, R2 20 kΩ → 3.33 V", "t")
    s.text(x0 + 250, 258, "internal 10 kΩ pull-up: R1 0 Ω, R2 22 kΩ → 3.44 V", "t")
    return s.render("diagram cond")


def states():
    s = Svg(1240, 470, "Sequence state machine: one switch press runs Case 1, then Case 2, then a latched safe OFF; "
                       "LS-01 high sends each case into a hold state; the switch stops everything from any state.")

    def st(x, y, w, name, sub, cls="st"):
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="10" class="{cls}"/>')
        s.text(x + w / 2, y + 24, name, "tb")
        s.text(x + w / 2, y + 42, sub, "ts")

    def tr(pts, label, lx, ly, anchor="middle"):
        s.line(pts, "tr")
        x, y = pts[-1]
        px, py = pts[-2]
        d = "r" if x > px else "l" if x < px else ("d" if y > py else "u")
        off = {"r": (-6, 0), "l": (6, 0), "d": (0, -6), "u": (0, 6)}[d]
        s.arrow(x + off[0], y + off[1], d, "ta")
        s.text(lx, ly, label, "ts", anchor)

    st(20, 40, 140, "IDLE", "all off, SOV closed")
    st(220, 40, 160, "C1_START", "zero currents 0.6 s")
    st(450, 40, 180, "C1_RUN", "P-02 d2 · P-01 d1")
    st(800, 40, 200, "C1_HOLD_LSH", "P-01 off, SOV closed")
    tr([(160, 69), (220, 69)], "switch", 190, 61)
    tr([(380, 69), (450, 69)], "P-02 on", 415, 61)
    tr([(630, 58), (800, 58)], "LS-01 high ≥ lshon", 715, 50)
    tr([(800, 82), (630, 82)], "clear ≥ lshoff + p1off", 715, 100)
    st(20, 250, 170, "C2_ISOLATE", "P-01 off, SOV closed")
    st(250, 250, 180, "C2_OPEN_BV01", "LED fast blink")
    st(520, 250, 170, "C2_FLUSH", "P-01 d1f + P-03 d3")
    st(800, 250, 200, "C2_HOLD_LSH", "P-01 + P-03 off")
    st(1050, 250, 180, "COMPLETE", "latched safe OFF", "st done")
    tr([(540, 98), (540, 180), (105, 180), (105, 250)], "t ≥ tc1 while not holding", 330, 172)
    tr([(190, 279), (250, 279)], "1 s", 220, 271)
    tr([(430, 268), (520, 268)], "ZSO-01 or tbv", 475, 260)
    tr([(520, 294), (430, 294)], "P-03 dry, probe wet", 475, 324)
    tr([(690, 268), (800, 268)], "LS-01 high", 745, 260)
    tr([(800, 292), (690, 292)], "clear", 745, 310)
    tr([(605, 308), (605, 360), (1140, 360), (1140, 308)], "TK-03 empty: LSL-03 dry ≥ 0.3 s, or IT-03 dry ≥ 1.5 s and the probe not wet, or tfmax", 870, 378)
    s.add('<rect x="1050" y="40" width="180" height="58" rx="10" class="st stop"/>')
    s.text(1140, 64, "STOPPED", "tb")
    s.text(1140, 82, "switch, any running state", "ts")
    s.text(620, 430, "P-02 stays at 100% from C1_RUN until COMPLETE; interlocks I-1…I-4 sit between this logic and the outputs.", "t")
    s.text(620, 450, "COMPLETE brakes all pumps and keeps SOV-01 de-energised; the next switch press returns to IDLE.", "t")
    return s.render("diagram states")


PRINT_CSS = """
svg{background:#fff;color:#111;font-family:%s}
.t{font-size:12px;fill:#111}.ts{font-size:10.5px;fill:#444}.tb{font-size:12.5px;font-weight:700;fill:#111}
.tbub{font-size:9.5px;font-weight:700;fill:#111}.io{font-size:10.5px;fill:#0b5a7a;font-weight:600}
.ln{fill:none;stroke:#0b5a7a;stroke-width:3}.pw{fill:none;stroke:#7a3b0b;stroke-width:2.6}.wire{fill:none;stroke:#111;stroke-width:1.6}
.sig{fill:none;stroke:#555;stroke-width:1.3;stroke-dasharray:5 4}.tr{fill:none;stroke:#111;stroke-width:1.4}
.eq{fill:none;stroke:#111;stroke-width:2}.eq.thin{stroke-width:1.1}.pumpfill{fill:#fff}.vlv{fill:#fff;stroke:#111;stroke-width:1.6}
.box{fill:#fff;stroke:#111;stroke-width:1.4}.box.hot{stroke:#b3261e}.res{fill:#fff;stroke:#111;stroke-width:1.4}
.bub{fill:#fff;stroke:#111;stroke-width:1.5}.liq{fill:#0b5a7a;fill-opacity:.12}.dot{fill:#111}
.fa{fill:#0b5a7a}.pa{fill:#7a3b0b}.ta{fill:#111}.elec{stroke:#b26b00;stroke-width:6}.probe{fill:#b26b00}
.zone{fill:#0b5a7a;fill-opacity:.05}.gnd{fill:none;stroke:#555;stroke-width:1.3}.pwt{font-size:10.5px;font-weight:600;fill:#7a3b0b}
.st{fill:#fff;stroke:#111;stroke-width:1.5}.st.done{stroke:#2e7d4f;stroke-width:2.5}.st.stop{stroke:#b3261e}
""" % FONT


def standalone(svg_inline, title):
    import re

    head, rest = svg_inline.split(">", 1)
    head = re.sub(r'class="[^"]*"', "", head)
    w, h = re.search(r'viewBox="0 0 (\d+) (\d+)"', head).groups()
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n{head} width="{w}" height="{h}">'
            f"<title>{esc(title)}</title><style>{PRINT_CSS}</style>"
            f'<rect width="100%" height="100%" fill="#fff"/>{rest}')


PRINT_FONT = "Arial, Helvetica, sans-serif"


def _a4(body, title):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">'
            f'<title>{esc(title)}</title><rect width="210" height="297" fill="#fff"/>'
            f'<g font-family="{PRINT_FONT}" fill="#000" stroke="none">{body}</g></svg>')


def _scale_bar(x, y):
    t = f'<path d="M{x},{y} h50 M{x},{y - 1.5} v3 M{x + 50},{y - 1.5} v3" stroke="#000" stroke-width="0.3" fill="none"/>'
    return t + f'<text x="{x + 25}" y="{y - 2}" font-size="2.8" text-anchor="middle">50 mm: measure it to check the print scale</text>'


def labels_sheet(tags, flags):
    """A4 sheet of equipment tags and flow-direction flags, printed at 100% scale."""
    b = [f'<text x="10" y="9" font-size="3.6" font-weight="bold">LAM Stage 2 rig · tag labels</text>',
         '<text x="10" y="13.5" font-size="2.8">Print at 100% (no fit to page). Cut on the lines and cover with clear tape.</text>',
         _scale_bar(150, 13)]
    w, h, gx, gy, x0, y0 = 60, 21, 5, 4, 10, 18
    for i, (tag, desc) in enumerate(tags):
        x, y = x0 + (i % 3) * (w + gx), y0 + (i // 3) * (h + gy)
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="none" stroke="#000" stroke-width="0.35"/>')
        b.append(f'<text x="{x + w / 2}" y="{y + 10}" font-size="7.2" font-weight="bold" text-anchor="middle">{esc(tag)}</text>')
        b.append(f'<text x="{x + w / 2}" y="{y + 16.5}" font-size="3.3" text-anchor="middle">{esc(desc)}</text>')
    fy = y0 + ((len(tags) + 2) // 3) * (h + gy) + 4
    b.append(f'<text x="10" y="{fy}" font-size="3.2" font-weight="bold">Flow-direction flags: tape around the tube with the arrow '
             'pointing along the flow (two per line)</text>')
    fw, fh, fgx, fgy = 92, 14, 6, 4
    for i, (tag, desc) in enumerate([f for f in flags for _ in (0, 1)]):
        x, y = 10 + (i % 2) * (fw + fgx), fy + 4 + (i // 2) * (fh + fgy)
        b.append(f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" rx="1.5" fill="none" stroke="#000" stroke-width="0.35"/>')
        b.append(f'<text x="{x + 3}" y="{y + 9.2}" font-size="5.4" font-weight="bold">{esc(tag)}</text>')
        b.append(f'<path d="M{x + 24},{y + 7} h17" stroke="#000" stroke-width="1.1"/>'
                 f'<path d="M{x + 41},{y + 4} l5,3 l-5,3 z"/>')
        b.append(f'<text x="{x + 49}" y="{y + 8.4}" font-size="3.3">{esc(desc)}</text>')
    return _a4("".join(b), "LAM Stage 2 rig tag labels")


def dial_sheet():
    """A4 sheet with BV-02 position dials (both turning directions), printed at 100% scale."""
    import math

    marks = [(0, "0% shut"), (25, "25%"), (50, "50%"), (70, "70%"), (75, "75%"), (100, "100% open")]

    def dial(cx, cy, sign, caption):
        out = [f'<text x="{cx + sign * 22}" y="{cy + 14}" font-size="3.3" font-weight="bold" text-anchor="middle">{caption}</text>']
        r0, r1 = 40, 44
        for k in range(0, 101, 5):
            ang = math.radians(-90 + sign * k * 0.9)
            rin = r0 - (5 if k % 25 == 0 else 2.5)
            out.append(f'<path d="M{cx + rin * math.cos(ang):.2f},{cy + rin * math.sin(ang):.2f} '
                       f'L{cx + r0 * math.cos(ang):.2f},{cy + r0 * math.sin(ang):.2f}" stroke="#000" stroke-width="0.3"/>')
        for k, text in marks:
            ang = math.radians(-90 + sign * k * 0.9)
            out.append(f'<path d="M{cx:.2f},{cy:.2f} L{cx + r0 * math.cos(ang):.2f},{cy + r0 * math.sin(ang):.2f}" '
                       f'stroke="#000" stroke-width="{0.45 if k in (0, 100) else 0.2}"/>')
            lx, ly = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang) + {70: -1.2, 75: 1.2}.get(k, 0)
            anchor = "middle" if k == 0 else ("start" if sign > 0 else "end")
            out.append(f'<text x="{lx:.2f}" y="{ly + 1.2:.2f}" font-size="3" text-anchor="{anchor}">{text}</text>')
        out.append(f'<path d="M{cx},{cy - r0} A{r0},{r0} 0 0 {1 if sign > 0 else 0} {cx + sign * r0},{cy}" '
                   'fill="none" stroke="#000" stroke-width="0.3"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="none" stroke="#000" stroke-width="0.3"/>'
                   f'<path d="M{cx - 5},{cy} h10 M{cx},{cy - 5} v10" stroke="#000" stroke-width="0.2"/>')
        out.append(f'<text x="{cx + sign * 30}" y="{cy + 5.5}" font-size="2.6" text-anchor="middle">along the pipe</text>')
        return "".join(out)

    b = ['<text x="10" y="9" font-size="3.6" font-weight="bold">BV-02 position dial (Q2.1)</text>',
         '<text x="10" y="13.5" font-size="2.8">Print at 100% (no fit to page). Use the dial whose arrow matches the way the '
         'handle turns to open.</text>', _scale_bar(150, 13)]
    b.append(dial(30, 75, 1, "handle turns clockwise to open"))
    b.append(dial(180, 75, -1, "handle turns anticlockwise to open"))
    b.append(dial(30, 175, 1, "spare · clockwise"))
    b.append(dial(180, 175, -1, "spare · anticlockwise"))
    notes = ["Position % = handle angle from shut ÷ 90°: 25% = 22.5°, 50% = 45°, 70% = 63°, 75% = 67.5°, 100% = 90°.",
             "1. Cut out the dial and the centre hole, slide it over the stem under the handle, and tape it flat.",
             "2. Turn the handle fully shut and fully open: it must stop on the 0% and 100% lines. If not, rotate the dial.",
             "3. Line up the centre line of the handle with each mark. Sequence (sheet 06): 100, 75, 70, 50, 25, then back up",
             "    50, 75, 100; the way back up shows hysteresis. After each move type MARK V75 (etc.) and hold 60 s.",
             "4. The paper's text says 75% and its table says 70%: record both."]
    for i, t in enumerate(notes):
        b.append(f'<text x="10" y="{236 + i * 6}" font-size="3.1">{esc(t)}</text>')
    return _a4("".join(b), "BV-02 position dial")

if __name__ == "__main__":
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open(f"{out}/pid.svg", "w") as f:
        f.write(standalone(pid(), "LAM Stage 2 rig P&ID"))
    print("wrote", f"{out}/pid.svg")
