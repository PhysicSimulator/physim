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

#include "test_support.h"

int main() {

  const auto& tests = tests::registry();
  std::cout << "Running " << tests.size() << " tests...\n";

  unsigned int total_failed_tests = 0;

  for (const auto& tc : tests) {
    std::cout << "[TEST] " << tc.name << "\n";

    tests::reset_current_test_failures();

    try {
      tc.fn();
    } catch (const tests::TestFailure&) {
      // already logged; treated as failure
    } catch (const std::exception& e) {
      tests::fail(
        "UNCAUGHT std::exception",
        tc.name,
        __FILE__,
        __LINE__,
        __func__,
        e.what()
      );
      tests::failures_in_current_test()++;
    } catch (...) {
      tests::fail("UNCAUGHT unknown", tc.name, __FILE__, __LINE__, __func__);
      tests::failures_in_current_test()++;
    }

    const int fails = tests::current_test_failure();
    if (fails == 0) {
      std::cout << " -> PASS\n";
    } else {
      std::cout << " -> FAIL (" << fails << ")\n";
      total_failed_tests++;
    }
  }

  std::cout << "\nSummary: " << (tests.size() - total_failed_tests)
    << " passed, " << total_failed_tests << " failed.\n";

  return total_failed_tests == 0 ? 0 : 1;
}
