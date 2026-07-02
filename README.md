# object-deps-report

An spl-core build extension that generates the **object-file dependency graph**
report for a variant using [clanguru](https://github.com/cuinixam/clanguru).

The extension wires a CMake custom target `objects-deps` into the variant build.
Because the report is built from the object files listed in
`compile_commands.json`, the target depends on the linked **executable** (so every
object is guaranteed to exist) and on `compile_commands.json`. Running the target
invokes `clanguru analyze` to produce an interactive HTML dependency graph.

![maintained](https://img.shields.io/badge/maintained-yes-success?style=flat-square)
![license](https://img.shields.io/badge/license-MQ--internal-009b9b?style=flat-square)
![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![pypeline](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cuinixam/pypeline/main/assets/badge/v0.json)

## Installation

Install this via pip (or your favorite package manager):

`pip install object_deps_report`

Then, in the consuming spl-core project's `CMakeLists.txt`, after `spl.cmake` and
the variant parts are included:

```cmake
include(".venv/Lib/site-packages/object_deps_report/index.cmake")
```

## Usage

Build the project first (so the executable and all objects exist), then build the
report target:

```powershell
cmake --build build/<variant>/<build_kit> --target objects-deps
```

The report is written to
`build/<variant>/<build_kit>/reports/object_dependencies.html`.

## How it works

The extension needs **no configuration file** and reads no KConfig/autoconf state.
Its `index.cmake` (included from your `CMakeLists.txt`) defers a hook to the end of
CMake configure that runs `object_deps_report generate ...`; that writes
`object_deps_report.cmake` into the build directory and `include()`s it. The
generated file contains:

- an `add_custom_command` that runs
  `clanguru analyze --compilation-database ${CMAKE_BINARY_DIR}/compile_commands.json --output-file <report>`;
- `DEPENDS $<TARGET_FILE:${LINK_TARGET_NAME}> ${CMAKE_BINARY_DIR}/compile_commands.json`
  — spl-core's linked executable target (so every object is built first, and the
  report regenerates when the binary changes) plus the compilation database
  (spl-core sets `CMAKE_EXPORT_COMPILE_COMMANDS ON`, so it always exists);
- `add_custom_target(objects-deps DEPENDS <report>)` — **not** part of the default
  (`ALL`) build, so the report is produced on demand.

> The `link` target exists only for the **`prod`** build kit (test kits build
> per-component GTest executables), so run `objects-deps` in a prod build.

## Start developing

The project is managed with [uv](https://docs.astral.sh/uv/) and orchestrated by
[pypeline](https://github.com/cuinixam/pypeline). Bootstrap the environment and
run the full pipeline (venv, pre-commit, tests) with:

```shell
pypeline run
```

## Committing changes

This repository uses [commitlint](https://github.com/conventional-changelog/commitlint) for checking if the commit message meets the [conventional commit format](https://www.conventionalcommits.org/en). Commit messages drive the automated release.

## Continuous integration & release

CI runs on **GitHub Actions** (`.github/workflows/ci.yml`): lint (pre-commit),
commitlint, a test matrix (Python 3.10/3.13 × Ubuntu/Windows), and a release job.
Releases are automated with [python-semantic-release](https://python-semantic-release.readthedocs.io/):
merging to `main` bumps the version from the conventional-commit history and
publishes to PyPI (trusted publishing) and GitHub Releases.

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
