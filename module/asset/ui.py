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


class AP_PT_asset_tools(ui.AP_PT_panel, Panel):
    bl_label = "Asset Fixing"
    bl_parent_id = "AP_PT_metadata_tools"
    # bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.APMetadataProperties
        col = layout.column(align=False)
        box = col.box()
        row = box.row(align=False)
        row.label(text="Force GN Subdiv:")
        row.operator("object.ap_use_gn_subdiv", text="Apply")
        if not props.meta_asset_type == "set":
            box = col.box()
            row = box.row(align=False)
            row.label(text=".lo not set:")
            row.operator("object.ap_create_lo", text="Fix")
