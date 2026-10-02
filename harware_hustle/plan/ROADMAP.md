# LAM Stage 2 flow rig: roadmap (rev F · portal rules, pump physics, P-01 fallback)

**Objective:** **By Sunday 4 October, 18:00 IST, upload the three files the LRC portal requires: a 10–12 minute Challenge Video (MP4), a 3–4 minute Journey Video (MP4) and the solution handwritten in blue or black ink, scanned to one PDF that also carries the ISA-5.1 P&ID, the labelled photos, the plots and the code link.** Together they must show a leak-free, ESP32-automated rig that runs Case 1 into Case 2 in one go, holds 3.0 L/min on an FT-01 calibrated in place by weighing, and stops within about one second of the flush tank running dry.
**Done when:** The single-take run (switch press → Case 1 with the external-fluid event → automatic Case 2 → automatic stop) passes three rehearsals in a row and is on video. Calibration maximum error ≤ 3% with repeats within ±1%, and R², a, b and average error reported. Every Task 1–3 question has measured data and a graph.
**Not doing:** (1) Wi-Fi, web or cloud dashboards. ADC2 dies with Wi-Fi on, and USB is safer on camera. (2) A machine-learning fault classifier. There is no training data, and a rule table is explainable. (3) Touching the FT-01 spool after calibration, or any tubing that arrives after Friday. (4) The pressure transducer: ordered on Friday it arrives too late to install and validate. (5) Rework of the custom PCB. All additions go on a small add-on board.
**Constraints:** About 2.5 build days. One rig and one scale are shared by everyone. Kit plus passives on hand. Online parts take 1–3 days, so they can only be upgrades. Pumps cut out at 8.25 bar. FT-01 is rated 0.8 MPa, and the PU tube and push-fits about 0.8–1 MPa. The portal takes exactly three files, all required, MP4 or PDF only, and none can be changed after saving. It has no field for code, photos or the P&ID, so they go inside the PDF and the video.

---

## Ground truth

- The LRC team portal's Hardware Hustle form asks for three uploads, each required: a Journey Video (MP4, 3–4 min, “your team's efforts and prototype development journey”), a Challenge Video (MP4, 10–12 min) and a Handwritten Solution (scanned PDF, “written using blue or black ink”). It accepts only MP4, has no code field, and warns that a saved submission cannot be changed. Its public rounds API lists the round as 29 Sep – 19 Oct. → Cut the Challenge Video to 11½ minutes, film a Journey Video from Friday onwards, write the paper by hand and scan it, and put the code link, photos and P&ID inside the PDF. Keep 4 Oct as the deadline unless the dashboard countdown or the organisers say otherwise.
- A 12 V sprayer diaphragm pump is not a flat positive-displacement source. A comparable 3-chamber pump (Shurflo 8000-543-238) gives 6.8 L/min open, 5.0 at 2.8 bar and 3.6 at 6.9 bar, while its current rises from 3.0 to 8.7 A. Scaled to our 6.1 L/min pump, P-02 at 100% reaches 3.0 L/min only at about 7 bar: near its 8.25 bar switch and the tube's rating. → Map P-02 at 100% against the BV-02 dial with IT-02 at M2. If the 3.0 L/min trim makes the switch cycle, hold 3.0 L/min with BV-02 open and a reduced d2 instead, and show the data. Keep the 100% sweep as the Q2.1 evidence.
- FT-01 is a YF-S401: 5,880 pulses per litre (F = 98·Q), 0.3–6 L/min, ±10% uncalibrated, output high above 4.5 V on a 5 V supply, rated 0.8 MPa. → Level-shift the pulse to 3.3 V before G14. Mount FT-01 after BV-02 so it never sees the pumps' 8.25 bar cut-off. Calibrate it in place.
- The paper's “8 mm pipe” is the tube's outside diameter. The kit tube is 8 mm OD × 5 mm ID, so 3 L/min runs at 2.55 m/s (Re ≈ 12,700), not 0.99 m/s, with about 19 kPa of friction per metre. → Measure the bore with calipers on day one and use it in Q1.2. Expect the loop's maximum to fall short of 6 L/min, and explain why with the pump and system curves.
- SOV-01's label reads 0–10 kg/cm², so it is a zero-differential (direct-acting) valve and will open on P-01's suction side. ¼-inch valves of this class (e.g. 2W025-08) have a 2.5 mm orifice (Cv ≈ 0.23), which costs about 0.8 bar at 3 L/min (1.3 bar at Kv 0.16), all of it on the suction side. Raising TK-01 by 0.3 m adds only 0.03 bar, so it helps priming, not this loss. P-01 may cavitate somewhere near 1.5–2.5 L/min at any duty. → Test P-01's flow through SOV-01 in hour one and use the strongest pump as P-01. If 50% duty cannot carry 3.0 L/min, raise the duty and show the data (3.0 L/min wins). If no duty reaches 3.0, run Case 1 on sump inventory with the planner's settings (sheet 03), so FT-01 still holds 3.0 L/min.
- Each IBT-2 IS pin has 10 kΩ to GND (5 kΩ when the two are tied), giving 0.59 V/A nominal. The BTS7960 sense ratio spreads from 3,000 to 14,000, so a pin can see 8 V. The 74HC244 buffer powered at 5 V needs about 3.5 V for a logic HIGH. → Add 3.3 kΩ (about 2 kΩ total, 0.24 V/A), then 10 kΩ in series and 100 nF at the pin, with a small Schottky (BAT85) from the pin to 3V3 so a driver fault (4–7 mA) cannot push the pin above 3.3 V. Calibrate each channel against the DMM. The 2.5 dB range ends at 1.25 V, and one measured IBT-2 (k ≈ 6,100) reaches it at about 4 A. Keep every channel under 1,100 mV at P-02's highest-pressure point. Power the IBT-2 VCC from 3.3 V.
- Rotor meters read high in pulsating flow (up to +5.5% in small liquid turbine meters), and the error changes with the pulsation's frequency and amplitude. A hall flow sensor's frequency also depends on the pipe attached to it and on its orientation. → Calibrate with P-02 pumping through the final installed spool, so the pulsation and plumbing are the real ones. Freeze that spool afterwards. Verify at the exact Case 1 setting (P-02 duty and BV-02 position), because the calibration runs vary the duty and so change the pulsation.
- Static weighing (ISO 4185) is a primary method for calibrating flow meters, provided the line runs full. In start-stop runs the scale is not the problem (1 g is 0.04% of 2.5 kg). The errors are fixed amounts per run: pump ramp and rotor slip at each end, drips, and water held in the outlet tube. They weigh most in short low-flow runs. R² ≥ 0.995 can still pass with 4–6% point errors, so it is a weak acceptance test. → Calibrate by weight on the 1 g scale, with each run at least 1.5 kg. The ESP32 times each run itself, so the pulse count and the collected mass share one window. Accept on maximum error and repeatability, and report R².
- ESP32 touch sensing works through a plastic wall, but the threshold is specific to each placement and the reading drifts. A foil on the wall also trips while water still covers the pickup, so on camera the system would stop with the tank visibly unfinished. → Make LSL-03 a bare-wire probe on the touch pin, taped at the dip-tube inlet. It goes dry exactly when P-03 can no longer draw. Re-capture the wet reading every run. P-03's current then separates “empty” from “BV-01 still shut”, and a timeout backs both up.
- ADC2 cannot be read while Wi-Fi is on, and only G36 and G39 are free ADC1 pins on this PCB. → Keep Wi-Fi off and stream telemetry over USB to the laptop console. G15 (ADC2) carries the third current channel.

---

## Critical path

Roughly 2.5 days. M1 → M2 → M3 → M4 → M5 → M7; M6 runs alongside and can slip.

### M1 — Rig physics proven on the bench  (EF with HY, Fri 10–14)
- **Do:** Connect LS-01 first (or jumper FSW to GND): an open float input reads “sump high” and I-1 blocks P-01 and P-03. Run the power-off checks, then apply 12 V. Drive the three IBT-2s and the D4184 from the console (`MANUAL`, `P n duty`, `SOV 1`). Pump TK-01 → SOV-01 → P-01 into the bucket on the scale at 50, 60, 70 and 100% for 30 s each, using the P-01 duty finder. Scope the FT-01 output with and without a 10 kΩ load. Check every input with `PINS`. Calibrate IS against the DMM in series.
- **Done when:** All three pumps start together (staggered) with no ESP32 reset. FT-01 at G14 is ≤ 3.3 V with clean edges, and the glitch count stays flat with the pumps running and FT-01 dry. The P-01 Q(duty) table exists and d1 is chosen to give ≥ 3.3 L/min, or, if no duty reaches 3.0, P-01's measured maximum is in the inventory planner and its Case 1 settings are chosen.
- **Retires:** SOV-01 starving P-01; 3.3 V logic into the IBT-2; motor noise in the pulse count; brown-out.
- **Est:** half a day (confidence: medium)

### M2 — Leak-free loop that matches the P&ID  (HY, Fri 14–24)
- **Do:** Build to Figure 1: dip tubes, raised TK-01 and TK-03, the FT-01 spool with its straight runs, the BV-02 dial, and P&ID tags and flow arrows on everything. Prime the loop, then run the leak test. Then map P-02 at 100% against the BV-02 dial (100, 75, 50, 40, 30%), 30 s each, logging flow and IT-02, and listen for the pressure switch clicking.
- **Done when:** 10 min at 3 L/min plus 2 min at BV-02 25% with zero wet tissue. No bubbles in the FT-01 spool. Flow CV under 3% over one minute. The LS-01 trip volume is measured. The dial position for 3.0 L/min at 100% is known, with IT-02 there and whether the switch cycles.
- **Retires:** Leaks, air in the meter, wrong routing.
- **Est:** half a day (confidence: medium)

### M3 — FT-01 calibrated and the required data recorded  (DC, Sat 08–13)
- **Do:** Do 15 gravimetric `CAL` runs (5 flows × 3, each ≥ 1.5 kg) and enter them in the workbench. Load a, b and fcut, verify at the exact Case 1 setting, then freeze the spool. Straight after, while the rig is set up, record the paper's required data: the BV-02 sweep (Q2.1) and the runs at about 1, 3 and maximum L/min (Q1.2).
- **Done when:** Maximum error ≤ 3% and repeats within ±1% at each flow; R² reported. Verification at the Case 1 setting within ±2% of the scale. The Q2.1 table (25/30/40/50/70/75/100%) and the Q1.2 table hold measured values, with plots saved.
- **Retires:** Calibration accuracy (team worry 2), and the risk of reaching Sunday with required answers still empty.
- **Est:** 5 h (confidence: high)

### M4 — Case 1 passes acceptance  (EF, Fri 20–24 dry · Sat 12–15 wet)
- **Do:** Set d1, then trim BV-02 so that P-02 at 100% gives 3.0 L/min. If the switch cycles there (IT-02 drops out in bursts, the pump clicks), open BV-02 fully and `SET d2` from the duty map to give 3.0 L/min instead, and record why. `SET tc1 180`. Run Case 1 and pour 0.8 L into TK-02 at +60 s, or at the planner's time and volume if P-01 is short.
- **Done when:** P-01 stops within 1.5 s of LS-01 tripping and restarts by itself after it clears, while P-02 never stops. Mean flow is 3.00 ± 0.10 L/min over 3 min, and the console shows mL/s and litres returned. Three passes in a row.
- **Retires:** Control firmware and holding 3 L/min (team worries 1 and 3).
- **Est:** half a day across two blocks (confidence: medium)

### M5 — Case 2 flushes and stops itself, with a backup take  (EF, Sat 15–22)
- **Do:** With the LSL-03 probe out of the water, run `TOUCHCAL EMPTY`. Run P-03 at d3 wet, then dry, and `SET i3dry` midway between the two currents. Then run Case 1 into Case 2 end to end.
- **Done when:** Every pump stops ≤ 1.0 s after the probe leaves the water (FLUSH_EMPTY, source LSL-03, in the event log), with no more than a puddle left in TK-03. The only manual action is BV-01. Three full runs in a row; the third is filmed in full as the backup take (by Sat 22:00), however rough.
- **Retires:** Detecting an empty flush tank at the source.
- **Est:** 4 h (confidence: low to medium)

### M6 — Extras that earn points  (DC, Sat 19–24)
- **Do:** Fault demos (unplug FT-01, close BV-03, throttle BV-02); the FIC disturbance test; a `BURST` pulsation capture; a dye transit over a marked 1.00 m of tube.
- **Done when:** Each fault demo produces the right diagnosis on the console, FIC restores 3.0 L/min after a BV-02 move, and the pulsation and dye plots are saved. None of this may delay M5's backup take.
- **Est:** 5 h (confidence: medium)

### M7 — Video and submission uploaded  (IV, Sun 08–18)
- **Do:** Three rehearsals; record the single take; shoot the edited segments; cut the Challenge Video (10–12 min) and the Journey Video (3–4 min) and export both as H.264 MP4; handwrite the paper in blue or black ink with the P&ID on page 4, then add appendix pages for the plots, photos and the code link and scan them into one PDF.
- **Done when:** All three files uploaded by 16:00, two hours before the cutoff, by one person, after a teammate who did not film checks both videos and the PDF against every requirement on pages 1–3 of the paper. Durations checked in the exported files: 10:00–12:00 and 3:00–4:00. The code link opens in a logged-out browser.
- **Est:** one day (confidence: high)

---

## Team

**08:00 stand-up, 10 minutes:** write a name on each role, read the objective and the done-when together, and agree the four checkpoint times. The rig and the scale are shared: book them in the run sheet.

### HY · Hydraulics lead
- **Owns:** 03 Hydraulics: P&ID, line list, fitting map, first water, inventory planner; 09 Video: the 0.8 L pour and the reset between runs; 08 Checklists: M2 hydraulic commissioning
- **Milestones:** M2 lead · M1 P-01 bucket tests · M3 bucket and BV-02 moves · M4 pour · M5 resets · M6 dye transit
- **First steps (Fri 08–10):**
  - [ ] Count every kit part against the fitting map (sheet 03). Give IV anything short before the parts run.
  - [ ] Measure the tube bore and the FT-01 barbs; enter both in the bench log (sheet 06).
  - [ ] Put the drip tray down. Raise TK-01 and TK-03 on stands so their water sits above the pump inlets.
  - [ ] Lay the loop out dry to the P&ID. Cut tubes to the line-list lengths only after the layout is checked.
  - [ ] 10:00: bucket on the scale and water ready for the P-01 test (M1).
- **Hands over:** A leak-free loop to DC for calibration (Sat 08:00); the reset routine to the take crew.

### EF · Electronics and firmware lead
- **Owns:** 04 Electrical: power, wiring, add-on board, I/O list; 05 Control: state machine, interlocks, diagnostics, commands, parameters; 08 Checklists: power-off check, M1 bring-up, M4 and M5 acceptance
- **Milestones:** M1 lead · M4 and M5 lead · console operator in every take · M6 fault demos and FIC
- **First steps (Fri 08–10):**
  - [ ] Flash the bare ESP32 over USB, no 12 V: `pio run -t upload`, or the Arduino IDE sketch on core 2.0.17. Start the console; check `fw=1.1`, then `PINS`.
  - [ ] Solder the add-on board (sheet 04): three IS channels, FT-01 divider pads, the LSL-03 probe lead.
  - [ ] DMM: measure each IBT-2's IS resistor to GND, unpowered; enter the values in the bench log.
  - [ ] Run the power-off check (sheet 08), then apply 12 V with no pumps connected.
  - [ ] 10:00: start M1. Connect LS-01, or jumper FSW to GND, before any pump test.
- **Hands over:** d1 after M1; a, b and fcut saved after M3; every changed parameter written in the bench log.

### DC · Data and calibration lead
- **Owns:** 06 Bench log and calibration: bench log, workbench, P-01 duty finder; 07 Answers: Q1.2, Q2.1–Q2.3, Q3.1, decision log; 08 Checklists: laptop readiness, M3 calibration
- **Milestones:** M3 lead · M1 duty finder · Q1.2 and Q2.1 data · M6 analysis
- **First steps (Fri 08–10):**
  - [ ] Console laptop plus one spare: USB driver (CP210x or CH340), Python 3.10+, `pip install -r tools/requirements.txt`.
  - [ ] Practise on the simulated take: `rig_console.py --replay`, type `SHOT`, then `analyze_run.py trend`. Practice only; never submit it.
  - [ ] Weigh station: bucket on the 1 g scale, the tare routine, and a jug holding exactly 800 g of water for the pour.
  - [ ] 10:00: run the P-01 duty finder (sheet 06) with EF and HY, and keep the bench log.
- **Hands over:** a, b and fcut to EF after M3; final numbers and plots to IV by Sun 12:00.

### IV · Integration, video and submission lead
- **Owns:** 00 Top 3 strategy, and the checkpoint calls on this sheet; 09 Video: storyboard, run script, abort rule; 08 Checklists: requirements coverage and M7 submission; 11 Downloads: printables and the code to share
- **Milestones:** M7 lead · checkpoint calls · photos · final P&ID · paper · upload
- **First steps (Fri 08–10):**
  - [ ] Log in to the LRC portal and read the Hardware Hustle form and countdown: three files (Journey MP4 3–4 min, Challenge MP4 10–12 min, handwritten PDF). Start filming Journey clips today, then send the follow-up message below.
  - [ ] Send the organiser message below (copy button).
  - [ ] Share this build book with the other three (Share menu), so ticks, the workbench and the bench log are shared.
  - [ ] Parts run when shops open: the buy-today list below, plus anything short from HY's count.
  - [ ] Print the tag labels, the BV-02 dial (both at 100% scale) and the P&ID at A3 (sheet 11). Photograph the kit before assembly.
  - [ ] Draft the Q3.1 and Q3.2 answers and the shot list. No hardware needed.
- **Hands over:** Calls the checkpoints (Fri 14:00, Sat 13:00, Sat 18:00, Sat 22:00). Before upload, a second person checks the submission.

---

## Parallel & lead-time

**Buy today:**
- Push-in male straight connector, 8 mm tube × ¼" BSPT (pneumatic code PC 8-02) × 4: Spares. All 8 in the kit are used (SOV-01 and the three ball valves), so one cracked fitting would stop M2. (Pneumatic or industrial fittings shop. Not an RO shop: RO fittings take ¼" (6.35 mm) tube and do not fit 8 mm.)
- Push-in equal tee, 8 mm (PE 8) × 1: Spare for TEE-01; the kit has only one. (Same shop)
- PTFE thread tape × 1 roll: Spare: the kit has one roll (item 43) for the 8 threaded joints. (Hardware or plumbing shop)
- Small cable ties, 100–150 mm × 1 pack: Spare: the kit has one pack (item 41); two per barbed joint on six pump ports and both ends of FT-01. (Hardware or electrical shop)
- 1N5819 or 1N4007 diode × 2: Flyback across the SOV-01 coil. Only needed if the valve driver has none (check first). (Electronics shop)
- BAT85 or BAT43 small-signal Schottky diode × 3: Clamp each IS pin (G15, G36, G39) to 3V3, cathode to 3V3. Not a 1N5819: its leakage through the 12 kΩ source would shift the reading. (Electronics shop)
- Drip tray the size of the rig, or a shallow storage-box lid × 1: Keeps a leak away from the SMPS and PCB. (Home or hardware store)
- Phone tripod or clamp × 1: Only if you have none: the single take needs a locked wide shot. (Mobile or electronics shop)
- Insurance: ESP32 NodeMCU-32S, 38-pin (same pinout as U7) × 1: U7 sits in a socket, so if the ESP32 dies, a swap and reflash takes 5 minutes. (Electronics shop, or next-day delivery)
- Insurance: BTS7960 (IBT-2) driver module × 1: A driver can fail on a stall or a short, and Case 2 needs all three. (Electronics shop, or next-day delivery)
- Insurance: YF-S401 flow sensor × 1: If FT-01 fails after calibration: swap it and recalibrate (about 2 h). (Electronics shop, or next-day delivery)

Buy everything not marked insurance today: M2 needs the fittings on Friday afternoon, and the clamp diodes go on before M2's dial map drives P-02 to its highest current. Anything ordered online today arrives Saturday at the earliest, so online is only for the insurance items. The pressure transducer is dropped.

**Organiser message:**

```
Subject: Stage 2 Hardware Hustle: clarifications from Team [Team ID] ([Team name])

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
[Your name], Team [Team ID]
```

**Follow-up message (Rev F):**

```
Subject: Stage 2 Hardware Hustle: follow-up from Team [Team ID] ([Team name])

Hello LRC team,

Four short follow-ups after reading the portal's submission form.

1. Video length. The paper asks for 10-15 minutes and the portal for a 10-12 minute Challenge Video. We will keep it within 10-12 minutes. Is that right?

2. Handwritten solution. We will write every answer by hand in blue or black ink. May we paste printed plots and photos onto the pages, or add printed appendix pages with handwritten captions, and include the P&ID drawn by hand on page 4?

3. Code. The form has no code upload. Is a GitHub or Drive link written in the PDF and shown in the video enough?

4. Deadline and Pump-02. The portal lists the round until 19 October; we are working to Sunday 4 October, 18:00 IST. Which is binding? And Case 1 sets Pump-02 at 100% while asking for 3 L/min. If holding 3 L/min at 100% means throttling the ball valve until the pump's pressure switch cycles, may we run Pump-02 at a lower duty with the valve open, and show the data?

Thank you,
[Your name], Team [Team ID]
```

**Off critical path:** M6 (evidence pack): fault demos, FIC, burst, dye transit.
**Contention:** one rig and one scale. Book rig time in the run sheet; batch the scale work.

## Checkpoints

- **After M1 (Fri ≈ 14:00):** P-01's flow through SOV-01 is known, so set d1. If even 100% gives under 3.0 L/min, enter P-01's maximum in the inventory planner (sheet 03): if it passes, Case 1 still holds 3.0 L/min at FT-01 on sump inventory, with the planner's pour time, pour volume and tc1. Only if it fails at P-01's maximum, lower the loop target to the highest flow it passes, and document why. If current sensing is unusable, `SET isok 0` and the diagnostics fall back to flow only.
- **After M2 (Fri night), P-02's operating point:** run the take with BV-02 open and a reduced d2 if, at the 3.0 L/min trim with P-02 at 100%, any of these holds: the pressure switch cycles; IT-02 is over 2.5 × its open-valve value (about 6 bar on a comparable pump); or a 5° move of the handle shifts the flow by more than 0.3 L/min, so the trim cannot be reset between takes. Ask the organisers (follow-up message, sheet 02).
- **After M2 (Fri night):** no calibration on a weeping joint. A leak-free loop is the gate for M3.
- **After M3 (Sat ≈ 13:00):** R² and K are known and the Q1.2 and Q2.1 data exist. Freeze the FT-01 spool: anything that moves it means calibrating again.
- **Sat 22:00 backup take:** a complete single-go video exists, however rough. Sunday is for a better take, never for a first one.
- **Sat 18:00 scope freeze:** anything not passing drops down the descope ladder (sheet 10).

## Open questions

| Question | Resolved by | When | If bad |
|---|---|---|---|
| Does P-01 at 50% move ≥ 3.3 L/min through SOV-01? | P-01 duty finder: 4 × 30 s on the scale | M1 | Use the strongest pump as P-01 and raise d1 (3.0 wins). If no duty reaches 3.0: inventory planner with P-01's maximum, then its pour time, pour volume and tc1. Last resort: loop target = the highest flow the planner passes, documented. |
| Where does P-02 at 100% give 3.0 L/min, and does the pressure switch cycle there? | M2 dial map: 100, 75, 50, 40, 30% for 30 s each, flow and IT-02 logged | M2 | Apply the M2 checkpoint rule: BV-02 open and a reduced d2 for the take; keep the 100% sweep for Q2.1. |
| Does any IS channel pass 1,100 mV at P-02's highest-pressure point? | Console mV at the 30% dial point | M2 | Put a resistor in parallel with that channel's IS load (halving it halves the voltage) and redo its gain. |
| Is FT-01's output push-pull or pull-up? | Scope it open, then with 10 kΩ to GND | M1 | Pick R1 and R2 from Figure 3. |
| Does the LSL-03 probe read clearly wet and dry? | PINS with the probe in water, then lifted out | M1 | Expose more bare wire, or move the GND wire closer. If it still fails, rely on IT-03 plus the tfmax backstop. |
| Does each IBT-2 have 10 kΩ on IS, and what is its real sense ratio? | DMM: resistance to GND, then two current points | M1 | Adjust the added resistor; per-channel gains g1–g3. |
| Does P-03's current drop clearly when it runs dry? | Run P-03 at d3 wet, then dry, in MANUAL with ILK 0 | M5 | Leave i3dry at 0: LSL-03 plus the tfmax backstop still end the flush. |
| What is the loop's maximum flow? Is 6 L/min reachable? | Duty map up to 100% with BV-02 open | M2 | Report the measured maximum and explain it with the system curve. |
| How much does the sump hold at the LS-01 trip? | Fill TK-02 on the scale | M2 | Enter it in the inventory planner. |
| What is each pump's minimum starting duty? | MANUAL ramp up from 10% | M1 | Set a floor for d1, d3 and FIC (0.15 by default). |

## Descope ladder

1. FIC closed-loop demo. Keep spec mode and the valve trim.
2. Fault demos beyond two. Keep the FT-01 unplug and the BV-02 throttle.
3. BURST pulsation analysis and the dye transit test.
4. The IT-01 channel and the ZSO-01 valve switch. Use the timed BV-01 window instead.
5. The LSL-03 capacitive trip. Fall back to IT-03 current plus the tfmax backstop.

**Floor:** Case 1 and Case 2 automated to spec, FT-01 calibrated (Q = af + b, R²), P&ID, 10–12 min Challenge Video, 3–4 min Journey Video, handwritten paper.
**Kill rule:** if Case 1 is not passing by Sat 14:00, stop every extra until it does.

## Replan triggers

- A finding on sheet 01 turns out wrong at the bench.
- A milestone runs 50% over its estimate.
- The ESP32 resets when pumps start (brown-out), or FT-01 counts pulses with no flow.
- A leak is still open after two hours of rework.
- The organisers answer differently on P-01's duty, the flush destination or the single take.
- The portal's countdown or the organisers give a different deadline, video length or paper format.
- P-01's maximum through SOV-01 is under 3.0 L/min, or P-02's 3.0 L/min trim makes its switch cycle.

## Changelog

- Rev A: First full plan: contract, ground truth, seven milestones, P&ID, wiring, firmware and bench tools.
- Rev B: (1) LSL-03 becomes a probe at the dip-tube inlet, so the flush stops exactly when TK-03 can no longer feed P-03 (the wall foil stopped with water still visible). A late BV-01 now re-prompts instead of ending the flush. (2) P-02 protective trips act only on true no-flow; partial patterns only raise an event, so noise cannot stop P-02 on camera. (3) The console no longer reboots the ESP32 when it connects. (4) The simulator showed that a 1.0 L sump start never trips LS-01 on the 0.8 L pour: the sump now starts 0.2 L below the trip, and the planner checks it. (5) A software-in-the-loop simulator runs the real firmware through 5 scenarios, all passing. Also: SOV-01 is confirmed direct-acting from its label; an M1 float-jumper note; P-03 duty set so the tee stays below atmospheric.
- Rev C: (1) The required Q1.2 and Q2.1 data moved from optional M6 into M3, straight after calibration, and the third M5 pass is filmed as a backup take by Sat 22:00. (2) A fitting map checks every joint against the exact kit counts: all 8 male push-fits are used, so 4 spares are ordered tonight, and FT-01's 7 mm barbs need the tube softened in hot water. (3) A first-water procedure: fill by weight, then prime P-02, P-01 and P-03 in that order and bleed the meter. (4) A reset procedure (about 6 min) and a single-take run script with roles, cues, forbidden actions and abort rules. The console now shows Case 1 and Case 2 elapsed time for the pour cue. (5) A laptop readiness checklist, plus a simulated full take in the kit to practise the console and plots on.
- Rev D: (1) A ‘How we place top 3’ sheet built on the round's own wording: real data, characterisation, calculations, plots, interpretation, and no simulations. It covers where points are won and lost, the judges' vocabulary, and Grand Finale readiness. (2) A requirements checklist traces every line of the paper to its evidence, including ‘Share the code’, which the plan had missed. (3) Evidence-grade outputs: a one-page FT-01 calibration certificate, and trend plots with shaded phases and labelled events. (4) A decision log ties each design choice to the measured data behind it, plus ready-to-fill Q2.1/Q2.2/Q2.3 interpretation sentences, and the P&ID now notes BV-02 as the throttling valve in place of the absent needle valve. (5) The video is re-cut around the problem statement's five verbs, with a caption for every number. The simulator stays a firmware test tool and never appears as evidence.
- Rev E: (1) Sheet 02 now opens with four role cards (HY, EF, DC, IV): what each person owns in this book, their milestones, and first steps they tick off, shared with the team. The schedule starts Fri 08:00 and M1 moves to 10:00. (2) A ready-to-send organiser message and a buy-today parts list: pneumatic push-fits (PC 8-02, not RO fittings), PTFE tape, ties, a flyback diode, a drip tray, and spare ESP32, IBT-2 and YF-S401 as insurance. The pressure transducer is dropped. (3) A shared bench log on sheet 06 records what the hardware shows at M1–M5, so firmware and parameters can be tuned from real readings. (4) Software: an Arduino IDE sketch that compiles the same `src/main.cpp` (checked with arduino-cli on core 2.0.17); firmware 1.1 reports its version to the console; the console saves screenshots at the float event, the end of Case 1, the three-pump flush and the automatic stop, draws the 3.0 L/min target band, and logs the parameters of every run. (5) Printables that were referenced but missing: the BV-02 position dial and the tag and flow-arrow labels; plus a code package for the judges, without the simulator. Also corrected: the state diagram's flush-end timing (IT-03 dry for 1.5 s, as in the firmware) and its BV-01 re-prompt path, and a stale ‘LSL-03 foil’ in the run sheet. The whole book is also exported as `BUILD_PLAN.md` for reading without a browser.
- Rev F: (1) The submission now matches the LRC portal's own form: a 10–12 min Challenge Video (the storyboard is cut from 14 to 11½ min, with `tc1` 180 s), a new 3–4 min Journey Video filmed from Friday, and the paper handwritten in blue or black ink and scanned to one PDF that carries the P&ID, photos, plots and code link. MP4 only, no code field, no changes after saving. A follow-up message asks the organisers about these points and the 19 Oct date in the rounds API. (2) P-02's Case 1 operating point: sprayer diaphragm pumps droop, so 3.0 L/min at 100% duty sits near 7 bar, close to the 8.25 bar switch. M2 now maps P-02 against the dial with IT-02, and a checkpoint rule moves the take to BV-02 open with a reduced d2 if the switch cycles there. IS channels get a 1,100 mV ceiling and a Schottky clamp to 3V3. (3) P-01 short of 3.0 L/min: a 0.3 m tank lift buys 0.03 bar against SOV-01's 0.8–1.3 bar, so the fallback is no longer ‘lower the target’. The inventory planner now takes P-01's measured flow, the pour time and tc1, and says whether Case 1 can still hold 3.0 L/min at FT-01 on sump inventory. The duty finder no longer extrapolates past the measured duties. (4) Calibration and Q2.1 follow the evidence: accept on maximum error and ±1% repeats (R² ≥ 0.995 alone passes 4–6% errors), runs of at least 1.5 kg, a 180 s against 3 × 60 s start-stop check, verification at the exact Case 1 setting, water temperature logged; Q2.1 adds 30% and 40% and predicts a gentle droop, a knee below 45% and switch cycling near 25%. Also: the dye transit needs 240 fps slow motion over at least 2 m; PTFE tape and ties are kit items, so they are spares. Sheet 04 opens with drawing E-01, a firmware connection diagram from each ESP32 pin to its device, with a table of every short form on it; it is also in the kit as a printable A3 SVG.
