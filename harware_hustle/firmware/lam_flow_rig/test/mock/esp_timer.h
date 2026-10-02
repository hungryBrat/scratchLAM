#pragma once
#include <cstdint>
namespace sim { extern uint64_t us; }
inline int64_t esp_timer_get_time() { return (int64_t)sim::us; }
