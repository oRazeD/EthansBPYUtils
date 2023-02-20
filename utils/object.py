import bpy
from dataclasses import dataclass
from enum import Enum, auto
from collections.abc import Iterable, Generator
from mathutils import Vector
import bpy.types as types


def filter_objects(obs: Iterable[types.Object], filter_instanced: bool=True, filter_linked: bool=True) -> set[types.Object]:
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
    # TODO add more filter types
    if filter_instanced:
        obs = (ob for ob in obs if not ob.is_instancer)
    if filter_linked:
        obs = {ob.data: ob for ob in obs}.values() # TODO Turn this into a generator!
    return obs


# TODO return_original arg
def get_hierarchy(obs_input: Iterable[types.Object], get_recursive: bool=True, set_select: bool=False, _return_original: bool=True) -> Generator[types.Object]:
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
    - When using set_select this function does not compensate for objects that aren't selectable, but will still return them for further use
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


@dataclass
class PosType(Enum):
    MAX_POS = auto()
    MIN_POS = auto()

def find_vertex_position(obs_input: Iterable[types.Object], pos_type: PosType=PosType.MAX_POS, axis_idx: int=0) -> float:
    """Find the tallest points in the viewlayer by looping through objects to find the highest vertex on any axis

    Parameters
    ----------
    obs_input : Iterable[bpy.types.Object]
    pos_type : str, optional
        by default 'max'
    """
    vert_pos = 0.0
    for ob in obs_input:
        ob_eval = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh_from_eval = ob_eval.to_mesh()

        axis_vert_coords = [(ob_eval.matrix_world @ v.co)[axis_idx] for v in mesh_from_eval.vertices]
        if not axis_vert_coords:
            continue

        if pos_type == PosType.MAX_POS:
            axis_co = max(axis_vert_coords)
            vert_pos = axis_co if axis_co > vert_pos else vert_pos
        elif pos_type == PosType.MIN_POS:
            axis_co = min(axis_vert_coords)
            vert_pos = axis_co if axis_co < vert_pos else vert_pos

        ob_eval.to_mesh_clear()
    return vert_pos


# TODO just an idea
def ob_in_viewing_spectrum(ob: types.Object, vec_check: Vector) -> bool:
    """Decide whether a given object is within the cameras viewing spectrum

    Parameters
    ----------
    ob : bpy.types.Object
    vec_check : Vector
    """
    vec1 = Vector((ob.dimensions.x * -1.25 + ob.location[0], ob.dimensions.y * -1.25 + ob.location[1], -100))
    vec2 = Vector((ob.dimensions.x * 1.25 + ob.location[0], ob.dimensions.y * 1.25 + ob.location[1], 100))

    for i in range(0, 3):
        if (
            vec_check[i] < vec1[i] and vec_check[i] < vec2[i]
            or vec_check[i] > vec1[i] and vec_check[i] > vec2[i]
        ):
            return False
    return True


def generate_point_cloud_ob(ob_name: str, verts: Iterable[int], edges: Iterable[int], faces: Iterable[int]) -> types.Object:
    """Generate a point cloud mesh object based on given vectors

    Parameters
    ----------
    ob_name : str
        Name of the newly created mesh and object
    verts : Iterable[int]
    edges : Iterable[int]
    faces : Iterable[int]
    """
    new_mesh = bpy.data.meshes.new(ob_name)
    new_ob = bpy.data.objects.new(ob_name, new_mesh)

    # Make a mesh from a list of vertices / edges / faces
    new_mesh.from_pydata(
        vertices=verts,
        edges=edges,
        faces=faces
    )
    new_mesh.update()

    bpy.context.collection.objects.link(new_ob) # TODO Link to active or make override arg

    return new_ob


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
