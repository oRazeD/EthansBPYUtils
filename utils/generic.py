import bpy
from collections.abc import Iterable


def display_error_message(message='', title='Screenshot Saver Warning', icon='ERROR') -> None:
    '''Display a custom error message in situations where a regular error message cannot be sent'''
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class OpInfo: # Mix-in class
    bl_options = {'REGISTER', 'UNDO'}
    bl_label = ""


class InContextMode():
    """Temporarily change context modes to perform contextual operations
    
    Parameters
    ----------
    context_mode : str, optional
        by default "EDIT"
    exit_mode : str, optional
        by default None

    Raises
    ------
    ValueError
        If given context_mode is not in VALID_MODES {'EDIT', 'EDIT_MESH', 'OBJECT', 'POSE', 'SCULPT'}
    """

    VALID_MODES = {'EDIT', 'EDIT_MESH', 'OBJECT', 'POSE', 'SCULPT'}

    def __init__(self, context_mode: str="EDIT", exit_mode: str=None):
        if not context_mode in self.VALID_MODES:
            raise ValueError(f"{context_mode} not in {self.VALID_MODES}")
        self.context_mode = context_mode

        if exit_mode:
            if not exit_mode in self.VALID_MODES:
                raise ValueError(f"{exit_mode} not in {self.VALID_MODES}")
            self.saved_context_mode = "EDIT" if exit_mode == "EDIT_MESH" else exit_mode
        else:
            self.saved_context_mode = "EDIT" if bpy.context.mode == "EDIT_MESH" else bpy.context.mode

    def __enter__(self):
        bpy.ops.object.mode_set(mode=self.context_mode)
        return self
     
    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        bpy.ops.object.mode_set(mode=self.saved_context_mode)


def save_attributes(attributes_to_save: Iterable[bpy.types.AttributeGroup]) -> dict:
    """Save all attributes of any given attribute

    Parameters
    ----------
    attributes_to_save : Iterable[bpy.types.Object]
        The attributes you want to look through and save

    Returns
    -------
    dict
        _description_
    """
    '''Recursive method of saving all attributes'''
    # This method saves a lot of unnecessary data, but is very
    # modular compared to saving every attribute individually
    saved_attributes = {}

    for data in attributes_to_save:
        for attr in dir(data):
            if data not in saved_attributes:
                saved_attributes[data] = {}

            saved_attributes[data][attr] = getattr(data, attr)

    return saved_attributes


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
