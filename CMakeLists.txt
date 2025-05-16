cmake_minimum_required(VERSION 3.12)
include(GNUInstallDirs)

set(APP_NAME "uFastAuthD")
set(SVERSION 1.2.3)

project(${APP_NAME})
project(${PROJECT_NAME} VERSION ${SVERSION} DESCRIPTION "Unmanarc's Fast Authentication Daemon")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")

configure_file(src/config.h.in ${${APP_NAME}_SOURCE_DIR}/src/config.h)

file(GLOB_RECURSE EDV_INCLUDE_FILES "src/*.h*")
file(GLOB_RECURSE EDV_SOURCE_FILES "src/*.c*")
add_executable( ${APP_NAME} ${EDV_INCLUDE_FILES} ${EDV_SOURCE_FILES} )

install( TARGETS ${APP_NAME} RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} )

if (EXTRAPREFIX)
    target_include_directories(${APP_NAME} PUBLIC ${EXTRAPREFIX}/include)
    target_link_libraries(${APP_NAME} "-L${EXTRAPREFIX}/lib")
    target_link_libraries(${APP_NAME} "-L${EXTRAPREFIX}/lib64")
endif()

if (CMAKE_INSTALL_PREFIX)
    target_include_directories(${APP_NAME} PUBLIC ${CMAKE_INSTALL_PREFIX}/include)
    target_include_directories(${APP_NAME} PUBLIC ${CMAKE_INSTALL_PREFIX}/usr/include)
    target_link_libraries(${APP_NAME} "-L${CMAKE_INSTALL_PREFIX}/lib")
    target_link_libraries(${APP_NAME} "-L${CMAKE_INSTALL_PREFIX}/lib64")
endif()


################################################################################
# PKG-CONFIG INIT:
find_package(PkgConfig REQUIRED)
################################################################################

################################################################################
# Find SQLite3
pkg_check_modules(SQLITE3 REQUIRED sqlite3)
include_directories(${SQLITE3_INCLUDE_DIRS})
link_directories(${SQLITE3_LIBRARY_DIRS})
target_link_libraries(${APP_NAME} ${SQLITE3_LIBRARIES})

################################################################################
# Find jsoncpp
pkg_check_modules(JSONCPP REQUIRED jsoncpp)
include_directories(${JSONCPP_INCLUDE_DIRS})
link_directories(${JSONCPP_LIBRARY_DIRS})
target_link_libraries(${APP_NAME} ${JSONCPP_LIBRARIES})

################################################################################
# Boost Packages:
find_package(Boost REQUIRED COMPONENTS regex)
include_directories(${Boost_INCLUDE_DIRS})
target_link_libraries(${APP_NAME} ${Boost_LIBRARIES})

################################################################################
# openssl package:
option(SSLRHEL7 "OpenSSL 1.1 For Red Hat 7.x provided by EPEL" OFF)
if (SSLRHEL7)
    pkg_check_modules(OPENSSL REQUIRED libssl11)
else()
    pkg_check_modules(OPENSSL REQUIRED libssl)
endif()
target_include_directories(${APP_NAME} PUBLIC ${OPENSSL_INCLUDE_DIRS})
target_compile_options(${APP_NAME} PUBLIC ${OPENSSL_CFLAGS_OTHER})
target_link_libraries(${APP_NAME} ${OPENSSL_STATIC_LDFLAGS})

################################################################################
# jsoncpp package:
pkg_check_modules(JSONCPP jsoncpp)
link_libraries(${JSONCPP_LIBRARIES})
target_include_directories(${APP_NAME} PUBLIC ${JSONCPP_INCLUDE_DIRS})
target_link_libraries(${APP_NAME} ${JSONCPP_LIBRARIES})

################################################################################
# libMantids packages:
pkg_check_modules(MANTIDS_LIBS REQUIRED
    mdz_xrpc_fast
    mdz_xrpc_templates mdz_xrpc_webserver mdz_xrpc_common mdz_xrpc_templates mdz_auth mdz_auth_db mdz_db mdz_db_sqlite3 mdz_proto_http mdz_proto_mime mdz_net_sockets mdz_thr_mutex mdz_thr_safecontainers mdz_thr_threads mdz_prg_service mdz_prg_logs mdz_mem_vars mdz_hlp_functions)
include_directories(${MANTIDS_LIBS_INCLUDE_DIRS})
link_directories(${MANTIDS_LIBS_LIBRARY_DIRS})
target_link_libraries(${APP_NAME} ${MANTIDS_LIBS_LIBRARIES})
################################################################################
