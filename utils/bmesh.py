import bpy, bmesh


class BMeshFromEditMode():
    '''Generate a temporary BMesh. Accepts Objects or Meshes as inputs temp change'''
    def __init__(self, input_data: bpy.types.Object | bpy.types.Mesh, update_mesh: bool=True):
        if isinstance(input_data, bpy.types.Mesh):
            self.input_data = input_data
        else:
            self.input_data = input_data.data

        self.update_mesh = update_mesh

    def __enter__(self):
        self.bm = bmesh.from_edit_mesh(self.input_data)
        return self
     
    def __exit__(self, _exc_type, _exc_value, _exc_traceback): # NOTE do not use self.bm.free() for BMeshes made in Edit Mode, uses same data regardless
        if self.update_mesh:
            bmesh.update_edit_mesh(self.input_data)


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
