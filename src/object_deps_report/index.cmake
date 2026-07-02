cmake_language(DEFER DIRECTORY ${CMAKE_SOURCE_DIR} CALL _spl_object_deps_hook())

function(_spl_object_deps_hook)
    set(OBJECT_DEPS_RUNNER object_deps_report.exe)
    if(BUILD_TYPE)
        set(build_type_arg "--build-type")
    endif()
    # call the extension generate function
    execute_process(
        COMMAND ${OBJECT_DEPS_RUNNER} generate --project-root-dir ${CMAKE_SOURCE_DIR} --variant ${VARIANT} --build-kit ${BUILD_KIT} ${build_type_arg} ${BUILD_TYPE}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        OUTPUT_VARIABLE output
        ERROR_VARIABLE error
        RESULT_VARIABLE result
    )

    # print stdout/stderr
    message(STATUS "STDERR: ${error}")
    message(STATUS "STDOUT: ${output}")

    # check if the command succeeded
    if(result)
        message(FATAL_ERROR "Generation of Object Dependencies extension failed.")
    else()
        message(STATUS "Generation of Object Dependencies extension was successful.")
    endif()

    # include the generated cmake file
    include(${CMAKE_BINARY_DIR}/object_deps_report.cmake)

endfunction(_spl_object_deps_hook)
