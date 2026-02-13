cmake_minimum_required(VERSION 3.25)

project(physim VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Options
option(PHYSIM_WARNINGS_AS_ERRORS "Warnings as errors" ON)
option(PHYSIM_ENABLE_SANITIZERS "Enable ASan/UBSan in Debug" ON)
option(PHYSIM_TESTING "Build tests" ON)
option(PHYSIM_ENABLE_COVERAGE "Enable coverage reporting" OFF)

if(PHYSIM_ENABLE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  message(STATUS "Coverage enabled")

  add_compile_options(--coverage -O0 -g)
  add_link_options(--coverage)
endif()

# --------------- Library ---------------
add_library(physim 
  src/energie.cpp
  src/collision.cpp
  src/energie.cpp
  src/units.cpp
)

add_library(physim::physim ALIAS physim)

target_compile_features(physim PUBLIC cxx_std_23)

target_include_directories(physim
  PUBLIC 
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

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

  target_compile_options(${tgt} PRIVATE
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
    $<$<CONFIG:Debug>:-fno-sanitize-recover=all>
  )

  target_link_options(${tgt} PRIVATE
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
  )
endfunction()

physim_apply_sanitizers(physim)

# --------------- Installation ---------------
include(GNUInstallDirs)

install(TARGETS physim
  EXPORT physimTargets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Export targets
install(EXPORT physimTargets
  FILE physimTargets.cmake
  NAMESPACE physim::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/physim
)

include(CMakePackageConfigHelpers)

configure_package_config_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/physimConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/physimConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/physim
)

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/physimConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/physimConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/physimConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/physim
)

# --------------- Testing ---------------
include(CTest)

set(BUILD_TESTING ${PHYSIM_TESTING} CACHE BOOL "Build tests" FORCE)

if (BUILD_TESTING)
  enable_testing()

  set(PHYSIM_TEST_MAIN ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_main.cpp)

  file(GLOB TEST_SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_*.cpp
  )

  foreach(test_src ${TEST_SOURCES})
    get_filename_component(test_name ${test_src} NAME_WE)

    # Skip test_main.cpp
    if (test_src STREQUAL PHYSIM_TEST_MAIN)
      continue()
    endif()

    add_executable(${test_name}
      ${PHYSIM_TEST_MAIN}
      ${test_src}
    )

    target_link_libraries(${test_name} PRIVATE physim::physim)

    target_include_directories(${test_name} PRIVATE
      ${CMAKE_CURRENT_SOURCE_DIR}/include
      ${CMAKE_CURRENT_SOURCE_DIR}/tests
    )

    target_compile_features(${test_name} PRIVATE cxx_std_23)

    physim_apply_strict_flags(${test_name})
    physim_apply_sanitizers(${test_name})

    add_test(NAME ${test_name} COMMAND ${test_name})
  endforeach()
endif()

