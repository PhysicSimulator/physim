cmake_minimum_required(VERSION 4.0)

project(physim VERSION 0.1 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Options
option(PHYSIM_WARNINGS_AS_ERRORS "Warnings as errors" ON)
option(PHYSIM_ENABLE_SANITIZERS "Enable ASan/UBSan in Debug" ON)
option(PHYSIM_TESTING "Build tests" ON)

# --------------- Library ---------------
add_library(physim 
  src/add.cpp  
)

target_include_directories(physim PUBLIC 
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(physim PUBLIC cxx_std_23)

# --------------- Strict compile flags ---------------
function(physim_apply_strict_flags tgt)
  if (MSVC)
    target_compile_options(${tgt} PRIVATE /W4)
    if (PHYSIM_WARNINGS_AS_ERRORS)
      target_compile_options(${tgt} PRIVATE /WX)
    endif()
  else()
    target_compile_options(${tgt} PRIVATE
      -Wall -Wextra -Wpedantic
      -Wshadow -Wconversion -Wsign-conversion
      -Wold-style-cast -Wcast-align
      -Woverloaded-virtual -Wnon-virtual-dtor
      -Wnull-dereference -Wdouble-promotion
      -Wformat=2 -Wimplicit-fallthrough
      -fno-omit-frame-pointer
      -fstack-protector-strong
    )
    if (PHYSIM_WARNINGS_AS_ERRORS)
      target_compile_options(${tgt} PRIVATE -Werror)
    endif()

    target_link_options(${tgt} PRIVATE
      -fstack-protector-strong
    )
  endif()
endfunction()

physim_apply_strict_flags(physim)

# --------------- Sanitizers (Debug only) ---------------
function(physim_apply_sanitizers tgt)
  if (NOT PHYSIM_ENABLE_SANITIZERS)
    return()
  endif()
  if (MSVC)
    return()
  endif()

  target_compile_options(${tgt} PRIVATE
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
    $<$<CONFIG:Debug>:-fno-sanitize-recover=all>
  )
  target_link_options(${tgt} PRIVATE
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
  )
endfunction()

physim_apply_sanitizers(physim)

# --------------- Testing ---------------
include(CTest)

if (BUILD_TESTING)
  #file(GLOB TEST_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_*.cpp)
  #add_executable(physim_tests ${TEST_SOURCES})
  add_executable(physim_tests
    tests/test_units.cpp
    tests/test_main.cpp
  )

  target_link_libraries(physim_tests PRIVATE physim)
  target_include_directories(physim_tests PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/tests
  )
  target_compile_features(physim_tests PRIVATE cxx_std_23)

  physim_apply_strict_flags(physim_tests)
  physim_apply_sanitizers(physim_tests)

  add_test(NAME physim_tests COMMAND physim_tests)
endif()
