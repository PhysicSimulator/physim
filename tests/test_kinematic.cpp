
#include "test_support.h"
#include "kinematics.hpp"
#include "energie.hpp"

namespace TestKinematics {

class TestCollision {
private:
  si::ekin_t _E;
  si::mass_t _m;
  si::velocity_t _v;
  si::momentum_t _p;
  si::Particle p1{};
  si::Particle p2{};

public:
  TestCollision() {
    _E = si::ekin_t{500.0};
    _m = si::mass_t{10.0};
    _v = si::velocity_t{10.0};
    _p = si::momentum_t{100};
    p1 = si::Particle(
      si::Energie(_E),
      si::mass_t(_m),
      si::velocity_t(_v),
      si::momentum_t(_p)
    );
    p2 = p1;
  }

  void test_1D_collision() {
    kinematics::Collision::_1D_collision(&p1, &p2);
    EXPECT_NEAR(p1.momentum().raw(), 100.0, 1e-9);
    EXPECT_NEAR(p2.momentum().raw(), 100.0, 1e-9);
  }
};

}

TEST_METHOD(TestKinematics::TestCollision, test_1D_collision)
