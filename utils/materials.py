import bpy
import bpy.types as types
from collections.abc import Iterable, Generator
from generic import filter_func_if_iterable


def get_shader_nodes_by_type(mats: types.Material | Iterable[types.Material], node_type: str, name_override: str='') -> Generator[bpy.types.Node]:
    """Get all shader nodes of a particular type(s)"""
    def find_node(mat: types.Material) -> None:
        for node in mat.node_tree.nodes:
            if node.type == node_type or name_override != '' and node.name.startswith(name_override):
                yield node

    # TODO figure out how to use filter_func_if_iterable with functions that have return values 
    if isinstance(mats, Iterable):
        for mat in mats:
            yield from find_node(mat)
    else:
        yield from find_node(mats)


def apply_mat_to_obs(obs: types.Object | Iterable[types.Object], mat: types.Material, apply_only_empty: bool=False) -> None:
    """Create & apply a material to objects, optionally only to empty material slots

    Parameters
    ----------
    obs : bpy.types.Object | Iterable[bpy.types.Object]
    mat : bpy.types.Material
    apply_empty : bool
        Apply the given material only to objects with no materials and empty material slots
    """
    def apply_mat(ob):
        for slot in ob.material_slots:
            if apply_only_empty and slot.name == '' or not apply_only_empty:
                slot.material = mat

        if not ob.active_material:
            ob.active_material = mat

    filter_func_if_iterable(apply_mat, obs)


def generate_node_links(mat: types.Material, input_node: types.ShaderNode, output_node: types.ShaderNode, links_to_create: dict) -> None:
    """Generate links between 2 shader nodes

    Parameters
    ----------
    mat : bpy.types.Material
    input_node : bpy.types.ShaderNode
    output_node : bpy.types.ShaderNode
    links_to_create : dict
    """
    for output_name, input_name in links_to_create.items():
        mat.node_tree.links.new(
            input_node.inputs[input_name],
            output_node.outputs[output_name]
        )


def link_ng_to_material(node_group, mat, location, hide) -> types.NodeGroup:
    ng = mat.node_tree.nodes.new('ShaderNodeGroup')
    ng.node_tree = node_group
    ng.name = node_group.name
    ng.location = (location.location[0], location.location[1] - 150)
    ng.hide = hide
    return ng


# TODO every function below needs a modularity pass
def inject_ng_into_mat_outputs(obs: types.Object | Iterable[types.Object], node_group: types.NodeGroup) -> None:
    """Add corresponding node groups to all material slots

    Parameters
    ----------
    ob : bpy.types.Object
    node_group : bpy.types.NodeGroup

    Notes
    -----
    - This function will override the use_nodes property on all materials
    """
    
    def inject_ng(ob):
        for slot in ob.material_slots:
            output_nodes = get_shader_nodes_by_type(slot, 'OUTPUT_MATERIAL')
            if not len(output_nodes): # Add output if none exist
                output_nodes = [slot.node_tree.nodes.new('ShaderNodeOutputMaterial')]

            for output_node in output_nodes:
                ng = link_ng_to_material(node_group, slot, output_node.location, True)

                for node_input in output_node.inputs:
                    for link in node_input.links:
                        original_node = slot.node_tree.nodes.get(link.from_node.name)

                        generate_node_links(
                            slot,
                            ng,
                            original_node,
                            {'Surface': 'Saved Surface', 'Volume': 'Saved Volume', 'Displacement': 'Saved Displace'}
                        )

                for input_name in {'Volume', 'Displacement'}: # TODO this is not modular code
                    for link in output_node.inputs[input_name].links:
                        slot.node_tree.links.remove(link)

                slot.node_tree.links.new(output_node.inputs["Surface"], ng.outputs["Output"])

    filter_func_if_iterable(inject_ng, obs)


def cleanup_ng_from_mat(node_name: str) -> None:
    '''Remove node groups & return original links if they exist'''
    for mat in bpy.data.materials:
        nodes = get_shader_nodes_by_type(mat, 'GROUP', node_name)
        for input_node in nodes:
            # TODO currently only works if the injected node has a single output
            output_node = input_node.outputs[0].links[0].to_node 

            if output_node is None:
                mat.node_tree.nodes.remove(input_node)
                continue

            for input in input_node.inputs:
                for link in input.links:
                    original_node = mat.node_tree.nodes.get(link.from_node.name)

                    generate_node_links(
                        mat,
                        input_node,
                        original_node,
                        {'Saved Surface': 'Surface', 'Saved Volume': 'Volume', 'Saved Displacement': 'Displacement'}
                    )

            mat.node_tree.nodes.remove(input_node)


#def bsdf_link_factory(input_name: list, node_group: types.ShaderNodeGroup, original_node_input: types.NodeSocket, mat_slot: types.Material) -> bool:
#    '''Add node group to all materials, save original links & link the node group to material output'''
#    node_found = False
#    for link in original_node_input.links:
#        node_found = True
#
#        mat_slot.node_tree.links.new(node_group.inputs[input_name], link.from_node.outputs[link.from_socket.name])
#        break
#    else:
#        try:
#            node_group.inputs[input_name].default_value = original_node_input.default_value
#        except TypeError:
#            if isinstance(original_node_input.default_value, float):
#                node_group.inputs[input_name].default_value = int(original_node_input.default_value)
#            else:
#                node_group.inputs[input_name].default_value = float(original_node_input.default_value)
#
#    return node_found


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
