import bpy
from typing import Any
from collections.abc import Iterable, Callable


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


def operator_report(self: bpy.types.Operator, message: str, error_type: str='INFO', return_type: str=None) -> None | set:
    """A more useful self.report() function, including more functionality and better type hinting. Used inside operators.

    Parameters
    ----------
    self : bpy.types.Operator
    message : str
        Report message to print
    error_type : str, optional
        Error Type in ('INFO', 'WARNING', 'ERROR',  'OPERATOR', 'PROPERTY', 'ERROR_INVALID_INPUT', 'ERROR_INVALID_CONTEXT', "ERROR_OUT_OF_MEMORY"), by default 'INFO'
    return_type : str, optional
        Type to return in ('FINISHED', 'CANCELLED', 'RUNNING_MODAL', 'PASS_THROUGH', 'INTERFACE'), by default None
    """
    self.report({error_type}, message)

    if return_type:
        return {return_type}


def filter_if_iterable(potential_iter: Any | Iterable[Any]) -> list:
    """Filter a potential iterable

    Parameters
    ----------
    potential_iter : Any | Iterable[Any]
        The potentially iterable object
    """
    return [potential_iter] if not isinstance(potential_iter, Iterable) else potential_iter


def filter_func_if_iterable(func: Callable, potential_iter: Any | Iterable[Any]) -> function(Iterable):
    """Filter a potential iterable and then call a given function

    Parameters
    ----------
    func : Callable
        The input function to call
    potential_iter : Any | Iterable[Any]
        The potentially iterable object

    Notes
    -----
    - This will currently ONLY work on functions that return None
    """
    if isinstance(potential_iter, Iterable):
        for iterable in potential_iter:
            func(iterable)
    else:
        func(potential_iter)


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
