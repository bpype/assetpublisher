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


class AP_OT_asset_working_file(bpy.types.Operator):
    """Operator to open working file"""

    bl_idname = "object.ap_working_file"
    bl_label = "Open Working File"
    bl_options = {"REGISTER"}

    asset_name: bpy.props.StringProperty(name="Asset Name")

    def execute(self, context: bpy.types.Context):
        self.report({"INFO"}, f"Opening {self.asset_name}")
        return {"FINISHED"}


class OBJECT_OT_ap_protected_publish(bpy.types.Operator):
    """Popup to warn user that publishing is protected"""

    bl_idname = "object.ap_protected_publish"
    bl_label = "Publish Protected"
    bl_options = {"REGISTER"}

    def execute(self, context):
        self.report({"ERROR"}, "Published assets cannot be modified")
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=260)

    def draw(self, context):
        layout = self.layout
        props = context.scene.APMetadataProperties
        layout.alert = False
        messages = [
            "Sorry, this asset has been published",
            # "and cannot be modified.",
            "Please select working file below to continue.",
        ]
        col = layout.column(align=True)
        for i, msg in enumerate(messages):
            col.label(text=msg, icon="ERROR" if i == 0 else "BLANK1")
        col.separator()
        row = col.row(align=False)
        row.label(text="", icon="BLANK1")
        row.operator("script.reload", text=f"{props.meta_asset_name} Rig", icon="ARMATURE_DATA")
        row.operator("script.reload", text=f"{props.meta_asset_name} Shader", icon="MATERIAL")


class AP_OT_set_gn_subdiv(bpy.types.Operator):
    """Operator to set GN_SubD on active object"""

    bl_idname = "object.ap_set_gn_subdiv"
    bl_label = "Set GN Subdiv"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return (obj := context.active_object) and obj.type == "MESH"

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        asset.set_gn_subdiv(obj)
        self.report({"INFO"}, f"Set GN_SubD on {obj.name}")
        return {"FINISHED"}


class AP_OT_use_gn_subdiv(bpy.types.Operator):
    """Operator to set GN_SubD on all objects with subdiv"""

    bl_idname = "object.ap_use_gn_subdiv"
    bl_label = "Use GN Subdiv"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return len(asset.get_objects_with_subdiv()) > 0

    def execute(self, context: bpy.types.Context):
        objs_with_subdiv = asset.get_objects_with_subdiv()
        asset.clean_existing_gn_subdiv()
        for obj in objs_with_subdiv:
            asset.set_gn_subdiv(obj)
        self.report({"INFO"}, f"Fixed {len(objs_with_subdiv)} objects")
        return {"FINISHED"}


class AP_OT_asset_create_lo(bpy.types.Operator):
    """Operator to create .lo asset from .hi object data"""

    bl_idname = "object.ap_create_lo"
    bl_label = "Create .lo Asset"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        asset.create_lo_asset()

        return {"FINISHED"}


registry = [
    OBJECT_OT_ap_protected_publish,
    AP_OT_asset_create_lo,
    AP_OT_use_gn_subdiv,
    AP_OT_set_gn_subdiv,
    AP_OT_asset_working_file,
]
