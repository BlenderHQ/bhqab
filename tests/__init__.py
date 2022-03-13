import bpy

from . import _test_preferences
from . import _test_operators
from . import _test_ui


_classes = (
    _test_preferences.BHQABT_Preferences,

    _test_operators.BHQABT_OT_Progress,

    _test_ui.BHQABT_PT_unit_tests,  # Unit tests.
    _test_ui.BHQABT_PT_func_tests,  # Functional tests.
    _test_ui.BHQABT_PT_WrappedText,
    _test_ui.BHQABT_PT_Progress,
    _test_ui.BHQABT_PT_developer_extras,
    _test_ui.BHQABT_PT_developer_extras_sub,
) + _test_operators.unit_test_ops

register, unregister = bpy.utils.register_classes_factory(_classes)
