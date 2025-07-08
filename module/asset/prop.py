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
from bpy.app.handlers import persistent


@persistent
def asset_locked(scene):
    props = bpy.context.scene.APMetadataProperties
    if props.meta_asset_status == "published":
        try:
            bpy.ops.object.ap_protected_publish("INVOKE_DEFAULT")
        except Exception as e:
            print(f"Error: {e}")
