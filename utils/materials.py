import bpy

#def create_apply_ng_mat(ob: type.Object) -> None:
#    '''Create & apply a material to objects without active materials'''
#    mat_name = 'GD_Material (do not touch contents)'
#
#    # Reuse GrabDoc created material if it already exists
#    if mat_name in bpy.data.materials:
#        mat = bpy.data.materials[mat_name]
#    else:
#        mat = bpy.data.materials.new(name = mat_name)
#
#        mat.use_nodes = True
#
#    # Apply the material to the appropriate slot
#    #
#    # Search through all material slots, if any slots have no name that means they have no material
#    # & therefore should have one added. While this does run every time this is called it should
#    # only really need to be used once per in add-on use.
#    # 
#    # We do not want to remove empty material slots as they can be used for masking off materials.
#    for slot in ob.material_slots:
#        if slot.name == '':
#            ob.material_slots[slot.name].material = mat
#    else:
#        if not ob.active_material or ob.active_material.name == '':
#            ob.active_material = mat
#
#
#def bsdf_link_factory(input_name: list, node_group: type.ShaderNodeGroup, original_node_input: type.NodeSocket, mat_slot: type.Material) -> bool:
#    '''Add node group to all materials, save original links & link the node group to material output'''
#    node_found = False
#
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
#
#
#def inject_ng_into_materials(self, context, setup_type: str) -> None:
#    '''Add corresponding node groups to all materials/objects'''
#    for ob in context.view_layer.objects:
#        if ob.name in self.rendered_obs and ob.name != "GD_Orient Guide":
#            # If no material slots found or empty mat slots found, assign a material to it
#            if not len(ob.material_slots) or '' in ob.material_slots:
#                create_apply_ng_mat(ob)
#
#            # Cycle through all material slots
#            for slot in ob.material_slots:
#                mat_slot = bpy.data.materials.get(slot.name)
#
#                output_node = None
#                original_node = None
#
#                if not mat_slot.use_nodes:
#                    mat_slot.use_nodes = True
#
#                if not setup_type in mat_slot.node_tree.nodes:
#                    # Get materials Output Material node
#                    for mat_node in mat_slot.node_tree.nodes:
#                        if mat_node.type == 'OUTPUT_MATERIAL' and mat_node.is_active_output:
#                            output_node = mat_slot.node_tree.nodes.get(mat_node.name)
#                            break
#
#                    if not output_node:
#                        output_node = mat_slot.node_tree.nodes.new('ShaderNodeOutputMaterial')
#
#                    # Add node group to material
#                    GD_node_group = mat_slot.node_tree.nodes.new('ShaderNodeGroup')
#                    GD_node_group.node_tree = bpy.data.node_groups[setup_type]
#                    GD_node_group.location = (output_node.location[0], output_node.location[1] - 140)
#                    GD_node_group.name = bpy.data.node_groups[setup_type].name
#                    GD_node_group.hide = True
#
#                    # Handle node linking
#                    for node_input in output_node.inputs:
#                        for link in node_input.links:
#                            original_node = mat_slot.node_tree.nodes.get(link.from_node.name)
#
#                            # Link original connections to the Node Group
#                            if node_input.name == 'Surface':
#                                mat_slot.node_tree.links.new(GD_node_group.inputs["Saved Surface"], original_node.outputs[link.from_socket.name])
#                            elif node_input.name == 'Volume':
#                                mat_slot.node_tree.links.new(GD_node_group.inputs["Saved Volume"], original_node.outputs[link.from_socket.name])
#                            elif node_input.name == 'Displacement':
#                                mat_slot.node_tree.links.new(GD_node_group.inputs["Saved Displacement"], original_node.outputs[link.from_socket.name])
#
#                            # Links for maps that feed information from the Principled BSDF
#                            if setup_type in {'GD_Albedo', 'GD_Roughness', 'GD_Metalness', 'GD_Normal'} and original_node.type == 'BSDF_PRINCIPLED':
#                                node_found = False
#
#                                for original_node_input in original_node.inputs:
#                                    if setup_type == 'GD_Albedo' and original_node_input.name == 'Base Color':
#                                        node_found = bsdf_link_factory(
#                                            input_name='Color Input',
#                                            node_group=GD_node_group,
#                                            original_node_input=original_node_input,
#                                            mat_slot=mat_slot
#                                        )
#
#                                    elif setup_type == 'GD_Roughness' and original_node_input.name == 'Roughness':
#                                        node_found = bsdf_link_factory(
#                                            input_name='Roughness Input',
#                                            node_group=GD_node_group,
#                                            original_node_input=original_node_input,
#                                            mat_slot=mat_slot
#                                        )
#
#                                    elif setup_type == 'GD_Metalness' and original_node_input.name == 'Metallic':
#                                        node_found = bsdf_link_factory(
#                                            input_name='Metalness Input',
#                                            node_group=GD_node_group,
#                                            original_node_input=original_node_input,
#                                            mat_slot=mat_slot
#                                        )
#
#                                    elif setup_type == 'GD_Normal' and original_node_input.name in {'Normal', 'Alpha'}:
#                                        node_found = bsdf_link_factory(
#                                            input_name=original_node_input.name,
#                                            node_group=GD_node_group,
#                                            original_node_input=original_node_input,
#                                            mat_slot=mat_slot
#                                        )
#
#                                        if ( # Does not work if Map Preview Mode is entered and *then* Texture Normals are enabled
#                                            original_node_input.name == 'Alpha'
#                                            and context.scene.grabDoc.useTextureNormals
#                                            and mat_slot.blend_method == 'OPAQUE'
#                                            and len(original_node_input.links)
#                                        ):
#                                            mat_slot.blend_method = 'CLIP'
#
#                                    elif node_found:
#                                        break
#
#                                if not node_found and setup_type != 'GD_Normal':
#                                    self.report({'WARNING'}, "Material slots found without links & will be rendered using the sockets default value.")
#
#                    # Remove existing links on the output node
#                    if len(output_node.inputs['Volume'].links):
#                        for link in output_node.inputs['Volume'].links:
#                            mat_slot.node_tree.links.remove(link)
#
#                    if len(output_node.inputs['Displacement'].links):
#                        for link in output_node.inputs['Displacement'].links:
#                            mat_slot.node_tree.links.remove(link)
#
#                    # Link Node Group to the output
#                    mat_slot.node_tree.links.new(output_node.inputs["Surface"], GD_node_group.outputs["Output"])
#
#
#def cleanup_ng_from_mat(setup_type: str) -> None:
#    '''Remove node group & return original links if they exist'''
#    for mat in bpy.data.materials:
#        if not mat.use_nodes:
#            mat.use_nodes = True
#        
#        # If there is a GrabDoc created material, remove it
#        if mat.name == 'GD_Material (do not touch contents)':
#            bpy.data.materials.remove(mat)
#
#        # If a material has a GrabDoc created Node Group, remove it
#        elif setup_type in mat.node_tree.nodes:
#            for mat_node in mat.node_tree.nodes:
#                if mat_node.type == 'OUTPUT_MATERIAL' and mat_node.is_active_output:
#                    output_node = mat.node_tree.nodes.get(mat_node.name)
#                    break
#
#            GD_node_group = mat.node_tree.nodes.get(setup_type)
#
#            for input in GD_node_group.inputs:
#                for link in input.links:
#                    original_node_connection = mat.node_tree.nodes.get(link.from_node.name)
#                    original_node_socket = link.from_socket.name
#
#                    if input.name == 'Saved Surface':
#                        mat.node_tree.links.new(output_node.inputs["Surface"], original_node_connection.outputs[original_node_socket])
#                    elif input.name == 'Saved Volume':
#                        mat.node_tree.links.new(output_node.inputs["Volume"], original_node_connection.outputs[original_node_socket])
#                    elif input.name == 'Saved Displacement':
#                        mat.node_tree.links.new(output_node.inputs["Displacement"], original_node_connection.outputs[original_node_socket])
#            
#            mat.node_tree.nodes.remove(GD_node_group)


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
