# Copyright (C) 2023 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of wkstools.
#
# wkstools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wkstools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wkstools.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
from pathlib import Path

src_path = "."
assetpublisher = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "__init__.py"
)

with open(assetpublisher, "r") as file:
    file_contents = file.read()

match = re.search(r'"version": \((\d+), (\d+), (\d+)\)', file_contents)

if match:
    version = tuple(int(match.group(i)) for i in range(1, 4))
    version_string = ".".join(str(x) for x in version)
    print("Version:", version_string)
else:
    print("Version information not found.")

home = Path.home()
assetpub_folder = os.path.join("3.6", "scripts", "addons", "assetpublisher")
blender_paths = [
    os.path.join(home, "blender3-win", assetpub_folder),
    os.path.join(home, "blender3-win-batam", assetpub_folder),
]

exclusion_list = [
    "__pycache__",
    ".vscode",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "README.md",
    "package.py",
    ".zip",
    ".git",
    ".pyc",
    ".blend1",
    "TODO.txt",
    ".mypy_cache",
    ".python-version",
]


def copy_items_recursively(src_path, dest_path):
    all_items = os.listdir(src_path)

    for item in all_items:
        src = os.path.join(src_path, item)
        dst = os.path.join(dest_path, item)

        if item in exclusion_list:
            continue

        if not os.path.isdir(src):
            shutil.copy2(src, dst)
            print(f"Copying File {item} to {dst}")
        else:
            shutil.copytree(
                src,
                dst,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(*exclusion_list),
            )
            print(f"Copying Folder {item} to {dst}")


for path in blender_paths:
    if not os.path.exists(path):
        os.makedirs(path)
    copy_items_recursively(src_path, path)

print("Copying Completed")
