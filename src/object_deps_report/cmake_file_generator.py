from pathlib import Path

from py_app_dev.core.logging import logger

from object_deps_report._spl_core.cmake_file import (
    CMakeComment,
    CMakeCustomCommand,
    CMakeCustomTarget,
    CMakeFile,
    CMakePath,
)
from object_deps_report._spl_core.spl_paths import SplPaths

#: The generated CMake file, written into the variant build dir (== ${CMAKE_BINARY_DIR}).
CMAKE_FILE_NAME = "object_deps_report.cmake"
#: Report location relative to the build directory (HTML dependency graph).
REPORT_RELATIVE_PATH = "reports/object_dependencies.html"
#: Name of the CMake custom target a developer invokes on demand.
TARGET_NAME = "objects-deps"
#: spl-core creates the linked executable as the target named by LINK_TARGET_NAME
#: (`link`) for the prod build kit — see spl-core spl.cmake. Depending on its
#: TARGET_FILE builds the executable (hence every object) first and re-runs the
#: report whenever the binary changes. Resolved by CMake, so we need no autoconf.
LINK_TARGET_FILE = "$<TARGET_FILE:${LINK_TARGET_NAME}>"


class CmakeFileGenerator:
    """Generate the CMake file for the Object Dependencies extension.

    The generated file registers a custom command that runs ``clanguru analyze``
    against ``compile_commands.json``. Because clanguru reads every object file
    listed in the compilation database, the command depends on spl-core's linked
    executable target (``$<TARGET_FILE:${LINK_TARGET_NAME}>``) so all objects are
    built first, and on ``compile_commands.json``. The ``objects-deps`` target is
    not part of the default (``ALL``) build, so the report is produced on demand.
    """

    def run(self, project_root_dir: Path, variant: str, build_kit: str, build_type: str | None = None) -> None:
        logger.info(f"[CMakeGen] Generating object dependencies CMake file for variant={variant} kit={build_kit} build_type={build_type}")
        spl_paths = SplPaths(project_root_dir, variant, build_kit, build_type)

        report = CMakePath(f"${{CMAKE_BINARY_DIR}}/{REPORT_RELATIVE_PATH}")
        compile_commands = CMakePath("${CMAKE_BINARY_DIR}/compile_commands.json")
        executable = CMakePath(LINK_TARGET_FILE)

        command = f"clanguru analyze --compilation-database {compile_commands} --output-file {report}"

        custom_command = CMakeCustomCommand(
            outputs=[report],
            commands=[command],
            # The linked executable target forces all objects to be compiled and
            # linked before clanguru runs; compile_commands.json is its direct input.
            depends=[executable, compile_commands],
            comment="Generate object dependencies report (clanguru)",
        )
        custom_target = CMakeCustomTarget(
            name=TARGET_NAME,
            depends=custom_command.outputs,
        )

        cmake_file = CMakeFile(spl_paths.build_dir.joinpath(CMAKE_FILE_NAME))
        cmake_file.add_element(CMakeComment("Object Dependencies Extension CMake Targets"))
        cmake_file.add_element(custom_command)
        cmake_file.add_element(custom_target)
        cmake_file.to_file()
        logger.info(f"Generated CMake file at {cmake_file.path}")
