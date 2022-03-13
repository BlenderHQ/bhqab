from email.policy import default
import random
import string

import bpy

from .. import ui
from .. import extend_bpy_types

import unittest


class BHQABT_OT_Progress(bpy.types.Operator):
    bl_idname = "bhqabt.progress"
    bl_label = "Progress"
    bl_options = {'INTERNAL'}

    cancellable: bpy.props.BoolProperty()

    def execute(self, context):
        self._progress = ui.progress.invoke()
        self._progress.cancellable = self.cancellable
        self._progress.label = f"{self._progress.as_pointer()}"
        self._progress.icon = 'INFO'
        self._progress.num_steps = 50

        wm = context.window_manager
        wm.modal_handler_add(self)
        self._timer = wm.event_timer_add(time_step=0.1, window=context.window)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        ui.progress.complete(self._progress)

    def modal(self, context, event):
        if event.type == 'TIMER':
            self._progress.step += 1

        if self._progress.value >= 100.0 or (not self._progress.valid) or event.type == 'ESC':
            self.cancel(context)
            return {'FINISHED'}

        return {'PASS_THROUGH'}


class TEST_unique_name(unittest.TestCase):
    func = extend_bpy_types.unique_name

    test_range = 1000
    str_list = [
        "".join(random.sample(string.ascii_letters, k=extend_bpy_types._UNIQUE_NAME_K))
        for _ in range(test_range)
    ]

    def test_simple_pure_python(self):
        self.assertTrue(not extend_bpy_types.unique_name(collection=self.str_list) in self.str_list)

    def test_window_manager_attr(self):
        # Set a lot of attributes with random name
        attribute_names_order = []

        for i in range(self.test_range):
            un = extend_bpy_types.unique_name(
                collection=bpy.types.WindowManager,
                prefix="bhqabt_",
                suffix="_test",
            )

            attribute_names_order.append(un)

            setattr(bpy.types.WindowManager, un, bpy.props.IntProperty(default=i))

        # Test if attribute values are order is the same as was set previously.
        for i in range(self.test_range):
            attr_name = attribute_names_order[i]

            val = getattr(bpy.context.window_manager, attr_name, -1)
            self.assertEqual(val, i,
                             msg=f"Failed for attribute {i} \"attr_name\": value {val} != {i}"
                             )

    def test_bpy_data_meshes(self):
        added_meshes = []

        for _ in range(self.test_range):
            un = extend_bpy_types.unique_name(
                collection=bpy.data.meshes,
                prefix="bhqabt_",
                suffix="_test",
            )
            mesh = bpy.data.meshes.new(name=un)
            added_meshes.append(mesh)

            self.assertEqual(mesh.name_full, un)

        for mesh in added_meshes:
            bpy.data.meshes.remove(mesh)


# ____________________________________________________________________________ #
# Generate unit test operators w.r.t test cases.

def ot_unit_test_execute(test_case_cls: unittest.TestCase):
    def wrapper(self, _context):
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(test_case_cls))
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        if result.failures or result.errors:
            self.report(
                type={'WARNING'},
                message=f"Finished with {len(result.failures)} failures "
                f"and {len(result.errors)} errors."
            )
        else:
            self.report(type={'INFO'}, message="Succeeded")

        return {'FINISHED'}
    return wrapper


unit_test_ops = tuple(
    (
        type(
            f"BHQABT_OT_test_{test_case_cls.func.__qualname__}",
            (bpy.types.Operator, ),
            dict(
                bl_idname=f"bhqabt.test_{test_case_cls.func.__qualname__}",
                bl_label=f"{test_case_cls.func.__module__}.{test_case_cls.func.__qualname__}",
                execute=ot_unit_test_execute(test_case_cls)
            )
        )
        for test_case_cls in (
            # NOTE: Add new test cases here.
            TEST_unique_name,
        )
    )
)
