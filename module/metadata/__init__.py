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

from bpy.app.handlers import load_post
from bpy.props import PointerProperty
from bpy.types import PropertyGroup, Scene

from . import operator, prop, ui

modules = [
    prop,
    operator,
    ui,
]


def register():
    Scene.APMetadataProperties = PointerProperty(type=prop.APMetadataProperties)
    load_post.append(prop.get_asset_name)
    load_post.append(prop.get_asset_status)
    load_post.append(prop.get_asset_task)


def unregister():
    del Scene.APMetadataProperties
