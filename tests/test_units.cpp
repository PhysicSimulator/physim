
#include <catch2/catch_test_macros.hpp>
#include "../include/units.h"

TEST_CASE("basic behvior") {
  REQUIRE(add(2, 3) == 5);
}
