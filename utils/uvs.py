import bpy
from .bmesh import BMeshFromEditMode
from collections.abc import Iterable
from generic import filter_func_if_iterable
import bpy.types as types


def has_uv_data(ob: types.Object) -> bool:
    """Verify the given object has uv data"""
    return True if hasattr(ob.data, 'uv_layers') else False


def remove_all_layers(obs: types.Object | Iterable[types.Object], keep_single: bool=True, keep_idx: int=0) -> None:
    """Remove all UV layers

    Parameters
    ----------
    obs : bpy.types.Object | Iterable[bpy.types.Object]
    keep_single : bool, optional
        Keep a single uv layer or not, by default True
    keep_idx : int, optional
        The index to keep instead of removing, by default 0
    """
    def remove_layers(ob):
        uv_layers = ob.data.uv_layers

        if keep_single:
            uvs_to_remove = [uv_layer for uv_layer in uv_layers if uv_layer != uv_layers[keep_idx]]
            
            while uvs_to_remove:
                uv_layers.remove(uvs_to_remove.pop())
        else:
            while len(uv_layers):
                uv_layers.remove(uv_layers[0])

    filter_func_if_iterable(remove_layers, obs)


def copy_uv_layers(ob:types.Object, copy_from_idx:int, copy_to_idx:int) -> None:
    """Create a BMesh and copy the contents of one UV layer to another

    Parameters
    ----------
    ob : bpy.types.Object
    copy_from_idx : int
        Index to copy the UV Layer from
    copy_to_idx : int
        Index to paste the UV Layer to
    """
    with BMeshFromEditMode(ob) as bmesh:
        layers = bmesh.bm.loops.layers
        layers.uv[copy_to_idx].copy_from(layers.uv[copy_from_idx])


def generate_uv_layers(obs: types.Object | Iterable[types.Object], **uv_channels: str | int) -> None:
    """Generate UV layer(s). If UV layers already exist maintain given naming conventions

    Parameters
    ----------
    obs: bpy.types.Object | Iterable[bpy.types.Object]
    **uv_channels : str | int
    """
    def setup_uv_channels(ob: types.Object):
        uv_layers = ob.data.uv_layers
        for uv_name, idx in uv_channels.items():
            try:
                uv_channel = uv_layers[idx]
                uv_channel.name = uv_name
            except IndexError:
                uv_layers.new(name=uv_name, do_init=False)

    filter_func_if_iterable(setup_uv_channels, obs)

    # TODO figure out more user friendly approach to calling the function
    #set_uv_layer(
    #    ob=ob,
    #    map1=0,
    #    texel_density=1,
    #    udim_mask=2,
    #    splat=3
    #)


def set_active_uv_layer(obs: types.Object | Iterable[types.Object], idx: int=0, set_render: bool=False) -> None:
    """Set active UV Layer on given input

    Parameters
    ----------
    obs : bpy.types.Object | Iterable[bpy.types.Object]
    idx : int, optional
        Index of the UV Layer to set as active, by default 0
    set_render : bool, optional
        Set active_render attribute of the given index, by default False
    """
    def set_active_idx(ob: types.Object):
        ob.data.uv_layers.active_index = idx
        ob.data.uv_layers[idx].active_render = set_render

    filter_func_if_iterable(set_active_idx, obs)


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
