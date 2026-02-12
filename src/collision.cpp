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

#include <physim/collision.hpp>

si::velocity_t after_collision(si::particle_t *p1, si::particle_t *p2) {
  return (2 * ((p1->m * p1->v) + (p2->m * p2->v)) / (p1->m + p2->m)) - p1->v;
}

void si::collision::_1D_collision_particle(si::particle_t *p1, si::particle_t *p2) {
  // p1:
  p1->set_v(after_collision, p1, p2); 
  p1->momentum();
  p1->ekin_CM();

  // p2:
  p2->set_v(after_collision, p2, p1);
  p2->momentum();
  p2->ekin_CM();
}
