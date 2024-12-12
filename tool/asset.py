# assetpublisher
# Copyright (C) 2024  Aditia A. Pratama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os

import bpy

from .. import wheels
from . import system

wheels.preload_dependencies()

from yaml import safe_load


class Asset:

    @classmethod
    def get_asset_data(cls):
        props = bpy.context.scene.APMetadataProperties
        collections_path = system.System.get_addon_data("collections")
        collections_yaml = system.System.get_files(collections_path, "yml")

        if props.meta_asset_type != "none":
            type_yaml = [
                y
                for y in collections_yaml
                if props.meta_asset_type in os.path.basename(y)
            ][0]

            with open(type_yaml, "r") as stream:
                data = safe_load(stream)

            asset_data = system.System.replace_name(
                data, "Name", props.meta_asset_name
            )

            return asset_data

    @classmethod
    def get_layer_collection_hierarchy(
        cls,
        lc: bpy.types.LayerCollection,
    ):
        children_list = []
        for child in lc.children:
            if len(child.children) > 0:
                children_list.append(
                    {child.name: cls.get_layer_collection_hierarchy(child)}
                )
            else:
                children_list.append(child.name)
        return children_list

    @classmethod
    def has_collection_structure(cls) -> bool:
        def is_subset(A, B):
            if isinstance(A, dict):
                return isinstance(B, dict) and all(
                    key in B and is_subset(value, B[key])
                    for key, value in A.items()
                )
            elif isinstance(A, list):
                return isinstance(B, list) and all(
                    any(is_subset(a, b) for b in B) for a in A
                )
            else:
                return A == B

        view_layer = bpy.context.view_layer
        layer_collection = view_layer.layer_collection

        current_hierarchy = cls.get_layer_collection_hierarchy(
            layer_collection
        )
        asset_data = cls.get_asset_data()
        return is_subset(asset_data, current_hierarchy)

    @classmethod
    def create_lo_asset(cls):
        props = bpy.context.scene.APMetadataProperties
        name = props.meta_asset_name
        code = props.meta_asset_code
        asset_name = f"{code}{name}_MDL.hi"
        hi_collection = bpy.data.collections.get(asset_name)
        hi_objects = [o for o in hi_collection.objects if o.type == "MESH"]
        transparent_shader = bpy.data.materials.get("SHD_Transparent")
        if not transparent_shader:
            materials_path = system.System.get_addon_data("materials")
            asset_path = os.path.join(materials_path, "shader.blend")
            with bpy.data.libraries.load(asset_path, link=False) as (
                data_from,
                data_to,
            ):
                for mat in data_from.materials:
                    if mat == "SHD_Transparent":
                        data_to.materials.append(mat)
            transparent_shader = bpy.data.materials.get("SHD_Transparent")

        lo_collection = bpy.data.collections.get(f"{code}{name}_MDL.lo")
        if not lo_collection.objects:
            for obj in hi_objects:
                lo_obj = system.System.duplicate(
                    obj, data=False, actions=False, collection=lo_collection
                )
                if not lo_obj.name.endswith(".lo"):
                    lo_obj.name = f"{lo_obj.name}.lo"

                for slot in lo_obj.material_slots:
                    slot.link = "OBJECT"
                    slot.material = transparent_shader
