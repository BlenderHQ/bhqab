# This means that this is the root file of the addon module (__init__.py).

bl_info = {
    "name": "Sample Addon",
    # Maximal tested Blender version. Newer versions would not be stop any
    # registration process, because (as a rule), newer versions hold older Python
    # API for backward compatibility.
    "version": (3, 1, 0),
    # Minimal tested (and supported as well) Blender version. Blender Python API
    # before this value do not guaranteed that some functions works as expected,
    # because of found during development process bugs from Blender side, which was
    # fixed in later versions.
    "blender": (2, 83, 0),
    "category": "Render",
    # NOTE: For compatibility reasons both keys should be kept.
    # (see https://developer.blender.org/T85675)
    "wiki_url": "https://...",
    "doc_url": "https://...",
}

import bpy

from . import bhq_addon_base


class SA_SceneProperties(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty()


class SA_ScenePanel(bpy.types.Panel):
    bl_label = "Sample"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.prop(context.scene.my_attr, "my_int")


class SamplePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    @bhq_addon_base.ui.template_addon_versioning("https://...compatibility-link")
    def draw(self, context):
        layout = self.layout
        layout.label(text="Hi!")


_types_register_queue = (
    (bpy.types.Scene, "my_attr", bpy.props.PointerProperty, SA_SceneProperties),
)


@bhq_addon_base.register(pref_cls=SamplePreferences)
def register():
    bhq_addon_base.register_extend_bpy_types(register_queue=_types_register_queue)


@bhq_addon_base.unregister(pref_cls=SamplePreferences)
def unregister():
    bhq_addon_base.unregister_extend_bpy_types(register_queue=_types_register_queue)
