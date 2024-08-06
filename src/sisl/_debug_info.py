# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Debug information for the tools required
_cython_build_version = """Cython version 3.0.11"""
_numpy_build_version = """2.0.1"""

_cc = """/usr/bin/gcc"""
_cc_version = """9.4.0"""
_cflags = """-O3 -DNDEBUG"""

_fc = """/usr/bin/gfortran"""
_fc_version = """9.4.0"""
_fflags = """-O3"""

_definitions = [
    ("NPY_NO_DEPRECATED_API", """"""),
    ("CYTHON_NO_PYINIT_EXPORT", """"""),
    ("CYTHON_TRACE_NOGIL", """"""),
    ("F2PY_REPORT_ATEXIT", """"""),
    ("F2PY_REPORT_ON_ARRAY_COPY", """10"""),
]

_cmake_args = [
    ("CMAKE_BUILD_TYPE", """Release"""),
    ("WITH_FORTRAN", """ON"""),
    ("WITH_COVERAGE", """OFF"""),
    ("WITH_LINE_DIRECTIVES", """OFF"""),
    ("WITH_ANNOTATE", """OFF"""),
    ("WITH_GDB", """OFF"""),
    ("NO_COMPILATION", """"""),
]


def print_debug_info():
    import importlib
    import sys
    from pathlib import Path

    print("[sys]")
    print(sys.version)

    # We import it like this to ensure there are no import errors
    # with sisl, this might be problematic, however, it should at least
    # provide consistent information
    import sisl._version as sisl_version

    fmt = "{0:30s}{1}"

    print("[sisl]")
    print(fmt.format("version", sisl_version.__version__))
    path = Path(sisl_version.__file__)
    print(fmt.format("path", str((path / "..").resolve())))

    def print_attr(module, attr: str = ""):
        try:
            mod = importlib.import_module(module)
            if attr:
                print(fmt.format(module, getattr(mod, attr)))
        except BaseException as e:
            print(fmt.format(module, "not found"))
            print(fmt.format("", str(e)))

    # regardless of whether it is on, or not, we try to import fortran extension
    print_attr("sisl.io.siesta._siesta")

    print(fmt.format("CC", _cc))
    print(fmt.format("CFLAGS", _cflags))
    print(fmt.format("C version", _cc_version))
    print(fmt.format("FC", _fc))
    print(fmt.format("FFLAGS", _fflags))
    print(fmt.format("FC version", _fc_version))
    print(fmt.format("cython build version", _cython_build_version))
    print(fmt.format("numpy build version", _numpy_build_version))
    # print("[definitions]")
    # for d, v in _definitions:
    #    print(fmt.format(d, v))
    print("[cmake_args]")
    for d, v in _cmake_args:
        print(fmt.format(d, v))

    print("[runtime modules]")
    for mod in (
        "numpy",
        "scipy",
        "xarray",
        "netCDF4",
        "pandas",
        "matplotlib",
        "dill",
        "pathos",
        "skimage",
        "plotly",
        "ase",
        "pymatgen",
    ):
        print_attr(mod, "__version__")
