import bpy


def exit_local_view() -> bool | str:
    local_view_exited = False
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D' and area.spaces[0].local_view:
            for region in area.regions:
                if region.type == 'WINDOW':
                    local_view_exited = True
                    report_string = 'Local View exited to render'

                    override = {'area': area, 'region': region}
                    bpy.ops.view3d.localview(override)

    return local_view_exited, report_string


def get_render_sync(set_render_vis: bool=False) -> dict[bpy.types.Object: dict[bool, bool, bool]]:
    """Generate a dictionary of object & collection viewlayer visibility generally for use in OpenGL viewport renders

    Parameters
    ----------
    set_render_vis : bool
        by default False
    """
    def layer_traverse(coll: bpy.types.Collection, layer: bpy.types.LayerCollection) -> bpy.types.LayerCollection:
        '''Traverse all layer collections to find the matching one'''
        if layer.collection == coll:
            yield {'layer_ob': layer, 'layer_hidden': layer.hide_viewport}

        for child in layer.children:
            yield from layer_traverse(coll, child)

    vlayer = bpy.context.view_layer

    ob_hide_states = {ob:{
                'render_hidden': ob.hide_render,
                'viewport_hidden': ob.hide_viewport,
                'layer_hidden': ob.hide_get()
            }
        for ob in vlayer.objects
    }
    coll_hide_states = {coll:{
                'render_hidden': coll.hide_render,
                'viewport_hidden': coll.hide_viewport,
                'layer_ob': next(layer_traverse(coll, vlayer.layer_collection))
            }
        for coll in bpy.data.collections
    }

    return ob_hide_states, coll_hide_states

    # TODO
    #if set_render_vis: 
    #    local_view, report_string = exit_local_view()
#
    #    for ob, vis in ob_hide_states.items():
    #        if vis['render_vis']:
    #            ob.hide_viewport = True
    #        else:
    #            ob.hide_viewport = False
    #            ob.hide_set(False)
#
    #    for coll, vis in coll_hide_states.items():
    #        if vis['render_vis']:
    #            coll.hide_viewport = True
    #        else:
    #            coll.hide_viewport = False
    #            vis['layer']['layer_ob'].hide_viewport = False


class TempAreaType():
    """Temporarily change the active area type"""

    VALID_TYPES = {
        'EMPTY', 'VIEW_3D', 'IMAGE_EDITOR',
        'NODE_EDITOR', 'SEQUENCE_EDITOR',
        'CLIP_EDITOR', 'DOPESHEET_EDITOR',
        'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR',
        'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR',
        'OUTLINER', 'PROPERTIES', 'FILE_BROWSER',
        'SPREADSHEET', 'PREFERENCES'
    }

    def __init__(self, context, new_area_type: str='3D_VIEW', area_override: bpy.types.Area=None):
        if not new_area_type in self.VALID_TYPES:
            raise ValueError(f"{new_area_type} not in {self.VALID_TYPES}")
        
        self.area = context.area if area_override is None else area_override
        self.new_area_type = new_area_type

    def __enter__(self):
        if self.area.type != self.new_area_type:
            self.saved_area_type = self.area.type
            self.area.type = self.new_area_type
        else:
            self.saved_area_type = None
        return self
     
    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        if self.saved_area_type is not None:
            self.area.type = self.saved_area_type


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
