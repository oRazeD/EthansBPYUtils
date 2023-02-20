import bpy, os, json
from pathlib import Path
from .generic import OpInfo
import bpy.types as types
from collections.abc import Iterable
from typing import Any
import logging
log = logging.getLogger(__name__)


class BPYUTILS_OT_open_folder(OpInfo, types.Operator):
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


def save_attributes_to_dict(attributes_to_save: Any | Iterable[Any]) -> dict:
    """Save all attributes of any given bpy.types

    Parameters
    ----------
    attributes_to_save : Any | Iterable[Any]
        The attributes you want to look through and save
    """
    if not isinstance(attributes_to_save, Iterable):
        attributes_to_save = [attributes_to_save]

    saved_attributes = {}
    for data in attributes_to_save:
        saved_attributes[data] = {attr: getattr(data, attr) for attr in dir(data)}

    return saved_attributes


def load_attributes_from_dict(attributes_to_load: dict=None) -> None:
    """Load all attributes from a dict object or file

    Parameters
    ----------
    attributes_to_load : dict
        Dict object to load the attributes from. If left empty will attempt to look for a temp json
    """
    for key, values in attributes_to_load.items():
        for name, value in values.items():
            try:
                setattr(key, name, value)
            except AttributeError: # read_only attr
                pass
            except TypeError: # This seems to only happen with specific bad contexts such as "dynamic" props
                log.debug(f'{name}: {value} had a TypeError.')


# Reminder that the tempfile module exists for temporary directories with a context manager
#
# with tempfile.TemporaryDirectory() as temp_dir:
def generate_temp_json(dict_input: dict, temp_name: str='temp', dir_override: str=None) -> None:
    """Generate a temporary json file at your add-ons installed path

    Parameters
    ----------
    dict_input : dict
        Input dictionary that will be serialized and saved to the temp file
    temp_name : str, optional
        Temporary file & directory name, by default 'temp'
    dir_override : str, optional
        Provide an override directory instead of using the add-on dir, by default None
    """
    addon_path = Path(__file__).parent[0] if dir_override is None else dir_override

    temps_path = Path(addon_path, temp_name)
    temps_path.mkdir(exist_ok=True)
    
    json_path = Path(temps_path, f"{temp_name}.json")

    converted_json = json.dumps(dict_input, indent=2)
    with open(json_path, "w") as outfile:
        outfile.write(converted_json)

    return json_path


def load_temp_json(temp_name: str='temp', dir_override: str=None, remove_file: bool=False) -> dict:
    """Load a JSON file (from a temp folder). This function is only meant to be used for and after using generate_temp_json()

    Parameters
    ----------
    temp_name : str, optional
        Temporary file & directory name, by default 'temp'
    dir_override : str, optional
        Provide an override directory instead of using the add-on dir, by default None
    remove_file : bool, optional
        Whethor or not to cleanup the file after accessing and assigning it to a variable, by default False
    """
    addon_path = Path(__file__).parent[0] if dir_override is None else dir_override

    temps_path = Path(addon_path, temp_name)
    json_path = Path(temps_path, f"{temp_name}.json")

    json_as_dict = json.load(json_path)

    if remove_file:
        pass

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
