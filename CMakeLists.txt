cmake_minimum_required(VERSION 3.4.0)

project(NumbaIDA)

add_subdirectory(sundials)

option(SKBUILD "Should be ON of being build by skbuild,
and OFF of being build by regular cmake" OFF)

if (NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
endif()

# find_library(LIB_IDA sundials_ida)
# message(STATUS "found ida at ${LIB_IDA}")

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

set(CMAKE_CXX_STANDARD 11)
add_library(NumbaIDA SHARED ${CMAKE_CURRENT_SOURCE_DIR}/src/NumbaIDA/IDAWrapper.cpp)
target_link_libraries(NumbaIDA sundials_ida_static)

set_target_properties(NumbaIDA PROPERTIES PREFIX "lib")

# Install libraries into the directory with driver.py
if (SKBUILD)
  install(TARGETS NumbaIDA DESTINATION numbaida)
else()
  # Breaking lots of rules. We would be breaking less if IDAWrapper.cpp was a C file.
  set(CMAKE_CXX_CLANG_TIDY clang-tidy; -fix-errors; -checks=*,-llvmlibc*,-cppcoreguidelines-avoid-non-const-global-variables,-google_readibility-casting,-modernize-use-trailing-return-type,cppcoreguidelines-pro-type-vararg,hicpp-vararg,-cppcoreguidelines-pro-bounds-pointer-arithmetic,-cppcoreguidelines-pro-type-cstyle-cast,-cppcoreguidelines-pro-type-vararg,hicpp-vararg,-hicpp-vararg)
  install(TARGETS NumbaIDA DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/NumbaIDA/)
endif()

