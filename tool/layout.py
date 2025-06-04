# assetpublisher
# Copyright (C) 2025  Aditia A. Pratama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import bpy


class CustomLayout:
    @classmethod
    def asset_check_row(
        cls,
        layout: bpy.types.UILayout,
        message: str,
        operator: str,
        alert: bool = False,
    ):
        row = layout.row(align=False)
        split = row.split(factor=0.7)
        split.alert = alert
        subsplit = split.split(factor=0.07)
        subsplit.label(text="", icon="DOT")
        subsplit.label(text=message)
        split.operator(operator, text="Fix", icon="SHADERFX")

    @classmethod
    def auto_row(
        cls,
        layout: bpy.types.UILayout,
        panel_width: int = 200,
        width_treshold: int = 280,
        max_column: int = 1,
        align: bool = False,
    ) -> bpy.types.UILayout:
        layout.use_property_split = True
        layout.use_property_decorate = False
        column = 2 if panel_width >= width_treshold else max_column
        return layout.box().grid_flow(
            columns=int(column),
            even_columns=True,
            even_rows=True,
            row_major=True,
            align=align,
        )
