import os

import bpy

from .. import ui

from . import _test_preferences
from . import _test_operators
from . import _test_ui


_classes = (
    _test_preferences.BHQABT_Preferences,

    _test_operators.BHQABT_OT_unit_tests_all,
    _test_operators.BHQABT_OT_Progress,

    _test_ui.BHQABT_PT_unit_tests,  # Unit tests.
    _test_ui.BHQABT_PT_func_tests,  # Functional tests.
    _test_ui.BHQABT_PT_WrappedText,
    _test_ui.BHQABT_PT_Progress,
    _test_ui.BHQABT_PT_developer_extras,
    _test_ui.BHQABT_PT_developer_extras_sub,
) + _test_operators.unit_test_ops

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


def register():
    ui.icon.from_atlas(
        atlas_fp=os.path.join(os.path.dirname(__file__), "icons", "qr.png"),
        tile_size=256,
        icon_names=(
            "bhqab_github",
            "bhq_github",
            "bhq_patreon",
        ),
        group_name="qr",
    )
    
    _cls_register()


def unregister():
    _cls_unregister()
