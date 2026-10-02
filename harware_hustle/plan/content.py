"""Plan content for the build book. Edited across review runs; build_page.py renders it."""

REV = "F · portal rules, pump physics, P-01 fallback"

OBJECTIVE = ("<strong>By Sunday 4 October, 18:00 IST, upload the three files the LRC portal requires: a 10–12 minute "
             "Challenge Video (MP4), a 3–4 minute Journey Video (MP4) and the solution handwritten in blue or black ink, "
             "scanned to one PDF that also carries the ISA-5.1 P&amp;ID, the labelled photos, the plots and the code link.</strong> "
             "Together they must show a leak-free, ESP32-automated rig that runs Case 1 into Case 2 in one go, holds 3.0 L/min "
             "on an FT-01 calibrated in place by weighing, and stops within about one second of the flush tank running dry.")
DONE_WHEN = ("The single-take run (switch press → Case 1 with the external-fluid event → automatic Case 2 → automatic stop) "
             "passes three rehearsals in a row and is on video. Calibration maximum error ≤ 3% with repeats within ±1%, "
             "and R², a, b and average error reported. Every Task 1–3 question has measured data and a graph.")
NOT_DOING = [
    "Wi-Fi, web or cloud dashboards. ADC2 dies with Wi-Fi on, and USB is safer on camera.",
    "A machine-learning fault classifier. There is no training data, and a rule table is explainable.",
    "Touching the FT-01 spool after calibration, or any tubing that arrives after Friday.",
    "The pressure transducer: ordered on Friday it arrives too late to install and validate.",
    "Rework of the custom PCB. All additions go on a small add-on board.",
]
CONSTRAINTS = [
    "About 2.5 build days. One rig and one scale are shared by everyone.",
    "Kit plus passives on hand. Online parts take 1–3 days, so they can only be upgrades.",
    "Pumps cut out at 8.25 bar. FT-01 is rated 0.8 MPa, and the PU tube and push-fits about 0.8–1 MPa.",
    "The portal takes exactly three files, all required, MP4 or PDF only, and none can be changed after saving. "
    "It has no field for code, photos or the P&amp;ID, so they go inside the PDF and the video.",
]

FINDINGS = [
    ("The LRC team portal's Hardware Hustle form asks for three uploads, each required: a Journey Video (MP4, 3–4 min, "
     "“your team's efforts and prototype development journey”), a Challenge Video (MP4, 10–12 min) and a Handwritten "
     "Solution (scanned PDF, “written using blue or black ink”). It accepts only MP4, has no code field, and warns that a "
     "saved submission cannot be changed. Its public rounds API lists the round as 29 Sep – 19 Oct.",
     "Cut the Challenge Video to 11½ minutes, film a Journey Video from Friday onwards, write the paper by hand and "
     "scan it, and put the code link, photos and P&amp;ID inside the PDF. Keep 4 Oct as the deadline unless the "
     "dashboard countdown or the organisers say otherwise.",
     [("LRC portal, team submission form (JS bundle)", "https://lrc2026.tworks.in/assets/Team-81254daf.js"),
      ("LRC rounds API", "https://api.lrc2026.tworks.in/api/rounds")]),
    ("A 12 V sprayer diaphragm pump is not a flat positive-displacement source. A comparable 3-chamber pump (Shurflo "
     "8000-543-238) gives 6.8 L/min open, 5.0 at 2.8 bar and 3.6 at 6.9 bar, while its current rises from 3.0 to 8.7 A. "
     "Scaled to our 6.1 L/min pump, P-02 at 100% reaches 3.0 L/min only at about 7 bar: near its 8.25 bar switch and "
     "the tube's rating.",
     "Map P-02 at 100% against the BV-02 dial with IT-02 at M2. If the 3.0 L/min trim makes the switch cycle, hold "
     "3.0 L/min with BV-02 open and a reduced d2 instead, and show the data. Keep the 100% sweep as the Q2.1 evidence.",
     [("Shurflo 8000-543-238 data sheet", "http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf"),
      ("Shurflo 8000 series tables", "https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf")]),
    ("FT-01 is a YF-S401: 5,880 pulses per litre (F = 98·Q), 0.3–6 L/min, ±10% uncalibrated, "
     "output high above 4.5 V on a 5 V supply, rated 0.8 MPa.",
     "Level-shift the pulse to 3.3 V before G14. Mount FT-01 after BV-02 so it never sees the pumps' "
     "8.25 bar cut-off. Calibrate it in place.",
     [("TinyTronics YF-S401", "https://www.tinytronics.nl/en/sensors/liquid/yf-s401-water-flow-sensor"),
      ("BC Robotics YF-S401", "https://bc-robotics.com/shop/liquid-flow-meter-yf-s401/")]),
    ("The paper's “8 mm pipe” is the tube's outside diameter. The kit tube is 8 mm OD × 5 mm ID, "
     "so 3 L/min runs at 2.55 m/s (Re ≈ 12,700), not 0.99 m/s, with about 19 kPa of friction per metre.",
     "Measure the bore with calipers on day one and use it in Q1.2. Expect the loop's maximum to fall "
     "short of 6 L/min, and explain why with the pump and system curves.",
     [("Kit list, item 1 (PU tube 8 mm OD × 5 mm ID)", None)]),
    ("SOV-01's label reads 0–10 kg/cm², so it is a zero-differential (direct-acting) valve and will open on P-01's "
     "suction side. ¼-inch valves of this class (e.g. 2W025-08) have a 2.5 mm orifice (Cv ≈ 0.23), which costs "
     "about 0.8 bar at 3 L/min (1.3 bar at Kv 0.16), all of it on the suction side. Raising TK-01 by 0.3 m adds only "
     "0.03 bar, so it helps priming, not this loss. P-01 may cavitate somewhere near 1.5–2.5 L/min at any duty.",
     "Test P-01's flow through SOV-01 in hour one and use the strongest pump as P-01. If 50% duty cannot carry "
     "3.0 L/min, raise the duty and show the data (3.0 L/min wins). If no duty reaches 3.0, run Case 1 on sump "
     "inventory with the planner's settings (sheet 03), so FT-01 still holds 3.0 L/min.",
     [("STC 2W025 data (Cv 0.23)", "https://valveman.com/products/stc2w025-1-4-solenoid-valve-1-4-npt-2-way-normally-closed/")]),
    ("Each IBT-2 IS pin has 10 kΩ to GND (5 kΩ when the two are tied), giving 0.59 V/A nominal. The "
     "BTS7960 sense ratio spreads from 3,000 to 14,000, so a pin can see 8 V. The 74HC244 buffer powered "
     "at 5 V needs about 3.5 V for a logic HIGH.",
     "Add 3.3 kΩ (about 2 kΩ total, 0.24 V/A), then 10 kΩ in series and 100 nF at the pin, with a small Schottky "
     "(BAT85) from the pin to 3V3 so a driver fault (4–7 mA) cannot push the pin above 3.3 V. Calibrate each channel against the DMM. "
     "The 2.5 dB range ends at 1.25 V, and one measured IBT-2 (k ≈ 6,100) reaches it at about 4 A. Keep every "
     "channel under 1,100 mV at P-02's highest-pressure point. Power the IBT-2 VCC from 3.3 V.",
     [("DCC-EX IBT_2 current-sense notes", "https://dcc-ex.com/reference/hardware/motorboards/IBT_2-motor-board-setup.html"),
      ("BTS7960 data sheet", "https://www.robotpower.com/downloads/BTS7960_v1.1_2004-12-07.pdf"),
      ("Espressif ADC ranges", "https://docs.espressif.com/projects/esp-idf/en/v4.4.7/esp32/api-reference/peripherals/adc.html")]),
    ("Rotor meters read high in pulsating flow (up to +5.5% in small liquid turbine meters), and the error changes "
     "with the pulsation's frequency and amplitude. A hall flow sensor's frequency also depends on the pipe attached "
     "to it and on its orientation.",
     "Calibrate with P-02 pumping through the final installed spool, so the pulsation and plumbing are the "
     "real ones. Freeze that spool afterwards. Verify at the exact Case 1 setting (P-02 duty and BV-02 position), "
     "because the calibration runs vary the duty and so change the pulsation.",
     [("EFRC guideline, pulsating-flow meter errors", "https://www.recip.org/wp-content/uploads/2020/12/EFRC-Guidelines-Flow-Meter-Errors-in-Pulsating-Flow-of-Reciprocating-Compressor-Systems-December-2020.pdf"),
      ("Brunel thesis, turbine meters in pulsating flow", "https://bura.brunel.ac.uk/handle/2438/4971?mode=full"),
      ("IEEE 8307842", "https://ieeexplore.ieee.org/document/8307842/")]),
    ("Static weighing (ISO 4185) is a primary method for calibrating flow meters, provided the line runs full. In "
     "start-stop runs the scale is not the problem (1 g is 0.04% of 2.5 kg). The errors are fixed amounts per run: "
     "pump ramp and rotor slip at each end, drips, and water held in the outlet tube. They weigh most in short "
     "low-flow runs. R² ≥ 0.995 can still pass with 4–6% point errors, so it is a weak acceptance test.",
     "Calibrate by weight on the 1 g scale, with each run at least 1.5 kg. The ESP32 times each run itself, so the "
     "pulse count and the collected mass share one window. Accept on maximum error and repeatability, and report R².",
     [("ISO 4185 preview", "https://cdn.standards.iteh.ai/samples/9959/8f87749e47c84061b7a6495487300f9b/ISO-4185-1980.pdf"),
      ("IMEKO TC9 2013, start-stop flow calibration", "https://www.imeko.org/publications/tc9-2013/IMEKO-TC9-2013-013.pdf"),
      ("datalogd, a measured YF-S401 curve", "https://datalogd.readthedocs.io/en/latest/api/datalogd.plugins.flowsensorcalibration_datafilter.html")]),
    ("ESP32 touch sensing works through a plastic wall, but the threshold is specific to each placement and the "
     "reading drifts. A foil on the wall also trips while water still covers the pickup, so on camera the system "
     "would stop with the tank visibly unfinished.",
     "Make LSL-03 a bare-wire probe on the touch pin, taped at the dip-tube inlet. It goes dry exactly when P-03 can "
     "no longer draw. Re-capture the wet reading every run. P-03's current then separates “empty” from "
     "“BV-01 still shut”, and a timeout backs both up.",
     [("Random Nerd Tutorials, ESP32 touch", "https://randomnerdtutorials.com/esp32-touch-pins-arduino-ide/"),
      ("Maakbaas, touch as a level sensor", "https://maakbaas.com/esp32-soil-moisture-sensor/logs/testing-the-sensor/")]),
    ("ADC2 cannot be read while Wi-Fi is on, and only G36 and G39 are free ADC1 pins on this PCB.",
     "Keep Wi-Fi off and stream telemetry over USB to the laptop console. G15 (ADC2) carries the third "
     "current channel.",
     [("Espressif ADC documentation", "https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/adc.html")]),
]

MILESTONES = [
    dict(id="M1", title="Rig physics proven on the bench", owner="EF with HY", when="Fri 10–14", crit=True,
         do="Connect LS-01 first (or jumper FSW to GND): an open float input reads “sump high” and I-1 blocks "
            "P-01 and P-03. Run the power-off checks, then apply 12 V. Drive the three IBT-2s and the D4184 from the console "
            "(<code>MANUAL</code>, <code>P n duty</code>, <code>SOV 1</code>). Pump TK-01 → SOV-01 → P-01 into "
            "the bucket on the scale at 50, 60, 70 and 100% for 30 s each, using the P-01 duty finder. Scope "
            "the FT-01 output with and without a 10 kΩ load. Check every input with <code>PINS</code>. "
            "Calibrate IS against the DMM in series.",
         done="All three pumps start together (staggered) with no ESP32 reset. FT-01 at G14 is ≤ 3.3 V with clean "
              "edges, and the glitch count stays flat with the pumps running and FT-01 dry. The P-01 Q(duty) table "
              "exists and d1 is chosen to give ≥ 3.3 L/min, or, if no duty reaches 3.0, P-01's measured maximum is "
              "in the inventory planner and its Case 1 settings are chosen.",
         retires="SOV-01 starving P-01; 3.3 V logic into the IBT-2; motor noise in the pulse count; brown-out.",
         est="half a day (confidence: medium)"),
    dict(id="M2", title="Leak-free loop that matches the P&ID", owner="HY", when="Fri 14–24", crit=True,
         do="Build to Figure 1: dip tubes, raised TK-01 and TK-03, the FT-01 spool with its straight runs, the BV-02 "
            "dial, and P&amp;ID tags and flow arrows on everything. Prime the loop, then run the leak test. Then map "
            "P-02 at 100% against the BV-02 dial (100, 75, 50, 40, 30%), 30 s each, logging flow and IT-02, and listen "
            "for the pressure switch clicking.",
         done="10 min at 3 L/min plus 2 min at BV-02 25% with zero wet tissue. No bubbles in the FT-01 spool. "
              "Flow CV under 3% over one minute. The LS-01 trip volume is measured. The dial position for 3.0 L/min "
              "at 100% is known, with IT-02 there and whether the switch cycles.",
         retires="Leaks, air in the meter, wrong routing.",
         est="half a day (confidence: medium)"),
    dict(id="M3", title="FT-01 calibrated and the required data recorded", owner="DC", when="Sat 08–13", crit=True,
         do="Do 15 gravimetric <code>CAL</code> runs (5 flows × 3, each ≥ 1.5 kg) and enter them in the workbench. Load a, "
            "b and fcut, verify at the exact Case 1 setting, then freeze the spool. Straight after, while the rig is set up, "
            "record the paper's required data: the BV-02 sweep (Q2.1) and the runs at about 1, 3 and maximum L/min (Q1.2).",
         done="Maximum error ≤ 3% and repeats within ±1% at each flow; R² reported. Verification at the Case 1 setting "
              "within ±2% of the scale. The Q2.1 table (25/30/40/50/70/75/100%) and the Q1.2 table hold measured values, "
              "with plots saved.",
         retires="Calibration accuracy (team worry 2), and the risk of reaching Sunday with required answers still empty.",
         est="5 h (confidence: high)"),
    dict(id="M4", title="Case 1 passes acceptance", owner="EF", when="Fri 20–24 dry · Sat 12–15 wet", crit=True,
         do="Set d1, then trim BV-02 so that P-02 at 100% gives 3.0 L/min. If the switch cycles there (IT-02 drops out in "
            "bursts, the pump clicks), open BV-02 fully and <code>SET d2</code> from the duty map to give 3.0 L/min "
            "instead, and record why. <code>SET tc1 180</code>. Run Case 1 and pour 0.8 L into TK-02 at +60 s, or "
            "at the planner's time and volume if P-01 is short.",
         done="P-01 stops within 1.5 s of LS-01 tripping and restarts by itself after it clears, while P-02 never "
              "stops. Mean flow is 3.00 ± 0.10 L/min over 3 min, and the console shows mL/s and litres returned. "
              "Three passes in a row.",
         retires="Control firmware and holding 3 L/min (team worries 1 and 3).",
         est="half a day across two blocks (confidence: medium)"),
    dict(id="M5", title="Case 2 flushes and stops itself, with a backup take", owner="EF", when="Sat 15–22", crit=True,
         do="With the LSL-03 probe out of the water, run <code>TOUCHCAL EMPTY</code>. Run P-03 at d3 wet, then dry, and "
            "<code>SET i3dry</code> midway between the two currents. Then run Case 1 into Case 2 end to end.",
         done="Every pump stops ≤ 1.0 s after the probe leaves the water (FLUSH_EMPTY, source LSL-03, in the event "
              "log), with no more than a puddle left in TK-03. The only manual action is BV-01. Three full runs in a row; "
              "the third is filmed in full as the backup take (by Sat 22:00), however rough.",
         retires="Detecting an empty flush tank at the source.",
         est="4 h (confidence: low to medium)"),
    dict(id="M6", title="Extras that earn points", owner="DC", when="Sat 19–24", crit=False,
         do="Fault demos (unplug FT-01, close BV-03, throttle BV-02); the FIC disturbance test; a <code>BURST</code> "
            "pulsation capture; a dye transit over a marked 1.00 m of tube.",
         done="Each fault demo produces the right diagnosis on the console, FIC restores 3.0 L/min after a BV-02 move, "
              "and the pulsation and dye plots are saved. None of this may delay M5's backup take.",
         retires=None,
         est="5 h (confidence: medium)"),
    dict(id="M7", title="Video and submission uploaded", owner="IV", when="Sun 08–18", crit=True,
         do="Three rehearsals; record the single take; shoot the edited segments; cut the Challenge Video (10–12 min) "
            "and the Journey Video (3–4 min) and export both as H.264 MP4; handwrite the paper in blue or black ink with "
            "the P&amp;ID on page 4, then add appendix pages for the plots, photos and the code link and scan them into one PDF.",
         done="All three files uploaded by 16:00, two hours before the cutoff, by one person, after a teammate who did "
              "not film checks both videos and the PDF against every requirement on pages 1–3 of the paper. Durations "
              "checked in the exported files: 10:00–12:00 and 3:00–4:00. The code link opens in a logged-out browser.",
         retires=None,
         est="one day (confidence: high)"),
]

BLOCKS = ["Fri 08–10", "Fri 10–14", "Fri 14–19", "Fri 19–24", "Sat 08–13", "Sat 13–19", "Sat 19–24", "Sun 08–13", "Sun 13–18"]
LANES = [
    ("HY · hydraulics", ["First steps: kit count against the fitting map; bore; drip tray and stands; dry layout",
                         "<i class=m>M1</i> P-01 bucket tests with EF",
                         "<i class=m>M2</i> build loop, tags, BV-02 dial",
                         "<i class=m>M2</i> first water, leak test, fix",
                         "<i class=m>M3</i> bucket and pour-back; BV-02 sweep moves",
                         "<i class=m>M4</i> pour event · <i class=m>M5</i> resets between runs",
                         "<i class=m>M5</i> backup take 22:00 · <i class=m>M6</i> dye transit",
                         "<i class=m>M7</i> rehearsals; BV-01 hand",
                         "Photos; standby fixes"]),
    ("EF · electronics, firmware", ["First steps: flash over USB; PINS; solder the add-on board; power-off check",
                                    "<i class=m>M1</i> power-up, drivers, IS gains, FT-01 scope",
                                    "Harness dressing; LSL-03 probe; LS-01 orientation",
                                    "<i class=m>M4</i> dry logic and interlock tests",
                                    "<i class=m>M3</i> console operator",
                                    "<i class=m>M4</i> acceptance · <i class=m>M5</i> TOUCHCAL, i3dry",
                                    "<i class=m>M5</i> backup take · <i class=m>M6</i> fault demos, FIC",
                                    "<i class=m>M7</i> runs the single take",
                                    "Event logs and screenshots for the edit"]),
    ("DC · data, calibration", ["First steps: laptops ready; replay practice; weigh station",
                                "<i class=m>M1</i> P-01 duty finder",
                                "LS-01 trip volume; duty map",
                                "Weigh-bucket setup; CAL dry run",
                                "<i class=m>M3</i> workbench, fit, verify; Q2.1 and Q1.2 data",
                                "Valve and Q1.2 plots; Case logs → trend plots",
                                "<i class=m>M6</i> burst and fault-demo analysis",
                                "Handwrite the data tables and Q1.2/Q2 answers; print the plots",
                                "Proofread the handwritten PDF against the paper"]),
    ("IV · integration, video", ["First steps: organiser message; share the book; parts run; print",
                                 "Parts to HY; photo log; owns the checklists; Journey filming starts",
                                 "P&amp;ID v1 printed; shot list; Journey clips",
                                 "Task 3 answers drafted",
                                 "Answer-sheet tables; Journey clips",
                                 "Film a Case 1 rehearsal; run script drills; handwrite Q3.1 and Q3.2",
                                 "Film the backup take; storyboard locked; handwrite the P&amp;ID on page 4",
                                 "<i class=m>M7</i> record; voice-over; Journey Video cut",
                                 "<i class=m>M7</i> Challenge Video cut; scan the PDF; export MP4s; upload by 16:00"]),
]

CHECKPOINTS = [
    "<strong>After M1 (Fri ≈ 14:00):</strong> P-01's flow through SOV-01 is known, so set d1. If even 100% gives "
    "under 3.0 L/min, enter P-01's maximum in the inventory planner (sheet 03): if it passes, Case 1 still holds "
    "3.0 L/min at FT-01 on sump inventory, with the planner's pour time, pour volume and tc1. Only if it fails at "
    "P-01's maximum, lower the loop target to the highest flow it passes, and document why. If current "
    "sensing is unusable, <code>SET isok 0</code> and the diagnostics fall back to flow only.",
    "<strong>After M2 (Fri night), P-02's operating point:</strong> run the take with BV-02 open and a reduced d2 "
    "if, at the 3.0 L/min trim with P-02 at 100%, any of these holds: the pressure switch cycles; IT-02 is over "
    "2.5 × its open-valve value (about 6 bar on a comparable pump); or a 5° move of the handle shifts the flow by "
    "more than 0.3 L/min, so the trim cannot be reset between takes. Ask the organisers (follow-up message, sheet 02).",
    "<strong>After M2 (Fri night):</strong> no calibration on a weeping joint. A leak-free loop is the gate for M3.",
    "<strong>After M3 (Sat ≈ 13:00):</strong> R² and K are known and the Q1.2 and Q2.1 data exist. Freeze the FT-01 "
    "spool: anything that moves it means calibrating again.",
    "<strong>Sat 22:00 backup take:</strong> a complete single-go video exists, however rough. Sunday is for a better "
    "take, never for a first one.",
    "<strong>Sat 18:00 scope freeze:</strong> anything not passing drops down the descope ladder (sheet 10).",
]

LINELIST = [
    ("L-101", "TK-01 dip tube → SOV-01 → TEE-01 → P-01 suction", "8×5 PU; 10×8 stub at the pump", "SOV-01, TEE-01",
     "Keep it under 1 m with no kinks: this is the suction-limited line."),
    ("L-102", "P-01 discharge → TK-02 top", "8×5 PU", "–", "Aim the outlet at the wall opposite LS-01."),
    ("L-201", "TK-02 dip tube → BV-03 → P-02 suction", "8×5 PU; 10×8 stub", "BV-03", "Dip tube ends 1 cm above the floor."),
    ("L-202", "P-02 → BV-02 → FT-01 → TK-01 top", "8×5 PU", "BV-02, FT-01",
     "FT-01 at the low point; ≥ 5 cm straight before it, ≥ 2.5 cm after."),
    ("L-301", "TK-03 dip tube → BV-01 → P-03 → TEE-01", "8×5 PU; 10×8 stub", "BV-01, LSL-03 probe",
     "Tape the LSL-03 probe 2–3 mm above the dip-tube inlet. Put the tee right at the SOV-01 outlet, so the dead leg is short."),
]

IOLIST = [
    ("G33", "R_PWM1 · U2-6", "IBT-2 #1 RPWM (P-01)", "PWM out, 20 kHz", ""),
    ("G32", "L_PWM1 · U2-5", "IBT-2 #1 LPWM", "out, held LOW", "one direction only"),
    ("G26 · G13", "R_EN1 · L_EN1 · U2-4/3", "IBT-2 #1 enables", "out", "LOW 300 ms after stop"),
    ("G19", "R_PWM2 · U3-6", "IBT-2 #2 RPWM (P-02)", "PWM out", ""),
    ("G18", "L_PWM2 · U3-5", "IBT-2 #2 LPWM", "out, held LOW", ""),
    ("G17 · G16", "R_EN2 · L_EN2 · U3-4/3", "IBT-2 #2 enables", "out", ""),
    ("G25", "R_PWM3 · U4-6", "IBT-2 #3 RPWM (P-03)", "PWM out", ""),
    ("G23", "L_PWM3 · U4-5", "IBT-2 #3 LPWM", "out, held LOW", ""),
    ("G22 · G21", "R_EN3 · L_EN3 · U4-4/3", "IBT-2 #3 enables", "out", ""),
    ("G27", "SV · SOLENOID_VALVE-1", "D4184 signal → SOV-01", "out", "HIGH = open"),
    ("G14", "FS · FLOW_SENSOR-1", "FT-01 yellow, through R1/R2", "in, interrupt", "VCC pin = 5 V to the red wire"),
    ("G35", "FSW · FLOAT_SWITCH-1", "LS-01 float", "in, PCB 10 kΩ pull-up + 100 nF", "check against G34"),
    ("G34", "SW · ON/OFF_SWITCH-1", "HS-01 tactile switch", "in, PCB pull-up", "LOW = pressed"),
    ("G36", "unrouted · socket pin 3", "IS from IBT-2 #2", "ADC1", "add-on"),
    ("G39", "unrouted · socket pin 4", "IS from IBT-2 #3", "ADC1", "add-on"),
    ("G15", "unrouted · socket pin 23", "IS from IBT-2 #1", "ADC2, Wi-Fi off", "add-on"),
    ("G4", "unrouted · socket pin 26", "LSL-03 probe at the TK-03 dip-tube inlet", "touch T0", "add-on; probe GND wire beside it"),
    ("G5", "unrouted · socket pin 29", "ZSO-01 contact on BV-01", "in, internal pull-up", "optional"),
    ("G2", "on-board LED", "status LED", "out", "fast blink = open BV-01"),
    ("3V3", "socket pin 1", "IBT-2 VCC × 3", "power", "moved from 5 V"),
]

INTERLOCKS = [
    ("I-1", "LS-01 high (debounced 0.5 s), or a broken float wire", "P-01 and P-03 off, SOV-01 closed. Never bypassed.",
     "Overfill protection for TK-02."),
    ("I-2", "P-03 asked to run while P-01 is stopped or SOV-01 is open", "P-03 held off.",
     "P-03 must discharge into a running P-01 with TK-01 isolated."),
    ("I-3", "SOV-01 asked open while P-03 runs", "SOV-01 held closed.", "Flush water must never flow back into TK-01."),
    ("I-4", "No flow with low current > 5 s (dry run), or no flow with high or cycling current > 3 s (blocked)",
     "P-02 tripped. A dry-run trip retries after 10 s, up to 3 times. Partial-flow patterns only raise an event.",
     "Protects the pump and FT-01 (0.8 MPa) without letting a noisy reading stop P-02 on camera."),
    ("Boot", "Reset or brown-out", "Every driver pin goes LOW in the first statement; the NC SOV closes.",
     "Fail-safe start. The reset reason is logged."),
]

FDI = [
    ("NORMAL", "ON", "normal", "≈ baseline", "–", "none"),
    ("RESTRICTION", "ON", "reduced", "up > 8%", "Valve partly closed, kink, partial blockage (B)", "event; under FIC the extra duty is flagged"),
    ("DISCHARGE_BLOCKED", "ON", "zero", "up > 15% or cycling", "Outlet closed or blocked; pump pressure switch cycling (C)", "trip P-02 after 3 s"),
    ("SUCTION_LOSS", "ON", "zero", "down > 20%", "Dry sump, air lock, BV-03 shut (C)", "trip after 5 s, retry ×3"),
    ("PARTIAL_SUCTION", "ON", "reduced", "down > 15%", "Air leak at a suction joint, low sump (B/E)", "event only, never a trip"),
    ("PUMP_FAILURE", "ON", "zero", "≈ 0 A", "Motor, driver, fuse or wiring (C/D)", "alarm"),
    ("FT01_SIGNAL_FAILURE", "ON", "zero", "≈ baseline", "Sensor wire, connector, jammed rotor (C)", "alarm; the process keeps running"),
    ("UNSTABLE_FLOW", "ON", "intermittent", "fluctuating", "Air drawn in, cavitation, pressure switch cycling (E)", "event"),
    ("FT01_INTERMITTENT", "ON", "intermittent", "steady", "Loose connector, interference (E)", "alarm"),
    ("NO_FLOW_CAUSE_UNKNOWN", "ON", "zero", "not wired", "FT-01 alone cannot tell (C)", "shows why more data is needed"),
    ("SPURIOUS_PULSES", "OFF", "present", "0 A", "Siphoning, interference on the pulse line", "event"),
]

COMMANDS = [
    ("START · STOP · RESET", "Run the sequence, stop everything, clear alarms. The switch does the same."),
    ("MANUAL · P n duty · SOV 0/1", "Drive pump n (1–3) at a duty % and the valve directly. Interlocks stay on."),
    ("ILK 0 · ILK 1", "Bypass I-2 and I-3 for a single-pump test (MANUAL only). I-1 can never be bypassed."),
    ("CAL s duty", "Timed P-02 run into the weigh bucket. Prints C,ms,run,pulses,t,f,duty."),
    ("FIC · SET sp 3.0", "Closed-loop flow control on P-02, with P-01 on float control."),
    ("SET k v · GET · SAVE · DEFAULTS", "Read and change parameters, stored in flash."),
    ("MARK text", "Write a marker into the log. For valve positions use MARK V50."),
    ("TOUCHCAL EMPTY · TOUCHCAL WET", "Store the LSL-03 probe reading dry (EMPTY) or wet (WET)."),
    ("IZERO · ZERO · LEARN", "Zero the current offsets, clear the totalisers, re-learn the diagnosis baseline."),
    ("BURST · PINS · HDR · NEXT", "Pulse-period dump; raw inputs; CSV header; skip the rest of Case 1 (rehearsal only)."),
]

PARAMS = [
    ("a", "0.010204", "workbench (M3)"),
    ("b", "0", "workbench (M3)"),
    ("fcut", "3 Hz", "workbench (M3)"),
    ("d1", "0.50", "P-01 duty finder (M1)"),
    ("d2", "1.00", "spec: leave at 1.00 unless the M2 checkpoint rule moves Case 1 to BV-02 open (then the duty map)"),
    ("d1f · d3", "0.50 · 0.45", "M5: P-03 a little weaker than P-01 keeps the tee below atmospheric, so SOV-01 stays pressed shut"),
    ("tc1", "240 s", "<code>SET tc1 180</code> so the single take fits a 10–12 min video; pour at +60 s, or as the inventory planner says"),
    ("lshon · lshoff · p1off", "500 · 3000 · 5000 ms", "M4: float behaviour"),
    ("bvmode · tbv", "0 · 15 s", "set bvmode 1 if ZSO-01 is fitted"),
    ("tchE · tchF", "0 · 0.5", "TOUCHCAL EMPTY with the probe dry (M5)"),
    ("i3dry", "0 A", "M5: midway between P-03's wet and dry current at d3"),
    ("g1 · g2 · g3", "0.004255 A/mV", "DMM calibration (M1)"),
    ("isok", "1", "0 if current sensing is not wired"),
]

Q32 = [
    ("A", "Healthy operation.", "–", "Current at baseline, level steady."),
    ("B", "Throttled valve: the pump works against higher pressure and the flow drops.", "Partial blockage; worn pump valves.",
     "Current rises with pressure, and the flow recovers when the valve reopens."),
    ("C", "Ambiguous: blocked line, dry or air-locked pump, failed pump, or failed sensor.", "–",
     "Current high or cycling = blocked; low = dry; about 0 = pump; normal = sensor (fluid visibly moving, levels changing)."),
    ("D", "Normal: no pump, no flow.", "If the pump was commanded on: pump, driver or supply failure.", "Compare the command with the current."),
    ("E", "Unstable flow: air drawn in at low sump level or through a leaky suction joint, cavitation, or the pressure switch cycling near dead-head.",
     "Intermittent sensor signal (loose connector, interference).",
     "Current fluctuates with the flow = hydraulic. Current steady while pulses drop out = sensor."),
]

STORY = [
    ("0:00–0:20", "Title card: team ID and name, then a 5 s preview of the automatic stop", "“Establish · Measure · Detect · Diagnose · Restore”",
     "The problem statement's own five verbs. Say that is how the video is organised."),
    ("0:20–1:40", "Architecture: walk the rig with the P&amp;ID", "P&amp;ID inset; tags on the hardware",
     "Trace L-101 → L-102 → L-201/202 → L-301 aloud with the direction of flow. Name every component, as the paper asks."),
    ("1:40–2:20", "Control and safety: PCB, drivers, add-on board", "State machine and interlock table",
     "Fail-safe choices: NC SOV, float open = high, interlocks I-1 to I-4, FT-01 after BV-02 because of its 0.8 MPa rating."),
    ("2:20–3:00", "Measure: calibration montage", "Workbench fit, then the certificate",
     "Weighing as the reference; a, b, maximum and average error, repeatability; ±x % at 3 L/min; K against the datasheet."),
    ("3:00–9:00", "Establish: the SINGLE TAKE, no cuts, real speed", "Console picture-in-picture; a caption at each event",
     "Switch → Case 1 at 3.0 L/min (tc1 = 180 s) → pour → P-01 stops, P-02 runs on, P-01 restarts → Case 2: SOV shuts, LED blinks, BV-01 opened → three pumps → TK-03 empty → automatic stop. Read out the stop latency. Use Case 1's steady minutes to name the components again."),
    ("9:00–10:15", "Detect and diagnose: fault demos", "DIAG events on the console",
     "Unplug FT-01 → FT01_SIGNAL_FAILURE, process continues. Close BV-03 → SUCTION_LOSS trip. Explain why FT-01 alone cannot tell these apart (Q3.2)."),
    ("10:15–10:50", "Restore (drop first if long)", "FIC trend through a BV-02 disturbance",
     "Close BV-02 to 50%: the loop restores 3.0 L/min and flags RESTRICTION from the extra duty."),
    ("10:50–11:30", "Results card and close", "Max and average error, 3.0 ± x L/min, stop latency, valve curve; code link on screen",
     "One sentence per number. Name each team member's role. The exported file must run 10:00–12:00."),
]

JOURNEY = [
    "Film from now on, in short clips on any phone (10–30 s, landscape): each milestone as it happens, and every failure with its fix. A leak found with tissue, the P-01 bucket test that came up short, the scope trace of FT-01, the first weighed run.",
    "The kit photos taken before assembly, the dry layout, and the P&amp;ID being drawn.",
    "Each member, 15 s to camera: their role and the one decision they would defend (the decision log).",
    "Cut 3:00–4:00 on Sunday morning: problem → plan → build → what broke and how we fixed it → the rig running. Real footage only; the simulator never appears.",
]

SUBMIT = [
    "<strong>Challenge Video</strong>: MP4 (H.264 + AAC), 10:00–12:00 by the exported file's own duration. Phone clips in .mov or HEVC must be re-encoded: <code>ffmpeg -i in.mov -c:v libx264 -crf 23 -c:a aac out.mp4</code>.",
    "<strong>Journey Video</strong>: MP4, 3:00–4:00.",
    "<strong>Handwritten Solution</strong>: the 11 printed pages filled in by hand in blue or black ink, team ID and name on every page. "
    "Page 4 holds the hand-drawn P&amp;ID. Appendix pages after page 11: the printed plots and annotated photos, each with a handwritten "
    "caption, and the code link written out in full. Scan at 300 dpi into one PDF, then read every page on a phone.",
    "<strong>Code</strong>: the portal has no code field. The link goes on page 3 beside “Share the code”, in the appendix, and on the "
    "video's last card. Open it in a logged-out browser before uploading.",
    "<strong>Upload</strong>: one person, on the portal, by 16:00. A saved submission cannot be changed, so the second-person check comes first. "
    "Read the dashboard countdown on Friday: the rounds API shows the window closing 19 Oct, but 4 Oct holds until the organisers say otherwise.",
]

OPENQ = [
    ("Does P-01 at 50% move ≥ 3.3 L/min through SOV-01?", "P-01 duty finder: 4 × 30 s on the scale", "M1",
     "Use the strongest pump as P-01 and raise d1 (3.0 wins). If no duty reaches 3.0: inventory planner with P-01's maximum, "
     "then its pour time, pour volume and tc1. Last resort: loop target = the highest flow the planner passes, documented."),
    ("Where does P-02 at 100% give 3.0 L/min, and does the pressure switch cycle there?",
     "M2 dial map: 100, 75, 50, 40, 30% for 30 s each, flow and IT-02 logged", "M2",
     "Apply the M2 checkpoint rule: BV-02 open and a reduced d2 for the take; keep the 100% sweep for Q2.1."),
    ("Does any IS channel pass 1,100 mV at P-02's highest-pressure point?", "Console mV at the 30% dial point", "M2",
     "Put a resistor in parallel with that channel's IS load (halving it halves the voltage) and redo its gain."),
    ("Is FT-01's output push-pull or pull-up?", "Scope it open, then with 10 kΩ to GND", "M1", "Pick R1 and R2 from Figure 3."),
    ("Does the LSL-03 probe read clearly wet and dry?", "PINS with the probe in water, then lifted out", "M1",
     "Expose more bare wire, or move the GND wire closer. If it still fails, rely on IT-03 plus the tfmax backstop."),
    ("Does each IBT-2 have 10 kΩ on IS, and what is its real sense ratio?", "DMM: resistance to GND, then two current points", "M1",
     "Adjust the added resistor; per-channel gains g1–g3."),
    ("Does P-03's current drop clearly when it runs dry?", "Run P-03 at d3 wet, then dry, in MANUAL with ILK 0", "M5",
     "Leave i3dry at 0: LSL-03 plus the tfmax backstop still end the flush."),
    ("What is the loop's maximum flow? Is 6 L/min reachable?", "Duty map up to 100% with BV-02 open", "M2",
     "Report the measured maximum and explain it with the system curve."),
    ("How much does the sump hold at the LS-01 trip?", "Fill TK-02 on the scale", "M2", "Enter it in the inventory planner."),
    ("What is each pump's minimum starting duty?", "MANUAL ramp up from 10%", "M1", "Set a floor for d1, d3 and FIC (0.15 by default)."),
]

LADDER = [
    "FIC closed-loop demo. Keep spec mode and the valve trim.",
    "Fault demos beyond two. Keep the FT-01 unplug and the BV-02 throttle.",
    "BURST pulsation analysis and the dye transit test.",
    "The IT-01 channel and the ZSO-01 valve switch. Use the timed BV-01 window instead.",
    "The LSL-03 capacitive trip. Fall back to IT-03 current plus the tfmax backstop.",
]

TRIGGERS = [
    "A finding on sheet 01 turns out wrong at the bench.",
    "A milestone runs 50% over its estimate.",
    "The ESP32 resets when pumps start (brown-out), or FT-01 counts pulses with no flow.",
    "A leak is still open after two hours of rework.",
    "The organisers answer differently on P-01's duty, the flush destination or the single take.",
    "The portal's countdown or the organisers give a different deadline, video length or paper format.",
    "P-01's maximum through SOV-01 is under 3.0 L/min, or P-02's 3.0 L/min trim makes its switch cycle.",
]

CHANGELOG_C = (
    "C", "2 · execution realism",
    "(1) The required Q1.2 and Q2.1 data moved from optional M6 into M3, straight after calibration, and the third M5 "
    "pass is filmed as a backup take by Sat 22:00. (2) A fitting map checks every joint against the exact kit counts: "
    "all 8 male push-fits are used, so 4 spares are ordered tonight, and FT-01's 7 mm barbs need the tube softened in hot "
    "water. (3) A first-water procedure: fill by weight, then prime P-02, P-01 and P-03 in that order and bleed the "
    "meter. (4) A reset procedure (about 6 min) and a single-take run script with roles, cues, forbidden actions and "
    "abort rules. The console now shows Case 1 and Case 2 elapsed time for the pour cue. (5) A laptop readiness "
    "checklist, plus a simulated full take in the kit to practise the console and plots on.")
CHANGELOG_D = (
    "D", "3 · what the judges reward",
    "(1) A ‘How we place top 3’ sheet built on the round's own wording: real data, characterisation, calculations, "
    "plots, interpretation, and no simulations. It covers where points are won and lost, the judges' vocabulary, and "
    "Grand Finale readiness. (2) A requirements checklist traces every line of the paper to its evidence, including "
    "‘Share the code’, which the plan had missed. (3) Evidence-grade outputs: a one-page FT-01 calibration certificate, "
    "and trend plots with shaded phases and labelled events. (4) A decision log ties each design choice to the measured "
    "data behind it, plus ready-to-fill Q2.1/Q2.2/Q2.3 interpretation sentences, and the P&amp;ID now notes BV-02 as the "
    "throttling valve in place of the absent needle valve. (5) The video is re-cut around the problem statement's five "
    "verbs, with a caption for every number. The simulator stays a firmware test tool and never appears as evidence.")
CHANGELOG_E = (
    "E", "team split · Friday start",
    "(1) Sheet 02 now opens with four role cards (HY, EF, DC, IV): what each person owns in this book, their milestones, "
    "and first steps they tick off, shared with the team. The schedule starts Fri 08:00 and M1 moves to 10:00. "
    "(2) A ready-to-send organiser message and a buy-today parts list: pneumatic push-fits (PC 8-02, not RO fittings), "
    "PTFE tape, ties, a flyback diode, a drip tray, and spare ESP32, IBT-2 and YF-S401 as insurance. The pressure "
    "transducer is dropped. (3) A shared bench log on sheet 06 records what the hardware shows at M1–M5, so firmware "
    "and parameters can be tuned from real readings. (4) Software: an Arduino IDE sketch that compiles the same "
    "<code>src/main.cpp</code> (checked with arduino-cli on core 2.0.17); firmware 1.1 reports its version to the console; "
    "the console saves screenshots at the float event, the end of Case 1, the three-pump flush and the automatic stop, "
    "draws the 3.0 L/min target band, and logs the parameters of every run. (5) Printables that were referenced but "
    "missing: the BV-02 position dial and the tag and flow-arrow labels; plus a code package for the judges, without the "
    "simulator. Also corrected: the state diagram's flush-end timing (IT-03 dry for 1.5 s, as in the firmware) and its "
    "BV-01 re-prompt path, and a stale ‘LSL-03 foil’ in the run sheet. The whole book is also exported as "
    "<code>BUILD_PLAN.md</code> for reading without a browser.")
CHANGELOG_F = (
    "F", "4 · portal rules and bench physics",
    "(1) The submission now matches the LRC portal's own form: a 10–12 min Challenge Video (the storyboard is cut from 14 "
    "to 11½ min, with <code>tc1</code> 180 s), a new 3–4 min Journey Video filmed from Friday, and the paper handwritten in "
    "blue or black ink and scanned to one PDF that carries the P&amp;ID, photos, plots and code link. MP4 only, no code field, "
    "no changes after saving. A follow-up message asks the organisers about these points and the 19 Oct date in the rounds API. "
    "(2) P-02's Case 1 operating point: sprayer diaphragm pumps droop, so 3.0 L/min at 100% duty sits near 7 bar, close to the "
    "8.25 bar switch. M2 now maps P-02 against the dial with IT-02, and a checkpoint rule moves the take to BV-02 open with a "
    "reduced d2 if the switch cycles there. IS channels get a 1,100 mV ceiling and a Schottky clamp to 3V3. "
    "(3) P-01 short of 3.0 L/min: a 0.3 m tank lift buys 0.03 bar against SOV-01's 0.8–1.3 bar, so the fallback is no longer "
    "‘lower the target’. The inventory planner now takes P-01's measured flow, the pour time and tc1, and says whether "
    "Case 1 can still hold 3.0 L/min at FT-01 on sump inventory. The duty finder no longer extrapolates past the measured duties. "
    "(4) Calibration and Q2.1 follow the evidence: accept on maximum error and ±1% repeats (R² ≥ 0.995 alone passes 4–6% "
    "errors), runs of at least 1.5 kg, a 180 s against 3 × 60 s start-stop check, verification at the exact Case 1 setting, "
    "water temperature logged; Q2.1 adds 30% and 40% and predicts a gentle droop, a knee below 45% and switch cycling near 25%. "
    "Also: the dye transit needs 240 fps slow motion over at least 2 m; PTFE tape and ties are kit items, so they are spares. "
    "Sheet 04 opens with drawing E-01, a firmware connection diagram from each ESP32 pin to its device, with a table of every "
    "short form on it; it is also in the kit as a printable A3 SVG.")
CHANGELOG = [
    ("A", "–", "First full plan: contract, ground truth, seven milestones, P&amp;ID, wiring, firmware and bench tools."),
    ("B", "1 · engineering correctness",
     "(1) LSL-03 becomes a probe at the dip-tube inlet, so the flush stops exactly when TK-03 can no longer feed P-03 "
     "(the wall foil stopped with water still visible). A late BV-01 now re-prompts instead of ending the flush. "
     "(2) P-02 protective trips act only on true no-flow; partial patterns only raise an event, so noise cannot stop "
     "P-02 on camera. (3) The console no longer reboots the ESP32 when it connects. (4) The simulator showed that a "
     "1.0 L sump start never trips LS-01 on the 0.8 L pour: the sump now starts 0.2 L below the trip, and the planner "
     "checks it. (5) A software-in-the-loop simulator runs the real firmware through 5 scenarios, all passing. "
     "Also: SOV-01 is confirmed direct-acting from its label; an M1 float-jumper note; P-03 duty set so the tee stays below atmospheric."),
    CHANGELOG_C,
    CHANGELOG_D,
    CHANGELOG_E,
    CHANGELOG_F,
]

SIMRESULTS = [
    ("S1 nominal single take", "Pour at 90 s holds P-01 within 0.5 s; P-02 never stops; Case 1 mean 2.99 L/min; flush ends on LSL-03 with 0.06 L left; sump peak 3.2 L", "pass"),
    ("S2 BV-01 opened late", "P-03 dry while TK-03 is full → re-prompt instead of a false COMPLETE; flush then completes on LSL-03", "pass"),
    ("S3 float wire broken", "I-1 holds P-01 and SOV-01 off; P-02 drains the sump and trips on dry run (fail-safe)", "pass"),
    ("S4 FT-01 unplugged mid-run", "Diagnosed FT01_SIGNAL_FAILURE in 1.9 s; no trip, process continues", "pass"),
    ("S5 15% current noise", "No protective trip; P-02 never stops", "pass"),
]

FITTINGS = [
    ("SOV-01 inlet and outlet", "PU male connector ¼\" × 8 mm", "2", "PTFE on the threads; the body arrow points away from TK-01"),
    ("BV-01, BV-02, BV-03", "PU male connector ¼\" × 8 mm", "6", "Uses 8 of the kit's 8 male connectors: buy 4 spares (PC 8-02, sheet 02)"),
    ("Pump ports P-01, P-02, P-03", "10×8 blue stub (about 15 cm) + PU unequal union 10→8", "6 + 6", "Barbed ports: two zip ties per barb. Threaded ¼\" ports: brass hose nipple with a washer, then the stub"),
    ("TEE-01", "PU equal tee 8 mm", "1", "Directly at the SOV-01 outlet"),
    ("FT-01 (7 mm barbs, 4 mm bore)", "8×5 PU, end softened 60 s in about 80 °C water, pushed fully on", "2 ends", "Two zip ties each end. The 8 mm-ID blue tube is too loose; do not use it here"),
    ("Tank connections", "None: dip tubes over the rim", "0", "No drilling. Brass hose nipples (5) and washers (10) stay spare"),
    ("Tube joins and repairs", "PU equal union 8 mm", "0–2 of 5", "Spares"),
    ("8×5 PU tube", "L-101 1.2 m · L-102 1.0 · L-201 0.9 · L-202 1.6 · L-301 1.0 + dip tubes", "≈ 6 m of 9", "Cut square; keep 3 m spare for remakes"),
]

FIRSTWATER = [
    "Fill by weight (1 kg = 1 L): TK-01 3.4 L, TK-02 at the inventory planner's sump start (2.1 L by default, below the LS-01 trip), TK-03 4.2 L. BV-01 shut, BV-02 fully open, BV-03 open.",
    "Console <code>MANUAL</code>, then <code>P 2 40</code>: water goes sump → P-02 → FT-01 → TK-01. Tap the FT-01 spool until no bubbles pass and the flow reading settles. Then <code>P 2 0</code>.",
    "<code>SOV 1</code>, then <code>P 1 40</code>: TK-01 → SOV-01 → P-01 → sump. Stop at the planner's sump start. Then <code>P 1 0</code>, <code>SOV 0</code>.",
    "Open BV-01, then <code>ILK 0</code>, <code>P 1 40</code>, <code>P 3 30</code>: flush water reaches the tee and the sump. Then <code>P 3 0</code>, <code>P 1 0</code>, <code>ILK 1</code>. Shut BV-01 and refill TK-03 to 4.2 L.",
    "Check each pump moves water from IN to OUT, then wrap every joint in dry tissue and run the M2 leak test.",
    "Measure the LS-01 trip volume: pour water from a weighed jug into TK-02 until <code>lsh</code> turns 1 on the console.",
]

RESET = [
    "Console: <code>RESET</code>, then <code>ZERO</code>. Restarting the console is safe; it no longer reboots the ESP32.",
    "Restore water by weight: TK-03 to 4.2 L, TK-02 to the planner's sump start, the rest in TK-01. Weigh the pour jug again (0.8 L, or the planner's volume).",
    "BV-01 shut, BV-02 on its trim mark, BV-03 open; the LSL-03 probe under water.",
    "Dry the drip tray (a wet tray hides a new leak) and wipe any spill.",
    "Cameras rolling, console logging; say the take number on camera.",
    "Operator presses the switch once.",
]

RUNSCRIPT = [
    ("Operator", "Presses the switch once. Opens BV-01 when the LED blinks fast (Case 2 +1 s).", "Pressing the switch again: that is STOP."),
    ("Pourer", "Pours the weighed jug (0.8 L, or the planner's volume) into TK-02 at Case 1 +60 s on the console clock (or the planner's time), away from the float.", "Pouring onto the float or before the cue."),
    ("Narrator", "Names each component and the direction of flow; reads out the numbers on screen.", "Talking over the stop event."),
    ("Console watcher", "Watches state, flow and alarms; calls the abort.", "Touching the keyboard during the take."),
    ("Camera", "Locked wide shot plus close-ups on cue: pour, LED, BV-01, TK-03 running dry.", "Moving the wide shot."),
]

ABORT = ("Abort the take (STOP, reset, retake) on any drip, a pump that fails to start, a fast-blinking LED, P-01 still running "
         "3 s after the pour, or flow more than 0.2 L/min off 3.0 for over 10 s.")

WIN_SOURCES = [
    ("Unstop: Lam Research Challenge 2026", "https://unstop.com/competitions/the-lam-research-challenge-2026-e-cell-iit-bombay-x-lam-research-x-t-works-iit-bombay-1737137"),
    ("LRC 2026 (T-Works)", "https://lrc2026.tworks.in/"),
    ("2025 winners, Industrial Automation India", "https://www.industrialautomationindia.in/news/lam-research-announces-2025-systems-engineering-competition-winners"),
]

WIN_PILLARS = [
    ("Nothing missing", "Every line of the paper traced to its evidence (requirements checklist, sheet 08). A missed requirement costs more than any extra earns.",
     "Requirements checklist all ticked; a second person signs it off"),
    ("The problem statement's spine, shown live", "Establish → measure → detect → diagnose → restore. Case 1 establishes 3.0 L/min, the weighed FT-01 measures it, the pour and the fault demos are detected, the console names the cause, and P-01's restart and FIC restore the flow.",
     "Five chapter cards in the video, each followed by its evidence"),
    ("Numbers you can trust", "Weighing as the reference, repeats, the uncertainty at 3 L/min, and a calibration certificate. Every plot carries units, a caption and one line of interpretation.",
     "Certificate, calibration plot, trend plots, Q2 tables"),
    ("Judgement backed by data", "Each design choice cites the measurement that forced it (decision log below): the SOV orifice and P-01's duty, FT-01's pressure rating, the 8 mm OD, the probe height.",
     "Decision log read out in the video and written into the paper"),
    ("Execution that looks like industry", "P&amp;ID tags on the hardware, fail-safe states, interlocks, a drip tray, a tidy labelled harness, and one unbroken take with no hidden hand.",
     "Annotated photos, single take, P&amp;ID"),
]

WIN_LOSE = [
    "A required answer missing or vague: no Q2.3 table, no R², no Q3.2 for every condition.",
    "A demo with a hidden hand: anything touched in Cases 1–2 other than BV-01.",
    "Plots without units, captions or interpretation; screenshots unreadable at 1080p.",
    "Simulated, estimated or invented numbers presented as data. The round says “no simulations”: every submitted number comes from the rig.",
    "Leaks, dangling wires or wet electronics anywhere in frame.",
    "Buzzwords without evidence (“AI”, “smart”, “state of the art”). Name the method and show its result.",
    "A Challenge Video outside 10–12 minutes, no Journey Video, a typed paper, or a file the portal rejects (only MP4 and a scanned PDF). Weak audio, or a component never named.",
    "No code link in the PDF and on the video, although the paper asks for the code and the portal has no field for it.",
]

WIN_VOCAB = [
    ("FDC (fault detection and classification)", "the diagnosis layer that names a fault from flow and current signatures"),
    ("Interlock · permissive · fail-safe", "I-1 to I-4; the NC valve and float wiring that fail to the safe state"),
    ("Installed vs inherent characteristic", "why BV-02's curve droops gently, then falls steeply once the valve's drop nears the pump's pressure limit"),
    ("K-factor · turndown · uncertainty (k = 2)", "what the calibration certificate reports"),
    ("Residence time · RTD · dead leg", "Q3.1, the mixed-sump washout, the short tee branch"),
]

FINALE = [
    "Rebuild drill: strip and rebuild the loop from the fitting map against the clock. Target under 60 minutes.",
    "One-page quick reference: pin map, console commands, parameters and the first-water order.",
    "Troubleshooting drill: inject each fault from sheet 05 and clear it against the clock.",
    "Keep the firmware generic: calibration and duties are parameters (SET/SAVE), never hard-coded.",
    "Each member explains one design trade-off in 60 seconds, from memory.",
]

DECISIONS = [
    ("P-01 duty d1 = ___ %", "P-01 duty finder: Q at 50% = ___ L/min, below the 3.3 needed; maximum ___ L/min at 100%. SOV-01's orifice (Cv ≈ 0.23) costs ≈ 0.8 bar on the suction side, which a 0.3 m tank lift cannot offset.", "Video 1:40; paper Q1.1 notes"),
    ("P-02 at ___ % with BV-02 at ___ %", "Dial map: 3.0 L/min at 100% needs BV-02 at ___ %, with IT-02 = ___ A (___ × open) and the switch cycling yes / no.", "Q2.1 plot; video 1:40"),
    ("FT-01 after BV-02", "FT-01 is rated 0.8 MPa; the pumps dead-head at 8.25 bar.", "P&amp;ID note 2"),
    ("Calibrated in place", "Measured K = ___ pulses/L against the datasheet's 5,880 (___ %).", "Certificate; Q2.2"),
    ("Top-entry dip tubes", "No wall penetration below the liquid except LS-01, so no leak path at the joints.", "P&amp;ID note 1; photos"),
    ("LSL-03 at the dip-tube inlet", "Trips with under 0.1 L left in TK-03 (event log), against about 0.4 L for a wall foil.", "Single take; M5 log"),
    ("Sump starts at ___ L, pour ___ L at +___ s", "LS-01 trip volume measured as ___ L and P-01 at ___ L/min: the float must not trip before the pour, the pour must cross it, and the sump must stay above its minimum to the end of Case 1.", "Inventory planner"),
    ("Velocities use the 5 mm bore", "Calipers: ID = ___ mm. At 3 L/min, v = 2.55 m/s, not 0.99 m/s.", "Q1.2"),
]

Q2TEXT = [
    ("Q2.1", "% open is the handle angle (90° = 100%). Between 100% and about 50% the flow falls only a little: the ball valve's own curve is quick-opening, so its drop is small, and the loss that does appear comes from the pump curve drooping as discharge pressure rises (P-02's current climbs with it). Below about 45% the valve's drop approaches the pump's limit and the flow falls steeply; near 25% the pressure switch cycles, so that point is a mean of on and off periods. 70% and 75% read almost the same, which is why 40% and 30% were added. This is the installed characteristic: valve and pump together, not the valve alone."),
    ("Q2.2", "a = ___ L/min per Hz, so K = 60/a = ___ pulses/L (___ % from the datasheet's 5,880). b = ___ L/min is the small flow needed before the rotor turns, which is why the firmware reports zero below fcut. R² = ___: FT-01 is linear over 1–___ L/min, and its largest error sits at the lowest flow, where the rotor slips most."),
    ("Q2.3", "f = N/t and Q = V/t share one ESP32-timed window. V comes from the weighed mass at ρ = 1000 g/L as given. At the measured water temperature of ___ °C, water is ___ g/L (996.2 at 28 °C); with air buoyancy (+0.1%) that would raise Q by about 0.5%, well inside the calibration error."),
]

TEAM_NOTE = ("<strong>08:00 stand-up, 10 minutes:</strong> write a name on each role, read the objective and the done-when "
             "together, and agree the four checkpoint times. The rig and the scale are shared: book them in the run sheet.")

TEAM = [
    dict(code="HY", role="Hydraulics lead",
         fit="The most hands-on, patient member. Owns every joint, every tube and every litre of water.",
         owns=[("#hydraulics", "03 Hydraulics: P&amp;ID, line list, fitting map, first water, inventory planner"),
               ("#video", "09 Video: the 0.8 L pour and the reset between runs"),
               ("#checklists", "08 Checklists: M2 hydraulic commissioning")],
         ms="M2 lead · M1 P-01 bucket tests · M3 bucket and BV-02 moves · M4 pour · M5 resets · M6 dye transit",
         first=[("fs-hy-count", "Count every kit part against the fitting map (sheet 03). Give IV anything short before the parts run."),
                ("fs-hy-bore", "Measure the tube bore and the FT-01 barbs; enter both in the bench log (sheet 06)."),
                ("fs-hy-stand", "Put the drip tray down. Raise TK-01 and TK-03 on stands so their water sits above the pump inlets."),
                ("fs-hy-layout", "Lay the loop out dry to the P&amp;ID. Cut tubes to the line-list lengths only after the layout is checked."),
                ("fs-hy-m1", "10:00: bucket on the scale and water ready for the P-01 test (M1).")],
         hands="A leak-free loop to DC for calibration (Sat 08:00); the reset routine to the take crew."),
    dict(code="EF", role="Electronics and firmware lead",
         fit="Whoever solders cleanly and is at home in a serial console. Owns everything electrical and the code on the ESP32.",
         owns=[("#electrical", "04 Electrical: power, wiring, add-on board, I/O list"),
               ("#control", "05 Control: state machine, interlocks, diagnostics, commands, parameters"),
               ("#checklists", "08 Checklists: power-off check, M1 bring-up, M4 and M5 acceptance")],
         ms="M1 lead · M4 and M5 lead · console operator in every take · M6 fault demos and FIC",
         first=[("fs-ef-flash", "Flash the bare ESP32 over USB, no 12 V: <code>pio run -t upload</code>, or the Arduino IDE sketch on core 2.0.17. "
                                "Start the console; check <code>fw=1.1</code>, then <code>PINS</code>."),
                ("fs-ef-addon", "Solder the add-on board (sheet 04): three IS channels, FT-01 divider pads, the LSL-03 probe lead."),
                ("fs-ef-is", "DMM: measure each IBT-2's IS resistor to GND, unpowered; enter the values in the bench log."),
                ("fs-ef-poweroff", "Run the power-off check (sheet 08), then apply 12 V with no pumps connected."),
                ("fs-ef-m1", "10:00: start M1. Connect LS-01, or jumper FSW to GND, before any pump test.")],
         hands="d1 after M1; a, b and fcut saved after M3; every changed parameter written in the bench log."),
    dict(code="DC", role="Data and calibration lead",
         fit="The member most careful with numbers and comfortable with Python. Owns every number that reaches the paper.",
         owns=[("#calibration", "06 Bench log and calibration: bench log, workbench, P-01 duty finder"),
               ("#answers", "07 Answers: Q1.2, Q2.1–Q2.3, Q3.1, decision log"),
               ("#checklists", "08 Checklists: laptop readiness, M3 calibration")],
         ms="M3 lead · M1 duty finder · Q1.2 and Q2.1 data · M6 analysis",
         first=[("fs-dc-laptops", "Console laptop plus one spare: USB driver (CP210x or CH340), Python 3.10+, "
                                  "<code>pip install -r tools/requirements.txt</code>."),
                ("fs-dc-replay", "Practise on the simulated take: <code>rig_console.py --replay</code>, type <code>SHOT</code>, then "
                                 "<code>analyze_run.py trend</code>. Practice only; never submit it."),
                ("fs-dc-scale", "Weigh station: bucket on the 1 g scale, the tare routine, and a jug holding exactly 800 g of water for the pour."),
                ("fs-dc-m1", "10:00: run the P-01 duty finder (sheet 06) with EF and HY, and keep the bench log.")],
         hands="a, b and fcut to EF after M3; final numbers and plots to IV by Sun 12:00."),
    dict(code="IV", role="Integration, video and submission lead",
         fit="The team's organiser. Owns the clock, the evidence and the upload.",
         owns=[("#win", "00 Top 3 strategy, and the checkpoint calls on this sheet"),
               ("#video", "09 Video: storyboard, run script, abort rule"),
               ("#checklists", "08 Checklists: requirements coverage and M7 submission"),
               ("#downloads", "11 Downloads: printables and the code to share")],
         ms="M7 lead · checkpoint calls · photos · final P&amp;ID · paper · upload",
         first=[("fs-iv-portal", "Log in to the LRC portal and read the Hardware Hustle form and countdown: three files (Journey MP4 3–4 min, "
                                 "Challenge MP4 10–12 min, handwritten PDF). Start filming Journey clips today, then send the follow-up message below."),
                ("fs-iv-org", "Send the organiser message below (copy button)."),
                ("fs-iv-share", "Share this build book with the other three (Share menu), so ticks, the workbench and the bench log are shared."),
                ("fs-iv-parts", "Parts run when shops open: the buy-today list below, plus anything short from HY's count."),
                ("fs-iv-print", "Print the tag labels, the BV-02 dial (both at 100% scale) and the P&amp;ID at A3 (sheet 11). "
                                "Photograph the kit before assembly."),
                ("fs-iv-draft", "Draft the Q3.1 and Q3.2 answers and the shot list. No hardware needed.")],
         hands="Calls the checkpoints (Fri 14:00, Sat 13:00, Sat 18:00, Sat 22:00). Before upload, a second person checks the submission."),
]

ORG_MSG = """Subject: Stage 2 Hardware Hustle: clarifications from Team [Team ID] ([Team name])

Hello LRC team,

We are building the Stage 2 rig and have five quick questions. Short answers are fine.

1. Pump-01 duty. Case 1 sets Pump-01 at 50%. The on/off valve sits in Pump-01's suction line, so at 50% Pump-01 may deliver less than Pump-02 drains at 100%. If our measurements show this, may we raise Pump-01's duty and justify it with the data, or must it stay at exactly 50%?

2. Video. Case 1 and Case 2 will run in one go, as required. Must that run be one uncut shot? May the 10-15 minute video also include separately recorded segments, such as calibration, the valve test and fault demonstrations?

3. Software. The hardware list mentions data-acquisition software. Is there an official program we must use, or may we use our own ESP32 firmware and laptop logger? We will share all of the code.

4. Additions. May we add small parts that do not modify the kit or the custom PCB: a perfboard with resistors and capacitors for signal conditioning, a bare-wire level probe in the flush tank, spare push-fit fittings, and stands to raise the tanks?

5. Submission. What is the exact deadline (date, time and time zone), and where do we upload? Are Drive or YouTube links acceptable for the video, and a GitHub or Drive link for the code? May the paper be typed, with extra pages for graphs?

Unless you advise otherwise, we will also:
a. Use ball valve BV-02 as the throttling valve, since the kit has no needle valve, and show it on the P&ID.
b. Return the flush water to the 10 L tank through Pump-02 and FT-01, the only return path.
c. Run Case 1 for a fixed time (about 4 minutes, including the external-fluid event), then start Case 2 automatically.
d. Report the measured maximum flow in Q1.2 if 6 L/min cannot be reached with the kit.
e. Record Q2.1 at both 70% and 75%, because the question text and the table differ.
f. Calculate the Q3.1 residence time as V/Q (12 s), and note that Q/V gives a rate rather than a time.
g. Not drill or modify any kit part. The tanks are fed by dip tubes over the rim.

Thank you,
[Your name], Team [Team ID]"""

ORG_MSG2 = """Subject: Stage 2 Hardware Hustle: follow-up from Team [Team ID] ([Team name])

Hello LRC team,

Four short follow-ups after reading the portal's submission form.

1. Video length. The paper asks for 10-15 minutes and the portal for a 10-12 minute Challenge Video. We will keep it within 10-12 minutes. Is that right?

2. Handwritten solution. We will write every answer by hand in blue or black ink. May we paste printed plots and photos onto the pages, or add printed appendix pages with handwritten captions, and include the P&ID drawn by hand on page 4?

3. Code. The form has no code upload. Is a GitHub or Drive link written in the PDF and shown in the video enough?

4. Deadline and Pump-02. The portal lists the round until 19 October; we are working to Sunday 4 October, 18:00 IST. Which is binding? And Case 1 sets Pump-02 at 100% while asking for 3 L/min. If holding 3 L/min at 100% means throttling the ball valve until the pump's pressure switch cycles, may we run Pump-02 at a lower duty with the valve open, and show the data?

Thank you,
[Your name], Team [Team ID]"""

PARTS = [
    ("Push-in male straight connector, 8 mm tube × ¼\" BSPT (pneumatic code PC 8-02)", "4",
     "Spares. All 8 in the kit are used (SOV-01 and the three ball valves), so one cracked fitting would stop M2.",
     "Pneumatic or industrial fittings shop. Not an RO shop: RO fittings take ¼\" (6.35 mm) tube and do not fit 8 mm."),
    ("Push-in equal tee, 8 mm (PE 8)", "1", "Spare for TEE-01; the kit has only one.", "Same shop"),
    ("PTFE thread tape", "1 roll", "Spare: the kit has one roll (item 43) for the 8 threaded joints.", "Hardware or plumbing shop"),
    ("Small cable ties, 100–150 mm", "1 pack", "Spare: the kit has one pack (item 41); two per barbed joint on six pump ports and both ends of FT-01.", "Hardware or electrical shop"),
    ("1N5819 or 1N4007 diode", "2", "Flyback across the SOV-01 coil. Only needed if the valve driver has none (check first).", "Electronics shop"),
    ("BAT85 or BAT43 small-signal Schottky diode", "3", "Clamp each IS pin (G15, G36, G39) to 3V3, cathode to 3V3. Not a 1N5819: its leakage through the 12 kΩ source would shift the reading.", "Electronics shop"),
    ("Drip tray the size of the rig, or a shallow storage-box lid", "1", "Keeps a leak away from the SMPS and PCB.", "Home or hardware store"),
    ("Phone tripod or clamp", "1", "Only if you have none: the single take needs a locked wide shot.", "Mobile or electronics shop"),
    ("<em>Insurance:</em> ESP32 NodeMCU-32S, 38-pin (same pinout as U7)", "1",
     "U7 sits in a socket, so if the ESP32 dies, a swap and reflash takes 5 minutes.", "Electronics shop, or next-day delivery"),
    ("<em>Insurance:</em> BTS7960 (IBT-2) driver module", "1", "A driver can fail on a stall or a short, and Case 2 needs all three.",
     "Electronics shop, or next-day delivery"),
    ("<em>Insurance:</em> YF-S401 flow sensor", "1", "If FT-01 fails after calibration: swap it and recalibrate (about 2 h).",
     "Electronics shop, or next-day delivery"),
]
PARTS_NOTE = ("Buy everything not marked insurance today: M2 needs the fittings on Friday afternoon, and the clamp diodes go on "
              "before M2's dial map drives P-02 to its highest current. Anything ordered online today arrives "
              "Saturday at the earliest, so online is only for the insurance items. The pressure transducer is dropped.")

BENCH = [
    ("b-bore", "Tube bore, 8 mm blue tube", "Calipers on a square-cut end, or the largest drill-bit shank that slides in (mm)", "Fri 08", "HY"),
    ("b-barb", "FT-01 barb outside diameter and bore", "Calipers (mm). Decides how the tube goes on.", "Fri 08", "HY"),
    ("b-isr", "IBT-2 IS resistor to GND, boards 1 / 2 / 3", "DMM, unpowered, IS pin to GND (kΩ)", "Fri 09", "EF"),
    ("b-ftout", "FT-01 output: push-pull or pull-up; high level open and with 10 kΩ to GND", "Scope while blowing gently through the meter (V)", "M1", "EF"),
    ("b-brown", "ESP32 reset when all three pumps start together?", "Watch for a BOOT event in the console (yes or no)", "M1", "EF"),
    ("b-glitch", "Glitch count over 60 s with the pumps on and FT-01 dry", "Console <code>glitches</code> column, start and end", "M1", "EF"),
    ("b-mind", "Minimum starting duty, P-01 / P-02 / P-03", "MANUAL, ramp up from 10% (%)", "M1", "EF"),
    ("b-isgain", "Current gains g1 / g2 / g3", "DMM in series against the console reading, at two duties (A/mV)", "M1", "EF"),
    ("b-p1", "P-01 flow through SOV-01 at 50 / 60 / 70 / 100%", "P-01 duty finder on this sheet (L/min)", "M1", "DC"),
    ("b-touch", "LSL-03 probe reading, dry / wet", "<code>PINS</code>: the touch value out of water and in water", "M1", "EF"),
    ("b-trip", "Sump volume at the LS-01 trip", "Pour from a weighed jug until <code>lsh</code> turns 1 (L)", "M2", "HY"),
    ("b-qmax", "Maximum loop flow, P-02 at 100%, BV-02 open", "Console, mean over 30 s (L/min)", "M2", "DC"),
    ("b-p2map", "P-02 at 100%: flow and IT-02 at BV-02 100 / 75 / 50 / 40 / 30%; does the switch click?", "30 s each, console means (L/min, A)", "M2", "DC"),
    ("b-ismax", "Highest IS reading on each channel (P-02 at the 30% dial point)", "Console mV; must stay under 1,100 mV", "M2", "EF"),
    ("b-bv02", "BV-02 position that gives 3.0 L/min with P-02 at 100%", "Dial reading (%), checked over 3 min", "M4", "DC"),
    ("b-wtemp", "Water temperature during calibration", "DMM thermocouple, or a kitchen thermometer (°C)", "M3", "DC"),
    ("b-i3", "P-03 current wet / dry at d3", "MANUAL with <code>ILK 0</code>, then lift the dip tube out (A)", "M5", "EF"),
    ("b-note", "Anything that surprised you", "Free text: what happened, when, and what you changed", "any", "all"),
]

TAGS = [
    ("TK-01", "Process tank · 10 L"), ("TK-02", "Sump · 4.2 L"), ("TK-03", "Flush tank · 4.2 L"),
    ("P-01", "Transfer pump · TK-01 → sump"), ("P-02", "Return pump · sump → TK-01"), ("P-03", "Flush pump"),
    ("SOV-01", "On/off valve · NC"), ("BV-01", "Flush isolation · manual"), ("BV-02", "Throttle valve"),
    ("BV-03", "Sump outlet isolation"), ("FT-01", "Flow transmitter"), ("LS-01", "Sump high-level float"),
    ("LSL-03", "Flush tank empty probe"), ("TEE-01", "Equal tee · flush inlet"), ("HS-01", "Start/stop switch"),
    ("UC-01", "ESP32 controller (PCB)"), ("P-01 DRV", "Pump driver · IBT-2"), ("P-02 DRV", "Pump driver · IBT-2"),
    ("P-03 DRV", "Pump driver · IBT-2"), ("PSU-01", "12 V DC SMPS"), ("SOV-01 DRV", "Valve driver"),
]
LINEFLAGS = [
    ("L-101", "TK-01 → SOV-01 → P-01"), ("L-102", "P-01 → sump"), ("L-201", "Sump → P-02"),
    ("L-202", "P-02 → FT-01 → TK-01"), ("L-301", "TK-03 → P-03 → TEE-01"),
]

GLOSSARY = [
    ("3V3", "3.3-volt supply rail", "ESP32 pin 1; powers the logic (VCC) of all three IBT-2s"),
    ("5V · VCC", "5-volt rail · VCC = positive supply voltage (from “voltage at the common collector”)", "LM2596 output; feeds the ESP32 5V pin, the FT-01 red wire and the valve-driver logic"),
    ("ADC · ADC1 · ADC2", "Analog-to-Digital Converter, units 1 and 2", "reads the three IS current signals; ADC2 (G15) works only with Wi-Fi off"),
    ("B+ · B−", "supply (battery) positive and negative terminals", "12 V into each IBT-2 from P1–P3"),
    ("BAT85", "small-signal Schottky diode (part number)", "clamps each IS pin to 3V3 on the add-on board"),
    ("BTS7960", "Infineon high-current half-bridge IC (part number)", "two per IBT-2, together one H-bridge"),
    ("BV", "Ball Valve", "BV-01 flush isolation, BV-02 throttle, BV-03 sump outlet"),
    ("D4184", "MOSFET switch module, named after its AOD4184 transistor", "switches 12 V to the SOV-01 coil"),
    ("EN · R_EN · L_EN", "Enable, right and left half-bridge", "HIGH lets the IBT-2 drive; LOW 300 ms after a stop"),
    ("ESP32 · NodeMCU-32S · U7", "Espressif ESP32 microcontroller on a NodeMCU-32S development board; U7 is its socket on the PCB", "runs the firmware"),
    ("F3", "Fuse 3 on the PCB", "protects every 12 V load; at least 15 A"),
    ("FS", "Flow Sensor (PCB net name)", "FLOW_SENSOR connector pin 1 → G14"),
    ("FSW", "Float SWitch (PCB net name)", "FLOAT_SWITCH connector pin 1 → G35"),
    ("FT", "Flow Transmitter (ISA-5.1 letters)", "FT-01, the YF-S401 on the return line"),
    ("G14, G33 …", "GPIO number", "G14 = GPIO 14"),
    ("GND", "Ground, the 0 V reference", "common to the PCB, every IBT-2, the D4184 and the sensors"),
    ("GPIO", "General-Purpose Input/Output", "each ESP32 pin the firmware drives or reads"),
    ("HS", "Hand Switch (ISA-5.1)", "HS-01, the start/stop push button"),
    ("IBT-2", "module name, no expansion: a motor-driver board built from two BTS7960s", "one per pump"),
    ("IS · R_IS · L_IS", "current-Sense output, right and left half-bridge", "tied together and read as pump current"),
    ("IT", "current (I) Transmitter (ISA-5.1)", "IT-01 to IT-03, the three pump-current channels"),
    ("JST XH", "Japan Solderless Terminal, XH series connector (2.5 mm pitch)", "every PCB signal connector"),
    ("LDO", "Low-DropOut regulator", "the ESP32 board's 3.3 V regulator"),
    ("LED", "Light-Emitting Diode", "on-board LED on G2"),
    ("LM2596", "step-down (buck) regulator IC (part number)", "makes the 5 V rail from 12 V"),
    ("LS · LSH · LSL", "Level Switch · Level Switch High · Level Switch Low (ISA-5.1)", "LS-01 (LSH-01) sump float; LSL-03 flush-tank probe"),
    ("M+ · M−", "motor output terminals", "IBT-2 output to its pump"),
    ("MOSFET", "Metal-Oxide-Semiconductor Field-Effect Transistor", "the switch inside the D4184"),
    ("NC", "Normally Closed", "SOV-01 shuts when unpowered, so a fault isolates TK-01"),
    ("P-01 to P-03", "Pump", "P-01 transfer, P-02 return, P-03 flush"),
    ("P1 to P5", "PCB 12 V output connectors", "P1–P3 to the IBT-2s, P4 to the D4184"),
    ("PCB", "Printed Circuit Board", "the T-Works control board"),
    ("PWM · RPWM · LPWM", "Pulse-Width Modulation; right and left PWM inputs", "RPWM sets pump speed at 20 kHz; LPWM is held LOW"),
    ("SMPS", "Switched-Mode Power Supply", "12 V, 29 A, mains in"),
    ("SOV", "Solenoid-Operated Valve", "SOV-01 on P-01's suction"),
    ("SV", "Solenoid Valve (PCB net name)", "SOLENOID_VALVE connector pin 1 ← G27"),
    ("SW", "SWitch (PCB net name)", "ON/OFF_SWITCH connector pin 1 → G34"),
    ("T0", "Touch channel 0 of the ESP32", "G4, the LSL-03 probe"),
    ("TK", "TanK", "TK-01 process, TK-02 sump, TK-03 flush"),
    ("TVS", "Transient-Voltage-Suppression diode", "5KP15A at the 12 V input"),
    ("U2 · U3 · U4", "PCB 6-pin driver headers", "one per IBT-2"),
    ("YF-S401", "Hall-effect rotor flow-sensor model", "FT-01"),
    ("ZSO", "position (Z) Switch, Open (ISA-5.1)", "ZSO-01, optional contact that closes when BV-01 is open"),
]
