
#include "../include/units.hpp"

Ekin& Ekin::classical_mechanic(mass m, velocity v) {
  this->unit = 0.5 * m * v * v;
  return *this;
}
