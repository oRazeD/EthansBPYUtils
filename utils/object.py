import bpy
from collections.abc import Iterable, Iterator


def filter_objects(obs: Iterable[bpy.types.Object], filter_instanced: bool=True, filter_linked: bool=True) -> set[bpy.types.Object]:
    """Removes instanced and duplicate references from input list

    Parameters
    ----------
    obs : Iterable[bpy.types.Object]
    filter_instanced : bool, optional
        Filter by instanced objects, by default True
    filter_linked : bool, optional
        Filter by linked objects, by default True

    Returns
    -------
    list[bpy.types.Object]
    """
    if filter_instanced:
        obs = {ob for ob in obs if not ob.is_instancer}
    if filter_linked:
        obs = {ob.data: ob for ob in obs}.values()
    return obs


def get_hierarchy(obs_input: Iterable[bpy.types.Object], get_recursive: bool=True, set_select: bool=False, _return_original: bool=True) -> Iterator[bpy.types.Object]:
    """Get hierarchy of the input objects

    Parameters
    ----------
    obs_input : Iterable[bpy.types.Object]
    get_recursive : bool, optional
        by default True
    set_select : bool, optional
        by default False
    return_original : bool, optional
        by default True

    Notes
    ----------
    - When using set_select this function does not compensate for objects that aren't selectable, but will still be available in the generator
    - This function WILL return repeat elements if potential children objects are used as an input
    """
    def get_object(ob):
        if set_select:
            ob.select_set(True)

        yield ob
        for child in ob.children:
            if not get_recursive and child.parent not in obs_input:
                return

            yield from get_object(child)

    for ob in obs_input:
        yield from get_object(ob)


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
