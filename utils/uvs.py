import bpy
from bmesh import BMeshFromEditMode
from collections.abc import Iterable


def has_uv_data(ob: bpy.types.Object) -> bool:
    """Verify the given object has uv data"""
    if hasattr(ob.data, 'uv_layers'):
        return True
    return False


def copy_uv_layers(ob:bpy.types.Object, copy_from_idx:int, copy_to_idx:int) -> None:
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


def generate_uv_layers(obs: bpy.types.Object | Iterable[bpy.types.Object], **uv_channels: str | int) -> None:
    """Generate UV layer(s). If UV layers already exist maintain given naming conventions

    Parameters
    ----------
    obs: bpy.types.Object | Iterable[bpy.types.Object]
    **uv_channels : str | int
    """
    def setup_uv_channels(ob: bpy.types.Object):
        uv_layers = ob.data.uv_layers
        for uv_name, idx in uv_channels.items():
            try:
                uv_channel = uv_layers[idx]
                uv_channel.name = uv_name
            except IndexError:
                uv_layers.new(name=uv_name, do_init=False)

    if isinstance(obs, Iterable):
        for ob in obs:
            setup_uv_channels(ob)
    else:
        setup_uv_channels(obs)

    #set_uv_layer(
    #    ob=ob,
    #    map1=0,
    #    texel_density=1,
    #    udim_mask=2,
    #    splat=3
    #)

def set_active_uv_layer(obs: bpy.types.Object | Iterable[bpy.types.Object], idx: int=0, set_render: bool=False) -> None:
    """Set active UV Layer on given input

    Parameters
    ----------
    obs : bpy.types.Object | Iterable[bpy.types.Object]
    idx : int, optional
        Index of the UV Layer to set as active, by default 0
    set_render : bool, optional
        Set active_render attribute of the given index, by default False
    """
    def set_active_idx(ob: bpy.types.Object):
        ob.data.uv_layers.active_index = idx
        ob.data.uv_layers[idx].active_render = set_render

    if isinstance(obs, Iterable):
        for ob in obs:
            set_active_idx(ob)
    else:
        set_active_idx(obs)


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
