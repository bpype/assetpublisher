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

from bpy.types import Panel


class AP_PT_metadata_panel:
    """
    Panel in 3D Viewport Sidebar
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AP"


class AP_PT_metadata_tools(AP_PT_metadata_panel, Panel):
    bl_label = "Asset Metadata"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene
        props = scn.APMetadataProperties

        col = layout.column(align=True)
        col.prop(props, "meta_asset_name", text="Name:", icon="ASSET_MANAGER")
        col.prop(props, "meta_asset_type", text="Type:")


registry = [
    AP_PT_metadata_tools,
]
