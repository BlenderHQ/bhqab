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

# ____________________________________________________________________________ #
# The module is designed to unify some basic functions that are used in several
# addons. See `./README.md` and `./LICENSE` files for details about possible
# usage and licensing.

import functools
import typing

if "bpy" in locals():
    from importlib import reload

    reload(ui_utilities)

    del reload
else:
    _full_registration_done = False

import bpy

from . import ui_utilities

# ____________________________________________________________________________ #
# Register / unregister workflow.

ADDON = __import__(__package__.split('.')[0])

BL_INFO = getattr(ADDON, "bl_info", None)
assert(BL_INFO is not None)

assert("name" in BL_INFO)
assert(isinstance(BL_INFO["name"], str))

assert("blender" in BL_INFO)
assert("version" in BL_INFO)
assert(isinstance(BL_INFO["blender"], tuple))
assert(isinstance(BL_INFO["version"], tuple))
assert(len(BL_INFO["blender"]) == len(BL_INFO["version"]) == 3)
assert(BL_INFO["blender"] <= BL_INFO["version"])

if BL_INFO["blender"] < (3, 0, 0):
    # https://developer.blender.org/T85675
    if bpy.app.version < (3, 0, 0):
        assert("wiki_url" in BL_INFO)
        assert(isinstance(BL_INFO["wiki_url"], str))
    else:
        assert("doc_url" in BL_INFO)
        assert(isinstance(BL_INFO["doc_url"], str))


def addon_name() -> str:
    """Top-level addon package `bl_info["name"]`

    Returns:
        str: Addon display name.
    """
    return BL_INFO["name"]


def addon_doc_url() -> str:
    """Top level addon package `bl_info["wiki_url"]` for Blender<3.0 and
    `bl_info["doc_url"]` for later versions of Blender.

    Returns:
        str: Documentation url.
    """
    if bpy.app.version < (3, 0, 0):
        return BL_INFO["wiki_url"]
    else:
        return BL_INFO["doc_url"]


def earliest_tested_version() -> tuple:
    """Earliest tested Blender version. It should be guarantee that the addon
    would work properly on previous Blender versions. This information would
    be retrieved from `bl_info["blender"]`. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package `bl_info["blender"]`.
    """
    return BL_INFO["blender"]


def latest_tested_version() -> tuple:
    """Latest tested Blender version. It should be guarantee that the addon
    would work properly on latest Blender versions. This information would
    be retrieved from `bl_info["version"]`. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package `bl_info["version"]`.
    """
    return BL_INFO["version"]


def version_string(ver: typing.Iterable) -> str:
    """String version separated by '.' charackter.

    Args:
        ver (typing.Iterable): Iterable which contains integer values.

    Returns:
        str: String representation of version.
    """
    return '.'.join((str(_) for _ in ver))


def register_helper(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon `register` function. Handles addon Blender
    versioning support w.r.t. earliest and latest tested Blender versions.

    In case if current Blender version is less than earliest tested, decorated
    `register` function would not be called. In this case would be registered
    only addon user preferences class (`pref_cls`). Note that class `draw`
    method should be decorated with
    :func:..py:currentmodule::`preferences_draw_versioning_helper`
    decorator to provide warning for end user.

    If current Blender version is greater than latest tested, only warning
    message would be printed into console and main `register` function would be
    called.

    Note that execution also implies that
    :func:..py:currentmodule::`unregister_helper`
    would unregister only user preferences class if regular registration
    function was not called.

    Args:
        pref_cls (bpy.types.AddonPreferences): Addon user preferences class,
        which would be the only class registered in case of current Blender
        version is less than earliest tested.
    """
    def register_helper_outer(reg_func):
        @functools.wraps(reg_func)
        def wrapper(*args, **kwargs):
            global _full_registration_done

            earliest_tested = earliest_tested_version()
            latest_tested = latest_tested_version()

            if bpy.app.version < earliest_tested:
                bpy.utils.register_class(pref_cls)
                print(
                    "{0} WARNING: Current Blender version ({1}) is less than older tested ({2}). "
                    "Registered only addon user preferences, which warn user about that.\n"
                    "Please, visit the addon documentation:\n{3}".format(
                        addon_name(), bpy.app.version_string, version_string(earliest_tested), addon_doc_url()
                    )
                )
                _full_registration_done = False
                return

            elif bpy.app.version > latest_tested:
                print(
                    "{0} WARNING: Current Blender version ({1}) is greater than latest tested ({2}).\n"
                    "Please, visit the addon documentation:\n{3}".format(
                        addon_name(), bpy.app.version_string, version_string(latest_tested), addon_doc_url()
                    )
                )

            ret = reg_func(*args, **kwargs)
            _full_registration_done = True
            return ret

        return wrapper
    return register_helper_outer


def unregister_helper(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon `unregister` function. Handles un-registration
    process after :func:..py:currentmodule::`register_helper` registration
    process.

    Args:
        pref_cls (bpy.types.AddonPreferences): Addon user preferences class.
    """
    def unregister_helper_outer(unreg_func):
        @functools.wraps(unreg_func)
        def wrapper(*args, **kwargs):
            global _full_registration_done
            if _full_registration_done:
                ret = unreg_func(*args, **kwargs)
                _full_registration_done = False
                return ret
            else:
                bpy.utils.unregister_class(pref_cls)
        return wrapper
    return unregister_helper_outer


def preferences_draw_versioning_helper(url_help: str):
    """Helper decorator for addon user preferences `draw` method. Should be used
    with :func:..py:currentmodule::`register_helper` and
    :func:..py:currentmodule::`unregister_helper`.

    If current Blender version is less than earliest tested, draw method would
    not be called, would be displayed only information about versioning with
    respective documentation link (`url_help`).

    If current Blender version is greater than latest tested, first would be
    displayed versioning information and only than - actual draw method content.

    Args:
        url_help (str): Addon documentation versioning information link.
    """
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
    return preferences_draw_versioning_helper_outer
