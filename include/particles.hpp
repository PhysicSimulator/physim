/* 
 * -*- coding: utf-8 -*- 
 * Copyright 2026 physim devlopers
 *
 * This file is part of physim.
 *
 * physim is free software: you can redistribute it and/or modify
 * it under the term of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the license, or
 * (at your option) any later version.
 *
 * physim is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with physim. If not, see <https:://www.gnu.org/license/#GPL>
*/

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
