"""spl-core build-tree path layout (taken over — see this package's __init__)."""

from pathlib import Path


class SplPaths:
    """Resolves the spl-core build/variant directories for a variant build.

    The layout ``build/<variant>/<build_kit>[/<build_type>]`` is defined by
    spl-core's ``spl.cmake``. ``<variant>`` keeps its ``/`` separator for
    flavor/subsystem variants (e.g. ``FLV/SUB``).

    Mirrors ``spl_build_extensions.artifacts.spl_paths.SplPaths`` so a future move
    into the spl-core package is a straight lift.
    """

    def __init__(self, project_root_dir: Path, variant: str, build_kit: str, build_type: str | None = None) -> None:
        self.project_root_dir = project_root_dir
        self.variant = variant.replace("\\", "/")
        self.build_kit = build_kit
        self.build_type = build_type

    @property
    def build_dir(self) -> Path:
        build_dir = self.project_root_dir.joinpath("build", self.variant, self.build_kit)
        if self.build_type:
            build_dir = build_dir.joinpath(self.build_type)
        return build_dir

    @property
    def variant_dir(self) -> Path:
        return self.project_root_dir.joinpath("variants", self.variant)
