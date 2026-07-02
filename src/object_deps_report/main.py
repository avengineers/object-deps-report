import sys
from pathlib import Path

import typer
from py_app_dev.core.logging import logger

from object_deps_report.cmake_file_generator import CmakeFileGenerator

package_name = "object_deps_report"

app = typer.Typer(name=package_name, help="An spl-core extension to generate the object dependency graph with clanguru", add_completion=False)


@app.callback(invoke_without_command=True)
def version(version: bool = typer.Option(None, "--version", "-v", is_eager=True, help="Show version and exit.")) -> None:
    """Print package version and exit when --version supplied."""
    if version:
        from object_deps_report import __version__

        typer.echo(__version__)
        raise typer.Exit()


@app.command()
def generate(
    project_root_dir: Path = typer.Option(..., "--project-root-dir", help="The project root directory."),  # noqa: B008
    variant: str = typer.Option(..., "--variant", help="The variant of the project."),
    build_kit: str = typer.Option(..., "--build-kit", help="The build kit."),
    build_type: str | None = typer.Option(None, "--build-type", help="The build type."),
) -> None:
    """Generate the CMake file wiring the 'objects-deps' target for this variant."""
    logger.info("[CLI] generate command invoked")
    try:
        cmake_generator = CmakeFileGenerator()
        cmake_generator.run(project_root_dir, variant, build_kit, build_type)
        logger.info("[CLI] generate command completed successfully")
    except Exception as e:
        logger.error(f"[CLI] generate command failed: {e}")
        typer.echo(f"Error generating CMake files: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
