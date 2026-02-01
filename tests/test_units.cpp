
#include "test_support.h"
#include "units.hpp"
#include <type_traits>

static energie kinetic_energie(mass m, velocity v) {
  return 0.5 * m * v * v;
}

static momentum calculation(mass m, velocity v) {
    return m * v;
}

class TestUnit {
private:
  Unit<double> u;

public:
  void default_construct_is_zero() {
    EXPECT_NEAR(*u, 0.0, 1e-12);
  }

  void construct_from_value() {
    Unit<double> tmp(10.0);
    EXPECT_NEAR(*tmp, 10.0, 1e-12);
  }

  void call_operator_assigns_from_invocable() {
    EXPECT_NEAR(*u(calculation, 10.0, 10.0), 100.0, 1e-12);
  } 

  void compile_time_properties() {
    EXPECT_TRUE((std::is_default_constructible_v<Unit<double>>));
    EXPECT_TRUE((std::is_copy_constructible_v<Unit<double>>));
    EXPECT_TRUE((std::is_move_constructible_v<Unit<double>>));
  }
};

TEST_METHOD(TestUnit, default_construct_is_zero)
TEST_METHOD(TestUnit, construct_from_value)
TEST_METHOD(TestUnit, call_operator_assigns_from_invocable)
TEST_METHOD(TestUnit, compile_time_properties)

class TestEkin {
private:
  Ekin e;

public:
  void default_construct_is_zero() {
    EXPECT_NEAR(*e, 0.0, 1e-12);
  }

  void construct_from_value() {
    Ekin tmp(10.0);
    EXPECT_NEAR(*tmp, 10.0, 1e-12);
  }

  void call_operator_assigns_from_invocable() {
    EXPECT_NEAR(*e(kinetic_energie, 10.0, 10.0), 500.0, 1e-12);
  }

  void compile_time_properties() {
    EXPECT_TRUE((std::is_default_constructible_v<Ekin>));
    EXPECT_TRUE((std::is_copy_constructible_v<Ekin>));
    EXPECT_TRUE((std::is_move_constructible_v<Ekin>));
  }

  void test_classical_mechanic() {
    EXPECT_NEAR(*e.classical_mechanic(10.0, 10.0), 500.0, 1e-12);
  }
};

TEST_METHOD(TestEkin, default_construct_is_zero)
TEST_METHOD(TestEkin, construct_from_value)
TEST_METHOD(TestEkin, call_operator_assigns_from_invocable)
TEST_METHOD(TestEkin, compile_time_properties)
