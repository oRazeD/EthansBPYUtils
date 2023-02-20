# NOTE this is just a few code snippets and will require some babying to integrate into your own files


# Imports

import bpy
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel
from bpy.types import Panel, Menu


# Setup

class GRABDOC_MT_presets(Menu):
    bl_label = ""
    preset_subdir = "grabDoc"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class GRABDOC_PT_presets(PresetPanel, Panel):
    bl_label = 'GrabDoc Presets'
    preset_subdir = 'grab_doc'
    preset_operator = 'script.execute_preset'
    preset_add_operator = 'grab_doc.preset_add'


class GRABDOC_OT_add_preset(AddPresetBase, bpy.types.Operator):
    bl_idname = "grab_doc.preset_add"
    bl_label = "Add a new preset"
    preset_menu = "GRABDOC_MT_presets"

    # Variable used for all preset values
    preset_defines = ["grabDoc=bpy.context.scene.grabDoc"]

    # Properties to store in the preset
    preset_values = [
        "grabDoc.item",
    ]

    # Where to store the preset
    preset_subdir = "grab_doc"


# UI

GRABDOC_PT_presets.draw_panel_header(self.layout)



# Registration

def register():
    bpy.utils.register_class(VGROUPSPLUS_property_group)

    bpy.types.Scene.vgroups_plus = PointerProperty(type = VGROUPSPLUS_property_group)

    bpy.utils.register_class(VGROUPSPLUS_collection_property)

    bpy.types.Scene.vgroups_coll_prop = CollectionProperty(type = VGROUPSPLUS_collection_property)
    bpy.types.Scene.custom_index = IntProperty()

def unregister():
    bpy.utils.unregister_class(VGROUPSPLUS_property_group)

    del bpy.types.Scene.vgroups_plus

    bpy.utils.unregister_class(VGROUPSPLUS_collection_property)

    del bpy.types.Scene.vgroups_coll_prop
    del bpy.types.Scene.custom_index