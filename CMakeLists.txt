cmake_minimum_required(VERSION 3.4.0)

# set(CMAKE_BUILD_TYPE Debug)

project(NumbaSUNDIALS)

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
target_link_libraries(NumbaIDA sundials_ida)

set_target_properties(NumbaIDA PROPERTIES PREFIX "lib")

# Install library into the directory with driver.py
if (SKBUILD)
  install(TARGETS NumbaIDA DESTINATION NumbaIDA)
else()
  install(TARGETS NumbaIDA DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/NumbaIDA/)
endif()
