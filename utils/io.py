import bpy, os, json
from pathlib import Path
from .generic import OpInfo


class BPYUTILS_OT_open_folder(OpInfo, bpy.types.Operator):
    """Opens up the File Explorer to the designated folder location"""
    bl_idname = "bpy_utils.open_folder"
    bl_label = "Open Folder"

    dir_path: bpy.props.StringProperty()

    def execute(self):
        try:
            bpy.ops.wm.path_open(filepath = bpy.path.abspath(self.dir_path))
        except RuntimeError:
            self.report({'ERROR'}, "No valid directory path set")
        return{'FINISHED'}


def blender_path_exists(filepath: str) -> bool:
    '''Check if blender specific filepath exists'''
    if not os.path.exists(bpy.path.abspath(filepath)):
        return False
    return True


# Reminder that the tempfile module exists for temporary directories with a context manager
#
# with tempfile.TemporaryDirectory() as temp_dir:

def generate_temp_json(dict_input: dict, temp_file_name: str='temp', temp_folder_name: str='temp', dir_override: str=None) -> None:
    """Generate a temporary json file at your add-ons installed path

    Parameters
    ----------
    dict_input : dict
        Input dictionary that will be serialized and saved to the temp file
    temp_file_name : str, optional
        by default 'temp'
    temp_folder_name : str, optional
        by default 'temp'
    dir_override : str, optional
        Provide an override directory instead of using the add-on dir, by default None
    """
    addon_path = Path(__file__).parent[0] if dir_override is None else dir_override

    temps_path = Path(addon_path, temp_folder_name)
    temps_path.mkdir(exist_ok=True)
    
    json_path = Path(temps_path, f"{temp_file_name}.json")

    converted_json = json.dumps(dict_input, indent=2)
    with open(json_path, "w") as outfile:
        outfile.write(converted_json)

    return json_path


def load_temp_json(temp_file_name: str='temp', temp_folder_name: str='temp', dir_override: str=None) -> dict:
    """Load a JSON file (from a temp folder). This function is only meant to be used for and after using generate_temp_json()

    Parameters
    ----------
    temp_file_name : str, optional
        by default 'temp'
    temp_folder_name : str, optional
        by default 'temp'
    dir_override : str, optional
        Provide an override directory instead of using the add-on dir, by default None
    """
    addon_path = Path(__file__).parent[0] if dir_override is None else dir_override

    temps_path = Path(addon_path, temp_folder_name)
    json_path = Path(temps_path, f"{temp_file_name}.json")

    json_as_dict = json.load(json_path)

    return json_as_dict


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
