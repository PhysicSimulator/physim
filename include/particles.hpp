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

#include "energie.hpp"
#include "units.hpp"

#include <functional>

namespace si {

typedef struct particle_t {
  Energie e{};
  mass_t m{};
  velocity_t v{};
  momentum_t p{};

  particle_t() = default;
  explicit particle_t(Energie _e, mass_t _m, velocity_t _v, momentum_t _p)
    : e(_e), m(_m), v(_v), p(_p) {}


  inline void momentum() {
    this->p = this->m * this->v;
  }

  template<class F, class... Args>
  requires  std::invocable<F, Args...> &&
            std::assignable_from<si::velocity_t&, std::invoke_result_t<F&, Args...>>
  void set_v(F f, Args... args);
  
} particle_t;

}
