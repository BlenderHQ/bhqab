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

import functools
import typing

if "bpy" in locals():
    from importlib import reload

    reload(utils_ui)
    reload(utils_log)

    del reload
else:
    _full_registration_done = False

from ._import_utils import (is_module_used_by_the_addon,
                            addon_bl_info)

from . import utils_log

try:
    import bpy
except ImportError as err:
    print(f"{utils_log.log.WARNING}Module \"{__name__}\" uses 'bpy' module Python API."
          "Please, ensure that 'bpy' is importable")
    raise ImportError(err)


from . import utils_ui


def addon_name() -> str:
    """Top-level addon package ``bl_info["name"]``

    Returns:
        str: Addon display name.
    """
    if is_module_used_by_the_addon():
        return addon_bl_info()["name"]
    return ""


def addon_doc_url() -> str:
    """Top level addon package ``bl_info["wiki_url"]`` for Blender<3.0 and
    ``bl_info["doc_url"]`` for later versions of Blender.

    Returns:
        str: Documentation url.
    """
    if is_module_used_by_the_addon():
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
    if is_module_used_by_the_addon():
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
    if is_module_used_by_the_addon():
        return addon_bl_info()["version"]
    return tuple()


def version_string(ver: typing.Iterable) -> str:
    """String version separated by '.' character.

    Args:
        ver (typing.Iterable): Iterable which contains integer values.

    Returns:
        str: String representation of version.
    """
    if is_module_used_by_the_addon():
        return '.'.join((str(_) for _ in ver))
    return ""


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
    if not is_module_used_by_the_addon():
        return

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
                          utils_log.log.WARNING,  # Warning start.
                          utils_log.log.END,  # Warning end.
                          _addon_name=addon_name(),
                          _b_ver_str=bpy.app.version_string,
                          _earltested=version_string(earliest_tested),
                          _addon_doc_url=addon_doc_url(),
                      ))
                _full_registration_done = False
                return

            elif bpy.app.version > latest_tested:
                print("{0}{_addon_name} WARNING: Current Blender version ({_b_ver_str}) is greater than latest tested "
                      "({_lattested}).\nPlease, visit the addon documentation:\n{_addon_doc_url}{1}".format(
                          utils_log.log.WARNING,  # Warning start.
                          utils_log.log.END,  # Warning end.
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
                        utils_log.log.FAIL,  # Failure start.
                        utils_log.log.END,  # Failure end.
                        _addon_name=addon_name(),
                    )
                )
            else:
                utils_log.log(f"{utils_log.log.CYAN}Registered addon: \"{addon_name()}\"")
            return ret

        return wrapper
    return register_helper_outer


def unregister_helper(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon ``unregister`` function. Handles un-registration
    process after :func:..py:currentmodule::`register_helper` registration
    process.

    Args:
        pref_cls (bpy.types.AddonPreferences): Addon user preferences class.
    """
    if not is_module_used_by_the_addon():
        return

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
                            utils_log.log.FAIL,  # Failure start.
                            utils_log.log.END,  # Failure end.
                            _addon_name=addon_name(),
                        ))
                else:
                    utils_log.log(f"{utils_log.log.CYAN}Unregistered addon: \"{addon_name()}\"")
                return ret
            else:
                bpy.utils.unregister_class(pref_cls)
        return wrapper
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
    if not is_module_used_by_the_addon():
        return

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


def submodule_registration_helper(msg_ok="", msg_err=""):
    """Helper function decorator for addon sub-module (un)registration.
    Main goal is to catch errors due sub-module (un)registration function call.

    Args:
        msg_ok (str, optional): Message to be printed on success. Defaults to "".
        msg_err (str, optional): Message to be printed on fail. Defaults to "".
    """
    if not is_module_used_by_the_addon():
        return

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
                utils_log.log(f"{utils_log.log.CYAN}")

            if any_err:
                print(
                    "{0}{_msg_err}{1}:".format(
                        utils_log.log.WARNING,  # Warning start.
                        utils_log.log.END,  # Warning end.
                        _msg_err=msg_err,
                    )
                )
                raise ValueError(err)
            else:
                utils_log.log(f"{utils_log.log.CYAN}{msg_ok}")
            return ret
        return wrapper
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
    if not is_module_used_by_the_addon():
        return

    for bpy_type, attr_name, prop_type, cls in register_queue:
        try:
            bpy.utils.register_class(cls)
        except ValueError as err:
            utils_log.log(f"{utils_log.log.WARNING}Unable to register extension to "
                          f"bpy.types.{bpy_type} for reason:\n{utils_log.log.FAIL}")
            raise ValueError(err)
        else:
            if hasattr(bpy_type, attr_name):
                utils_log.log(f"{utils_log.log.WARNING}Unable to set property of bpy.type ({bpy_type}) to "
                              "attribute with name \"{attr_name}\". Its already registered.")
                raise AttributeError(f"Property \"{attr_name}\" already exists.")
            else:
                setattr(bpy_type, attr_name, prop_type(type=cls))

        utils_log.log(f"{utils_log.log.CYAN}Registered extend bpy types")


def unregister_extend_bpy_types(register_queue: tuple) -> None:
    """Helper function for extend `bpy.types` un-registration.

    Args:
        register_queue (tuple): tuple of tuples (`bpy.types`_.[class], attr_name, prop_type, cls)
    """
    if not is_module_used_by_the_addon():
        return

    for bpy_type, attr_name, _prop_type, cls in register_queue:
        try:
            bpy.utils.unregister_class(cls)
        except ValueError as err:
            print(f"{utils_log.log.WARNING} Unable to unregister class {cls} for reason:\n{err}")
        else:
            if hasattr(bpy_type, attr_name):
                delattr(bpy_type, attr_name)
            else:
                print(f"{utils_log.log.WARNING}Unable to delete attribute \"{attr_name}\" "
                      "from class {bpy_type} because it have no such attribute")

        utils_log.log(f"{utils_log.log.CYAN}Unregistered extend bpy types")
