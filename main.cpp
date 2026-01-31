
#include "lib/units.h"
#include <iostream>

energie kinetic_energie(double m, double v) {
  return 0.5 * m * v * v;
}

int main() {
  
  Ekin e;
  e = 10.0;
  e(kinetic_energie, 10.0, 10.0);

  std::cout << *e << std::endl;

  return 0;
}
