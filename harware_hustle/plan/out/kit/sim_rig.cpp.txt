// Software-in-the-loop test: compiles the real firmware against mock ESP32 functions and a simple
// tank/pump model, then plays the competition sequence and failure cases.
//   g++ -std=gnu++14 -O2 -Itest/mock test/sim_rig.cpp -o /tmp/sim_rig && /tmp/sim_rig
#include "mock/Arduino.h"

namespace sim {
uint64_t us = 0;
int pinLevel[40] = {0};
int pinOut[40] = {0};
uint32_t mv[40] = {0};
uint16_t touch[40] = {0};
uint32_t pwm[16] = {0};
std::string rx, tx;
uint32_t gpioIn = 0;
}  // namespace sim
SimSerial Serial;
void (*simIsr)() = nullptr;

#include "../src/main.cpp"

#include <functional>
#include <vector>

struct Scenario {
  const char* name;
  double tk1 = 3.4, sump = 2.3, tk3 = 4.2;   // litres; sump starts just below the trip
  double trip = 2.5;                          // sump volume at LS-01 trip
  double pourAt = 90, pourL = 0.8;            // s, L (pourAt < 0: no pour)
  double bvOpenDelay = 5;                     // s after C2_OPEN_BV01 (negative: never)
  double bvOpenSecondDelay = 3;               // s after a re-prompt
  bool floatBroken = false;
  double ftUnplugAt = -1;                     // s
  double currentNoise = 0.03;                 // relative
  double q1Max = 6.4, q1SuctionCap = 3.6;     // P-01 through SOV-01
  double q2 = 3.0;                            // P-02 at 100% with BV-02 trimmed
  double q3PerDuty = 7.0;                     // P-03 L/min per unit duty
  std::vector<std::string> commands;          // console lines sent at t = 0.5 s
  double runFor = 480;                        // s
  const char* dumpPrefix = nullptr;           // write console-format CSVs for --replay practice
};

struct Result {
  std::vector<std::string> events;
  double p2StoppedInCase1 = 0, maxSump = 0, minSump = 99, tk3End = 0, completeAt = -1, flowAvgC1 = 0;
  int holds = 0;
  std::string completeSource;
};

static double rnd() { return (std::rand() / (double)RAND_MAX) * 2 - 1; }

static Result run(const Scenario& sc) {
  // reset firmware globals that persist between runs
  sim::us = 0;
  sim::tx.clear();
  sim::rx.clear();
  for (auto& p : params) p.v = p.def;
  state = St::IDLE;
  stateMs = 0;
  lsh = Debounce();
  button = Debounce();
  zso = Debounce();
  alarms = 0;
  p2Trip = false;
  flushReprompts = 0;
  P1.cmd = P1.out = P2.cmd = P2.out = P3.cmd = P3.out = 0;
  P1.en = P2.en = P3.en = false;
  sov.cmd = sov.out = false;
  flow = Flow();
  fdi = Fdi();
  fic = Fic();
  ftCount = ftLastRise = ftHighUs = ftGlitch = 0;
  lastStartMs = 0;

  Result R;
  FILE* fTele = nullptr;
  FILE* fEv = nullptr;
  if (sc.dumpPrefix) {
    fTele = fopen((std::string(sc.dumpPrefix) + "_telemetry.csv").c_str(), "w");
    fEv = fopen((std::string(sc.dumpPrefix) + "_events.csv").c_str(), "w");
    fprintf(fEv, "host_time,t_ms,tag,text\n");
  }
  double tk1 = sc.tk1, sump = sc.sump, tk3 = sc.tk3;
  bool bvOpen = false, ftLevel = false, pressed = false, fsw = false;
  double phase = 0, bvDue = -1, c1Start = -1, c1Flow = 0, c1N = 0;
  sim::pinLevel[pin::BUTTON] = HIGH;
  setup();
  const double dt = 1e-4;  // 100 us
  size_t parsed = 0;
  for (long step = 0; step < (long)(sc.runFor / dt); step++) {
    const double t = step * dt;
    sim::us = (uint64_t)(t * 1e6);

    // operator actions
    if (step == 5000)
      for (auto& c : sc.commands) sim::rx += c + "\n";
    if (t >= 1.0 && t < 1.2) pressed = true;
    else pressed = false;
    sim::pinLevel[pin::BUTTON] = pressed ? LOW : HIGH;
    if (sc.pourAt >= 0 && step == (long)(sc.pourAt / dt)) sump += sc.pourL;
    if (bvDue >= 0 && t >= bvDue) {
      bvOpen = true;
      bvDue = -1;
    }

    // plant
    const bool p1 = P1.out > 0.05, p2 = P2.out > 0.05, p3 = P3.out > 0.05;
    double qIn = 0;
    if (p1 && sov.out && tk1 > 0.2) qIn = std::min(sc.q1Max * P1.out - 0.4, sc.q1SuctionCap);
    double q3 = 0;
    if (p3 && bvOpen && tk3 > 0.05) q3 = sc.q3PerDuty * P3.out;
    if (p1 && !sov.out) qIn = q3;  // series: P-03 is the only source behind a closed SOV-01
    double q2 = (p2 && sump > 0.15) ? sc.q2 * P2.out : 0;
    tk1 += (q2 - (sov.out ? qIn : 0)) * dt / 60;
    tk3 -= q3 * dt / 60;
    sump += (qIn - q2) * dt / 60;
    if (tk3 < 0) tk3 = 0;
    R.maxSump = std::max(R.maxSump, sump);
    R.minSump = std::min(R.minSump, sump);

    // instruments
    if (sump > sc.trip) fsw = true;
    else if (sump < sc.trip - 0.05) fsw = false;
    sim::pinLevel[pin::FLOAT] = (sc.floatBroken || fsw) ? HIGH : LOW;
    sim::touch[pin::TOUCH] = (uint16_t)((tk3 > 0.08 ? 20 : 60) + 2 * rnd());
    auto amps = [&](bool on, bool flowing, double duty, double wet, double dry) {
      return on ? (flowing ? wet : dry) * duty * (1 + sc.currentNoise * rnd()) : 0.0;
    };
    sim::mv[pin::IS1] = (uint32_t)(amps(p1, qIn > 0, P1.out, 2.0, 1.0) * 235);
    sim::mv[pin::IS2] = (uint32_t)(amps(p2, q2 > 0, P2.out, 2.8, 1.3) * 235);
    sim::mv[pin::IS3] = (uint32_t)(amps(p3, q3 > 0, P3.out, 2.0, 0.9) * 235);
    const bool ftConnected = !(sc.ftUnplugAt >= 0 && t >= sc.ftUnplugAt);
    phase += 98.0 * q2 * dt;
    if (phase >= 0.5) {
      phase -= 0.5;
      ftLevel = !ftLevel;
      if (ftConnected) {
        sim::gpioIn = ftLevel ? (1u << pin::FT) : 0;
        if (simIsr) simIsr();
      }
    }

    loop();

    // read serial output
    size_t nl;
    while ((nl = sim::tx.find('\n', parsed)) != std::string::npos) {
      std::string ln = sim::tx.substr(parsed, nl - parsed);
      parsed = nl + 1;
      if (fTele && ln.rfind("H,", 0) == 0) fprintf(fTele, "host_time,%s\n", ln.c_str() + 2);
      if (fTele && ln.rfind("D,", 0) == 0) fprintf(fTele, "sim+%.1f,%s\n", t, ln.c_str() + 2);
      if (fEv && ln.rfind("E,", 0) == 0) {
        std::string rest = ln.substr(2);
        size_t c1 = rest.find(','), c2 = rest.find(',', c1 + 1);
        std::string text = rest.substr(c2 + 1);
        for (auto& ch : text) if (ch == '"') ch = '\'';
        fprintf(fEv, "sim+%.1f,%s,%s,\"%s\"\n", t, rest.substr(0, c1).c_str(), rest.substr(c1 + 1, c2 - c1 - 1).c_str(), text.c_str());
      }
      if (ln.rfind("E,", 0) == 0) {
        char buf[300];
        snprintf(buf, sizeof buf, "%7.2f s  %s", t, ln.c_str() + 2);
        R.events.push_back(buf);
        if (ln.find("-> C2_OPEN_BV01") != std::string::npos && !bvOpen) {
          const double d = (R.events.size() && ln.find("open BV-01") != std::string::npos && ln.find("P-03 dry") != std::string::npos)
                               ? sc.bvOpenSecondDelay
                               : sc.bvOpenDelay;
          if (d >= 0) bvDue = t + d;
        }
        if (ln.find("-> C1_RUN") != std::string::npos && c1Start < 0) c1Start = t;
        if (ln.find("-> C1_HOLD_LSH") != std::string::npos) R.holds++;
        if (ln.find("FLUSH_EMPTY") != std::string::npos) {
          R.completeAt = t;
          size_t a = ln.find("source=");
          R.completeSource = ln.substr(a + 7, ln.find(" detect") - a - 7);
          R.tk3End = tk3;
        }
      }
    }
    if (sim::tx.size() > 1 << 20) {
      sim::tx.erase(0, parsed);
      parsed = 0;
    }
    const bool inC1 = state == St::C1_RUN || state == St::C1_HOLD;
    if (inC1 && c1Start >= 0 && t > c1Start + 10) {
      if (!p2) R.p2StoppedInCase1 += dt;
      c1Flow += flow.q;
      c1N += 1;
    }
  }
  R.flowAvgC1 = c1N > 0 ? c1Flow / c1N : 0;
  if (fTele) fclose(fTele);
  if (fEv) fclose(fEv);
  return R;
}

static int failures = 0;
static void check(bool ok, const char* what) {
  printf("    [%s] %s\n", ok ? "PASS" : "FAIL", what);
  if (!ok) failures++;
}

int main() {
  std::srand(7);
  const std::vector<std::string> commissioned = {"SET d1 0.55", "SET tchE 60", "SET i3dry 0.65"};

  Scenario s1{"S1 nominal single take"};
  s1.commands = commissioned;
  s1.dumpPrefix = std::getenv("SIM_DUMP");
  Result r1 = run(s1);
  printf("\n== %s ==\n", s1.name);
  for (auto& e : r1.events) printf("  %s\n", e.c_str());
  check(r1.holds >= 1, "pour trips LS-01 and P-01 holds at least once");
  check(r1.p2StoppedInCase1 < 0.05, "P-02 never stops during Case 1");
  check(std::fabs(r1.flowAvgC1 - 3.0) < 0.1, "Case 1 mean flow 3.0 +/- 0.1 L/min");
  check(r1.completeAt > 0 && r1.completeSource == "LSL-03 probe dry", "flush ends on the LSL-03 probe");
  check(r1.tk3End < 0.15, "TK-03 is essentially empty when the system stops");
  check(r1.maxSump < 4.0, "sump never overflows (peak < 4.0 L)");
  printf("    flowAvgC1=%.3f L/min, sump %.2f..%.2f L, TK-03 left %.3f L\n", r1.flowAvgC1, r1.minSump, r1.maxSump, r1.tk3End);

  Scenario s2{"S2 operator opens BV-01 late"};
  s2.commands = commissioned;
  s2.bvOpenDelay = -1;
  s2.bvOpenSecondDelay = 3;
  Result r2 = run(s2);
  printf("\n== %s ==\n", s2.name);
  for (auto& e : r2.events) if (e.find("STATE") != std::string::npos || e.find("FLUSH") != std::string::npos) printf("  %s\n", e.c_str());
  check(r2.completeSource == "LSL-03 probe dry", "late BV-01 is re-prompted, flush still completes on the probe");
  check(r2.tk3End < 0.15, "TK-03 empty at stop");

  Scenario s3{"S3 float wire broken"};
  s3.commands = commissioned;
  s3.floatBroken = true;
  s3.runFor = 120;
  Result r3 = run(s3);
  printf("\n== %s ==\n", s3.name);
  int shown = 0;
  for (auto& e : r3.events) if (shown++ < 14) printf("  %s\n", e.c_str());
  check(r3.maxSump <= s3.sump + 1e-6, "P-01 never fills the sump with the float wire open (I-1 fail-safe)");

  Scenario s4{"S4 FT-01 unplugged during Case 1"};
  s4.commands = commissioned;
  s4.ftUnplugAt = 150;
  s4.runFor = 230;
  Result r4 = run(s4);
  printf("\n== %s ==\n", s4.name);
  bool diag = false, trip = false;
  for (auto& e : r4.events) {
    if (e.find("FT01_SIGNAL_FAILURE") != std::string::npos) diag = true;
    if (e.find("TRIP") != std::string::npos) trip = true;
    if (e.find("DIAG") != std::string::npos || e.find("TRIP") != std::string::npos) printf("  %s\n", e.c_str());
  }
  check(diag, "FDI names FT01_SIGNAL_FAILURE");
  check(!trip, "no protective trip: the process keeps running");

  Scenario s5{"S5 noisy current, no pour"};
  s5.commands = commissioned;
  s5.currentNoise = 0.15;
  s5.pourAt = -1;
  s5.runFor = 230;
  Result r5 = run(s5);
  printf("\n== %s ==\n", s5.name);
  bool trip5 = false;
  for (auto& e : r5.events) if (e.find("TRIP") != std::string::npos) trip5 = true;
  check(!trip5, "15% current noise causes no protective trip");
  check(r5.p2StoppedInCase1 < 0.05, "P-02 never stops");

  printf("\n%s: %d failure(s)\n", failures ? "FAILED" : "ALL PASS", failures);
  return failures ? 1 : 0;
}
