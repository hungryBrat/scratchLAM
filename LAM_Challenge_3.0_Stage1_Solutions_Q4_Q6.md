# Lam Research Challenge 3.0 — Stage 1
## Technical Engineering Assessment — Solution Manual
### Task 4 (Closed-Loop Control Engineering) and Task 6 (Industrial Communication)

---

## 0. Preliminaries

### 0.1 Given process parameters (used in Tasks 4 and 6)

| Parameter | Symbol | Value |
|---|---|---|
| Pipe internal diameter | D | 10 mm |
| Fluid density | ρ | 1000 kg/m³ |
| Dynamic viscosity | μ | 1×10⁻³ Pa·s |
| Required flow range | Q | 1–6 L/min |
| Process pipeline length | L | 3 m |
| Plant transfer function | G(s) | 6/(4s+1) |
| ADC resolution | — | 12 bit |
| Sensor output | — | 4–20 mA |
| Supply voltage | — | 24 VDC |

### 0.2 Derived geometry (required repeatedly below)

A = πD²/4 = π(0.010)²/4 = **7.854×10⁻⁵ m²**

| Condition | Q | v = Q/A | Transport delay θ = L/v |
|---|---|---|---|
| Minimum flow | 1 L/min = 1.667×10⁻⁵ m³/s | **0.212 m/s** | **14.14 s** |
| Maximum flow | 6 L/min = 1.000×10⁻⁴ m³/s | **1.273 m/s** | **2.36 s** |

These transport delays are used as independent physical evidence in Q4.2.

### 0.3 Notation

| Symbol | Meaning |
|---|---|
| K_p, τ, θ | process gain, time constant, dead time |
| K_c, T_i, T_d | controller gain, integral time, derivative time |
| K_u, T_u, ω_u | ultimate gain, ultimate period, ultimate frequency |
| SP, PV, CO/MV | setpoint, process variable, controller output / manipulated variable |

---

# TASK 4 — CLOSED LOOP CONTROL ENGINEERING

**Plant transfer function:** G(s) = 6/(4s+1)

---

## Q4.1 — Process gain, time constant and settling time

### Statement
Determine: process gain, time constant and approximate settling time T_s = 4τ.

### Method
Compare the given transfer function against the canonical first-order lag:

    G(s) = K_p / (τ s + 1)

### Working

By direct inspection of G(s) = 6/(4s + 1):

| Parameter | Value | Basis |
|---|---|---|
| **Process gain, K_p** | **6** (output units per input unit, e.g. % PV per % CO) | K_p = lim(s→0) G(s) = 6/1 = 6 |
| **Time constant, τ** | **4 s** | coefficient of s in the denominator |
| **Dead time, θ** | **0 s** | no e^(−θs) term present |
| **Pole location** | s = −1/τ = −0.25 rad/s | single real LHP pole |
| **Open-loop bandwidth** | ω_b = 1/τ = 0.25 rad/s (0.0398 Hz) | −3 dB corner |

**Unit step response:**

    y(t) = K_p (1 − e^(−t/τ)) = 6 (1 − e^(−t/4))

| t | t/τ | y(t) | % of final value |
|---|---|---|---|
| 4 s | 1τ | 3.79 | 63.2 % |
| 8 s | 2τ | 5.19 | 86.5 % |
| 12 s | 3τ | 5.70 | 95.0 % |
| **16 s** | **4τ** | **5.89** | **98.2 %** |

### Answer

> **K_p = 6, τ = 4 s, θ = 0 s, T_s = 4τ = 16 s** (2 % settling-band criterion; 98.2 % of final value attained).

### Discussion / assumptions
- The model is **self-regulating** (finite DC gain), **minimum-phase**, **non-oscillatory** and **first-order**.
- Because it is first order with no dead time, its phase lag is bounded by −90° as ω → ∞. **A pure first-order plant under proportional control can therefore never be driven unstable.** This result is used directly in Q4.2 and is the single most important conclusion of this question.
- T_s = 4τ is the 2 % criterion. Other conventions: 3τ → 5 % band, 5τ → 1 % band. State the criterion used.

---

## Q4.2 — Disturbance causing oscillation every 7 s

### Statement
A disturbance causes oscillation every 7 s. Identify possible causes, sensor delay effects and actuator saturation effects.

### Step 1 — Convert the observation into frequency-domain data

    T_u = 7 s
    ω_u = 2π/T_u = 2π/7 = 0.898 rad/s
    f_u = 1/7 = 0.143 Hz

### Step 2 — Prove the given model cannot explain the observation (key diagnostic)

Close the loop on G(s) = 6/(4s+1) with an ideal PI controller G_c(s) = K_c(1 + 1/(T_i s)).

Characteristic equation 1 + G_c G = 0:

    (4s + 1) + 6K_c (1 + 1/(T_i s)) = 0
    ⇒ 4s² + (1 + 6K_c) s + 6K_c/T_i = 0

Comparing with 4(s² + 2ζω_n s + ω_n²):

    ω_n = √( 6K_c / (4 T_i) )
    2ζω_n = (1 + 6K_c)/4

For **sustained** (undamped, ζ = 0) oscillation the s-coefficient must vanish:

    1 + 6K_c = 0  ⇒  K_c = −1/6

which is physically impossible for a direct-acting loop.

> **Conclusion: a first-order plant with P or PI control can only *ring and decay* — it cannot sustain a fixed-amplitude 7 s oscillation. A persistent 7 s cycle is therefore positive evidence of un-modelled phase lag or of a nonlinearity in the loop.**

(If the observed oscillation is *decaying*, PI action alone is a sufficient explanation: ω_d = ω_n√(1−ζ²) = 0.898 rad/s with ζ > 0.)

### Step 3 — Possible causes, ranked

#### Cause 1 — Un-modelled dead time / transport lag (most probable)

Require the loop phase to reach −180° at ω_u with proportional control on a first-order-plus-dead-time plant:

    −tan⁻¹(τ ω_u) − ω_u θ = −180°

    tan⁻¹(4 × 0.898) = tan⁻¹(3.590) = 74.44°
    ω_u θ = 180° − 74.44° = 105.56° = 1.8423 rad
    ⇒ θ = 1.8423 / 0.898 = **2.05 s**

**Independent physical corroboration (from §0.2):** the pipeline transport delay at maximum flow is θ = L/v = 3/1.273 = **2.36 s**. The 2.05 s required to explain a 7 s cycle and the 2.36 s the pipe geometry actually delivers agree to within 13 % — so **the pipeline transport lag alone accounts for the observed oscillation.**

Corresponding loop parameters at the ultimate frequency:

    |G(jω_u)| = 6 / √(1 + (τω_u)²) = 6 / √(1 + 3.590²) = 6/3.727 = 1.610
    K_u = 1/|G(jω_u)| = **0.621**

#### Cause 2 — Nonlinearity: valve stiction / hysteresis
The 8 % hysteresis reported in Q2.2 produces a classic **stick–slip limit cycle** when combined with integral action: the integrator winds up until breakaway force is exceeded, the valve jumps past the required position, and the cycle repeats.

*Signature:* near-square-wave CO, triangular or saw-tooth PV, and — the discriminating test — **amplitude and period largely independent of K_c**. Reducing controller gain does not remove it.

#### Cause 3 — External periodic disturbance
Pump vane-pass pulsation, the pulsating SOV supply of Q2.3 (100 cycles, 0–15 bar), or cyclic utility loading at 0.143 Hz being *passed through* rather than *generated by* the loop.

*Discriminating test:* place the controller in **MANUAL**. If the 7 s cycle persists with a frozen output, the source is external; if it stops, the loop is generating it.

### Step 4 — Sensor delay effects

Model the transmitter as a lag τ_s plus transport/scan delay θ_s. The added phase is

    φ_sensor(ω) = −tan⁻¹(τ_s ω) − ω θ_s

| Effect | Explanation | Quantification at ω_u = 0.898 rad/s |
|---|---|---|
| Direct loss of stability margin | Sensor phase lag subtracts from phase margin without changing DC gain, so it is invisible in steady state | **1 s of pure delay = 51.4° of phase lost** |
| Stale information | The controller corrects based on a PV that the process has already moved past → systematic overshoot → cycling | — |
| PV filtering makes it worse | Filters bought to suppress noise pay for it in phase lag | Require τ_f ≪ τ/10 = **0.4 s** |
| Discrete sampling | Adds an average delay of T_scan/2 | 100 ms scan → 50 ms → **2.6°**, negligible here |
| Sensor location | A thermowell with a 10–30 s response would dominate the 4 s plant τ entirely | design check required |

### Step 5 — Actuator saturation effects

| Effect | Mechanism | Consequence |
|---|---|---|
| **Loss of loop gain** | At 0 % or 100 % travel the valve no longer responds to CO; the loop is effectively **open** | Error grows unchecked; the plant runs in feedforward |
| **Integral windup** | The integrator keeps accumulating while the output is pinned at a limit | On recovery a large stored output is held → large overshoot → opposite-sign saturation → **self-sustaining limit cycle** whose period is set by wind-up/unwind time, not plant dynamics |
| **Amplitude-limited limit cycle** | Describing-function view: saturation is an amplitude-dependent gain N(A) that *falls* as amplitude rises | If the small-signal loop is unstable, amplitude grows until N(A)·\|G(jω_u)\| = 1 — giving a **bounded, constant-amplitude** oscillation rather than divergence. This is precisely what a steady 7 s cycle looks like |
| **Rate saturation** | Finite valve stroking speed | Behaves as an additional pure phase lag at ω_u |
| **Asymmetry** | Fail-close valves often open slower than they close | Produces asymmetric, non-sinusoidal cycles |

### Step 6 — Corrective actions (quantified)

1. **Anti-reset windup** — back-calculation or conditional integration whenever CO is at a limit. First action, zero cost.
2. **Detune using the measured T_u = 7 s and K_u = 0.621**

   | Method | K_c | T_i | T_d |
   |---|---|---|---|
   | Ziegler–Nichols PI | 0.45K_u = **0.28** | T_u/1.2 = **5.83 s** | — |
   | Ziegler–Nichols PID | 0.6K_u = **0.37** | T_u/2 = **3.50 s** | T_u/8 = **0.88 s** |
   | Tyreus–Luyben PI (robust, preferred for dead-time-dominant loops) | K_u/3.2 = **0.19** | 2.2T_u = **15.4 s** | — |

3. **Dead-time compensation** — a Smith predictor built on (K_p = 6, τ = 4 s, θ = 2.1 s), or simply accept the reduced achievable bandwidth.
4. **Gain scheduling on flow** — θ varies from 2.36 s to 14.14 s over the 5.9:1 turndown (§0.2). **No single fixed tuning can be both stable at low flow and responsive at high flow**; schedule K_c ∝ 1/θ or tune at the worst case (minimum flow).
5. **Mechanical remedy** — if stiction is confirmed, no tuning will remove the cycle. Fit a digital valve positioner or replace the trim (see the globe-valve selection of Q2.2).

### Answer summary

> ω_u = 0.898 rad/s. The given first-order model **cannot** sustain this oscillation (K_c = −1/6 would be required), so ~2.05 s of un-modelled dead time must exist — which the 3 m pipeline supplies (2.36 s at 6 L/min). With K_u = 0.621, retune to ZN-PI (K_c = 0.28, T_i = 5.83 s) with anti-windup, and gain-schedule on flow. Sensor lag consumes phase margin at 51.4° per second of delay; actuator saturation converts linear instability into a bounded limit cycle via integral windup.

---

## Q4.3 — Slurry transfer sketch and PID controller

### Statement
Design a hand sketch to transfer iron-ore slurry (60 % slurry, 40 % water by weight) to a height of 15 m into a horizontally mounted filter press on the 2nd floor, using: 1 pump, 1 tank, 2 manual valves, 1 On/Off valve, 1 NRV, 2 pressure transmitters, 1 density meter, a VFD pump and a drain valve. Explain the formula and functions of the components of a PID controller.

### Part A — Process calculations

**Assumptions (state these):**
- Iron ore is hematite, ρ_s = 4900 kg/m³; carrier water ρ_w = 1000 kg/m³.
- "60 % slurry / 40 % water by weight" is read as 60 % solids by mass.
- g = 9.81 m/s²; slurry is homogeneous and non-settling at design velocity.

**Slurry mixture density** (mass-fraction mixing rule):

    1/ρ_m = x_s/ρ_s + x_w/ρ_w
           = 0.60/4900 + 0.40/1000
           = 1.2245×10⁻⁴ + 4.0000×10⁻⁴
           = 5.2245×10⁻⁴ m³/kg

    ρ_m = **1914 kg/m³  (SG ≈ 1.91)**

**Solids concentration by volume:**

    C_v = (x_s/ρ_s) / (1/ρ_m) = 1.2245×10⁻⁴ / 5.2245×10⁻⁴ = **0.234 → 23.4 % v/v**

(A realistic filter-press feed concentration — this validates the assumption set.)

**Static head to the 2nd floor:**

    ΔP_static = ρ_m g h = 1914 × 9.81 × 15 = 2.817×10⁵ Pa = **2.82 bar**

**Total pump duty:**

    P_discharge = ΔP_static (2.82 bar) + ΔP_friction + ΔP_filter-press

The filter-press cake resistance is **not constant** — it rises through the cycle from roughly 1 bar at start of fill to 6–8 bar at the end of the squeeze. Hence:

    Design TDH ≈ **10–12 bar**

> **This rising, time-varying back-pressure is precisely why a VFD with closed-loop pressure control is mandatory and a fixed-speed pump is unacceptable.**

### Part B — The sketch

```
        ┌──────────────────── 2nd FLOOR  (+15 m) ─────────────────────┐
        │                                                             │
        │            ┌─────┐                                          │
        │            │ PT-2│  filter-press inlet pressure  = CV       │
        │            └──┬──┘                                          │
        │               │                                             │
        │   ───╫────────┴────────►  ┌───────────────────────────┐     │
        │     MV-2                  │  FILTER PRESS (horizontal)│     │
        │   (manual isolation)      └───────────────────────────┘     │
        │               ▲                                             │
        └───────────────┼─────────────────────────────────────────────┘
                        │
                        │   15 m VERTICAL RISER
                        │
                      ──┼──   XV-1   automatic ON/OFF valve (fail-close)
                        │
                      ──◄──   NRV    non-return valve
                        │
                     ┌──┴──┐
                     │ DT  │  DENSITY METER (Coriolis / nuclear)
                     └──┬──┘
                     ┌──┴──┐
                     │PT-1 │  pump discharge pressure
                     └──┬──┘
                        │
      ┌─────┐        ┌──┴──┐
      │ VFD ├────────┤  P  │  CENTRIFUGAL SLURRY PUMP  (final control element)
      └──▲──┘        └──┬──┘
         │              │
         │            ──╫──   MV-1   manual suction isolation
         │              │
         │      ┌───────┴──────────────┐
         │      │                      │
         │      │   SLURRY TANK T-101  │   agitated,  60/40 w/w,  SG 1.91
         │      │                      │
         │      └───────┬──────────┬───┘
         │              │        ──╫──  DRAIN VALVE (low point, flush)
         │              └──────────┘
         │
   ┌─────┴──────────┐
   │   PIC  (PID)   │ ◄──────── PT-2   (4–20 mA)   controlled variable
   │    PLC / DCS   │ ◄──────── DT     density — feed-quality interlock
   └────────────────┘ ◄──────── PT-1   pump protection / dry-run trip
            │
            └────────► VFD speed reference (4–20 mA / fieldbus)  = MV
```

### Part C — Component functions and placement justification

| Tag | Component | Location | Engineering justification |
|---|---|---|---|
| T-101 | Slurry tank | grade | Agitated to keep 23.4 % v/v solids in suspension; settling in the tank starves the pump |
| MV-1 | Manual valve 1 | tank outlet / pump suction | Isolates the pump for maintenance without draining the tank |
| P-101 | VFD-driven centrifugal slurry pump | grade, **flooded suction** | Positive suction head is essential: abrasive slurry will not self-prime and cavitation destroys slurry impellers. The **VFD speed is the manipulated variable** |
| PT-1 | Pressure transmitter 1 | pump discharge | Pump protection: dry-run and blocked-suction detection; gives pump ΔP for performance monitoring |
| DT | Density meter | discharge line, **vertical run** | Confirms feed SG = 1.91. Mounting in a vertical upward flow run prevents partial-fill / stratification error. Used as an interlock on XV-1, not inside the control loop |
| NRV | Non-return valve | immediately downstream of pump, **before** the riser | **Critical.** Prevents the 15 m / 2.82 bar slurry column from draining back through the pump on trip — which would cause reverse rotation and leave settled solids set hard in the casing |
| XV-1 | Automatic ON/OFF valve | after NRV | Fail-close sequencing valve for the fill / squeeze / blow-down cycle; closed on density or pressure interlock |
| MV-2 | Manual valve 2 | filter-press inlet | Local isolation for filter-cloth changes and cake discharge |
| PT-2 | Pressure transmitter 2 | filter-press inlet | **The controlled variable** — the press fill-pressure profile |
| DV | Drain valve | lowest point of tank / suction line | Water flush after every cycle. Without it, settled iron ore sets hard and the line is lost |

### Part D — Control philosophy

- **Single loop:** PV = PT-2, MV = VFD speed reference, controller = PIC (PID).
- **Setpoint is a ramped pressure profile**, not a fixed value: approximately 1 bar → 7 bar over the fill/squeeze cycle, matching the rising cake resistance.
- **DT (density)** acts as a permissive / interlock (trip XV-1 if SG falls outside band), *not* as a cascade secondary.
- **PT-1** provides pump protection and a suction-health trip.
- **Output clamp:** minimum VFD speed must maintain the slurry **critical settling velocity** (typically 1.5–2 m/s). Running slower deposits a solids bed and plugs the line — so the PID output low limit is a *process* constraint, not merely an actuator one.

### Part E — PID controller: formula and function of each term

**Ideal (ISA standard) form:**

    u(t) = K_c [ e(t) + (1/T_i) ∫₀ᵗ e(τ) dτ + T_d · de(t)/dt ] ,   e(t) = SP − PV

**Parallel (independent-gains) form:**

    u(t) = K_p e(t) + K_i ∫₀ᵗ e(τ) dτ + K_d de(t)/dt ,   K_i = K_c/T_i ,  K_d = K_c T_d

**Laplace / transfer-function form:**

    G_c(s) = K_c ( 1 + 1/(T_i s) + T_d s )

| Term | Acts on | Function | Application to this slurry loop |
|---|---|---|---|
| **P — Proportional** | the **present** error | Provides immediate corrective action proportional to error; sets loop speed and bandwidth | Drives VFD speed in proportion to the pressure error. **Alone it leaves a steady-state offset** — the press never reaches setpoint pressure |
| **I — Integral** | the **accumulated past** error | Integrates error until e = 0, eliminating offset; adds a pole at the origin (Type-1 loop) | **Essential here**, because cake resistance rises continuously so the required speed drifts throughout the cycle. Must be fitted with **anti-windup** since the VFD saturates at 50 Hz |
| **D — Derivative** | the **rate of change** (predicted future) of error | Anticipatory damping; adds phase lead, permitting higher K_c for the same stability margin | **Normally disabled or heavily filtered** on slurry service: pump vane-pass pulsation makes the signal noisy and derivative gain rises with frequency (∝ ω), amplifying that noise into the VFD. If used, apply as **derivative-on-measurement** (−T_d dPV/dt) |

**Mandatory practical refinements:**
- **Derivative on measurement** — avoids the derivative "kick" when SP is ramped.
- **Setpoint weighting / SP ramping** — avoids proportional kick on the fill profile.
- **Anti-reset windup** (back-calculation or integrator clamping) — the VFD *will* saturate.
- **Bumpless auto/manual transfer.**
- **Output limits 20–100 % speed** — see critical settling velocity above.

### Answer summary

> ρ_slurry = **1914 kg/m³ (SG 1.91)**, 23.4 % solids by volume, static head **2.82 bar**, design TDH **10–12 bar**. The sketch is a flooded-suction VFD slurry pump feeding a 15 m riser, with PT-2 at the press inlet as the controlled variable and VFD speed as the manipulated variable, under a ramped-pressure PID profile with anti-windup and a minimum-speed clamp set by the critical settling velocity. PID: u = K_c[e + (1/T_i)∫e dt + T_d de/dt]; P gives speed, I removes offset (essential as cake resistance rises), D is filtered or disabled due to pump pulsation noise.

---

# TASK 6 — INDUSTRIAL COMMUNICATION

---

## Q6.1 — CAN vs RS-485 vs UART for a 20 m industrial thermal plant

### Statement
Temperature sensors are distributed across a 20 m process area containing motors, VFDs, electrical heaters and welding machines. Choose between CAN, RS-485 and UART, and justify on noise immunity, communication distance, latency, scalability and reliability.

### Step 1 — Characterise the electrical environment (this drives the decision)

| Source | Disturbance mechanism | Magnitude |
|---|---|---|
| VFDs | IGBT switching at 2–16 kHz | dv/dt of 5–10 kV/µs, radiated and conducted |
| Welding machines | Arc striking, high di/dt | Broadband transients, large earth currents |
| Electrical heaters | Contactor/SCR switching | Conducted surges, harmonic distortion |
| Motors | Inrush, commutation | Magnetic field coupling |

The dominant consequence is **ground-potential difference**: with welders and VFDs sharing the earth system, 10–20 V of shift between the control panel and a sensor 20 m away is routine.

### Step 2 — Comparison of the three options

| Criterion | UART (TTL / RS-232) | RS-485 (2-wire, half duplex) | CAN (ISO 11898-2) |
|---|---|---|---|
| Signalling | **Single-ended**, referenced to local GND | **Differential**, ±200 mV receiver threshold | Differential, dominant / recessive |
| Noise immunity | **Poor** — no common-mode rejection | **High** — common-mode range −7 V to +12 V; twisted pair converts interference into rejected common mode | High, plus bit-stuffing and 15-bit CRC |
| Max distance | ~15 m (RS-232); <1 m (TTL) | **1200 m @ 100 kbps** | 1000 m @ 50 kbps; 40 m @ 1 Mbps |
| Topology | **Point-to-point only** | **Multidrop** — 32 unit loads (256 with 1/8-UL transceivers) | Multidrop, ~64–110 nodes |
| Latency / determinism | Not applicable | Deterministic **polled** master–slave | Deterministic by **priority arbitration**; lowest latency for high-priority frames |
| Payload per frame | Unlimited stream | Unlimited (Modbus: 252 bytes) | **8 bytes** (64 with CAN-FD) |
| Error handling | Parity only | Protocol CRC-16 + timeout/retry (Modbus RTU) | **Hardware ACK, error counters, bus-off fault confinement** |
| Availability of temperature transmitters | Universal | **Universal** (Modbus RTU is the de-facto standard) | Requires CANopen/DeviceNet stack; far fewer devices |
| Cost per node | Lowest | Low | Highest (controller + protocol stack) |

### Step 3 — Selection and justification

> ### **Selected: RS-485 physical layer running Modbus RTU.**

**1. Noise immunity — the deciding criterion.**
A single-ended UART references the signal to ground, so any ground-potential shift between panel and field appears **directly as signal error**. In an environment with VFDs and welders this is disqualifying. RS-485 transmits the signal as a **difference** across a twisted pair: interference couples equally into both conductors, becomes common mode, and is rejected over a −7 V to +12 V window while the receiver still resolves a ±200 mV differential. This criterion alone eliminates UART.

**2. Communication distance.**
20 m is trivial for RS-485 (1200 m capability, **60× headroom**) and for CAN (1000 m). It is marginal for RS-232 and impossible for TTL UART. The headroom means future expansion of the process area requires no re-engineering of the physical layer.

**3. Latency.**
Temperature is a **slow** process variable — thermal time constants are seconds to minutes, so a 100–500 ms scan is more than sufficient. The binding constraint is the controller time constant, not Nyquist.

*Worked latency budget — 12 sensors, Modbus RTU, 8N1:*

| Item | @ 19200 bps | @ 115200 bps |
|---|---|---|
| Request (8 B) + response (9 B) = 17 B = 187 bits | 9.74 ms | 1.62 ms |
| 3.5-character silent interval | 2.0 ms | 0.34 ms |
| Slave turnaround / processing | ~8 ms | ~3 ms |
| **Per node** | **≈ 20 ms** | **≈ 5 ms** |
| **Full 12-sensor scan** | **≈ 240 ms** | **≈ 60 ms** |

Comfortably adequate. CAN's sub-millisecond priority latency is real but **not required** for temperature; paying its cost and complexity here is not justifiable.

**4. Scalability.**
One shielded twisted pair daisy-chained past all sensors. Standard transceivers support 32 unit loads; 1/8-unit-load transceivers support 256. Adding a sensor means adding a node and a register-map entry — **no new cable run**. UART would require 12 dedicated ports and 12 separate cables.

**5. Reliability.**
Modbus RTU's CRC-16 detects all single-bit, double-bit and burst errors up to 16 bits. Timeout-and-retry handles transient corruption. A failed slave is detected by exception response or timeout and is isolated diagnostically without bringing down the bus.

### Step 4 — Mandatory installation practice

The noise immunity above is only realised if the installation is correct:

- **Shielded twisted pair, 120 Ω characteristic impedance** (e.g. Belden 3105A / equivalent instrumentation cable).
- **Daisy-chain topology only** — no star, no stubs longer than 0.3 m.
- **120 Ω termination resistors at the two physical ends only** (not at intermediate nodes).
- **Fail-safe bias resistors** (typically 560 Ω–1 kΩ pull-up/pull-down) so the idle bus state is defined and noise cannot be decoded as a start bit.
- **Shield bonded at one point only** (panel end) to prevent a shield ground loop.
- **Segregation:** route ≥300 mm from VFD motor cables; cross at 90° where unavoidable; use separate cable trays.
- **Galvanically isolated RS-485 transceivers** wherever the ground-potential difference may exceed the −7 V/+12 V common-mode window — strongly recommended given the welding load.

### Step 5 — Runner-up and rejected option

| Verdict | Option | Reason |
|---|---|---|
| **Selected** | RS-485 / Modbus RTU | Differential noise immunity, multidrop scalability, adequate deterministic latency, universal device support, lowest lifecycle cost |
| **Runner-up** | CAN (CANopen) | Choose instead if the same bus must also carry fast, event-driven control or safety data where a single faulty node must not corrupt the network (bus-off confinement) and priority determinism is a hard requirement |
| **Rejected** | UART (TTL/RS-232) | Single-ended (no common-mode rejection), point-to-point only, ≤15 m, no arbitration or error recovery. Fails on noise immunity, distance and scalability simultaneously |

---

## Q6.2 — Packet transmission time at 115200 bps

### Statement
A pressure-monitoring packet contains 64 bytes at 115200 bps.
(a) Calculate the approximate transmission time for one packet.
(b) Assuming 8N1 format (8 data bits, no parity, 1 stop bit), calculate the approximate transmission time for one complete packet.

### Given
- Packet size = 64 bytes
- Bit rate R = 115200 bps

### Part (a) — Raw payload bits only

    N_bits = 64 bytes × 8 bits/byte = 512 bits

    t = N_bits / R = 512 / 115200 = 4.4444×10⁻³ s

> ### **t ≈ 4.44 ms**

### Part (b) — Including 8N1 framing

One 8N1 character frame:

    1 start bit + 8 data bits + 0 parity bits + 1 stop bit = **10 bits per byte**

    Time per character = 10 / 115200 = 86.8 µs

    N_bits = 64 bytes × 10 bits/byte = 640 bits

    t = 640 / 115200 = 5.5556×10⁻³ s

> ### **t ≈ 5.56 ms**

### Interpretation

| Quantity | Value |
|---|---|
| Framing overhead | (640 − 512)/512 = **25 %** |
| Protocol efficiency | 8/10 = **80 %** |
| Effective payload throughput | 115200 × 0.8 / 8 = **11,520 bytes/s** |
| Maximum packet rate (100 % bus load) | 1 / 5.556 ms = **180 packets/s** |
| Time per character | **86.8 µs** |

### Assumptions
1. Continuous, back-to-back transmission with no inter-character idle gap.
2. No bus turnaround delay, slave processing time or retries.
3. No higher-layer framing overhead beyond the 64 bytes stated.

**Practical correction:** in a real Modbus RTU link the mandatory **3.5-character silent interval** (3.5 × 86.8 µs = **304 µs**) must precede and follow the frame, plus slave processing time. Realistic frame-to-frame spacing is therefore ≈ **6.2 ms plus turnaround**, not 5.56 ms.

---

## Q6.3 — PLC logic sequence for 2000-sample acquisition with 3-sigma detection

### Statement
A PLC CPU has an analog input conversion/sampling speed of 500 µs per channel. To acquire 2000 samples of a flow transmitter in 200 s, for FT values of approximately 2.2–3.5 m³/hr, write a logic sequence for capturing the data and computing the mean mass flow rate (kg/s) with density 5.204 kg/m³, and code 3-sigma deviation logic. Overall CPU scan time is around 15 ms.

### Step 1 — Timing analysis (performed first; it dictates the architecture)

| Quantity | Derivation | Value |
|---|---|---|
| Required samples | given | 2000 in 200 s |
| **Sample period T_s** | 200 s / 2000 | **100 ms (10 Hz)** |
| ADC conversion time | given | 500 µs per channel |
| CPU scan time | given | 15 ms |
| Scans per sample | 100 / 15 | **6.67 — not an integer** |
| ADC load per scan | 0.5 / 15 | 3.3 % — **conversion is not the bottleneck** |
| Nyquist limit | f_s / 2 | signal content must be **< 5 Hz**; anti-alias filter required |

**Critical conclusion:**

> Because 100 ms is **not an integer multiple** of the 15 ms scan time, sampling from the main cyclic program (OB1) would introduce **up to 15 ms of jitter — 15 % of the sample period** — and would drift by one whole sample over the 200 s run, corrupting the timebase.
>
> **Therefore the acquisition must be executed from a 100 ms timer/cyclic-interrupt organisation block** (Siemens OB35 / Rockwell Periodic Task / IEC 61131 timed task), **not from the main scan.** This makes the sample instants hardware-timed and jitter-free.
>
> If only OB1 is available, use a free-running system-clock comparison — `IF (SysTime − t_last) ≥ 100 ms` — rather than a retriggered TON, to prevent cumulative drift.

### Step 2 — Scaling to mass flow rate

**Assumption:** FT calibrated 0–5 m³/hr → 4–20 mA → 12-bit ADC (0–4095 counts). Density ρ = 5.204 kg/m³ (note: a *gas* service, given the low density).

    Q [m³/hr]  = (RAW / 4095) × 5.0
    ṁ [kg/s]   = Q × ρ / 3600

**Resolution check:**

    ΔQ = 5 / 4095 = **1.22×10⁻³ m³/hr**
    Δṁ = 1.22×10⁻³ × 5.204 / 3600 = **1.77×10⁻⁶ kg/s**  (≈ 0.04 % of reading — adequate)

**Expected values over the stated FT band:**

| Q (m³/hr) | Calculation | ṁ (kg/s) |
|---|---|---|
| 2.2 (min) | 2.2 × 5.204 / 3600 | **3.180×10⁻³** |
| 2.85 (mid) | 2.85 × 5.204 / 3600 | **4.120×10⁻³** |
| 3.5 (max) | 3.5 × 5.204 / 3600 | **5.059×10⁻³** |

> **Expected mean mass flow rate ≈ 4.12×10⁻³ kg/s (4.12 g/s)**

**Memory requirement:** 2000 × REAL (4 bytes) = **8 kB** array.

### Step 3 — Statistics (single-pass, no array re-scan)

Accumulate Σx and Σx² on the fly:

    μ = Σx / N

    σ = √[ ( Σx² − (Σx)²/N ) / (N − 1) ]        (Bessel-corrected sample std. deviation)

    UCL = μ + 3σ        LCL = μ − 3σ

**Statistical debounce requirement:** for a normal distribution, ±3σ encloses 99.73 % of samples. In 2000 samples the expected number of *false* alarms is

    2000 × 0.0027 ≈ **5.4**

> Therefore a **single** excursion must not raise an alarm. Require **3 consecutive violations** (Western Electric rule 1 with debounce) before asserting the alarm bit.

**Numerical-precision warning:** with ṁ ≈ 4×10⁻³, the term (Σx² − (Σx)²/N) suffers **catastrophic cancellation** in 32-bit REAL. Use **LREAL (64-bit)**, or scale the variable to g/s, or use Welford's online recurrence. This is the principal implementation trap in this question.

### Step 4 — Structured Text implementation

```pascal
(*=================== DECLARATIONS ===================*)
VAR
    Step        : INT   := 0;
    N           : INT   := 0;
    RAW         : INT;                      (* 12-bit, 0..4095 *)
    Q           : LREAL;                    (* m3/hr *)
    mdot        : LREAL;                    (* kg/s  *)
    Buf         : ARRAY[1..2000] OF LREAL;
    Sx, Sxx     : LREAL := 0.0;             (* Sum x , Sum x^2 *)
    Mu, Sigma   : LREAL;
    UCL, LCL    : LREAL;
    CoV         : LREAL;
    ViolCnt     : INT   := 0;
    Alarm       : BOOL  := FALSE;
    Done        : BOOL  := FALSE;
    Fault       : BOOL  := FALSE;
    RangeWarn   : BOOL  := FALSE;
END_VAR

VAR CONSTANT
    RHO   : LREAL := 5.204;                 (* kg/m3          *)
    SPAN  : LREAL := 5.0;                   (* m3/hr at 20 mA *)
    NMAX  : INT   := 2000;
    QLO   : LREAL := 2.2;
    QHI   : LREAL := 3.5;
END_VAR

(*===== CALLED FROM THE 100 ms CYCLIC-INTERRUPT OB - NOT FROM OB1 =====*)

CASE Step OF

0:  (* ---------- INIT / ARM ---------- *)
    IF StartPB AND NOT Done THEN
        N       := 0;
        Sx      := 0.0;
        Sxx     := 0.0;
        ViolCnt := 0;
        Alarm   := FALSE;
        Fault   := FALSE;
        Step    := 10;
    END_IF;

10: (* ---------- ACQUIRE: exactly one sample per 100 ms interrupt ---------- *)

    (* 1. Read and validate the raw channel *)
    RAW := AI_Ch1;
    IF (RAW < 205) OR (RAW > 4095) THEN     (* < 4 mA => open loop / broken wire *)
        Fault := TRUE;
        Step  := 90;
        RETURN;
    END_IF;

    (* 2. Scale to engineering units *)
    Q    := (LREAL(RAW) / 4095.0) * SPAN;   (* m3/hr *)
    mdot := Q * RHO / 3600.0;               (* kg/s  *)

    (* 3. Plausibility check against the declared FT band *)
    IF (Q < QLO * 0.9) OR (Q > QHI * 1.1) THEN
        RangeWarn := TRUE;                  (* flag only - do not abort the run *)
    END_IF;

    (* 4. Store and accumulate in a single pass *)
    N      := N + 1;
    Buf[N] := mdot;
    Sx     := Sx  + mdot;
    Sxx    := Sxx + mdot * mdot;

    (* 5. Live 3-sigma test, once the baseline is statistically valid *)
    IF N > 30 THEN
        Mu    := Sx / LREAL(N);
        Sigma := SQRT( (Sxx - (Sx * Sx) / LREAL(N)) / LREAL(N - 1) );
        UCL   := Mu + 3.0 * Sigma;
        LCL   := Mu - 3.0 * Sigma;

        IF (mdot > UCL) OR (mdot < LCL) THEN
            ViolCnt := ViolCnt + 1;
            IF ViolCnt >= 3 THEN            (* debounce: 3 consecutive *)
                Alarm := TRUE;
            END_IF;
        ELSE
            ViolCnt := 0;                   (* reset on any in-band sample *)
        END_IF;
    END_IF;

    IF N >= NMAX THEN                       (* 2000 samples = 200 s *)
        Step := 20;
    END_IF;

20: (* ---------- FINAL BATCH STATISTICS ---------- *)
    Mu     := Sx / LREAL(NMAX);
    Sigma  := SQRT( (Sxx - (Sx * Sx) / LREAL(NMAX)) / LREAL(NMAX - 1) );
    UCL    := Mu + 3.0 * Sigma;
    LCL    := Mu - 3.0 * Sigma;
    CoV    := 100.0 * Sigma / Mu;           (* % - process stability index *)

    MeanMassFlow := Mu;                     (* kg/s -> HMI / historian *)
    Done   := TRUE;
    Step   := 0;

90: (* ---------- FAULT ---------- *)
    Alarm := TRUE;
    IF ResetPB THEN
        Fault := FALSE;
        Step  := 0;
    END_IF;

END_CASE;
```

### Step 5 — Sequence summary (flow-chart form)

```
        START
          │
          ▼
      INIT: clear N, Sx, Sxx, ViolCnt, flags
          │
          ▼
  ┌── [100 ms CYCLIC INTERRUPT] ──────────────────────┐
  │                                                   │
  │   READ AI channel  (500 us conversion)            │
  │          │                                        │
  │          ▼                                        │
  │   VALIDATE 4-20 mA  (RAW < 205 -> FAULT)          │
  │          │                                        │
  │          ▼                                        │
  │   SCALE:  Q    = RAW/4095 x 5.0     [m3/hr]       │
  │           mdot = Q x 5.204 / 3600   [kg/s]        │
  │          │                                        │
  │          ▼                                        │
  │   STORE Buf[N] ;  Sx += mdot ;  Sxx += mdot^2     │
  │          │                                        │
  │          ▼                                        │
  │   IF N > 30 :                                     │
  │        Mu, Sigma  ->  UCL = Mu+3s , LCL = Mu-3s   │
  │        out-of-band ?  -> ViolCnt++                │
  │        ViolCnt >= 3   -> ALARM                    │
  │        in-band        -> ViolCnt = 0              │
  │          │                                        │
  │          ▼                                        │
  │      N = 2000 ?  ── NO ──► wait next interrupt ───┘
  │          │
  │         YES
  │          ▼
  │   FINAL: Mu, Sigma, CoV  ->  HMI / historian
  │          ▼
  └────────  DONE
```

### Key engineering points to present

1. **Sample from a hardware-timed 100 ms interrupt, not the 15 ms main scan**, because 100/15 = 6.67 is non-integral (15 % jitter and cumulative drift otherwise).
2. **The 500 µs ADC conversion is only 3.3 % of one scan** and is therefore not the limiting factor — the scan time is.
3. **Nyquist:** 10 Hz sampling admits signal content only below 5 Hz; an anti-alias filter is required.
4. **3σ needs a debounce**, because ~5.4 false alarms are statistically *expected* in 2000 normal samples.
5. **Use LREAL** to avoid catastrophic cancellation at ṁ ≈ 4×10⁻³ kg/s.
6. **Expected result:** mean mass flow ≈ **4.12×10⁻³ kg/s**, over a band of 3.18×10⁻³ to 5.06×10⁻³ kg/s.

---

## Q6.4 — The OSI model and its comparison with TCP/IP

### Statement
Explain the OSI model and describe the function of each of its seven layers. Compare the OSI model with the TCP/IP model.

### Part A — What the OSI model is

The **Open Systems Interconnection (OSI)** reference model, ISO/IEC 7498-1 (1984), is a seven-layer abstract framework that partitions the functions of a communication system into a stack of layers. Each layer serves the layer above and is served by the layer below, and communicates logically with its **peer layer** on the remote system.

Its purpose is **layer independence**: a layer's implementation may be replaced (copper to fibre at Layer 1, for example) without altering any other layer.

### Part B — The seven layers

| # | Layer | Function | Protocol Data Unit | Industrial example |
|---|---|---|---|---|
| **7** | **Application** | Provides network services directly to the user process; defines the **semantics** of the data exchanged | Data | Modbus function codes, OPC UA, MQTT, HTTP, FTP |
| **6** | **Presentation** | **Syntax**: data encoding and serialisation, encryption, compression — makes data representation machine-independent | Data | TLS, ASCII/EBCDIC, OPC UA binary encoding, JPEG |
| **5** | **Session** | Establishes, manages, synchronises and terminates **dialogues** between applications; checkpointing and recovery | Data | RPC, NetBIOS, OPC UA SecureChannel/Session |
| **4** | **Transport** | **End-to-end** delivery between processes: segmentation and reassembly, flow control, error recovery, port addressing | Segment (TCP) / Datagram (UDP) | TCP port 502 (Modbus TCP), UDP (EtherNet/IP implicit I/O) |
| **3** | **Network** | **Logical addressing and routing between networks**; path determination, fragmentation, congestion control | Packet | IP, ICMP; routers operate here |
| **2** | **Data Link** | Node-to-node transfer across **one** physical link: framing, **physical (MAC) addressing**, error detection (CRC), media-access control | Frame | Ethernet MAC, switches, CAN arbitration, Modbus RTU framing |
| **1** | **Physical** | Transmission of raw **bits**: voltage levels, bit timing, modulation, connectors, cabling | Bit | RS-485 differential pair, RJ45/Cat6, fibre, hubs |

**Mnemonic (Layer 7 → 1):** *All People Seem To Need Data Processing.*

**Encapsulation.** As data descends the stack, each layer prepends its own header:

    L7 Data → L4 Segment → L3 Packet → L2 Frame (+ trailer/CRC) → L1 Bits

and each header is stripped in turn on the way up at the receiver. This is the mechanism by which layer independence is realised.

### Part C — Comparison: OSI vs TCP/IP

| Aspect | OSI model | TCP/IP model |
|---|---|---|
| Number of layers | **7** | **4** (or 5, if Physical is split from Network Access) |
| Origin | ISO/IEC 7498-1, 1984 — the **model was designed first**, protocols afterwards | ARPANET, 1970s — the **protocols were built first**, the model described afterwards |
| Status | Reference and teaching model; never fully implemented as a deployed stack | The de-facto operational standard of the internet |
| Layers 5–7 | Three distinct layers (Session, Presentation, Application) | Merged into a single **Application** layer |
| Layers 1–2 | Two distinct layers (Physical, Data Link) | Merged into a single **Network Access / Link** layer |
| Transport layer | Supports connection-oriented **and** connectionless service | Same (TCP connection-oriented, UDP connectionless) |
| Network layer | Supports connection-oriented and connectionless | **Connectionless only** (IP) |
| Protocol coupling | **Protocol-independent** and generic | **Protocol-specific** — TCP and IP are named in the model itself |
| Strength | Clear conceptual separation; excellent for teaching, design and fault diagnosis | Proven, simple, universally deployed |

**Layer mapping:**

```
        OSI                             TCP/IP
    ┌──────────────┐
  7 │ Application  │ ┐
    ├──────────────┤ │
  6 │ Presentation │ ├──────────►  Application
    ├──────────────┤ │             (HTTP, MQTT, OPC UA, Modbus TCP)
  5 │   Session    │ ┘
    ├──────────────┤
  4 │  Transport   │ ───────────►  Transport      (TCP, UDP)
    ├──────────────┤
  3 │   Network    │ ───────────►  Internet       (IP, ICMP, ARP)
    ├──────────────┤
  2 │  Data Link   │ ┐
    ├──────────────┤ ├──────────►  Network Access (Ethernet, Wi-Fi, RS-485)
  1 │   Physical   │ ┘
    └──────────────┘
```

### Part D — Relevance to this plant

- The **RS-485 / Modbus RTU** link selected in Q6.1 occupies only **L1** (RS-485 electrical), **L2** (RTU framing + CRC-16) and **L7** (Modbus function codes). It deliberately **omits L3–L6**. That omission is exactly why it is non-routable but also low-latency and low-overhead.
- Migrating to **Modbus TCP** inserts genuine L3 and L4 (IP + TCP port 502), making the data routable onto the plant network — at the cost of additional latency and jitter.
- **PROFINET RT** deliberately **bypasses L3 and L4 entirely**, running VLAN-tagged frames directly at L2 (Ethertype 0x8892) to achieve deterministic cycle times.

> These three cases are a direct demonstration of why the layered model is an engineering tool and not merely a teaching device: **what you include and what you omit from the stack determines routability, determinism and overhead.**

---

## Q6.5 — Industrial Internet of Things (IIoT)

### Statement
What is an Industrial Internet of Things (IIoT) system? Explain its main components and how it is used in industries for real-time monitoring, data collection and process automation.

### Part A — Definition

> **IIoT is the application of networked sensors, actuators, edge computing and analytics to industrial assets, so that machine-generated data is continuously acquired, contextualised and acted upon to improve availability, quality, throughput and energy efficiency.**

**How IIoT differs from consumer IoT:**

| Attribute | Consumer IoT | **Industrial IoT** |
|---|---|---|
| Timing requirement | Best effort | **Deterministic / real-time** |
| Consequence of failure | Inconvenience | **Safety, environmental and production loss** |
| Environment | Benign | Harsh — EMI, vibration, temperature, hazardous area |
| Asset lifetime | 2–5 years | **20–30 years** |
| Interoperability | Greenfield | Must coexist with legacy OT protocols |
| Security model | Confidentiality-led | **Availability- and safety-led (IEC 62443)** |

### Part B — Main components: the five-layer IIoT architecture

**1. Perception / Sensing layer — "the things"**
Smart sensors and actuators: temperature, pressure, flow and level transmitters; vibration, current and acoustic sensors; RFID and machine vision. In this facility: the 12 distributed temperature transmitters (Q6.1), PT-1 and PT-2 and the density meter (Q4.3), and the flow transmitter (Q6.3). Increasingly these are **digitally native** (HART, IO-Link, Ethernet-APL) and carry **diagnostics alongside the primary variable**.

**2. Network / Connectivity layer**
Transports data from the field to the edge and beyond.
- *Wired:* RS-485/Modbus, PROFINET, EtherNet/IP, EtherCAT, Ethernet-APL
- *Wireless:* WirelessHART, ISA100.11a, LoRaWAN, 5G URLLC, Wi-Fi 6
- *Messaging:* **MQTT** (with Sparkplug B) and **OPC UA** (client/server and pub/sub)

OPC UA is the pivotal interoperability standard because it carries an **information model** — semantics and asset context — not merely raw values.

**3. Edge layer — "the computer next to the machine"**
Edge gateways and industrial PCs performing protocol translation, filtering and aggregation, store-and-forward buffering, local analytics and ML inference.

*Why the edge is architecturally essential:*

| Driver | Explanation |
|---|---|
| **Bandwidth** | 12 sensors at 100 Hz over 30 days = 3.1×10⁹ samples (cf. Q5.2). Shipping all of it to the cloud is wasteful; the edge transmits **features and exceptions** |
| **Latency** | Closed-loop control cannot tolerate a cloud round trip |
| **Resilience** | The plant must continue to run when the WAN link is down |
| **Security** | The edge is the enforcement point of the IT/OT boundary |

**4. Platform / Data layer**
Cloud or on-premise: time-series historian, data lake, device management, **digital twin**, asset registry, analytics and ML training. Responsible for ingestion, storage and **contextualisation** — binding a signal to its position in the asset hierarchy.

**5. Application / Presentation layer**
Dashboards, alarm and notification services, CMMS and ERP/MES integration, reporting, and closed-loop optimisation recommendations.

**Cross-cutting: Security (IEC 62443).**
Defence in depth — segmentation into zones and conduits, an OT/IT DMZ, firewalls or unidirectional gateways, device identity and certificates, signed firmware, role-based access control, and continuous monitoring. In IIoT the threat model includes **safety**, not merely data loss, so security must be architectural rather than an add-on.

### Part C — Industrial use cases

| Use case | Mechanism | Value delivered |
|---|---|---|
| **Real-time monitoring** | Streaming PV and alarm data to dashboards; exception reporting from the edge | Immediate visibility across distributed assets; faster operator response |
| **Predictive maintenance** | Vibration, current and temperature trending with edge ML; detects bearing wear, pump cavitation, heater-element degradation before failure | Converts unplanned downtime to planned; typically 20–40 % maintenance cost reduction |
| **Statistical process control** | The 3σ logic of Q6.3 run continuously across all assets and cross-correlated | Detects drift and excursions before product is scrapped |
| **Instrument health and calibration** | Transmitter self-diagnostics (HART/IO-Link) flag zero and span drift — directly addressing the +0.08 bar drift of Q3.4 | **Condition-based** calibration replaces fixed-interval calibration |
| **Energy optimisation** | Sub-metering plus load correlation; VFD energy profiling | Identifies the dominant consumers; supports ISO 50001 |
| **Digital twin** | A physics-plus-data model run in parallel with the real asset | Model-based fault detection: raise a flag when measured ≠ predicted — e.g. detecting the 20 % heat-exchanger fouling of Q2.4, or the 20 % pipe scale deposition of Q1.4, from a rising ΔP residual |
| **Process automation** | Optimised setpoints pushed from analytics back to the PLC, with the PLC retaining safety authority | Yield and throughput improvement without ceding safety to the cloud |

### Part D — Application to this facility

The existing PLC panel of Q6.3 becomes an **edge node**:

- It **retains** the deterministic 100 ms control and acquisition loops locally.
- An **OPC UA / MQTT gateway** publishes derived information to the plant historian:
  - flow statistics μ, σ and CoV, and 3σ excursion events (Q6.3)
  - pipeline ΔP trend as a **scale-deposition indicator** (Q1.4)
  - valve hysteresis signature as a **stiction indicator** (Q2.2)
  - heat-exchanger fouling factor (Q2.4)
  - control-loop oscillation index — the 7 s cycle of Q4.2 — as a **loop-health indicator**
- Analytics then convert these indicators into maintenance work orders.

> **Guiding principle: control stays at the edge; insight moves to the cloud.** This is the defining characteristic of a correctly architected IIoT system, and the reason IIoT augments rather than replaces the existing control system.

---

# Appendix A — Consolidated answers

| Question | Result |
|---|---|
| **Q4.1** | K_p = 6; τ = 4 s; θ = 0 s; **T_s = 4τ = 16 s** (2 % band) |
| **Q4.2** | ω_u = 0.898 rad/s. The given first-order model **cannot** sustain oscillation (would need K_c = −1/6), so θ ≈ **2.05 s** of un-modelled dead time exists — corroborated by the pipeline transport delay of **2.36 s** at 6 L/min. K_u = **0.621**. Retune ZN-PI: K_c = 0.28, T_i = 5.83 s, with anti-windup and gain scheduling on flow |
| **Q4.3** | ρ_slurry = **1914 kg/m³ (SG 1.91)**; 23.4 % solids v/v; static head **2.82 bar**; design TDH **10–12 bar**. PID: u = K_c[e + (1/T_i)∫e dt + T_d de/dt] |
| **Q6.1** | **RS-485 / Modbus RTU** selected. 12-node scan ≈ **240 ms** @ 19200 bps (≈60 ms @ 115200 bps). CAN is runner-up; UART rejected |
| **Q6.2** | (a) **4.44 ms**  (b) **5.56 ms**; 25 % framing overhead, 80 % efficiency |
| **Q6.3** | T_s = **100 ms**; use a **100 ms cyclic-interrupt OB**, not the 15 ms scan (100/15 = 6.67). Mean ṁ ≈ **4.12×10⁻³ kg/s**; band 3.18×10⁻³ to 5.06×10⁻³ kg/s. 3σ with 3-consecutive debounce (≈5.4 false alarms expected otherwise) |
| **Q6.4** | 7 OSI layers mapped to 4 TCP/IP layers; Modbus RTU occupies L1+L2+L7 only |
| **Q6.5** | 5-layer IIoT architecture with IEC 62443 security cross-cutting; control at the edge, insight in the cloud |

---

# Appendix B — Assumptions register

| # | Question | Assumption | Justification |
|---|---|---|---|
| 1 | Q4.1 | T_s = 4τ corresponds to the 2 % settling band | Standard convention; stated explicitly |
| 2 | Q4.2 | The un-modelled lag is pipeline transport delay | Independently computed as 2.36 s at 6 L/min from the given D = 10 mm and L = 3 m, against the 2.05 s required by the 7 s period — a 13 % agreement |
| 3 | Q4.2 | Ideal (non-interacting) PI controller form | Standard textbook form; the conclusion is unchanged for the interacting form |
| 4 | Q4.3 | Iron ore is hematite, ρ_s = 4900 kg/m³ | Typical hematite 4900–5100 kg/m³; result C_v = 23.4 % is a realistic filter-press feed, validating the assumption |
| 5 | Q4.3 | "60 % slurry by weight" means 60 % solids by mass | Standard slurry-engineering convention |
| 6 | Q4.3 | Filter-press back-pressure rises to 6–8 bar through the cycle | Typical membrane/recessed-plate press operation |
| 7 | Q6.1 | Modbus RTU at 19200 bps, 8N1, 12 nodes | Most common industrial default; 115200 bps also evaluated |
| 8 | Q6.2 | Continuous back-to-back transmission, no turnaround, no retries | Required for the "approximate" time requested; the practical correction is stated separately |
| 9 | Q6.3 | FT calibrated 0–5 m³/hr → 4–20 mA → 12-bit ADC (0–4095) | The stated 2.2–3.5 m³/hr band sits comfortably inside a 0–5 m³/hr span |
| 10 | Q6.3 | 100 ms cyclic-interrupt OB is available on the CPU | Standard on all modern PLC platforms; a free-running-clock fallback for OB1 is given |
| 11 | General | g = 9.81 m/s²; steady-state, isothermal, incompressible liquid unless stated | Standard engineering practice |

---

*End of solution manual — Task 4 and Task 6.*
