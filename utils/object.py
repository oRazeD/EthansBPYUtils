import bpy
from collections.abc import Iterable


def filter_objects(obs: Iterable[bpy.types.Object], filter_instanced: bool=True, filter_linked: bool=True) -> list[bpy.types.Object]:
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
    return list(obs)


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
