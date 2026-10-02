# Automated three-pump flow rig: controller and analysis code

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
