# Hardware Hustle build kit

LAM Research Challenge 3.0, Stage 2. Firmware, bench tools and the printable P&ID.

## Bring-up order
1. Flash the bare ESP32 over USB, with no 12 V connected:
   - PlatformIO: `cd firmware/lam_flow_rig && pio run -t upload && pio device monitor`
   - Arduino IDE: open `firmware/arduino_ide/lam_flow_rig/lam_flow_rig.ino`, board "NodeMCU-32S", esp32 core 2.0.17 or 3.x
2. Type `PINS` and press the switch: `button` should read 0 while it is pressed.
3. Run the power-off checklist, then apply 12 V. `MANUAL`, then `P 1 30`, then `P 1 0`, and the same for pumps 2 and 3.
4. Start the console: `pip install -r tools/requirements.txt`, then `python tools/rig_console.py --port COM5`
   (on Linux: `/dev/ttyUSB0`).

## Daily commands
START / STOP / RESET · MANUAL · P n duty · SOV 0|1 · CAL seconds duty · FIC · SET key value · GET · SAVE ·
MARK text · TOUCHCAL EMPTY|WET · IZERO · ZERO · LEARN · BURST · PINS · NEXT (rehearsal only)

## Telemetry (10 Hz)
D,t_ms,state,q_lpm,q_mls,f_hz,v_tot_l,v_c1_l,v_c2_l,d1,d2,d3,i1_a,i2_a,i3_a,lsh,sov,zso,touch,diag,alarms,sp,ft_duty_pct,glitches
Events: E,t_ms,TAG,text.  Calibration: C,t_ms,run,pulses,time_s,f_hz,duty.

## Analysis
- `python tools/cal_fit.py runs/<stamp>_cal.csv --plot cal.png`: Q2.2/Q2.3 tables, R², errors, SET lines
- `python tools/analyze_run.py valve <telemetry> <events>`: Task 2 table and plots
- `python tools/analyze_run.py trend <telemetry> <events>`: flow (mL/s, L/min) and litres against time
- `python tools/analyze_run.py dutymap|step|burst ...`: FIC feed-forward, tuning, pulsation
- `python tools/theory.py --id 5.0 --measured 1.0 3.0 4.8`: Q1.2 and Q3.1 tables

Firmware compiles without warnings on Arduino-ESP32 core 2.0.17 (PlatformIO espressif32 7.0.1) and core 3.1.3.
