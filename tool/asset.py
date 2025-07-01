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
from pathlib import Path

import bpy

from .. import wheels
from .system import System as ap_system

wheels.preload_dependencies()

from yaml import safe_load


class Asset:

    @classmethod
    def get_asset_data(cls):
        props = bpy.context.scene.APMetadataProperties
        collections_path = ap_system.get_addon_data("collections")
        collections_yaml = ap_system.get_files(collections_path, "yml")

        if props.meta_asset_type != "none":
            type_yaml = [y for y in collections_yaml if props.meta_asset_type in os.path.basename(y)][0]

            with open(type_yaml, "r") as stream:
                data = safe_load(stream)

            asset_data = ap_system.replace_name(data, "Name", props.meta_asset_name)

            return asset_data

    @classmethod
    def get_layer_collection_hierarchy(
        cls,
        lc: bpy.types.LayerCollection,
    ):
        children_list = []
        for child in lc.children:
            if len(child.children) > 0:
                children_list.append({child.name: cls.get_layer_collection_hierarchy(child)})
            else:
                children_list.append(child.name)
        return children_list

    @classmethod
    def has_collection_structure(cls) -> bool:
        def is_subset(A, B):
            if isinstance(A, dict):
                return isinstance(B, dict) and all(key in B and is_subset(value, B[key]) for key, value in A.items())
            elif isinstance(A, list):
                return isinstance(B, list) and all(any(is_subset(a, b) for b in B) for a in A)
            else:
                return A == B

        view_layer = bpy.context.view_layer
        layer_collection = view_layer.layer_collection

        current_hierarchy = cls.get_layer_collection_hierarchy(layer_collection)
        asset_data = cls.get_asset_data()
        return is_subset(asset_data, current_hierarchy)

    @classmethod
    def is_lo_ready(cls) -> bool:
        props = bpy.context.scene.APMetadataProperties
        name = props.meta_asset_name
        code = props.meta_asset_code
        asset_name = f"{code}{name}_MDL.lo"
        hi_asset_name = f"{code}{name}_MDL.hi"
        lo_collection = bpy.data.collections.get(asset_name)
        hi_collection = bpy.data.collections.get(hi_asset_name)
        if not lo_collection.objects:
            print(f"{lo_collection.name} has no objects")
            return False
        if len(lo_collection.objects) != len(hi_collection.objects):
            return False
        for obj in lo_collection.objects:
            if not obj.name.endswith(".lo"):
                print(f"{obj.name} is not a LOD")
                return False
            if not (mat := obj.active_material):
                return False
            if mat.name != "SHD_Transparent":
                return False
            if mat_slot := obj.material_slots.get("SHD_Transparent"):
                if mat_slot.link != "OBJECT":
                    return False
        return True

    @classmethod
    def create_lo_asset(cls):
        props = bpy.context.scene.APMetadataProperties
        name = props.meta_asset_name
        code = props.meta_asset_code
        asset_name = f"{code}{name}_MDL.hi"
        hi_collection = bpy.data.collections.get(asset_name)
        hi_objects = [o for o in hi_collection.objects if o.type == "MESH"]
        if not bpy.data.materials.get("SHD_Transparent"):
            materials_path = ap_system.get_addon_data("materials")
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
        if lo_collection.objects:
            for obj in lo_collection.objects:
                bpy.data.objects.remove(obj)
        # if not lo_collection.objects:
        for obj in hi_objects:
            lo_obj = ap_system.duplicate(obj, data=False, actions=False, collection=lo_collection)
            if not lo_obj.name.endswith(".lo"):
                lo_obj.name = f"{lo_obj.name}.lo"

            if mat_slots := lo_obj.material_slots:
                for slot in mat_slots:
                    slot.link = "OBJECT"
                    slot.material = transparent_shader

    @classmethod
    def get_objects_with_subdiv(cls) -> list:
        objs_with_subdiv = []
        for obj in bpy.data.objects:
            if (
                (mods := obj.modifiers)
                and any(m.type == "SUBSURF" and m.show_render for m in mods)
                or any(
                    m.type == "NODES"
                    and hasattr(m.node_group, "name")
                    and m.node_group.name.startswith("GN_SubD")
                    and not any("Level" in inp.name for inp in m.node_group.inputs)
                    for m in mods
                )
            ):
                objs_with_subdiv.append(obj)
        return objs_with_subdiv

    @classmethod
    def append_nodegroups(cls, group_path: str, group_name: str):
        if node_group := bpy.data.node_groups.get(group_name):
            return node_group

        with bpy.data.libraries.load(group_path, link=False) as (
            data_from,
            data_to,
        ):
            data_to.node_groups = [name for name in data_from.node_groups if name.startswith(group_name)]
        return bpy.data.node_groups.get(group_name)

    @classmethod
    def set_gn_subdiv(cls, obj: bpy.types.Object) -> None:
        if obj.type == "MESH":
            mod_path = ap_system.get_addon_data("modifiers")
            gn_blend = [b for b in ap_system.get_files(mod_path, "blend") if "geonodes" in bpy.path.basename(b)][0]
            gn_subdiv = cls.append_nodegroups(gn_blend, "GN_SubD")
            subsurf_mod = next((mod for mod in obj.modifiers if mod.type == "SUBSURF"), None)

            if subsurf_mod:
                subsurf_mod.show_render = False
            else:
                subsurf_mod = obj.modifiers.new("SubD", "SUBSURF")
                subsurf_mod.show_render = False

            if not (gn_mod := obj.modifiers.get("GN_SubD")):
                gn_mod = obj.modifiers.new(gn_subdiv.name, "NODES")
            gn_mod.node_group = gn_subdiv
            obj.modifiers.move(obj.modifiers.find("GN_SubD"), len(obj.modifiers) - 1)

    @classmethod
    def clean_existing_gn_subdiv(cls):
        for node_group in bpy.data.node_groups:
            if node_group.name.startswith("GN_SubD") and not any("Level" in inp.name for inp in node_group.inputs):
                bpy.data.node_groups.remove(node_group)
        for obj in bpy.data.objects:
            if (mods := obj.modifiers) and any(m.type == "NODES" and not hasattr(m.node_group, "name") for m in mods):
                for m in mods:
                    obj.modifiers.remove(m)


    

