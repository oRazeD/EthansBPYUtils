import bpy, bmesh

class BMeshFromEditMode():
    '''Generate a temporary BMesh. Accepts Objects or Meshes as inputs'''
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