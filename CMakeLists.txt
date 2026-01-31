cmake_minimum_required(VERSION 4.0)

project(physic_simulator VERSION 0.1 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(physic_simulator 
  src/add.cpp  
)

target_include_directories(physic_simulator PUBLIC include)
target_compile_features(physic_simulator PUBLIC cxx_std_23)

# --- Testing ---
include(CTest)
if (BUILD_TESTING)
  # Fetch Catch2
  include(FetchContent)
  FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.5.4
  )
  FetchContent_MakeAvailable(Catch2)

  add_executable(tests
    tests/test_units.cpp
  )
  target_link_libraries(tests PRIVATE physic_simulator Catch2::Catch2WithMain)

  add_test(NAME physic_simulator_tests COMMAND tests)
endif()
