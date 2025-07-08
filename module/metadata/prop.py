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

from pathlib import Path

import bpy
from bpy.app.handlers import persistent
from bpy.props import EnumProperty, StringProperty
from bpy.types import PropertyGroup

CONVENTIONS = {
    "char": "C_",
    "prop": "P_",
    "set": "S_",
    "vehicle": "V_",
}


@persistent
def get_asset_task(dummy):
    props = bpy.context.scene.APMetadataProperties
    file_path = Path(bpy.data.filepath)
    if props.meta_asset_status == "working":
        if "_RIG" in file_path.name:
            props.meta_asset_task = "rig"
        elif "_SHD" in file_path.name:
            props.meta_asset_task = "shader"
        elif "_MDL" in file_path.name:
            props.meta_asset_task = "model"
        else:
            props.meta_asset_task = "none"


@persistent
def get_asset_status(dummy):
    props = bpy.context.scene.APMetadataProperties
    if file_path := Path(bpy.data.filepath):
        if path_list := file_path.parents:
            if "02_Publish" in path_list[0].parts:
                props.meta_asset_status = "published"
            elif "01_Working" in path_list[0].parts:
                props.meta_asset_status = "working"
            else:
                props.meta_asset_status = "none"


@persistent
def get_asset_name(dummy):
    global CONVENTIONS
    asset_coll = set()
    colls = [
        col for assettype, assetname in CONVENTIONS.items() for col in bpy.data.collections if assetname in col.name
    ]
    if colls:
        asset_coll.add(colls[0])
    list_asset_coll = list(asset_coll)
    if list_asset_coll:
        scene = bpy.context.scene
        props = scene.APMetadataProperties
        asset_clean_name = (
            list_asset_coll[0].name.split(".")[0] if "." in list_asset_coll[0].name else list_asset_coll[0].name
        )
        props.meta_asset_name = asset_clean_name[2:]
        props.meta_asset_type = [
            assettype for assettype, assetname in CONVENTIONS.items() if asset_clean_name[:2] == assetname
        ][0]


def update_asset_code(self, context):
    props = context.scene.APMetadataProperties
    if props.meta_asset_type != "none":
        props.meta_asset_code = CONVENTIONS[props.meta_asset_type]


class APMetadataProperties(PropertyGroup):
    """Asset Publisher Metadata Properties"""

    meta_asset_name: StringProperty(
        name="Asset name",
        default="Asset Name here...",
    )  # type: ignore

    meta_asset_type: EnumProperty(
        items=(
            ("char", "Character", "Character"),
            ("prop", "Prop", "Prop"),
            ("set", "Set", "Set"),
            ("vehicle", "Vehicle", "Vehicle"),
            ("none", "Not Available", "Not Available"),
        ),
        default="none",
        update=update_asset_code,
    )  # type: ignore
    meta_asset_code: EnumProperty(
        items=(
            ("C_", "C_", "Character"),
            ("P_", "P_", "Prop"),
            ("S_", "S_", "Set"),
            ("V_", "V_", "Vehicle"),
            ("none", "", ""),
        ),
        default="none",
    )  # type: ignore
    meta_asset_status: EnumProperty(
        items=(
            ("working", "Working", "Working"),
            ("published", "Published", "Published"),
            ("none", "Not Available", "Not Available"),
        ),
        default="none",
    )

    meta_asset_task: EnumProperty(
        items=(
            ("none", "Not Available", "Not Available"),
            ("rig", "Rig", "Rig"),
            ("shader", "Shader", "Shader"),
            ("model", "Model", "Model"),
        ),
        default="none",
    )


registry = [APMetadataProperties]
