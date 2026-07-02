"""spl-core domain primitives, taken over into this extension (temporary).

The build-tree path layout (:class:`SplPaths`) and the CMake element model
(:mod:`cmake_file`) are **spl-core domain concepts** — the layout
``build/<variant>/<build_kit>[/<build_type>]`` is defined by spl-core's
``spl.cmake``, and the generated CMake plugs into a spl-core build.

They live here only because spl-core does not yet expose them as a Python API
(spl-core ships the CMake side; the Python-side equivalents currently sit in the
*private* ``spl-build-extensions`` package, which cannot be a dependency of a
publicly-CI'd tool). They are therefore taken over here, matching the
[[yanga]] / [[yanga-core]] pattern where reusable framework primitives are owned
by the lower-level shared library.

TODO(refactor): move this subpackage into the ``spl-core`` package (public, on
PyPI) so every extension — this one, ``sbom``, ``spl-build-extensions`` — depends
on spl-core for it. When that lands, delete ``_spl_core`` and import from
``spl_core`` instead. See the "spl-core owns build primitives" vault idea.
"""
