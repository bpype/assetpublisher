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

from ...tool import Asset as asset
from ...tool import System as ap_system


class AP_OT_collection_from_yaml(Operator):
    """
    Operator to create collection from yaml in data folder
    """

    bl_idname = "outliner.ap_collection_from_yaml"
    bl_label = "Collection from Yaml Data"

    @classmethod
    def poll(cls, context):
        return context.scene.APMetadataProperties.meta_asset_type != "none" and not asset.has_collection_structure()

    def execute(self, context: Context):
        asset_data = asset.get_asset_data()
        ap_system.process_asset_data(asset_data)

        return {"FINISHED"}


registry = [
    AP_OT_collection_from_yaml,
]
