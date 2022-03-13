import bpy

from . import _test_preferences
from . import _test_operators
from . import _test_ui

from .. import registration


_classes = (
    _test_preferences.BHQABT_Preferences,

    _test_operators.BHQABT_OT_Progress,

    _test_ui.BHQABT_PT_WrappedText,
    _test_ui.BHQABT_PT_Progress,
    _test_ui.BHQABT_PT_developer_extras,
    _test_ui.BHQABT_PT_developer_extras_sub,
)


@registration.register(pref_cls=_test_preferences.BHQABT_Preferences)
def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


@registration.unregister(pref_cls=_test_preferences.BHQABT_Preferences)
def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
