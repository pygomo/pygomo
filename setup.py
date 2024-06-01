# The entire use case of this setup.py file is to integrate CMake
# to the project for the build process of the project's extension
# modules and its external dependencies registered in git submodules

# All of this is done by reconfiguring setuptools' builtin commands
# to make the commands build_clib and build_ext fetch the project's
# external dependencies and build them along side with the actual
# project's extension modules respectively

# ruff: noqa: N801

from __future__ import annotations

from pathlib import Path

import setuptools
from setuptools.command.build import build as _build
from setuptools.command.build_clib import build_clib as _build_clib
from setuptools.command.build_ext import build_ext as _build_ext


class build(_build):
    def initialize_options(self: build) -> None:
        super().initialize_options()

        # The code below is necessary since the C/C++ libraries and
        # extension modules are configured in CMake and not here

        # This makes the distribution tells that it has
        # C/C++ libraries and extension modules to build
        self.distribution.has_c_libraries = lambda: True
        self.distribution.has_ext_modules = lambda: True

        # It's not valid for this to be None
        # so we set it to be an empty list
        self.distribution.libraries = []


class build_clib(_build_clib):
    def run(self: build_clib) -> None:
        # The code below fetches the project's external dependencies
        # with git submodules to the extern/ directory

        # If there's no .git directory in the current working directory,
        # it means that we are building from a sdist (source distribution)
        # where the project's external dependencies are already fetched
        if not Path(".git").exists():
            # We return since there's no .git directory and the project's external
            # dependencies are already fetched in the sdist (source distribution)
            return

        # This ensures that we have the project's external dependencies
        # updated by updating the registered submodules in the .gitmodules file
        self.spawn(["git", "submodule", "update", "--init", "--recursive", "--force"])


class build_ext(_build_ext):
    def run(self: build_ext) -> None:
        # This ensures that build_clib is ran before building the
        # extension modules, because the C/C++ libraries built in
        # build_clib are the project's external dependencies
        self.run_command("build_clib")

        # This will be used for getting the package's directory
        build_py = self.get_finalized_command("build_py")

        # This is the current working directory
        source_dir = Path().absolute()

        # This will get the build directory and package directory
        # into the variables build_dir and package_dir. If --inplace
        # we set these to the provided directories
        if not self.inplace:
            build_dir = Path(self.build_temp).absolute()
            package_dir = Path(self.build_lib).absolute() / "pygomo"
        else:
            build_dir = Path(source_dir / "build").absolute()
            package_dir = Path(build_py.get_package_dir("pygomo")).absolute()

        # Make sure that these directories exists
        package_dir.mkdir(parents=True, exist_ok=True)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir.mkdir(parents=True, exist_ok=True)

        # This is where the actual building begins, the project
        # uses CMake for the building process
        # fmt: off
        self.spawn(["cmake", "-S", str(source_dir),
                             "-B", str(build_dir),
                             "-G", "Ninja"])
        self.spawn(["cmake", "--build",   str(build_dir)])
        self.spawn(["cmake", "--install", str(build_dir),
                             "--prefix",  str(source_dir)])
        # fmt: on


cmdclass = {
    "build": build,
    "build_clib": build_clib,
    "build_ext": build_ext,
}

if __name__ == "__main__":
    setuptools.setup(cmdclass=cmdclass)
