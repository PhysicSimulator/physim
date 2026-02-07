
#include "test_support.h"
#include "units.hpp"
#include "energie.hpp"
#include <type_traits>

class TestUnit {
private:
  si::unit_t<si::Dim< 0, 0, 0>> u;

public:
  void default_construct_is_zero() {
    EXPECT_NEAR(u.raw(), 0.0, 1e-12);
  }

  void construct_from_value() {
    si::unit_t<si::Dim< 0, 0, 0>> tmp(10.0);
    EXPECT_NEAR(tmp.raw(), 10.0, 1e-12);
  }

  void compile_time_properties() {
    EXPECT_TRUE((std::is_default_constructible_v<si::unit_t<si::Dim< 0, 0, 0>>>));
    EXPECT_TRUE((std::is_copy_constructible_v<si::unit_t<si::Dim< 0, 0, 0>>>));
    EXPECT_TRUE((std::is_move_constructible_v<si::unit_t<si::Dim< 0, 0, 0>>>));
  }
};

TEST_METHOD(TestUnit, default_construct_is_zero)
TEST_METHOD(TestUnit, construct_from_value)
TEST_METHOD(TestUnit, compile_time_properties)

class TestEkin {
private:
  si::ekin_t e;

public:
  void default_construct_is_zero() {
    EXPECT_NEAR(e.raw(), 0.0, 1e-12);
  }

  void construct_from_value() {
    si::ekin_t tmp(10.0);
    EXPECT_NEAR(tmp.raw(), 10.0, 1e-12);
  }

  void compile_time_properties() {
    EXPECT_TRUE((std::is_default_constructible_v<si::ekin_t>));
    EXPECT_TRUE((std::is_copy_constructible_v<si::ekin_t>));
    EXPECT_TRUE((std::is_move_constructible_v<si::ekin_t>));
  }

  void test_classical_mechanic() {
    EXPECT_NEAR(
        si::classical_mechanic(si::mass_t{10.0}, si::velocity_t{10.0}).raw(),
        500.0,
        1e-12);
  }
};

TEST_METHOD(TestEkin, default_construct_is_zero)
TEST_METHOD(TestEkin, construct_from_value)
TEST_METHOD(TestEkin, test_classical_mechanic)
TEST_METHOD(TestEkin, compile_time_properties)
