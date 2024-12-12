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
from bpy.types import Context, Operator

from ... import tool


class AP_OT_collection_from_yaml(Operator):
    """
    Operator to create collection from yaml in data folder
    """

    bl_idname = "outliner.ap_collection_from_yaml"
    bl_label = "Collection from Yaml Data"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context: Context):
        props = context.scene.APMetadataProperties
        collections_path = tool.System.get_addon_data("collections")
        collections_yaml = tool.System.get_files(collections_path, "yml")

        if props.meta_asset_type != "none":
            type_yaml = [
                y
                for y in collections_yaml
                if props.meta_asset_type in os.path.basename(y)
            ][0]

            with open(type_yaml, "r") as stream:
                data = safe_load(stream)

            asset_data = tool.System.replace_name(
                data, "Name", props.meta_asset_name
            )

            tool.System.process_asset_data(asset_data)

        return {"FINISHED"}


registry = [
    AP_OT_collection_from_yaml,
]
