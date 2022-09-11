from typing import Any
import bpy
from collections.abc import Iterable
import logging
log = logging.getLogger(__name__)


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


def display_error_message(message='', title='Warning', icon='ERROR') -> None:
    '''Display a custom error message in situations where a regular error message cannot be sent'''
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


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


def load_attributes_from_dict(attributes_to_load: dict) -> None:
    """Load all attributes from a dict"""
    for key, values in attributes_to_load.items():
        for name, value in values.items():
            try:
                setattr(key, name, value)
            except AttributeError: # read_only attr
                pass
            except TypeError: # This seems to only happen with specific bad contexts such as "dynamic" props
                log.debug(f'{name}: {value} had a TypeError.')


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
