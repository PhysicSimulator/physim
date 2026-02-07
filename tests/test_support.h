
#pragma once

#include <exception>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace tests {

  struct TestCase {
    std::string name;
    std::function<void()> fn;
  };

  inline std::vector<TestCase>& registry() {
    static std::vector<TestCase> r;
    return r;
  }

  inline void register_test(std::string name, std::function<void()> fn) {
    registry().push_back(TestCase{std::move(name), std::move(fn)});
  }

  struct TestFailure : std::exception {
    std::string msg;
    explicit TestFailure(std::string m) : msg(std::move(m)) {}
    const char* what() const noexcept override { return msg.c_str() ;}
  };

  inline std::string location_str(const char* file, int line, const char* func) {
    std::ostringstream os;
    os << file << ":" << line << " (" << func << ")";
    return os.str();
  }

  inline void fail(
      std::string_view kind,
      std::string_view expr,
      const char* file,
      int line,
      const char* func,
      std::string_view detail = {}
      ) {
    std::cerr << "  [" << kind << "] " << location_str(file, line, func) << "\n"
              << "    expr: " << expr << "\n";
    if (!detail.empty()) std::cerr << "    detail: " << detail << "\n";
  }

  inline int& failures_in_current_test() {
    static thread_local int n = 0;
    return n;
  }

  inline void reset_current_test_failures() { failures_in_current_test() = 0; }

  inline int current_test_failure() { return failures_in_current_test(); }
}

// --- token concatenation helpers (2-step expansion) ---
#define T_CONCAT_IMPL(a, b) a##b
#define T_CONCAT(a, b) T_CONCAT_IMPL(a, b)

// ---------- Test registration ----------
#define TEST_CASE(NAME) TEST_CASE_IMPL(NAME, __COUNTER__)

#define TEST_CASE_IMPL(NAME, ID)                                              \
  static void T_CONCAT(test_fn_, ID)();                                       \
  namespace {                                                                 \
    struct T_CONCAT(test_reg_, ID) {                                          \
      T_CONCAT(test_reg_, ID)() {                                             \
        ::tests::register_test((NAME), &T_CONCAT(test_fn_, ID));              \
      }                                                                       \
    };                                                                        \
    static const T_CONCAT(test_reg_, ID) T_CONCAT(test_reg_instance_, ID){};  \
  }                                                                           \
  static void T_CONCAT(test_fn_, ID)()

// ---------- Assertions / expectations ----------
#define EXPECT_TRUE(EXPR)                                                     \
  do {                                                                        \
    if (!(EXPR)) {                                                            \
      ::tests::fail("EXPECT_TRUE", #EXPR, __FILE__, __LINE__, __func__);      \
      ::tests::failures_in_current_test()++;                                  \
    }                                                                         \
  } while (0)

#define ASSERT_TRUE(EXPR)                                                     \
  do {                                                                        \
    if (!(EXPR)) {                                                            \
      ::tests::fail("ASSERT_TRUE". #EXPR, __FILE__, __LINE__, __func__);      \
      throw ::tests::TestFailure("ASSERT_TRUE failed");                       \
    }                                                                         \
  } while (0)

#define EXPECT_EQ(A, B)                                                       \
  do {                                                                        \
    auto _a = (A);                                                            \
    auto _b = (B);                                                            \
    if (!(_a == _b)) {                                                        \
      std::ostringstream _os;                                                 \
      _os << "lhs=" << _a << " rhs=" << _b;                                   \
      ::tests::fail("EXPECT_EQ", #A " == " #B, __FILE__, __LINE__, __func__,  \
                    _os.str());                                               \
      ::tests::failures_in_current_test()++;                                  \
    }                                                                         \
  } while (0)

#define ASSERT_EQ(A, B)                                                       \
  do {                                                                        \
    auto _a = (A);                                                            \
    auto _b = (B);                                                            \
    if (!(_a == _b)) {                                                        \
      std::ostringstream _os;                                                 \
      _os << "lhs=" << _a << " rhs=" << _b;                                   \
      ::tests::fail("ASSERT_EQ", #A " == " #B, __FILE__, __LINE__, __func__,  \
                    _os.str());                                               \
      throw ::tests::TestFailure("ASSERT_EQ failed");                         \
    }                                                                         \
  } while (0)

#define EXPECT_NEAR(A, B, EPS)                                                \
  do {                                                                        \
    auto _a = (A);                                                            \
    auto _b = (B);                                                            \
    auto _e = (EPS);                                                          \
    if (!(((_a > _b) ? (_a - _b) : (_b - _a)) <= _e)) {                       \
      std::ostringstream _os;                                                 \
      _os << "lhs=" << _a << " rhs=" << _b << " eps=" << _e;                  \
      ::tests::fail("EXPECT_NEAR", #A " ~= " #B, __FILE__, __LINE__, __func__,\
                    _os.str());                                               \
      ::tests::failures_in_current_test()++;                                  \
    }                                                                         \
  } while (0)

// Expect that a expression throws some exception type
#define EXPECT_THROWS_AS(EXPR, EXC_TYPE)                                      \
  do {                                                                        \
    bool _thrown = false;                                                     \
    try { (void)(EXPR); }                                                     \
    catch (const EXC_TYPE) { _thrown = true; }                                \
    catch (...) {}                                                            \
    if (!_thrown) {                                                           \
      ::tests::fail(EXPECT_THROWS_AS, #EXPR, __FILE__, __LINE__, __func__,    \
                    "did not throw " #EXC_TYPE);                              \
      ::tests::failures_in_current_test()++;                                  \
    }                                                                         \
  } while (0)

#define TEST_METHOD(FIXTURE, METHOD)                                          \
  TEST_CASE(#FIXTURE "." #METHOD) {                                           \
    FIXTURE fx;                                                               \
    fx.METHOD();                                                              \
  }

