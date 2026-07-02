from pathlib import Path

from object_deps_report.cmake_file_generator import (
    CMAKE_FILE_NAME,
    LINK_TARGET_FILE,
    TARGET_NAME,
    CmakeFileGenerator,
)


class TestCmakeFileGenerator:
    """Tests for the object dependencies CMake generator."""

    def test_generates_command_and_target_with_dependencies(self, tmp_path: Path) -> None:
        """The generated file wires a custom command depending on the spl-core
        link target and compile_commands.json, plus the on-demand objects-deps target."""
        CmakeFileGenerator().run(tmp_path, "MYVARIANT", "prod")

        generated = tmp_path / "build" / "MYVARIANT" / "prod" / CMAKE_FILE_NAME
        assert generated.exists()
        content = generated.read_text()

        # custom command runs clanguru analyze on the compilation database
        assert "add_custom_command(" in content
        assert "clanguru analyze --compilation-database ${CMAKE_BINARY_DIR}/compile_commands.json" in content
        assert "--output-file ${CMAKE_BINARY_DIR}/reports/object_dependencies.html" in content

        # depends on the spl-core linked executable target (CMake-resolved, no autoconf)
        # and on compile_commands.json
        assert f"DEPENDS {LINK_TARGET_FILE} ${{CMAKE_BINARY_DIR}}/compile_commands.json" in content

        # on-demand custom target, NOT part of the default (ALL) build
        assert f"add_custom_target(\n    {TARGET_NAME}\n" in content
        assert f"{TARGET_NAME} ALL" not in content

    def test_no_config_files_required(self, tmp_path: Path) -> None:
        """Generation reads no autoconf/variant config — an empty project tree works."""
        CmakeFileGenerator().run(tmp_path, "MYVARIANT", "prod")

        generated = tmp_path / "build" / "MYVARIANT" / "prod" / CMAKE_FILE_NAME
        assert generated.exists()
        assert LINK_TARGET_FILE in generated.read_text()

    def test_handles_variant_with_subsystem_and_build_type(self, tmp_path: Path) -> None:
        """Variant with subsystem and a build type resolve into the nested build dir."""
        CmakeFileGenerator().run(tmp_path, "FLV/SUB", "prod", "Release")

        generated = tmp_path / "build" / "FLV" / "SUB" / "prod" / "Release" / CMAKE_FILE_NAME
        assert generated.exists()
        assert LINK_TARGET_FILE in generated.read_text()
