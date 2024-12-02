# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# NOTE: The original author of this file is Sybren Stüvel. This file is copied from the
# Flamenco project: https://developer.blender.org/diffusion/F/browse/main/addon/flamenco/wheels/__init__.py

"""External dependencies loader."""

import contextlib
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Iterator

_my_dir = Path(__file__).parent
_log = logging.getLogger(__name__)


def load_wheel(module_name: str, fname_prefix: str) -> ModuleType:
    """Loads a wheel from 'fname_prefix*.whl', unless the named module can be imported.

    This allows us to use system-installed packages before falling back to the shipped wheels.
    This is useful for development, less so for deployment.
    """

    try:
        module = __import__(module_name)
    except ImportError as ex:
        _log.debug(
            "Unable to import %s directly, will try wheel: %s", module_name, ex
        )
    else:
        _log.debug(
            "Was able to load %s from %s, no need to load wheel %s",
            module_name,
            module.__file__,
            fname_prefix,
        )
        assert isinstance(module, ModuleType)
        return module

    wheel = _wheel_filename(fname_prefix)

    # Load the module from the wheel file. Keep a backup of sys.path so that it
    # can be restored later. This should ensure that future import statements
    # cannot find this wheel file, increasing the separation of dependencies of
    # this add-on from other add-ons.
    with _sys_path_mod_backup(wheel):
        try:
            module = __import__(module_name)
        except ImportError as ex:
            raise ImportError(
                "Unable to load %r from %s: %s" % (module_name, wheel, ex)
            ) from None

    _log.debug("Loaded %s from %s", module_name, module.__file__)
    assert isinstance(module, ModuleType)
    return module


def load_wheel_global(module_name: str, fname_prefix: str) -> ModuleType:
    """Loads a wheel from 'fname_prefix*.whl', unless the named module can be imported.

    This allows us to use system-installed packages before falling back to the shipped wheels.
    This is useful for development, less so for deployment.
    """

    try:
        module = __import__(module_name)
    except ImportError as ex:
        _log.debug(
            "Unable to import %s directly, will try wheel: %s", module_name, ex
        )
    else:
        _log.debug(
            "Was able to load %s from %s, no need to load wheel %s",
            module_name,
            module.__file__,
            fname_prefix,
        )
        return module

    wheel = _wheel_filename(fname_prefix)

    wheel_filepath = str(wheel)
    if wheel_filepath not in sys.path:
        sys.path.insert(0, wheel_filepath)

    try:
        module = __import__(module_name)
    except ImportError as ex:
        raise ImportError(
            "Unable to load %r from %s: %s" % (module_name, wheel, ex)
        ) from None

    _log.debug("Globally loaded %s from %s", module_name, module.__file__)
    return module


@contextlib.contextmanager
def _sys_path_mod_backup(wheel_file: Path) -> Iterator[None]:
    old_syspath = sys.path[:]

    try:
        sys.path.insert(0, str(wheel_file))
        yield
    finally:
        # Restore without assigning new instances. That way references held by
        # other code will stay valid.

        sys.path[:] = old_syspath


def _wheel_filename(fname_prefix: str) -> Path:
    path_pattern = f"{fname_prefix}*.whl"
    wheels: list[Path] = list(_my_dir.glob(path_pattern))
    if not wheels:
        raise RuntimeError(f"Unable to find wheel at {path_pattern!r}")

    # Get platform-specific tag based on sys.platform
    if sys.platform.startswith("win"):  # Windows
        platform_tag = "win_amd64"
    elif sys.platform.startswith("linux"):  # Linux
        platform_tag = "manylinux"
    else:
        platform_tag = None  # Allow for universal wheels

    # Filter wheels by platform or 'none' for universal wheels
    platform_wheels = [
        wheel
        for wheel in wheels
        if platform_tag in wheel.name or "none" in wheel.name
    ]

    if not platform_wheels:
        raise RuntimeError(
            f"No wheels found for platform: {platform_tag or 'universal'}"
        )

    # Sort by modification time to get the most recent one
    platform_wheels.sort(key=lambda filepath: filepath.stat().st_mtime)

    return platform_wheels[-1]


def preload_dependencies() -> None:
    """Pre-load the modules from a wheel so that the API can find it."""
    module = load_wheel_global("yaml", "PyYAML")
    _log.debug(f"Loaded wheel: {module.__name__}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    wheel = _wheel_filename("PyYAML")
    print(f"Wheel: {wheel}")
