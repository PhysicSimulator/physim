
#include "../include/kinematics.hpp"
#include "units.hpp"

typedef struct new_velocity {
  si::velocity_t v1{};
  si::velocity_t v2{};
  new_velocity() = default;
  new_velocity(si::velocity_t _v1, si::velocity_t _v2) {
    v1 = _v1;
    v2 = _v2;
  }
  new_velocity& operator=(new_velocity v) {
    this->v1 = v.v1;
    this->v2 = v.v2;
    return *this;
  }
} new_velocity;

void kinematics::Collision::_1D_collision(si::Particle *p1, si::Particle *p2) {
  auto after_collision = [p1, p2]() {
    return new_velocity {
      2 * ((p1->mass() * p1->velocity() + p2->mass() * p2->velocity())
          /(p1->mass() + p2->mass())) - p1->velocity(),
      2 * ((p1->mass() * p1->velocity() + p2->mass() * p2->velocity())
          /(p1->mass() + p2->mass())) - p2->velocity()
    };
  };

  new_velocity res = after_collision();

  auto new_momentum = [](si::Particle *p) {
    return p->mass() * p->velocity();
  };

  p1->set<si::velocity_t>() = res.v1;
  p2->set<si::velocity_t>() = res.v2;

  p1->set<si::momentum_t>() = new_momentum(p1);
  p2->set<si::momentum_t>() = new_momentum(p2);
}
