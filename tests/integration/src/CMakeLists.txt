cmake_minimum_required(VERSION 3.16)
project(test_lib LANGUAGES CXX)

message(STATUS "LIBRARY_FETCH_TAG=${LIBRARY_FETCH_TAG}")
if(DEFINED LIBRARY_SOURCE_DIR)
    # This uses the existing project directory, so uncommitted changes may hide
    # errors that would occur in a clean checkout.
    message(STATUS "Testing library build tree at ${LIBRARY_SOURCE_DIR}")
    find_package(GTest REQUIRED)
    add_subdirectory(${LIBRARY_SOURCE_DIR} ${LIBRARY_SOURCE_DIR}/build)
elseif(DEFINED LIBRARY_FETCH_DIR)
    # Use FetchContent to add dependencies.
    include(FetchContent)
    set(INSTALL_GTEST OFF CACHE BOOL "")
    set(BUILD_GMOCK OFF CACHE BOOL "")
    FetchContent_Declare(googletest
        GIT_REPOSITORY "https://github.com/google/googletest"
        GIT_TAG "v${GTEST_VERSION}"
    )
    message("Using FetchContent for ${LIBRARY_FETCH_DIR}")
    FetchContent_Declare(gtest-infra
        SOURCE_DIR ${LIBRARY_FETCH_DIR}
    )
    FetchContent_MakeAvailable(googletest)
    FetchContent_MakeAvailable(gtest-infra)
else()
    # All default search locations are disabled to ensure that only the test
    # installation is found.
    find_package(GTestInfra REQUIRED)
    find_package(GTest REQUIRED)
    message(STATUS "Testing installed library at ${GTestInfra_DIR}")
endif()

add_executable(test_lib test_lib.cpp)
target_link_libraries(test_lib
PRIVATE
    GTestInfra::gtest-infra
    GTest::gtest
    GTest::gtest_main
)
