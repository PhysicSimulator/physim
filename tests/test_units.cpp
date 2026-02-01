
#include "test_support.h"
#include "units.hpp"
#include <type_traits>

static int plus_one(int x) { return x + 1; }

struct UnitTests {
  void default_construct_is_zero() {
    Ekin e;
    EXPECT_NEAR(*e, 0.0, 1e-12);
  }

  void construct_from_value() {
    Ekin e(12.5);
    EXPECT_NEAR(*e, 12.5, 1e-12);
  }

  void call_operator_assigns_from_invocable() {
    Ekin e(10.0);
    e(plus_one, 41);
    EXPECT_NEAR(*e, 42.0, 1e-12);
  }

  void compile_time_properties() {
    EXPECT_TRUE((std::is_default_constructible_v<Ekin>));
    EXPECT_TRUE((std::is_copy_constructible_v<Ekin>));
    EXPECT_TRUE((std::is_move_constructible_v<Ekin>));
  }
};

TEST_METHOD(UnitTests, default_construct_is_zero);
TEST_METHOD(UnitTests, construct_from_value);
TEST_METHOD(UnitTests, call_operator_assigns_from_invocable);
TEST_METHOD(UnitTests, compile_time_properties);
