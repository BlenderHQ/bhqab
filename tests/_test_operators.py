import random
import string
import unittest

import bpy

from . import _test_preferences

from .. import registration
from .. import extend_bpy_types
from .. import shaders
from .. import ui


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


# ____________________________________________________________________________ #
# Unit tests.

class TEST_registration_is_debug(unittest.TestCase):
    func = registration.is_debug

    def test(self):
        self.assertEqual(registration.is_debug(), True)


class TEST_registration_current_addon(unittest.TestCase):
    func = registration.current_addon

    def test(self):
        self.assertNotEqual(registration.current_addon(), None)
        self.assertEqual(registration.current_addon().__package__, "bhq_addon_base")


class TEST_registration_addon_bl_info(unittest.TestCase):
    func = registration.addon_bl_info

    def test(self):
        self.assertNotEqual(registration.addon_bl_info(), None)
        self.assertTrue(isinstance(registration.addon_bl_info(), dict))


class TEST_registration_addon_display_name(unittest.TestCase):
    func = registration.addon_display_name

    def test(self):
        self.assertNotEqual(registration.addon_display_name(), None)
        self.assertEqual(registration.addon_display_name(), "BlenderHQ Addon Base Test")


class TEST_registration_addon_doc_url(unittest.TestCase):
    func = registration.addon_doc_url

    def test(self):
        self.assertNotEqual(registration.addon_doc_url(), None)
        self.assertEqual(registration.addon_doc_url(), "https://github.com/BlenderHQ/bhq_addon_base")


class TEST_registration_earliest_tested_version(unittest.TestCase):
    func = registration.earliest_tested_version

    def test(self):
        self.assertNotEqual(registration.earliest_tested_version(), None)
        self.assertEqual(len(registration.earliest_tested_version()), 3)
        self.assertGreaterEqual(registration.earliest_tested_version(), (2, 80, 0))


class TEST_registration_latest_tested_version(unittest.TestCase):
    func = registration.latest_tested_version

    def test(self):
        self.assertNotEqual(registration.latest_tested_version(), None)
        self.assertEqual(len(registration.latest_tested_version()), 3)


class TEST_registration_version_string(unittest.TestCase):
    func = registration.version_string

    def test(self):
        self.assertEqual(registration.version_string(ver=(2, 93, 1)), "2.93.1")
        self.assertEqual(registration.version_string(ver=(0, 1, 0)), "0.1.0")


class TEST_registration_addon_preferences(unittest.TestCase):
    func = registration.addon_preferences

    def test(self):
        self.assertTrue(
            isinstance(registration.addon_preferences(bpy.context),
                       _test_preferences.BHQABT_Preferences)
        )


class _FakePreferencesClear(bpy.types.AddonPreferences):
    bl_idname = "bhqabt_fake_pref"

    def draw(self, _context):
        pass


class TEST_registration_register(unittest.TestCase):
    func = registration.register

    def test_all_ok(self):
        @registration.register(pref_cls=_FakePreferencesClear)
        def fake_register():
            pass

        print('\n')
        fake_register()

    def test_err(self):
        @registration.register(pref_cls=_FakePreferencesClear)
        def fake_register():
            raise AttributeError("Grr")

        print('\n')
        fake_register()

        is_fake_preferences_registered = False
        try:
            bpy.utils.unregister_class(_FakePreferencesClear)
        except RuntimeError:
            is_fake_preferences_registered = True

        self.assertTrue(is_fake_preferences_registered)


class TEST_registration_unregister(unittest.TestCase):
    func = registration.unregister

    def test_all_ok(self):
        @registration.unregister(pref_cls=_FakePreferencesClear)
        def fake_unregister():
            pass

        print('\n')
        fake_unregister()

    def test_err(self):
        @registration.unregister(pref_cls=_FakePreferencesClear)
        def fake_unregister():
            raise AttributeError("Grr")

        print('\n')
        fake_unregister()

        is_fake_preferences_registered = False
        try:
            bpy.utils.unregister_class(_FakePreferencesClear)
        except RuntimeError:
            is_fake_preferences_registered = True

        self.assertTrue(is_fake_preferences_registered)


class _FakeWindowManagerProperties(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty()


class _FakeWindowManagerItem(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty()


_fake_extend_bpy_types_register_queue = (
    (
        bpy.types.WindowManager,
        "bhqabt",
        bpy.props.PointerProperty,
        _FakeWindowManagerProperties
    ),
    (
        bpy.types.WindowManager,
        "bhqabt_collection",
        bpy.props.CollectionProperty,
        _FakeWindowManagerItem
    ),
)


class TEST_registration_register_extend_bpy_types(unittest.TestCase):
    func = registration.register_extend_bpy_types

    def test_all_ok(self):
        registration.register_extend_bpy_types(register_queue=_fake_extend_bpy_types_register_queue)

        wm = bpy.context.window_manager
        self.assertTrue(hasattr(wm, "bhqabt"))
        self.assertTrue(hasattr(wm, "bhqabt_collection"))


class TEST_registration_unregister_extend_bpy_types(unittest.TestCase):
    func = registration.unregister_extend_bpy_types

    def test_all_ok(self):
        registration.unregister_extend_bpy_types(register_queue=_fake_extend_bpy_types_register_queue)

        wm = bpy.context.window_manager
        self.assertFalse(hasattr(wm, "bhqabt"))
        self.assertFalse(hasattr(wm, "bhqabt_collection"))


class TEST_extend_bpy_types_unique_name(unittest.TestCase):
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
        if hasattr(test_case_cls, "func")
        else None
        for test_case_cls in (
            # NOTE: Add new test cases here.
            TEST_registration_is_debug,
            TEST_registration_current_addon,
            TEST_registration_addon_bl_info,
            TEST_registration_addon_display_name,
            TEST_registration_addon_doc_url,
            TEST_registration_earliest_tested_version,
            TEST_registration_latest_tested_version,
            TEST_registration_version_string,
            TEST_registration_addon_preferences,
            TEST_registration_register,
            TEST_registration_unregister,
            TEST_registration_register_extend_bpy_types,
            TEST_registration_unregister_extend_bpy_types,
            None,
            TEST_extend_bpy_types_unique_name,
        )
    )
)
