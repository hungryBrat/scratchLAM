#pragma once
#include <map>
#include <string>
class Preferences {
 public:
  bool begin(const char*, bool) { return true; }
  void end() {}
  float getFloat(const char* k, float d) { auto it = store().find(k); return it == store().end() ? d : it->second; }
  size_t putFloat(const char* k, float v) { store()[k] = v; return 4; }
 private:
  static std::map<std::string, float>& store() { static std::map<std::string, float> m; return m; }
};
