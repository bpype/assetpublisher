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

import bpy

from ...tool import Asset as asset
from ...tool import CustomLayout as custom_layout
from .. import ui


class AP_PT_asset_tools(ui.AP_PT_panel, bpy.types.Panel):
    bl_label = "Asset Fixing"
    bl_parent_id = "AP_PT_metadata_tools"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.APMetadataProperties
        col = layout.column_flow(columns=1)

        col.label(text="Asset Check:", icon="BORDERMOVE")
        panel_width = context.region.width
        box = custom_layout.auto_row(col, panel_width=panel_width, width_treshold=150)
        col = box.column(align=False)
        if len(asset.get_objects_with_subdiv()) > 0:  # and props.meta_asset_type in {"set", "prop"}:
            message = f"Subd in {len(asset.get_objects_with_subdiv())} objects"
            custom_layout.asset_check_row(col, message, "object.ap_use_gn_subdiv", alert=True)
        if not props.meta_asset_type == "set" and not asset.is_lo_ready():
            custom_layout.asset_check_row(col, "LOD has issues", "object.ap_create_lo", alert=True)


def add_gn_modifier(self, context: bpy.types.Context):
    props = context.scene.APMetadataProperties
    if props.meta_asset_type in {"set", "prop"}:
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        box = custom_layout.auto_row(layout, panel_width=200, width_treshold=280, max_column=2, align=False)
        box.label(text="Add Modifier:")
        box.operator("object.ap_set_gn_subdiv", text="GN_SubD", icon="MOD_SUBSURF")


def register():
    bpy.types.DATA_PT_modifiers.prepend(add_gn_modifier)


def unregister():
    bpy.types.DATA_PT_modifiers.remove(add_gn_modifier)
