"""CMake element model (taken over — see this package's __init__).

A typed model for the CMake fragments this extension generates. Rendering matches
``spl_build_extensions.generators.cmake_file`` so generated ``.cmake`` is identical
across the SPL extensions; the model is a spl-core domain concept pending a move
into the spl-core package.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

CMAKE_TAB = "    "


class CMakeElement(ABC):
    @abstractmethod
    def to_string(self) -> str: ...

    def __str__(self) -> str:
        return self.to_string()


class CMakePath:
    """A path (or CMake path expression) rendered with forward slashes."""

    def __init__(self, path: str | Path) -> None:
        self.path = path

    def to_string(self) -> str:
        return self.path if isinstance(self.path, str) else self.path.as_posix()

    def __str__(self) -> str:
        return self.to_string()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CMakePath) and other.to_string() == self.to_string()

    def __hash__(self) -> int:
        return hash(self.to_string())


@dataclass
class CMakeComment(CMakeElement):
    comment: str

    def to_string(self) -> str:
        return f"# {self.comment}"


@dataclass
class CMakeCustomCommand(CMakeElement):
    outputs: list[CMakePath]
    commands: list[str]
    depends: list[CMakePath] = field(default_factory=list)
    comment: str = ""

    def to_string(self) -> str:
        content = ["add_custom_command("]
        body = [f"OUTPUT {_paths_to_string(self.outputs)}"] + [f"COMMAND {cmd}" for cmd in self.commands]
        if self.depends:
            body.append(f"DEPENDS {_paths_to_string(self.depends)}")
        comment = self.comment.replace("\\", "/")
        body.extend([f'COMMENT "{comment}"', "VERBATIM"])
        content.extend(f"{CMAKE_TAB}{line}" for line in body)
        content.append(")")
        return "\n".join(content)


@dataclass
class CMakeCustomTarget(CMakeElement):
    name: str
    depends: list[CMakePath] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    #: Attach to the default build target so it runs on every build.
    all: bool = False

    def to_string(self) -> str:
        content = ["add_custom_target(", f"{CMAKE_TAB}{self.name}{' ALL' if self.all else ''}"]
        content.extend(f"{CMAKE_TAB}COMMAND {cmd}" for cmd in self.commands)
        if self.depends:
            content.append(f"{CMAKE_TAB}DEPENDS {_paths_to_string(self.depends)}")
        content.append(")")
        return "\n".join(content)


class CMakeFile:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.elements: list[CMakeElement] = []

    def add_element(self, *element: CMakeElement) -> "CMakeFile":
        self.elements.extend(element)
        return self

    def to_string(self) -> str:
        return "\n".join(str(element) for element in self.elements)

    def to_file(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.to_string() + "\n")


def _paths_to_string(paths: list[CMakePath]) -> str:
    return " ".join(str(path) for path in paths)
