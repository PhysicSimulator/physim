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

using ekin_t = energie_t;
using epot_t = energie_t;

class Energie {
  private:
    ekin_t kinetic{};
    epot_t potential{};

  public:
    Energie() = default;
    Energie(ekin_t _kinetic);
    inline ekin_t& ekin() noexcept { return kinetic; }
    inline epot_t epot() noexcept { return potential; }
};

ekin_t classical_mechanic(si::mass_t m, si::velocity_t v);

}
