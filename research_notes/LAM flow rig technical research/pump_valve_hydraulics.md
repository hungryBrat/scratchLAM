# Hydraulics of a small 12 V diaphragm-pump loop (PWM pumps, ball-valve throttling, 5 mm bore tubing)

## Q1. PWM speed control of small 12 V diaphragm pumps (linearity, start/sustain duty, current, inrush, 20 kHz, pulsation)

### Takeaway
These pumps use brushed permanent-magnet DC motors, so 20 kHz PWM from a BTS7960 (rated to 25 kHz) is a legitimate way to vary speed. Flow vs duty is not proportional, though. Expect a dead zone (no rotation below some duty, often reported around 30-40%; a higher duty is needed to start than to keep running), then a roughly linear but offset region. The slope falls as discharge pressure rises, because flow = displacement x rpm minus pressure-dependent slip, and rpm = (D x Vs - I x R)/kE with I rising with pressure. Current rises strongly with discharge pressure (~3 A open to ~9 A at 7 bar on a comparable Shurflo). Starting current is several times running current. Pulsation is at rpm x chambers / 60, about 100-180 Hz.

### Cited Findings
- Shurflo 8000-543-238 (comparable 12 V, 3-chamber, ~6.8 L/min, 100 psi): "MOTOR: Permanent Magnet"; "Positive Displacement 3 Chamber Diaphragm Pump"; "CAM: 3.0 Degree". Speed falls from 2206-2660 rpm (open) to 1900-2225 rpm (100 psi) as current rises 3.0 -> 8.7 A. — [Shurflo 8000-543-238 data sheet (PDF)](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf)
- Shurflo 8030-813-239 (6.1 L/min, 150 psi switch): current 5.5 A at 20 psi rising to 12.0 A at 150 psi; catalogue lists "Max Draw" 12.0 A. — [Shurflo 8000 catalogue (PDF)](https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf)
- Indian analogue: ASPEE Gardenia "double motor" battery sprayer (AGRDM012): double-motor pump, 6.0 L/min, 110 psi, used with a 12 V 12 A(h) battery. — [BigHaat, ASPEE Gardenia AGRDM012](https://www.bighaat.com/hi/products/aspee-gardenia-double-motor-battery-sprayer-agrdm012)
- Generic 12 V 36 W agricultural sprayer diaphragm pump: rated current 3 A, 3.5 L/min max, switch set 73 psi. — [ManoMano listing](https://www.manomano.co.uk/p/12v-36w-diaphragm-pump-double-thread-mini-high-pressure-dc-water-pump-for-agricultural-sprayer-220263555)
- 12 V 5.5 GPM diaphragm pump manual: "This pump requires a 15 amp fuse"; a cause of failure to prime is "The initial amp supply is not enough to sufficiently start the motor"; a cause of "pump fails to turn off" is "Insufficient voltage". — [VEVOR NMDP52 manual (PDF)](https://pdf.lowes.com/productdocuments/708a9dd0-5cd6-410b-b75f-74d3866cf05c/88568163.pdf)
- Forum reports on 12 V pump PWM: at "a low duty cycle (less than 40%) ... it does not rotate"; "the start-up current of the pump is likely to be several times" the running current. — [All About Circuits forum thread, speed control of 12 V DC pump motor](https://forum.allaboutcircuits.com/threads/speed-control-and-on-off-switch-for-12v-dc-motor.145333/post-1234815) (search-snippet only; page returned 403 on fetch)
- Caution about pump type: a 12 V "pump with integrated speed dial" in an Arduino thread pulsed on/off at PWM 128/255 and read 7 V at full PWM. Cause: "The circuit you are using is suitable for controlling brushed 'standard' DC motors with PWM. The motor that you have is BLDC". The fix was driving its own controller's potentiometer input. — [Arduino Forum, "problems with pump speed control"](https://forum.arduino.cc/t/problems-with-pump-speed-control/445205)
- Infineon BTS7960: "PWM capability of up to 25 kHz combined with active freewheeling", current sense, slew-rate adjustment, dead-time generation, over-temperature/over-current protection; current-limitation level 43 A typical. — [BTS7960B datasheet (components101 mirror, PDF)](https://components101.com/sites/default/files/component_datasheet/BTS7960B-Datasheet.pdf) (via search summary)
- The YF-S401 may misread pulsating flow: "pulsating flow from a piston or diaphragm pump probably not [OK]". — [Arduino Forum, YF-S401](https://forum.arduino.cc/t/flow-sensor-yf-s401/1254486)

### Inferences
- Linearity: for a brushed PM motor in continuous conduction (20 kHz is well above the electrical time constant of a small motor), average terminal voltage ≈ D x Vs, so rpm ≈ (D x Vs - I x R)/kE. Flow ≈ V_disp x rpm - slip(P). At free discharge (Pump-2 back to the tank, ~1-2 bar line loss), flow vs duty should be roughly a straight line with an x-intercept (dead zone) somewhere around 20-40% duty, not a line through the origin. **Calibrate flow against duty empirically at 6-8 duty points per pump; do not assume flow = duty x 6.1 L/min.** Three nominally identical pumps will need separate calibrations.
- Start vs sustain: static friction, diaphragm preload, check-valve cracking pressure and any trapped pressure in the line mean the start duty is higher than the minimum running duty (hysteresis). Use a kick-start (e.g. 100% for 200-300 ms, then ramp to target) and never command a steady duty inside the dead zone. A stalled motor at, say, 30% duty draws ~0.3 x stall current continuously and heats up.
- Stall/inrush: no stall-current figure for these pumps was found. For a pump drawing ~3 A open and ~9-12 A near cut-off, stall at 12 V is plausibly 15-25 A (inference, not sourced). The BTS7960's 43 A limit covers it, but the 12 V supply must handle three simultaneous starts (or stagger the starts by ~0.5 s). The 15 A fuse figure for a 5.5 GPM pump gives a sense of scale.
- Current as a pressure/fault sensor: on the Shurflo curve current rises ~0.8 A per bar. The BTS7960 IS pins (or an INA219) can detect discharge pressure trends, a closed valve, dry running (current below the open-flow value) and the pressure switch opening (current drops to ~0 while PWM is on, because the switch is in series with the motor).
- Pressure-switch interaction under PWM: at reduced duty the motor's stall torque falls roughly in proportion to D. Against a nearly closed valve the pump may stall below the switch cut-off rather than switching off (the VEVOR manual's "insufficient voltage" cause). Firmware should treat "high current + few/no flow pulses for >1-2 s" as stall and cut the drive.
- 20 kHz concerns: none fundamental for brushed motors. Effects to expect: (a) BTS7960 switching losses rise with frequency (20 kHz is within the 25 kHz rating, but the slew-rate resistor matters); (b) inaudible switching, though the pump itself is loud at 100-200 Hz; (c) brush arcing/commutation noise and the pressure switch's contact bounce will appear on current-sense and on the YF-S401 signal line, so route/filter the flow-sensor input (RC + Schmitt/pull-up) and use the ESP32 PCNT glitch filter.
- Pulsation frequency = rpm x chambers / 60. With Shurflo-like speeds (1,900-2,660 rpm): 3 chambers gives 95-133 Hz, 4 chambers 127-177 Hz, 5 chambers 158-222 Hz (computed). Frequency scales with duty, so it can serve as an rpm proxy if a pressure transducer or microphone is available.
- Ideal kinematic ripple (half-sine discharge per chamber, rigid system; computed): 3 chambers ~14% peak-to-peak of mean; 4 chambers ~32%; 5 chambers ~5%. Even chamber counts are worse than odd. Real ripple is larger because of check-valve dynamics, but PU tube compliance damps it. At F = 98 x Q, the YF-S401 outputs ~294 Hz at 3 L/min, only 2-3 pulses per pump stroke, so it partly follows the 100-150 Hz pulsation and its instantaneous period is noisy. Average counts over >=1 s windows.

### Gaps
- No manufacturer data was found on PWM duty vs flow for knapsack-sprayer diaphragm pumps; the dead-zone duty (~20-40%) is from forum and indirect sources only.
- No stall-current or inrush-current figure was found for any comparable 12 V sprayer pump.
- The All About Circuits and BTS7960 quotations come from search snippets because the pages were not fetched (403 / PDF).

## Q2. Pump curve: flow vs discharge pressure for comparable pumps

### Takeaway
Small 12 V wobble-plate diaphragm pumps are NOT flat-curve positive-displacement pumps. Manufacturer tables show flow falling 15% by just 0.7 bar and roughly 45-50% by the 6.9 bar cut-off, while current roughly triples; a pump rated "6.1 L/min open flow" should be expected to deliver only ~5 L/min at 1-1.5 bar and only ~2.7-3.2 L/min at 7-8.25 bar.

### Cited Findings
- Shurflo 8000-543-238 (12 VDC, "Positive Displacement 3 Chamber Diaphragm Pump", 3.0 degree cam, permanent-magnet motor, 100 psi demand switch) official typical-performance table, verbatim: OPEN 6.8 L/min, 2206/2660 rpm (min/max), 3.0 A; 10 psi (0.69 bar) 5.8 L/min, 3.6 A; 20 psi (1.38 bar) 5.5 L/min, 4.2 A; 30 psi 5.1 L/min, 4.9 A; 40 psi (2.76 bar) 5.0 L/min, 5.5 A; 50 psi 4.8 L/min, 6.0 A; 60 psi (4.1 bar) 4.6 L/min, 6.5 A; 70 psi 4.4 L/min, 7.1 A; 80 psi (5.5 bar) 4.2 L/min, 7.6 A; 90 psi 3.9 L/min, 8.3 A; 100 psi (6.9 bar) 3.6 L/min, 1900/2225 rpm, 8.7 A. "All data based on testing with water." — [Shurflo 8000-543-238 Product Data Sheet (Depco mirror, PDF)](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf)
  - Same sheet: motor speed drops only ~14-16% (2206->1900 min, 2660->2225 max rpm) while flow drops 47% (6.8->3.6 L/min), so most of the flow loss at pressure is volumetric (diaphragm/valve compliance and check-valve leakage/backflow), not motor slowing. — [same sheet](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf)
  - Same sheet: duty cycle "Intermittent (See Temperature Rise Chart)"; temperature-rise chart shows motor case heating curves for 60/80/100 psi continuous running over 90 min at 70 F still air. — [same sheet](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf)
- Shurflo 8000-series 12 VDC catalogue tables (PSI / L/min / A): 8000-343-236 (all-Viton, 4.5 L/min max): 20 psi 3.5 L/min 3.9 A; 40 psi 3.2 / 4.9 A; 60 psi 2.9 / 5.8 A. 8000-542-136 ("low flow", 4.5 L/min max): 20 psi 4.2 / 4.1 A; 40 psi 3.7 / 5.1 A; 60 psi 3.4 / 6.0 A. 8000-543-136 (6.8 L/min max, 60 psi switch): 20 psi 4.7 / 5.0 A; 40 psi 4.3 / 6.2 A; 60 psi 3.9 / 7.3 A. 8030-813-239 (6.1 L/min max, 150 psi switch, 12 A max): 20 psi 5.9 / 5.5 A; 40 psi 5.4 / 6.8 A; 80 psi 4.5 / 9.1 A; 100 psi 4.2 / 10.1 A; 150 psi 3.1 / 12.0 A. 8000-543-290 (100 psi): 20 psi 4.7 / 5.0 A; 60 psi 3.9 / 7.3 A; 100 psi 3.2 / 8.8 A. — [Shurflo 8000 Series catalogue pages (PDF, prumyslove-trysky.cz mirror)](https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf)
- The 8030-813-239 is the closest Shurflo analogue to the team's pump (6.1 L/min max, high cut-off): its catalogue curve gives ~5.9 L/min at 1.4 bar, ~4.5 L/min at 5.4 bar, ~4.2 L/min at 6.9 bar, and current rising 5.5 A -> 10.1 A over that range. — [Shurflo 8000 Series catalogue (PDF)](https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf)
- Internal-bypass versions behave very differently: 8000-543-250 (45 psi internal bypass): 20 psi 4.9 L/min 4.0 A; 30 psi 4.2 / 4.7 A; 40 psi 2.6 / 5.2 A; 50 psi 0.7 / 5.5 A. 8000-543-210 (35 psi bypass): 10 psi 4.8; 20 psi 4.5; 30 psi 4.0; 40 psi 0.19 L/min. Flow collapses over the last ~1 bar before the bypass setting while the motor keeps running. — [Shurflo 8000 Series catalogue (PDF)](https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf)
- Shurflo describes the 8000 series as "self-priming up to 8 vertical feet [2.4 m]", "can run dry without damage", built-in check valve, available as Switch, Bypass, or Switch/Bypass configurations. — [Pentair Shurflo 8000 series page](https://www.pentair.com/en-us/flow/commercial-products/water-supply-pumps/spray-pumps/8000_series_diaphgram_pumps.html)
- Seaflo 42 series (12 V, 11.3 L/min open, 55 psi shut-off, 41 psi restart, 7.5 A max) and Seaflo 22 series (12 V, 5 L/min, 100 psi, 6.0 A) are both marketed with an "internal bypass feature" that reduces cycling. Retailer pages give only max ratings, no curve. — [Overton's Seaflo 42](https://www.overtons.com/seaflo-42-series-12v-3.0-gpm-variable-flow-water-pump-118493.html); [DK Hardware Seaflo 22](https://www.dkhardware.com/seaflo-marine-fdp1-013-100-22-seaflo-22-series-12v-water-pressure-pump-13-gpm-100-psi-on-demand-diaphragm-pump-product-9180448.html)
- Singflo FL-30 (low-pressure 12 V diaphragm, 10 L/min free flow, 17 psi working pressure, 2.5 A rated, 4.5 A max, 2 m suction lift, 12 m max head). — [DirectIndustry Topsflo/Singflo listing](https://trends.directindustry.com/topsflo-industry-technology-co-limited/project-160944-1157378.html)
- Generic 12 V 36 W "double thread" agricultural sprayer pump: 3 A rated, 3.5 L/min max, pressure switch set at 73 psi. — [ManoMano listing](https://www.manomano.co.uk/p/12v-36w-diaphragm-pump-double-thread-mini-high-pressure-dc-water-pump-for-agricultural-sprayer-220263555)

### Inferences
- Applying the Shurflo 8000-543-238 shape (normalised: 1.00 open, 0.85 at 0.7 bar, 0.81 at 1.4 bar, 0.74 at 2.8 bar, 0.68 at 4.1 bar, 0.62 at 5.5 bar, 0.53 at 6.9 bar) to a pump rated 6.1 L/min open gives roughly 5.2 L/min at 0.7 bar, 4.9 at 1.4 bar, 4.5 at 2.8 bar, 4.1 at 4.1 bar, 3.8 at 5.5 bar, 3.2 at 6.9 bar. Cheap Chinese/Indian sprayer pumps are generally leakier than Shurflo, so the real droop is likely at least this steep. This must be measured on the bench, not assumed.
- Consequence for the team: "6.1 L/min" is a zero-back-pressure number. Any restriction in the discharge (5 mm tube, YF-S401, push-fits, ball valve) moves the operating point down this curve, so 6 L/min is unlikely to be reachable at 100% duty (see Q6).
- The curve is a gently falling line, not a flat plateau. So the team's expectation of "flat from 100% valve down to ~50%" needs to be re-checked: flow will start falling as soon as the valve adds any measurable pressure drop (each 0.7 bar costs roughly 10-15% of flow), then the pressure switch takes over near cut-off (Q3, Q5).
- Current is a useful proxy for discharge pressure: on the Shurflo curves current rises roughly linearly with pressure (~0.8 A per bar for the 8000-543-238). An INA219/ACS712 reading on each pump can serve as a cheap pressure indicator.

### Gaps
- No published flow-vs-pressure curve was found for the specific Indian "double motor knapsack sprayer" pump (6.1 L/min, 120 psi). Its chamber count, internal-bypass presence, and droop must be measured.
- Seaflo publishes pressure/flow/current tables in some product manuals, but none were retrieved in this session.

## Q3. Pressure-switch behaviour when throttled; internal bypass

### Takeaway
A demand-switch pump that is throttled downstream does not settle at a steady low flow. Once the discharge pressure reaches the cut-off it switches off, and it restarts only after pressure decays by the switch differential (about 15 psi / 1 bar on Shurflo; ~14 psi on Seaflo). With no accumulator and stiff PU tubing that decay is fast, so the pump short-cycles: the flow meter shows bursts and gaps, and supply current shows a square-ish on/off train with peaks near the pump's highest-current point. Pumps with an internal bypass instead recirculate internally, so delivered flow collapses smoothly near the bypass pressure while the motor keeps running at high current.

### Cited Findings
- Shurflo 8000-543-238 pressure switch: "Adjustable Shut-Off (Range 80-100 PSI) Factory Set @100 PSI, Turn On 85 PSI ± 5 PSI", i.e. ~15 psi (~1.0 bar) hysteresis. Current at 100 psi just before cut-off is 8.7 A vs 3.0 A open-flow. — [Shurflo 8000-543-238 data sheet (PDF)](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf)
- Seaflo 42 series: "shut-off pressure is 55 PSI with a restart pressure of 41 PSI ± 5 PSI" (~14 psi differential); the series has "an internal bypass feature that allows the pump to provide the amount of water you demand without cycling". — [Overton's, Seaflo 42 series](https://www.overtons.com/seaflo-42-series-12v-3.0-gpm-variable-flow-water-pump-118493.html)
- Shurflo sells the same 8000 pump as Switch, Bypass, or Switch/Bypass versions; internal-bypass pumps "will continue to run without damage once the bypass pressure is reached" and suit applications "where smooth, consistent flow is needed". Their curves show flow collapsing near the bypass setting, e.g. 8000-543-250 (45 psi bypass): 4.9 L/min at 20 psi, 2.6 L/min at 40 psi, 0.7 L/min at 50 psi, while current still rises to 5.5 A. — [Shurflo 8000 series catalogue (PDF)](https://www.prumyslove-trysky.cz/dokumenty/shurflo-8000.pdf)
- VEVOR NMDP52 (5-chamber 12 V, 70 psi, 5.5 GPM) manual: "When there is little to no water demand, the bypass valve opens to allow water to flow back from the outlet side to the inlet side, keeping a steady flow of water within the pump with almost no cycling". "The pressure setting for full bypass must be at least 8psi higher than the shut-off pressure of the pump. If the switch and bypass is adjusted too closely ... the pump will not shut off." Troubleshooting: "PULSATING FLOW - PUMP CYCLES ON AND OFF: Check lines for kinks. Plumbing lines or fittings may be too small. ... Check fitting tightness for air leaks." "PUMP FAILS TO TURN OFF ... Punctured diaphragm ... Insufficient voltage." — [VEVOR NMDP52-G55-70-12 manual (Lowe's PDF)](https://pdf.lowes.com/productdocuments/708a9dd0-5cd6-410b-b75f-74d3866cf05c/88568163.pdf)
- General pump-control guidance: short-cycling occurs "when flow demand falls below the pump's minimum operational threshold or when system pressure fluctuations exceed the pressure switch differential"; running very close to shut-off pressure produces rapid cycling. — [Industrial Monitor Direct, constant-pressure pump short cycling](https://industrialmonitordirect.com/blogs/knowledgebase/constant-pressure-pump-short-cycling-fix)

### Inferences
- With the team's pump (cut-off ~8.25 bar / 120 psi) the switch only matters once the throttling valve plus line drop approaches ~8 bar. Below that, flow follows the falling pump curve (Q2). Above it, the pump cycles. On the YF-S401 this shows as a pulse train with gaps; averaged over a window it gives a lower "mean flow" that depends on the averaging window and on how much the PU tube and any trapped air act as an accumulator.
- Insufficient voltage is listed as a cause of "pump fails to turn off" (VEVOR). Under PWM at low duty the motor may not have enough torque to reach the cut-off pressure, so the pump stalls against the closed valve instead of switching off. Expect a stalled motor drawing high current (see Q1). The firmware should detect "high current + zero pulses" and cut the PWM.
- The supply-current trace is the clearest diagnostic. Steady current means steady flow on the pump curve. A square on/off train means switch cycling. Steady high current with falling flow means an internal bypass is recirculating (check whether the pump head has a second adjustment screw or a bypass port).
- Low-cost "double motor knapsack sprayer" pumps usually have only a pressure switch (single adjustment screw under a rubber cap). If the head has two screws, one is likely a bypass. The team should check this on the actual unit.

### Gaps
- No datasheet was found for the specific Indian 120 psi sprayer pump stating its restart pressure, differential or whether it has an internal bypass.
- No published oscilloscope trace of current/flow during switch short-cycling for these small pumps was found; cycle frequency depends on system compliance and must be observed.

## Q4. Self-priming, suction lift, restrictive suction-side solenoid valve

### Takeaway
These pumps self-prime to roughly 2-3 m of lift, which means they can only pull a few tenths of a bar of vacuum. A 2.5 mm-orifice direct-acting solenoid (Kv ~0.16 m3/h, Cv ~0.19) on Pump-1's suction drops ~0.14 bar at 1 L/min, ~1.3 bar at 3 L/min and ~5 bar at 6 L/min. More than ~1 bar of suction drop is physically impossible, so **Pump-1 will be suction-starved at roughly 1.5-2.5 L/min**, with cavitation noise, air coming out of solution, erratic YF-S401 readings and no response to higher PWM duty. Flooded suction from the 10 L tank helps by only ~0.01-0.03 bar per 10-30 cm of head.

### Cited Findings
- Burkert type 6014 direct-acting valve, G1/4, 2.5 mm orifice: "Kv value 0.16 m3/h (2.67 l/min at dp = 1 bar water)"; direct acting, "requires no pressure differential to open". — [Tameson, Burkert 6014 312525](https://tameson.com/products/solenoid-valve-3-2-way-g1-4-no-brass-fkm-0-4bar-58psi-110vac-6014-312525)
- A UK-catalogue 1/4" direct-acting 2/2 valve with 2.5 mm orifice (K2W025-08) is listed with a flow of 3.4 L/min (test dP not stated in the snippet). — [Pneumatics Direct, K2W025-08-12DC](https://pneumaticsdirect.co.uk/products/m311-20272/K2W025-08-12DC) (search snippet only, not fetched)
- Shurflo 8000-543-238: "Self-Priming Up To 10 Ft. Vertical, Max. Inlet Pressure 30 PSI (2.1 Bar)". — [Shurflo data sheet (PDF)](http://www.depcopump.com/datasheets/shurflo/8000-543-238.pdf). The series catalogue and web page say "Self-priming up to 8 vertical feet [2.4m]". — [Pentair 8000 series](https://www.pentair.com/en-us/flow/commercial-products/water-supply-pumps/spray-pumps/8000_series_diaphgram_pumps.html)
- Singflo FL-30 (12 V diaphragm): "maximum suction lift of 2 m". — [DirectIndustry Singflo FL-30](https://trends.directindustry.com/topsflo-industry-technology-co-limited/project-160944-1157378.html)
- VEVOR 12 V 5-chamber diaphragm pump manual, install rules: inlet and outlet hoses "must be 1/2" (13 mm) ID reinforced hoses"; "Avoid any kinks or fittings which could cause excessive restrictions"; "Strainer should be attached to the inlet side"; "If a check valve is installed in the plumbing, it must have a cracking pressure of no more than 2 psi"; "Do not apply inlet pressure in excess of 30psi". Troubleshooting for "failure to prime but motor operates" lists "Restricted intake or discharge line", "Air leak in intake line", "The initial amp supply is not enough to sufficiently start the motor". — [VEVOR NMDP52 manual (PDF)](https://pdf.lowes.com/productdocuments/708a9dd0-5cd6-410b-b75f-74d3866cf05c/88568163.pdf)

Computed suction-valve pressure drop, dP[bar] = (Q[m3/h]/Kv)^2:

| Kv (Cv) | 1 L/min | 1.5 | 2 | 3 | 4 | 6 L/min |
|---|---|---|---|---|---|---|
| 0.12 (0.14) | 0.25 bar | 0.56 | 1.00 | 2.25 | 4.0 | 9.0 |
| 0.16 (0.19), Burkert 2.5 mm | 0.14 | 0.32 | 0.56 | 1.27 | 2.25 | 5.06 |
| 0.20 (0.23) | 0.09 | 0.20 | 0.36 | 0.81 | 1.44 | 3.24 |
| 0.25 (0.29) | 0.06 | 0.13 | 0.23 | 0.52 | 0.92 | 2.07 |

Maximum mean flow if the pump can tolerate 0.3 / 0.5 / 0.7 bar of suction-side drop: Kv 0.16 gives 1.5 / 1.9 / 2.2 L/min; Kv 0.20 gives 1.8 / 2.4 / 2.8 L/min.

### Inferences
- A 2.4-3 m self-priming lift corresponds to ~0.24-0.3 bar of vacuum on air (dry). Wet, these pumps can pull somewhat more, but the absolute ceiling is atmosphere minus vapour pressure (~1.01 - 0.03 = ~0.98 bar at 25 °C), and well before that, dissolved air comes out and the diaphragms' inlet valves stop filling. A realistic usable suction-side loss budget is ~0.3-0.5 bar, so 3 L/min through a Kv 0.16 valve (1.27 bar) and 6 L/min (5 bar) are not achievable on Pump-1.
- The mean-flow table understates the problem. A 3-chamber diaphragm pump draws pulsatile flow (peak instantaneous suction flow well above the mean), and dP scales with Q^2, so the valve pressure spikes on every suction stroke. Expect cavitation crackle and bubbles downstream even when the mean-flow dP looks acceptable (e.g. at 1.5-2 L/min).
- Symptoms to recognise on the bench: Pump-1 flow plateaus as duty rises; current stays relatively low (the pump is not building discharge pressure); there is a rattling or gravelly sound; bubbles show in the clear PU discharge line; YF-S401 counts become erratic. These are not firmware faults.
- Fixes, in order of effort: (1) move the NC solenoid to Pump-1's discharge side, where it has up to ~8 bar to work with (1.3 bar at 3 L/min is then acceptable, though it still costs ~10-20% of flow per the pump curve); (2) use a larger-orifice direct-acting or zero-differential (assisted-lift) valve with 4-6 mm orifice (Kv ~0.4-0.8); (3) keep the tank outlet above the pump inlet (flooded suction), keep the suction line short and straight, and add an inlet strainer per the pump manual. A pilot-operated (servo) solenoid needs a minimum differential (typically ~0.3-0.5 bar) and will not open reliably on the suction side.
- Pump-2 drains a sump. If the sump level is below the pump, that is a lift, and the same suction budget applies to the sump hose and any fittings. The mini ball valve must be on the discharge side of Pump-2 for the throttling experiment to mean what the team intends (Q5).

### Gaps
- The actual Kv of the team's Chinese 1/4" brass NC solenoid is unknown (the orifice is "probably ~2.5 mm"). Measure it: with the solenoid open on the discharge side at a known flow, read dP, then Kv = Q[m3/h]/sqrt(dP[bar]).
- No source gave the maximum wet-suction vacuum (bar) for small sprayer diaphragm pumps; only dry self-priming lift (2-3 m) is published.

## Q5. Quarter-turn ball valve throttling characteristic and installed characteristic

### Takeaway
A round-bore ball valve has a very non-linear inherent characteristic: Cv stays a small fraction of its maximum for most of the travel and roughly doubles over the last 10% (full bore). Its loss coefficient goes from K ~0.05 open to ~5.5 at 30° closed to ~200 at 60° closed. Against a drooping diaphragm-pump curve this gives an installed curve that is nearly flat from 100% to ~60-70% open (by handle angle), falls gently to ~50%, then drops steeply below ~40%, with the pressure switch reached at roughly 25-40% open. The team's "flat to ~50%, then steep" expectation is qualitatively right, but the plateau is ~4.5-5 L/min (not 6.1), ~10% is already lost at 50%, and the 25% position probably cycles the switch.

### Cited Findings
- Ball-valve minor-loss coefficients (referenced to pipe velocity, dP = K rho v^2/2): "Fully open: 0.05; 1/3 closed: 5.5; 2/3 closed: 200". — [Engineering ToolBox, Minor loss coefficients](https://www.engineeringtoolbox.com/minor-loss-coefficients-pipes-d_626.html)
- Inherent characteristic is defined at constant pressure drop across the valve; Hisaka shows a ball-valve flow-vs-opening-angle curve (numbers not tabulated); full-bore 1/4" ball valve Cv = 3.0 fully open; Cv = Q x sqrt(G/dP) [gpm, psi]. — [Hisaka, What is Cv](https://www.hisaka.co.jp/valve/english/techdoc-en/techdoc01-en/)
- Neles/Valmet T2H trunnion ball valve (round bore), Cv vs relative opening h (% of 90° travel), DN25: 10% 0.676; 20% 1.51; 30% 2.81; 40% 4.89; 50% 7.7; 60% 11.5; 70% 17; 80% 26; 90% 46.6; 100% 105. As a fraction of max: 50% open = 7.3% of Cv; 70% = 16%; 80% = 25%; 90% = 44%. — [Valmet T2/T2H Cv table](https://www.valmet.com/globalassets/flow-control/services/T2_T2H.html)
- Neles T5G (explicitly "REDUCED BORE") DN80: 10% 2.71; 20% 9.17; 30% 16.4; 40% 26.8; 50% 40.1; 60% 55; 70% 71.1; 80% 101; 90% 150; 100% 200, so 50% open = 20% of Cv and 90% = 75%. Reduced bore gives a less extreme, more linear-looking curve, because the full-open Cv is capped by the smaller bore. — [Valmet T5/T5G Cv table](https://www.valmet.com/globalassets/flow-control/services/T5_T5G.html)
- Ball-valve open area is the overlap of two circles (bore and port) whose centres move apart as the ball rotates, A_open = f(R_bore, R_port, displacement l, rotation phi), with phi from 0 (shut) to pi/2 (open). Simscape uses default discharge coefficient 0.64. So flow area vs handle angle is strongly non-linear and depends on bore/port ratio. — [MathWorks Simscape Fluids, Ball Valve (IL)](https://www.mathworks.com/help/hydro/ref/ballvalveil.html)
- V-port (characterised) ball valves are the version made for throttling. Valves Online tabulates their Cv from 15% to 100% open and notes the Cv progression "is not a linear progression"; for standard full-bore valves it gives only the fully-open Cv. — [Valves Online, ball-valve flow rates](https://valvesonline.com.au/references/flow-rates/ball-valves)

### Inferences
- "% open" is ambiguous. 50% of handle angle (45°) is roughly 7-20% of max Cv (Valmet tables) and an even smaller fraction of geometric area for a full-bore valve. The team should define the positions as handle angle in degrees (0/22.5/27/45/67.5° from open for 100/75/70/50/25%), mark them with a printed protractor or detent template, and report Cv or measured dP alongside.
- Installed-characteristic model (computed here; assumptions: pump curve = Shurflo 8000-543-238 shape scaled to 6.1 L/min open and extrapolated to the 8.25 bar cut-off; 2 m of 5 mm tube; 4 fittings at K = 1.5; YF-S401 at K = 4 (~0.5 bar at 6 L/min); valve K interpolated log-linearly in angle through the Engineering ToolBox points), pump at 100% duty:

| Valve open (by angle) | Valve K | Flow | Pump discharge pressure |
|---|---|---|---|
| 100% | 0.05 | 4.8 L/min | 1.7 bar |
| 75% | 1.7 | 4.7 | 1.8 |
| 70% | 3.4 | 4.7 | 1.9 |
| 60% | 11 | 4.5 | 2.3 |
| 50% | 33 | 4.3 | 3.5 |
| 40% | 98 | 3.7 | 5.7 |
| 30% | 290 | 2.7 | 8.2 (at cut-off) |
| 25% | 490 | ~2.3 if it could run; actually above 8.25 bar, so switch cycles | 9.4 (exceeds cut-off) |

  Using the Valmet full-bore shape with Cv_max = 1.5 instead (a smaller mini valve) moves the knee earlier: 4.5 L/min at 75%, 3.6 at 50%, 2.8 at 40%, cut-off by ~35-40% open. With Cv_max = 3.0 the result is close to the K-table case. A larger meter/fitting loss (K = 12) lowers the plateau to ~4.6 L/min but hardly moves the knee.
- With the pump slowed (PWM) to give ~3 L/min fully open (same normalised curve), the model gives 3.0 L/min at 100-70% open, 2.85 at 50%, 2.6 at 40%, 2.2 at 30%, 1.9 at 25% with no cut-off. The plateau is flatter because velocities and valve dP are lower. Caveat: at reduced duty the motor's stall torque, and so the maximum pressure it can reach, falls roughly in proportion to the average voltage. A slowed pump may stall against the valve before the switch trips, so the real curve below ~40% open will fall faster than this model.
- Contradiction to flag: a diaphragm pump is not "insensitive to the valve until it is mostly closed". The curve has a gentle negative slope everywhere (each bar of valve dP costs ~0.15-0.3 L/min here), and the steep part sits between ~45% and ~25% open by angle, which is only about 18° of handle travel. The 70% and 75% positions will be nearly indistinguishable (<2% apart), so that pair adds little information. Positions at 40% and 30-35% would capture the knee better.
- If the ball valve is on the suction side of Pump-2 (between sump and pump) instead of the discharge, the physics changes completely. Throttling then lowers inlet pressure; the pump starves and cavitates once the valve dP approaches ~0.3-0.6 bar (see Q4), and the pressure switch never trips. The P&ID should be checked.

### Gaps
- No Cv-vs-angle data was found for 1/4" mini brass ball valves specifically (bore typically 4-6 mm, often reduced-port); the Valmet tables are for large trunnion valves and only indicate shape. Measuring dP across the valve at 2-3 flows per position would give its actual Cv curve.
- The Engineering ToolBox K values give only three points (open, 1/3, 2/3 closed); the interpolation between and beyond them is an assumption.

## Q6. Flow in 5 mm ID tube at 1/3/6 L/min; minor losses; YF-S401 pressure drop; is 6 L/min reachable

### Takeaway
In 5 mm ID tube the flow is turbulent at all three set-points (Re ~4,800 / 14,300 / 28,500), so pressure drop rises roughly with Q^1.75: ~0.03 / 0.18 / 0.62 bar per metre. Pipe friction alone will not stop 6 L/min, but the small-bore components (2.5 mm solenoid orifice on the suction side, the YF-S401's 4 mm ports and internal jet, the mini ball valve's reduced bore, push-fit bodies) together with the pump's falling curve make 6 L/min at the meter unlikely; ~4.5-5.5 L/min at 100% duty is a more realistic expectation until measured.

### Cited Findings
Tube numbers (computed here with water at 25 °C: rho = 997 kg/m3, mu = 0.890 mPa s, nu = 0.893e-6 m2/s; D = 5.0 mm, A = 19.63 mm2; Colebrook with smooth wall; Blasius f = 0.3164 Re^-0.25 agrees within 3%). Formulas: Darcy-Weisbach dP = f (L/D) rho V^2/2 for the tube and dP = K rho V^2/2 for fittings (the minor-loss form is given by [Engineering ToolBox, Minor loss coefficients](https://www.engineeringtoolbox.com/minor-loss-coefficients-pipes-d_626.html)):

| Q (L/min) | Mean V (m/s) | Re | Regime | f (Colebrook, smooth) | dP per metre | Dynamic pressure 0.5 rho V^2 (= dP for K = 1) |
|---|---|---|---|---|---|---|
| 1 | 0.85 | 4,750 | turbulent (just above transition) | 0.038 | 2.7 kPa/m (0.027 bar/m) | 0.36 kPa |
| 3 | 2.55 | 14,300 | turbulent | 0.028 | 18 kPa/m (0.18 bar/m) | 3.2 kPa |
| 6 | 5.09 | 28,500 | turbulent | 0.024 | 62 kPa/m (0.62 bar/m) | 12.9 kPa |

(0.5 L/min: V = 0.42 m/s, Re = 2,380, borderline laminar/transitional.)

- YF-S401 (DFRobot SEN0216): flow range 0.3-6 L/min; "1 L = 5880 square waves" (i.e. F = 98 x Q[L/min]); accuracy "±5% (0.3-3 L/min)" only; proof pressure "<0.8 MPa"; inlet/outlet "Inner Diameter 4 mm", "Outside Diameter 7 mm". No pressure-drop figure published. — [DFRobot wiki SEN0216](https://wiki.dfrobot.com/sen0216/)
- A generic YF-S401 datasheet (Alldatasheet copy) gives conflicting specs: "Flow Rate Range: 1~5 L/min", "Water resistant 0.35MPa", "Water Pressure: ≤1.75MPa", "Internal diameter: 1.2mm", "F = (98 * Q) ± 2%" and, in the cautions, "F = 90 * Q"; also "Install it in vertical, inclination should not beyond 5 degree". — [YF-S401 datasheet (iarduino.ru mirror, PDF)](https://iarduino.ru/lib/2377bf7550064248856024f6728d7cc3.pdf)
- Arduino forum advice on the YF-S401: "Smooth flow like a centrifugal, vane or peristaltic pump should be OK, pulsating flow from a piston or diaphragm pump probably not"; another member: "you will need to calibrate the sensor you have". — [Arduino Forum, "Flow Sensor YF-S401"](https://forum.arduino.cc/t/flow-sensor-yf-s401/1254486)
- Reference Cv of a 1/4" full-bore two-way ball valve fully open: Cv = 3.0 (Hisaka). — [Hisaka, What is Cv](https://www.hisaka.co.jp/valve/english/techdoc-en/techdoc01-en/)
- Valve dP from Cv (water): dP[psi] = (Q[gpm]/Cv)^2 (Cv = Q x sqrt(G/dP)). — [Hisaka](https://www.hisaka.co.jp/valve/english/techdoc-en/techdoc01-en/)

Computed valve/orifice pressure drops (from the Cv formula above; Cv values are assumptions to bracket the hardware):

| Element (assumed Cv) | 1 L/min | 3 L/min | 6 L/min |
|---|---|---|---|
| Cv 0.15 | 0.21 bar | 1.9 bar | 7.7 bar |
| Cv 0.20 | 0.12 bar | 1.1 bar | 4.3 bar |
| Cv 0.25 | 0.08 bar | 0.69 bar | 2.8 bar |
| Cv 0.40 | 0.03 bar | 0.27 bar | 1.1 bar |
| Cv 0.80 | 0.01 bar | 0.07 bar | 0.27 bar |
| Cv 3.0 (1/4" full-bore ball valve, open) | ~0 | ~0 | 0.02 bar |

Sharp-edged orifice estimate (Cd = 0.62, no recovery, upper bound): 2.5 mm hole 0.15 / 1.35 / 5.4 bar at 1 / 3 / 6 L/min; 3 mm hole 0.07 / 0.65 / 2.6 bar; 4 mm hole 0.02 / 0.21 / 0.82 bar.

### Inferences
- The 5 mm tube is not the bottleneck: 2 m of it costs ~0.36 bar at 3 L/min and ~1.2 bar at 6 L/min. Fittings add K x 0.13 bar each at 6 L/min. Engineering ToolBox gives threaded 90° elbow K = 1.5, tee branch flow K = 1.0, tee line flow K = 0.2, ball valve fully open K = 0.05 ([source](https://www.engineeringtoolbox.com/minor-loss-coefficients-pipes-d_626.html)). That is ~0.13-0.2 bar per elbow/tee branch at 6 L/min and ~0.03-0.05 bar at 3 L/min. Push-fit bodies whose bore is smaller than 5 mm will be worse.
- A 1.2 mm "internal diameter" cannot be the whole YF-S401 flow path (6 L/min through 1.2 mm would be ~88 m/s). It is probably a jet/nozzle or a misprint; the 4 mm port ID (DFRobot) is the credible figure. The "Water resistant 0.35 MPa" line may be a garbled pressure-drop or pressure-rating line and cannot be relied on. The YF-S401 dP must be measured (gauge before and after, or the pump-current proxy).
- Putting it together for Pump-2 discharge at 6 L/min: ~1.2 bar of tube (2 m) + ~0.5-1 bar of fittings + an unknown YF-S401 dP (plausibly 0.5-2 bar given 4 mm ports and an internal jet onto the rotor) + ~0.1-0.3 bar for the open mini ball valve gives ~2-4 bar. On the scaled Shurflo curve (Q2) a 6.1 L/min-open pump gives only ~4.2-4.6 L/min at 2-4 bar. **6 L/min at the meter is very unlikely** with this hardware; 3 L/min is comfortably reachable.
- For Pump-1, the suction-side solenoid (2.5 mm orifice) is the dominant restriction (see Q4).
- The YF-S401's own spec gives accuracy only to 3 L/min, and diaphragm-pump pulsation may disturb its readings. Use timed bucket/volumetric collection (stopwatch + measuring jug or tank level) as ground truth at 1, 3, 6 L/min.

### Gaps
- No published pressure-drop vs flow curve for the YF-S401 was found, and the generic datasheets disagree on flow range, pulse constant (98 vs 90 Hz per L/min) and internal diameter.
- Minor-loss K values specific to 8 mm push-to-connect fittings (whose internal bore is often below the tube ID) were not found in a manufacturer source; the Engineering ToolBox values are for generic threaded/flanged fittings.

## Q7. Measuring actual velocity (dye/bubble transit) vs mean velocity

### Takeaway
A visible dye front or the nose of a small bubble travels near the fastest (centreline) fluid, not the mean. In turbulent pipe flow that is ~1.2-1.3x the mean velocity (higher at the team's low Re); in laminar flow it is 2x. A tube-filling (Taylor) bubble also moves at ~1.2x mean in turbulent flow, by Nicklin's correlation. The standard way to get the mean velocity is the ISO/ASME transit-time ("Allen salt-velocity") method: time the centroids of the tracer concentration curves at two stations, not the leading edge. So "measured front speed is ~20-30% above theory" is the expected physics, not an error.

### Cited Findings
- Power-law turbulent profile u/U = (y/R)^(1/n); mean/centreline ratio V/U = 2n^2/((n+1)(2n+1)); "n=7 seems to be applicable to a wide range of pipe flows" (the one-seventh law). — [Cambridge Univ. Eng. Dept., Power law velocity profile](https://www-mdp.eng.cam.ac.uk/web/library/enginfo/aerothermal_dvd_only/aero/fprops/pipeflow/node22.html)
- Transit-time (formerly "Allen velocity") method: flow rate from "the transit time of 'labelled' fluid particles between two cross-sections of the conduit a known distance apart", with the transit time "determined from the difference of the mean arrival times of the tracer at each detector position". — [ISO 2975-7 / BS 5857 transit-time method summaries](https://iteh.es/catalog/standards/iso/d6b6a4aa-ad9d-4804-978c-9685e97c8bdf/iso-2975-7-1977) (via search summary)
- US Bureau of Reclamation: salt-velocity transit time is measured "between the centroids of the two plotted conductivity cloud areas above the background conductivity level"; the plots show "a leading and a trailing edge"; "a turbulator is sometimes used to ensure adequate mixing ... by the time they reach the first electrode station"; the method has "high potential accuracy" and is accepted by ASME for turbine testing. — [USBR Water Measurement Manual, Ch. 12 Tracers](https://www.usbr.gov/tsc/techreferences/mands/wmm/chap12_06.html)
- Taylor (1954) showed that in turbulent pipe flow, longitudinal spreading becomes a 1-D diffusion with an effective coefficient orders of magnitude larger than molecular diffusion; Hart, Guymer, Jones & Stovin (2013) tested 2,000 < Re < 50,000 and report "significant deviation from his prediction for Re < 20,000". — [Coventry Univ. repository, Hart et al. 2013](https://pureportal.coventry.ac.uk/en/publications/longitudinal-dispersion-coefficients-within-turbulent-and-transit/)
- Nicklin et al. (1962): Taylor-bubble velocity U_b = C1 U_L + C0, where C1 is "equal to the ratio of the maximum to mean liquid velocity"; "for turbulent flow, C1 ≈ 1.2, increasing with decreasing Re_L and approaching C1 ≈ 1.9 at Re_L = 100". — [arXiv 2109.09091, Taylor bubble motion in vertical pipes, Part I](https://arxiv.org/pdf/2109.09091) (via search summary)

### Inferences
- Centreline/mean ratio from the power law: n = 6 gives 1.26, n = 7 gives 1.22, n = 8 gives 1.20 (computed). At the rig's Re (4,800-28,500) the profile is less flat (n ~5-6.5 using White's approximation n ≈ f^-1/2 with f = 0.038-0.024), so expect the dye-front or bubble speed to be ~1.25-1.3x the mean at 3-6 L/min and ~1.3x or more at 1 L/min (Re 4,750, near transition). Laminar Hagen-Poiseuille flow (centreline = 2x mean) applies only below Re ~2,300 (< ~0.5 L/min in 5 mm tube).
- Timing scale: at 3 L/min the mean velocity is 2.55 m/s, so a 1.0 m test section takes 0.39 s (front ~0.31 s); at 6 L/min, 0.20 s; at 1 L/min, 1.18 s. Hand stopwatch timing (~0.2 s reaction error) is useless below ~3 m. Use phone slow-motion video (240 fps gives 4 ms frames) against a ruler, or two photo-interrupters/LDRs, or two conductivity electrode pairs (salt tracer) logged by the ESP32 at >=1 kHz. Coiling 3-5 m of clear PU tube on a board lengthens the path.
- Recommended protocol: inject a short pulse of food dye (or saline for conductivity) at least ~50 tube diameters (~0.25 m) upstream of station 1 so it is cross-sectionally mixed. Record the concentration-time curve at stations 1 and 2 (an LED-photodiode across clear tube works for dye), and compute transit time from the centroid of each curve (sum of t*c / sum of c). Velocity = L / (t2 - t1). Report the leading-edge speed separately and expect it to be ~1.2-1.3x the centroid speed. Compare the centroid speed with Q/A from the bucket-timed flow.
- Pulsation caveat: the diaphragm pump's 100+ Hz pulsation is faster than the transit times, so it averages out over a 1 m section. Switch cycling (Q3) does not average out, so avoid velocity tests at valve positions where the switch is cycling.
- Bubbles: a small bubble entrained near the wall will lag; a bubble on the centreline will lead. Only tube-filling slugs give a repeatable ~1.2x. In a 5 mm horizontal tube, surface tension dominates (Eotvos number ~3.4, near Bretherton's no-rise limit), so buoyancy drift is small, but the bubble's own interface friction adds uncertainty. Dye centroid timing is more defensible for the paper.

### Gaps
- No source specific to millimetre-scale PU tubing at Re 5,000-30,000 quantifying front-to-mean ratio was found; the 1.2-1.3x figure rests on power-law profile theory and Nicklin's correlation (vertical pipes).
- The ISO 2975-7 and Nicklin quotations came via search-result summaries of the documents, not full-text reads.
