
#pragma once

#include "units.hpp"
#include "energie.hpp"

#include <type_traits>

namespace si {

class Particle {
private:
  Energie e{};
  mass_t m{};
  velocity_t v{};
  momentum_t p{};

public:
  Particle() = default;
  explicit Particle(Energie _e, mass_t _m, velocity_t _v, momentum_t _p)
    : e(_e), m(_m), v(_v), p(_p) {}

  template<class U>
  inline U& set() {
    if constexpr (std::is_same_v<U, Energie>) {
      return this->e;
    }
    else if constexpr (std::is_same_v<U, ekin_t>) {
      return this->e.ekin();
    }
    else if constexpr (std::is_same_v<U, epot_t>) {
      return this->e.epot();
    }
    else if constexpr (std::is_same_v<U, mass_t>) {
      return this->m;
    }
    else if constexpr (std::is_same_v<U, velocity_t>) {
      return this->v;
    }
    else if constexpr (std::is_same_v<U, momentum_t>) {
      return this->p;
    }
    else {
      return nullptr;
    }
  }

  inline constexpr mass_t mass() noexcept { return m; };
  inline constexpr velocity_t velocity() noexcept { return v; }
  inline constexpr momentum_t momentum() noexcept { return p; }
  inline constexpr Energie energie() noexcept { return e; }
  inline constexpr ekin_t ekin() noexcept { return e.ekin(); }
  inline constexpr epot_t epot() noexcept { return e.epot(); }

};

}
