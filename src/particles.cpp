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

#include "../include/particles.hpp"

template<class F, class ...Args>
requires  std::invocable<F, Args...> &&
          std::assignable_from<si::velocity_t&, std::invoke_result_t<F&, Args...>>
void si::particle_t::set_v(F f, Args... args) {
  this->v = std::invoke(std::forward<F>(f), std::forward<Args>(args)...);
}

