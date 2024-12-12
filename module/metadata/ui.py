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

from .. import ui


class AP_PT_metadata_tools(ui.AP_PT_panel, Panel):
    bl_label = "Asset Publisher"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene
        props = scn.APMetadataProperties

        col = layout.column(align=True)
        col.prop(props, "meta_asset_name", text="Name:", icon="ASSET_MANAGER")
        col.prop(props, "meta_asset_type", text="Type:")
