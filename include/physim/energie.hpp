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

namespace si {

typedef struct ekin_t : energie_t {
  using energie_t::unit_t;
  ekin_t *classical_mechanic(si::mass_t m, si::velocity_t v);
} ekin_t;

typedef struct epot_t : energie_t {
  energie_t epot{};

  epot_t() = default;
  epot_t(double _epot) : epot(_epot) {}
  epot_t(energie_t _epot) : epot(_epot) {}
} epot_t;


} // namespace si
