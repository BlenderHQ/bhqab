import bpy

from . import _test_preferences
from . import _test_operators

from .. import ui


class View3DPanelBase:
    bl_category = "BlenderHQ Addon Base Test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}


class BHQABT_PT_unit_tests(bpy.types.Panel, View3DPanelBase):
    bl_label = "Unit Tests"

    def draw(self, context):
        layout = self.layout

        for unit_test_ot in _test_operators.unit_test_ops:
            layout.operator(operator=unit_test_ot.bl_idname)


class BHQABT_PT_func_tests(bpy.types.Panel, View3DPanelBase):
    bl_label = "Functional Tests"

    def draw(self, _context):
        pass


class BHQABT_PT_WrappedText(bpy.types.Panel, View3DPanelBase):
    bl_idname = "BHQABT_PT_WrappedText"
    bl_label = "Wrapped Text"
    bl_parent_id = "BHQABT_PT_func_tests"

    def draw(self, context):
        layout = self.layout

        _test_preferences.test_draw_wrapped_text(context, layout)


class BHQABT_PT_Progress(bpy.types.Panel, View3DPanelBase):
    bl_idname = "BHQABT_PT_Progress"
    bl_label = "Progress Bars"
    bl_parent_id = "BHQABT_PT_func_tests"

    def draw(self, _context):
        layout = self.layout
        props = layout.operator(operator=_test_operators.BHQABT_OT_Progress.bl_idname, text="Progress Bar")
        props.cancellable = False
        props = layout.operator(operator=_test_operators.BHQABT_OT_Progress.bl_idname, text="Cancellable Progress Bar")
        props.cancellable = True


class BHQABT_PT_developer_extras(bpy.types.Panel, View3DPanelBase):
    bl_idname = "BHQABT_PT_developer_extras"
    bl_label = "Developer Extras Test"
    bl_parent_id = "BHQABT_PT_func_tests"

    def draw(self, context):
        layout = self.layout
        text = "Given that the Blender preferences include the \"Developer " \
            "Extras\" option, there should be another sub-panel."
        ui.draw_wrapped_text(context, layout, text)
        layout.prop(context.preferences.view, "show_developer_ui")


class BHQABT_PT_developer_extras_sub(bpy.types.Panel, View3DPanelBase):
    bl_idname = "BHQABT_PT_developer_extras_sub"
    bl_label = "Developer Extras Test"
    bl_parent_id = "BHQABT_PT_developer_extras"

    @classmethod
    def poll(cls, context):
        return ui.developer_extras_poll(context)

    def draw(self, context):
        ui.template_developer_extras_warning(context, self.layout)
