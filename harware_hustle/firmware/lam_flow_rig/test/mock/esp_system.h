#pragma once
typedef enum { ESP_RST_POWERON = 1, ESP_RST_BROWNOUT = 9 } esp_reset_reason_t;
inline esp_reset_reason_t esp_reset_reason() { return ESP_RST_POWERON; }
