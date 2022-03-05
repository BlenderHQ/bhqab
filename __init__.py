# BlenderHQ addon base module.
# Copyright (C) 2022  Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# <pep8 compliant>


# The module is designed to unify some basic functions that are used in several
# addons. See `./README.md` and `./LICENSE` files for details about possible
# usage and licensing.

# Module metadata.
__version__ = (1, 0)

__author__ = \
    "Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)"
__copyright__ = \
    "Copyright (C) 2022  Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)"
__maintainer__ = \
    "Ivan Perevala (ivpe)"
__credits__ = \
    ["Vlad Kuzmin (ssh4)", ]
__license__ = \
    "GPLv3"

bl_info = {
    "name": "BlenderHQ Addon Base Test",
    # Maximal tested Blender version. Newer versions would not be stop any
    # registration process, because (as a rule), newer versions hold older Python
    # API for backward compatibility.
    "version": (3, 1, 0),
    # Minimal tested (and supported as well) Blender version. Blender Python API
    # before this value do not guaranteed that some functions works as expected,
    # because of found during development process bugs from Blender side, which was
    # fixed in later versions.
    "blender": (2, 83, 0),
    "category": "Development",
    "warning": "This addon is exclusively part of the module testing",
    # NOTE: For compatibility reasons both keys should be kept.
    # (see https://developer.blender.org/T85675)
    "wiki_url": "https://github.com/BlenderHQ/bhq_addon_base",
    "doc_url": "https://github.com/BlenderHQ/bhq_addon_base",
}


import functools
import string
import random
import typing
import os

if "bpy" in locals():
    from importlib import reload

    reload(utils_ui)

    del reload
else:
    _full_registration_done = False

# ____________________________________________________________________________ #
# Log utils.

_DEBUG = False


class _log_meta(type):
    @property
    def TAB(cls):
        return cls._TAB

    @property
    def BLUE(cls):
        return cls._BLUE

    @property
    def CYAN(cls):
        return cls._CYAN

    @property
    def GREEN(cls):
        return cls._GREEN

    @property
    def WARNING(cls):
        return cls._WARNING

    @property
    def FAIL(cls):
        return cls._FAIL

    @property
    def END(cls):
        return cls._END


class log(object, metaclass=_log_meta):
    """
    The module also provides opportunities to simplify the debugging and output
    of more detailed messages to the console. It is clear that from the user
    experience for ordinary users it may not be very necessary (usually they do
    not like consoles), this part is focused more on those who will set up
    addons on many computers, etc.

    There is a class :py:class:`log` for outputting such debug messages.
    In order for it to display the message, you must either manually set the
    variable ``_DEBUG`` to a positive value, or put in the root folder of the
    addon an empty file called ``DEBUG``, ``DEBUG.txt``, ``_DEBUG`` or
    ``_DEBUG.txt``.

    .. Note:: This workaround allows to make the addon maintenance faster because
        the developer should not set variable before each public commit. Obvious
        that possible existing file always should be in ``./.gitignore``, so its
        would not present by default on user installations.

    A class behaves similarly to the ``print`` function in a python except that
    the message will only be entered if debug mode is active. The class contains
    several attributes for displaying colored text in messages, they can be used
    when formatting the line before the call (but in this case, the
    initialization of the class instance).

    Attributes:
        TAB: One level of tabs in the message.
        BLUE: Blue message color.
        CYAN: Cyan message color.
        GREEN: Green message color.
        WARNING: Orange warning message color.
        FAIL: Red fail message color.
        END: End of message color formatting.
    """
    _TAB = ' ' * 2
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _WARNING = '\033[93m'
    _FAIL = '\033[91m'

    _END = '\033[0m'

    # UNDERLINE = '\033[4m'
    # BOLD = '\033[1m'
    # HEADER = '\033[95m'

    def __init__(self, *args, **kwargs) -> None:
        if _DEBUG:
            args += (log.END,)
            print(*args, **kwargs)

# ____________________________________________________________________________ #


_is_bpy_exists = False
try:
    import bpy
    import blf
    import gpu  # Just to validate it exists
    from bl_ui import space_statusbar  # Just to validate it exists
except ImportError:
    pass  # Skip import error for (at least) documentation purposes.
else:
    # 'bpy' may be a fake module.
    if bpy.app.version is not None and blf.MONOCHROME is not None:
        _is_bpy_exists = True


_addon = None
_bl_info = None

if _is_bpy_exists:
    _addon = __import__(__package__.split('.')[0])
    _bl_info = getattr(_addon, "bl_info", None)

    # Basic assertions to validate the addon 'bl_info' data.
    assert(_bl_info is not None)

    assert("name" in _bl_info)
    assert(isinstance(_bl_info["name"], str))

    assert("blender" in _bl_info)
    assert("version" in _bl_info)
    assert(isinstance(_bl_info["blender"], tuple))
    assert(isinstance(_bl_info["version"], tuple))
    assert(len(_bl_info["blender"]) == len(_bl_info["version"]) == 3)
    assert(_bl_info["blender"] <= _bl_info["version"])

    if _bl_info["blender"] < (3, 0, 0):
        # https://developer.blender.org/T85675
        if bpy.app.version < (3, 0, 0):
            assert("wiki_url" in _bl_info)
            assert(isinstance(_bl_info["wiki_url"], str))
        else:
            assert("doc_url" in _bl_info)
            assert(isinstance(_bl_info["doc_url"], str))


def is_bpy_exists():
    return _is_bpy_exists


def addon_owner():
    return _addon


def addon_bl_info():
    return _bl_info


def __dbg_exists(name: str) -> bool:
    return (is_bpy_exists()
            and addon_owner()
            and os.path.isfile(
                os.path.join(os.path.dirname(os.path.realpath(addon_owner().__file__)), name)))


for __n in ("DEBUG", "DEBUG.txt", "_DEBUG", "_DEBUG.txt"):
    if __dbg_exists(__n):
        _DEBUG = True


try:
    import bpy
except ImportError as err:
    print(f"{log.WARNING}Module \"{__name__}\" uses 'bpy' module Python API."
          "Please, ensure that 'bpy' is importable")
    raise ImportError(err)


from . import utils_ui
from . import utils_shader


def _func_placeholder(*args, **kwargs):
    pass


def addon_name() -> str:
    """Top-level addon package ``bl_info["name"]``

    Returns:
        str: Addon display name.
    """
    if is_bpy_exists():
        return addon_bl_info()["name"]
    return ""


def addon_doc_url() -> str:
    """Top level addon package ``bl_info["wiki_url"]`` for Blender<3.0 and
    ``bl_info["doc_url"]`` for later versions of Blender.

    Returns:
        str: Documentation url.
    """
    if is_bpy_exists():
        if bpy.app.version < (3, 0, 0):
            return addon_bl_info()["wiki_url"]
        else:
            return addon_bl_info()["doc_url"]
    return ""


def earliest_tested_version() -> tuple:
    """Earliest tested Blender version. It should be guarantee that the addon
    would work properly on previous Blender versions. This information would
    be retrieved from ``bl_info["blender"]``. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package ``bl_info["blender"]``.
    """
    if is_bpy_exists():
        return addon_bl_info()["blender"]
    return tuple()


def latest_tested_version() -> tuple:
    """Latest tested Blender version. It should be guarantee that the addon
    would work properly on latest Blender versions. This information would
    be retrieved from ``bl_info["version"]``. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package ``bl_info["version"]``.
    """
    if is_bpy_exists():
        return addon_bl_info()["version"]
    return tuple()


def version_string(ver: typing.Iterable) -> str:
    """String version separated by '.' character.

    Args:
        ver (typing.Iterable): Iterable which contains integer values.

    Returns:
        str: String representation of version.
    """
    return '.'.join((str(_) for _ in ver))


def register_helper(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon ``register`` function. Handles addon Blender
    versioning support w.r.t. earliest and latest tested Blender versions.

    In case if current Blender version is less than earliest tested, decorated
    ``register`` function would not be called. In this case would be registered
    only addon user preferences class (``pref_cls``). Note that class ``draw``
    method should be decorated with
    :py:func:`preferences_draw_versioning_helper`
    decorator to provide warning for end user.

    If current Blender version is greater than latest tested, only warning
    message would be printed into console and main ``register`` function would be
    called.

    Note that execution also implies that
    :py:func:`unregister_helper`
    would unregister only user preferences class if regular registration
    function was not called.

    Args:
        pref_cls (`bpy.types.AddonPreferences`_): Addon user preferences class,
            which would be the only class registered in case of current Blender
            version is less than earliest tested.
    """

    if is_bpy_exists():
        def register_helper_outer(reg_func):
            @functools.wraps(reg_func)
            def wrapper(*args, **kwargs):
                global _full_registration_done

                earliest_tested = earliest_tested_version()
                latest_tested = latest_tested_version()

                if bpy.app.version < earliest_tested:
                    bpy.utils.register_class(pref_cls)
                    print("{0}{_addon_name} WARNING: Current Blender version ({_b_ver_str}) is less than older tested "
                          "({_earltested}). Registered only addon user preferences, which warn user about that.\n"
                          "Please, visit the addon documentation:\n{_addon_doc_url}{1}".format(
                              log.WARNING,  # Warning start.
                              log.END,  # Warning end.
                              _addon_name=addon_name(),
                              _b_ver_str=bpy.app.version_string,
                              _earltested=version_string(earliest_tested),
                              _addon_doc_url=addon_doc_url(),
                          ))
                    _full_registration_done = False
                    return

                elif bpy.app.version > latest_tested:
                    print(
                        "{0}{_addon_name} WARNING: Current Blender version ({_b_ver_str}) is greater than latest "
                        "tested ({_lattested}).\nPlease, visit the addon documentation:\n{_addon_doc_url}{1}".format(
                            log.WARNING,  # Warning start.
                            log.END,  # Warning end.
                            _addon_name=addon_name(),
                            _b_ver_str=bpy.app.version_string,
                            _lattested=version_string(latest_tested),
                            _addon_doc_url=addon_doc_url(),
                        ))

                ret = None
                is_any_err = False
                try:
                    ret = reg_func(*args, **kwargs)
                except ValueError:
                    is_any_err = True
                except AttributeError:
                    is_any_err = True
                else:
                    _full_registration_done = True

                if is_any_err:
                    print(
                        "{0}Unable to register addon: \"{_addon_name}\".\n"
                        "Please, try again in debug mode (add 'DEBUG.txt' file to addon root directory).{1}".format(
                            log.FAIL,  # Failure start.
                            log.END,  # Failure end.
                            _addon_name=addon_name(),
                        )
                    )
                else:
                    log(f"{log.CYAN}Registered addon: \"{addon_name()}\"")
                return ret

            return wrapper
    else:
        register_helper_outer = _func_placeholder
    return register_helper_outer


def unregister_helper(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon ``unregister`` function. Handles un-registration
    process after :py:func:`register_helper` registration
    process.

    Args:
        pref_cls (`bpy.types.AddonPreferences`_): Addon user preferences class.
    """
    if is_bpy_exists():
        def unregister_helper_outer(unreg_func):
            @functools.wraps(unreg_func)
            def wrapper(*args, **kwargs):
                global _full_registration_done
                if _full_registration_done:
                    ret = None
                    is_any_err = False
                    try:
                        ret = unreg_func(*args, **kwargs)
                    except ValueError:
                        is_any_err = True
                    except AttributeError:
                        is_any_err = True
                    else:
                        _full_registration_done = False

                    if is_any_err:
                        print(
                            "{0}Unable to unregister addon: \"{_addon_name}\".\n"
                            "Please, try again in debug mode (add 'DEBUG.txt' file to addon root directory).{1}".format(
                                log.FAIL,  # Failure start.
                                log.END,  # Failure end.
                                _addon_name=addon_name(),
                            ))
                    else:
                        log(f"{log.CYAN}Unregistered addon: \"{addon_name()}\"")
                    return ret
                else:
                    bpy.utils.unregister_class(pref_cls)
            return wrapper
    else:
        unregister_helper_outer = _func_placeholder
    return unregister_helper_outer


def preferences_draw_versioning_helper(url_help: str):
    """Helper decorator for addon user preferences ``draw`` method. Should be used
    with :py:func:`register_helper` and :py:func:`unregister_helper`.

    If current Blender version is less than earliest tested, draw method would
    not be called, would be displayed only information about versioning with
    respective documentation link (``url_help``).

    If current Blender version is greater than latest tested, first would be
    displayed versioning information and only than - actual draw method content.

    Args:
        url_help (str): Addon documentation versioning information link.
    """
    if is_bpy_exists():
        def preferences_draw_versioning_helper_outer(draw_func):
            @functools.wraps(draw_func)
            def wrapper(self, context):
                layout = self.layout
                layout.use_property_split = True
                layout.use_property_decorate = False

                def _draw_compatibility_link(lay) -> None:
                    lay.label(text="Please, read the documentation about compatibility support:")
                    props = col.operator("wm.url_open", text="Read about compatibility", icon='URL')
                    props.url = url_help

                if bpy.app.version < earliest_tested_version():
                    col = layout.column(align=True)
                    col.label(
                        text="You Blender version is less than minimal supported!",
                        icon='ERROR'
                    )
                    _draw_compatibility_link(col)
                    return

                elif bpy.app.version > latest_tested_version():
                    col = layout.column(align=True)
                    col.label(text="Your Blender version may be not tested", icon='INFO')
                    _draw_compatibility_link(col)

                return draw_func(self, context)

            return wrapper
    else:
        preferences_draw_versioning_helper_outer = _func_placeholder
    return preferences_draw_versioning_helper_outer


def submodule_registration_helper(msg_ok="", msg_err=""):
    """Helper function decorator for addon sub-module (un)registration.
    Main goal is to catch errors due sub-module (un)registration function call.

    Args:
        msg_ok (str, optional): Message to be printed on success. Defaults to "".
        msg_err (str, optional): Message to be printed on fail. Defaults to "".
    """
    if is_bpy_exists():
        def submodule_registration_helper_outer(reg_func):
            @functools.wraps(reg_func)
            def wrapper(*args, **kwargs):
                ret = None
                any_err = ""
                try:
                    tmp_ret = reg_func(*args, **kwargs)
                except ValueError as err:
                    any_err = err
                except AttributeError as err:
                    any_err = err
                else:
                    ret = tmp_ret
                    log(f"{log.CYAN}")

                if any_err:
                    print(
                        "{0}{_msg_err}{1}:".format(
                            log.WARNING,  # Warning start.
                            log.END,  # Warning end.
                            _msg_err=msg_err,
                        )
                    )
                    raise ValueError(err)
                else:
                    log(f"{log.CYAN}{msg_ok}")
                return ret
            return wrapper
    else:
        submodule_registration_helper_outer = _func_placeholder
    return submodule_registration_helper_outer


def register_extend_bpy_types(register_queue: tuple) -> None:
    """Helper function for extend `bpy.types`_ registration.

    Args:
        register_queue (tuple): tuple of tuples
            (`bpy.types`_.[class], attr_name, prop_type, cls), where ``attr_name`` is
            name of attribute which should be set (for example,
            `bpy.types.Scene`_.my_property), ``prop_type`` is type of property to be set
            (`bpy.props.PointerProperty`_ or `bpy.props.CollectionProperty`_), ``cls`` is an
            instance of `bpy.types.PropertyGroup`_ to be registered and set.

    Raises:
        ValueError: Raised when one of ``cls`` classes could not be registered via
            `bpy.utils.register_class`_.
        AttributeError: Raised when `bpy.types`_.[class] already has attribute
            with given name.

    """
    if is_bpy_exists():
        for bpy_type, attr_name, prop_type, cls in register_queue:
            try:
                bpy.utils.register_class(cls)
            except ValueError as err:
                log(f"{log.WARNING}Unable to register extension to "
                    f"bpy.types.{bpy_type} for reason:\n{log.FAIL}")
                raise ValueError(err)
            else:
                if hasattr(bpy_type, attr_name):
                    log(f"{log.WARNING}Unable to set property of bpy.type ({bpy_type}) to "
                        "attribute with name \"{attr_name}\". Its already registered.")
                    raise AttributeError(f"Property \"{attr_name}\" already exists.")
                else:
                    setattr(bpy_type, attr_name, prop_type(type=cls))

            log(f"{log.CYAN}Registered extend bpy types")


def unregister_extend_bpy_types(register_queue: tuple) -> None:
    """Helper function for extend `bpy.types` un-registration.

    Args:
        register_queue (tuple): tuple of tuples (`bpy.types`_.[class], attr_name, prop_type, cls)
    """
    if is_bpy_exists():
        for bpy_type, attr_name, _prop_type, cls in register_queue:
            try:
                bpy.utils.unregister_class(cls)
            except ValueError as err:
                print(f"{log.WARNING} Unable to unregister class {cls} for reason:\n{err}")
            else:
                if hasattr(bpy_type, attr_name):
                    delattr(bpy_type, attr_name)
                else:
                    print(f"{log.WARNING}Unable to delete attribute \"{attr_name}\" "
                          "from class {bpy_type} because it have no such attribute")

            log(f"{log.CYAN}Unregistered extend bpy types")


# ____________________________________________________________________________ #
# Tests.

if is_bpy_exists():
    _SAMPLE_TEXT = """
    A grasshopper spent the summer hopping about in the sun and singing to his heart's content. One day, an ant went hurrying by, looking very hot and weary.

    "Why are you working on such a lovely day?" said the grasshopper.

    "I'm collecting food for the winter," said the ant, "and I suggest you do the same." And off she went, helping the other ants to carry food to their store. The grasshopper carried on hopping and singing. When winter came the ground was covered with snow. The grasshopper had no food and was hungry. So he went to the ants and asked for food.

    "What did you do all summer when we were working to collect our food?" said one of the ants.

    "I was busy hopping and singing," said the grasshopper.

    "Well," said the ant, "if you hop and sing all summer, and do no work, then you must starve in the winter."
    """

    def _test_draw_wrapped_text(context, layout):
        compact_ui = context.region.width < 450

        addon_pref = context.preferences.addons[__package__].preferences

        if compact_ui:
            layout.prop(addon_pref, "wrapped_text_tab")
        else:
            row = layout.row(align=True)
            row.prop(addon_pref, "wrapped_text_tab", expand=True)

        if addon_pref.wrapped_text_tab == 'CHAR':
            if compact_ui:
                layout.prop(addon_pref, "wrapped_text_char")
            else:
                grid = layout.grid_flow(row_major=True, columns=20, even_columns=True, align=True)
                grid.use_property_split = False
                grid.prop(addon_pref, "wrapped_text_char", expand=True)
            layout.prop(addon_pref, "wrapped_text_char_interval")
        layout.prop(addon_pref, "wrapped_text_length")
        layout.label(
            text=f"`.utils_ui.draw_wrapped_text` (region width: {context.region.width}px, type: \'{context.region.type}\')",
            icon='INFO'
        )

        if addon_pref.wrapped_text_tab == 'LONG':
            text = _SAMPLE_TEXT
            if addon_pref.wrapped_text_length > 0:
                if addon_pref.wrapped_text_length < len(text):
                    text = text[0:addon_pref.wrapped_text_length]
                elif addon_pref.wrapped_text_length > len(text):
                    num_iterations = int(addon_pref.wrapped_text_length / len(text))
                    if num_iterations > 1:
                        text *= num_iterations
                    num_chars_left = addon_pref.wrapped_text_length - len(text)
                    text += text[0:num_chars_left]

        elif addon_pref.wrapped_text_tab == 'CHAR':
            num_chars = 500
            if addon_pref.wrapped_text_length > 0:
                num_chars = addon_pref.wrapped_text_length

            text = ""
            num_iterations = int(num_chars / addon_pref.wrapped_text_char_interval)

            if num_iterations < 1:
                text = addon_pref.wrapped_text_char * num_chars
            else:
                text = ((addon_pref.wrapped_text_char * addon_pref.wrapped_text_char_interval) + ' ') * num_iterations

        layout.label(text=f"Text Block ({len(text)} characters):", icon='INFO')
        utils_ui.draw_wrapped_text(context, layout, text=text)

    class _BHQABT_Preferences(bpy.types.AddonPreferences):
        bl_idname = __package__

        tab: bpy.props.EnumProperty(
            items=(
                ('WRAPPED_TEXT', "Wrapped Text", ""),
            )
        )

        wrapped_text_tab: bpy.props.EnumProperty(
            items=(
                ('LONG', "Long Text Block", ""),
                ('CHAR', "Single Character", ""),
            ),
            default='LONG',
            name="Text Block",
        )

        wrapped_text_char: bpy.props.EnumProperty(
            items=[(_, _, _) for _ in string.printable],
            default='A',
            name="Character",
        )

        wrapped_text_char_interval: bpy.props.IntProperty(name="Spacer Interval", default=10, min=1)
        wrapped_text_length: bpy.props.IntProperty(name="Text Length", default=-1, min=-1)

        @preferences_draw_versioning_helper(url_help=addon_doc_url())
        def draw(self, context):
            layout = self.layout

            layout.prop_tabs_enum(self, "tab")
            if self.tab == 'WRAPPED_TEXT':
                _test_draw_wrapped_text(context, layout)

    class _BHQABT_View3DPanelBase:
        bl_category = "BlenderHQ Addon Base Test"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'

    class _BHQABT_PT_WrappedText(bpy.types.Panel, _BHQABT_View3DPanelBase):
        bl_idname = "BHQABT_PT_WrappedText"
        bl_label = "Wrapped Text"

        def draw(self, context):
            layout = self.layout

            _test_draw_wrapped_text(context, layout)

    class _BHQABT_OT_Progress(bpy.types.Operator):
        bl_idname = "bhqabt.progress"
        bl_label = "Progress"
        bl_options = {'REGISTER'}

        cancellable: bpy.props.BoolProperty()

        def execute(self, context):
            self.progress = utils_ui.progress.invoke()
            self.progress.cancellable = self.cancellable
            self.progress.label = f"Test Progress {random.randint(100, 200)}"
            self.progress.icon = 'INFO'
            self.progress.num_steps = 50

            wm = context.window_manager
            wm.modal_handler_add(self)
            self._timer = wm.event_timer_add(time_step=0.1, window=context.window)

            return {'RUNNING_MODAL'}

        def cancel(self, context):
            wm = context.window_manager
            wm.event_timer_remove(self._timer)

            utils_ui.progress.complete(self.progress)

        def modal(self, context, event):
            if event.type == 'TIMER':
                self.progress.step += 1

            if self.progress.value >= 1.0 or self.progress.cancel or event.type == 'ESC':
                self.cancel(context)
                return {'CANCELLED'}

            return {'PASS_THROUGH'}

    class _BHQABT_PT_Progress(bpy.types.Panel, _BHQABT_View3DPanelBase):
        bl_idname = "BHQABT_PT_Progress"
        bl_label = "Progress Bars"

        def draw(self, _context):
            layout = self.layout
            layout.operator(operator=_BHQABT_OT_Progress.bl_idname, text="Progress Bar")
            props = layout.operator(operator=_BHQABT_OT_Progress.bl_idname, text="Cancellable Progress Bar")
            props.cancellable = True

    _classes = (
        _BHQABT_Preferences,
        _BHQABT_PT_WrappedText,
        _BHQABT_OT_Progress,
        _BHQABT_PT_Progress,
    )

    _cls_register, _cls_unregister = bpy.utils.register_classes_factory(classes=_classes)

    @register_helper(_BHQABT_Preferences)
    def register():
        _cls_register()

    @unregister_helper(_BHQABT_Preferences)
    def unregister():
        _cls_unregister()
