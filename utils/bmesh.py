import bpy, bmesh


class BMeshFromEditMode():
    '''Generate a temporary BMesh. Accepts Objects or Meshes as inputs temp change'''
    def __init__(self, bm_data: bpy.types.Object | bpy.types.Mesh):
        if bpy.context.mode != 'EDIT_MESH':
            raise ValueError("Object not in Edit Mode")
        elif bm_data is None:
            raise ValueError("Object is None")

        if isinstance(bm_data, bpy.types.Object):
            self.bm_data = bm_data.data
        elif isinstance(bm_data, bpy.types.Mesh):
            self.bm_data = bm_data
        else:
            raise ValueError("Object is the incorrect data type")

    def __enter__(self):
        self.bm = bmesh.from_edit_mesh(self.bm_data)
        return self
     
    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        bmesh.update_edit_mesh(self.bm_data)
        #self.bm.free() # Causes crashes? Edit Mode uses the same BMesh regardless, free unnecessary


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
