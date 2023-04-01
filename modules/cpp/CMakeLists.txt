cmake_minimum_required(VERSION 3.16)

project(planning VERSION 1.0)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(GTest REQUIRED)

include_directories(${GTEST_INCLUDE_DIRS}
                    include
                    )

add_executable(planning src/main.cpp)
add_executable(TestPrimitives tests/test_primitives.cpp)

target_link_libraries(TestPrimitives
                      ${GTEST_LIBRARIES}
                      pthread
                      )