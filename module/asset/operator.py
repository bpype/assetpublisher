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
from ... import tool as tool


class AP_OT_asset_create_lo(Operator):
    """
    Operator to create .lo asset from .hi object data
    """

    bl_idname = "object.ap_create_lo"
    bl_label = "Create .lo Asset"

    @classmethod
    def poll(cls, context: Context):
        return True

    def execute(self, context: Context):
        tool.Asset.create_lo_asset()

        return {"FINISHED"}


registry = [AP_OT_asset_create_lo]
