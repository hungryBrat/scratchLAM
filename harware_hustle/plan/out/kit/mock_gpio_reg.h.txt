#pragma once
#include <cstdint>
namespace sim { extern uint32_t gpioIn; }
#define GPIO_IN_REG 0
#define REG_READ(r) (sim::gpioIn)
