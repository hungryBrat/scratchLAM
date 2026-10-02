// Minimal host-side stand-ins for the Arduino-ESP32 API used by main.cpp (simulation only).
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <strings.h>
#include <cstdlib>
using std::max;
using std::min;

#define IRAM_ATTR
#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define CHANGE 3
#define constrain(x, lo, hi) ((x) < (lo) ? (lo) : ((x) > (hi) ? (hi) : (x)))
typedef int portMUX_TYPE;
#define portMUX_INITIALIZER_UNLOCKED 0
#define portENTER_CRITICAL(m) (void)(m)
#define portEXIT_CRITICAL(m) (void)(m)
#define portENTER_CRITICAL_ISR(m) (void)(m)
#define portEXIT_CRITICAL_ISR(m) (void)(m)
enum adc_attenuation_t { ADC_0db, ADC_2_5db, ADC_6db, ADC_11db };

namespace sim {
extern uint64_t us;
extern int pinLevel[40];
extern int pinOut[40];
extern uint32_t mv[40];
extern uint16_t touch[40];
extern uint32_t pwm[16];
extern std::string rx, tx;
}
inline unsigned long millis() { return (unsigned long)(sim::us / 1000); }
inline unsigned long micros() { return (unsigned long)sim::us; }
inline void delay(unsigned long) {}
inline void pinMode(uint8_t, uint8_t) {}
inline void digitalWrite(uint8_t p, uint8_t v) { sim::pinOut[p] = v; }
inline int digitalRead(uint8_t p) { return sim::pinLevel[p]; }
inline uint32_t analogReadMilliVolts(uint8_t p) { return sim::mv[p]; }
inline void analogSetPinAttenuation(uint8_t, adc_attenuation_t) {}
inline uint16_t touchRead(uint8_t p) { return sim::touch[p]; }
inline void ledcSetup(uint8_t, uint32_t, uint8_t) {}
inline void ledcAttachPin(uint8_t, uint8_t) {}
inline void ledcWrite(uint8_t ch, uint32_t d) { sim::pwm[ch] = d; }
inline int digitalPinToInterrupt(int p) { return p; }
extern void (*simIsr)();
inline void attachInterrupt(int, void (*f)(), int) { simIsr = f; }
inline void enableLoopWDT() {}

struct SimSerial {
  void begin(unsigned long) {}
  int available() { return (int)sim::rx.size(); }
  int read() { int c = (unsigned char)sim::rx[0]; sim::rx.erase(0, 1); return c; }
  void print(const char* s) { sim::tx += s; }
  void println(const char* s = "") { sim::tx += s; sim::tx += "\n"; }
  int printf(const char* fmt, ...) {
    char b[1024];
    va_list ap; va_start(ap, fmt); int n = vsnprintf(b, sizeof b, fmt, ap); va_end(ap);
    sim::tx += b; return n;
  }
};
extern SimSerial Serial;
