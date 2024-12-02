# Copyright (C) 2024 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of assetpublisher.
#
# assetpublisher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# assetpublisher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with assetpublisher.  If not, see <https://www.gnu.org/licenses/>.
import glob
import os

import bpy

# from yaml import safe_load  # type: ignore
from bpy.utils import script_paths

from .. import __package__ as base_package


class System:

    @classmethod
    def traverse_tree(cls, t):
        """
        Traverse Tree Function
        """
        yield t
        for child in t.children:
            yield from System.traverse_tree(child)

    @classmethod
    def redraw_ui(cls) -> None:
        """
        Forces blender to redraw the UI.
        """
        for screen in bpy.data.screens:
            for area in screen.areas:
                area.tag_redraw()

    @classmethod
    def get_addon_data(cls, dirname: str):
        """
        Get user addon data installation directory
        """
        scripts_path_to_check = []

        for path in script_paths():
            scriptpath = os.path.join(path, "addons", base_package)
            scripts_path_to_check.append(scriptpath)

        user_resources = next(
            (path for path in scripts_path_to_check if os.path.exists(path)),
            None,
        )
        if user_resources:
            return os.path.join(user_resources, "data", dirname)

    @classmethod
    def get_files(cls, dirpath, ext: str) -> list:
        """
        Get files from folder with specified ext
        """
        return glob.glob(os.path.join(dirpath, f"*.{ext}"))

    @classmethod
    def layer_collection(cls, name, _layer_collection=None):
        """
        Layer Collection by collection name
        """
        if _layer_collection is None:
            _layer_collection = bpy.context.view_layer.layer_collection
        if _layer_collection.name == name:
            return _layer_collection
        else:
            for l_col in _layer_collection.children:
                if rez := System.layer_collection(
                    name=name, _layer_collection=l_col
                ):
                    return rez

    @classmethod
    def replace_name(cls, data: list, old_name: str, name: str):
        if isinstance(data, list):
            return [cls.replace_name(item, old_name, name) for item in data]
        elif isinstance(data, dict):
            return {
                cls.replace_name(key, old_name, name): cls.replace_name(
                    value, old_name, name
                )
                for key, value in data.items()
            }
        elif isinstance(data, str):
            return data.replace(old_name, name)
        else:
            return data

    @classmethod
    def process_asset_data(cls, data, parent_collection=None):

        color = "COLOR_06"

        def find_collection_case_insensitive(collection_name):
            for col in bpy.data.collections:
                if col.name.lower() == collection_name.lower():
                    return col
            return None

        def create_collection(collection_name, parent=None):
            existing_collection = find_collection_case_insensitive(
                collection_name
            )
            if existing_collection:
                existing_collection.name = collection_name
                existing_collection.color_tag = color
                return existing_collection

            new_collection = bpy.data.collections.new(collection_name)
            new_collection.color_tag = color

            if parent:
                parent.children.link(new_collection)
            else:
                bpy.context.scene.collection.children.link(new_collection)

            return new_collection

        if isinstance(data, list):
            for item in data:
                cls.process_asset_data(item, parent_collection)
        elif isinstance(data, dict):
            for key, value in data.items():
                current_collection = create_collection(key, parent_collection)
                cls.process_asset_data(value, current_collection)
        elif isinstance(data, str):
            create_collection(data, parent_collection)

    @classmethod
    def duplicate(cls, obj, data=True, actions=True, collection=None):
        obj_copy = obj.copy()
        if data:
            obj_copy.data = obj_copy.data.copy()
        if actions and obj_copy.animation_data:
            obj_copy.animation_data.action = (
                obj_copy.animation_data.action.copy()
            )
        collection.objects.link(obj_copy)
        return obj_copy
