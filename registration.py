import os
import sys
import types
import typing
import functools

import bpy


_ADDON_WITH_MODULE = sys.modules[__package__.split('.')[0]]
_ADDON_BL_INFO = getattr(_ADDON_WITH_MODULE, "bl_info", None)

_MODULE_DEBUG_MODE = False

_FULL_REGISTRATION_DONE = False


def __dbg_file_exists(name: str) -> bool:
    if isinstance(_ADDON_WITH_MODULE, types.ModuleType):
        dbg_fp = os.path.join(os.path.dirname(os.path.realpath(_ADDON_WITH_MODULE.__file__)), name)
        return os.path.isfile(dbg_fp)
    return False


for __n in ("DEBUG", "DEBUG.txt", "_DEBUG", "_DEBUG.txt"):
    if __dbg_file_exists(__n):
        _MODULE_DEBUG_MODE = True

from . import _log


def is_debug() -> bool:
    """Returns a positive value if the module is in the debug state.

    Returns:
        bool: Positive means that debug state is active.
    """
    return _MODULE_DEBUG_MODE


def current_addon() -> types.ModuleType:
    """Returns the module of the addon to which it belongs as a sub-module.

    Returns:
        module: Module owner.
    """
    return _ADDON_WITH_MODULE


def addon_bl_info() -> dict:
    """Returns the ``bl_info`` attribute of the addon module to which it belongs as a sub-module.

    Returns:
        dict: :py:func:`current_addon`. ``bl_info``
    """
    return _ADDON_BL_INFO


def addon_display_name() -> str:
    """
    Top-level addon package ``bl_info["name"]``

    Returns:
        str: Addon display name.
    """
    return addon_bl_info()["name"]


def addon_doc_url() -> str:
    """Top level addon package ``bl_info["wiki_url"]`` for Blender v2.8+
    and ``bl_info["doc_url"]`` for later versions of Blender (v3.0+).

    Returns:
        str: Documentation url.
    """
    _bl_info = addon_bl_info()
    if bpy.app.version < (3, 0, 0) and "wiki_url" in _bl_info:
        return _bl_info["wiki_url"]
    elif "doc_url" in _bl_info:
        return _bl_info["doc_url"]
    return ""


def earliest_tested_version() -> tuple:
    """Earliest tested Blender version. It should be guarantee that the addon
    would work properly on previous Blender versions. This information would
    be retrieved from ``bl_info["blender"]``. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package ``bl_info["blender"]``.
    """
    return addon_bl_info()["blender"]


def latest_tested_version() -> tuple:
    """Latest tested Blender version. It should be guarantee that the addon
    would work properly on latest Blender versions. This information would
    be retrieved from ``bl_info["version"]``. Note that this field should contains
    only tuple of 3 integers.

    Returns:
        tuple: Addon package ``bl_info["version"]``.
    """
    return addon_bl_info()["version"]


def version_string(ver: typing.Iterable) -> str:
    """String version separated by '.' character.

    Args:
        ver (typing.Iterable): Iterable which contains integer values.

    Returns:
        str: String representation of version.
    """
    return '.'.join((str(_) for _ in ver))


def addon_preferences(context: bpy.types.Context) -> bpy.types.AddonPreferences:
    """Current addon user preferences.

    Args:
        context (`bpy.types.Context`_): Current context.

    Returns:
        `bpy.types.AddonPreferences`_: Addon user preferences.
    """
    addon = current_addon()
    if addon:
        if __package__ in context.preferences.addons:
            return context.preferences.addons[__package__].preferences
    return None


def register(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon ``register`` function. Handles addon Blender
    versioning support w.r.t. earliest and latest tested Blender versions.

    In case if current Blender version is less than earliest tested, decorated
    ``register`` function would not be called. In this case would be registered
    only addon user preferences class (``pref_cls``). Note that class ``draw``
    method should be decorated with
    :py:func:`bhq_addon_base.ui.template_addon_versioning`
    decorator to provide warning for end user.

    If current Blender version is greater than latest tested, only warning
    message would be printed into console and main ``register`` function would be
    called.

    Note that execution also implies that
    :py:func:`unregister`
    would unregister only user preferences class if regular registration
    function was not called.

    Args:
        pref_cls (`bpy.types.AddonPreferences`_): Addon user preferences class,
            which would be the only class registered in case of current Blender
            version is less than earliest tested.
    """
    def _register_outer(reg_func):
        @functools.wraps(reg_func)
        def _wrapper(*args, **kwargs):
            global _FULL_REGISTRATION_DONE

            _FULL_REGISTRATION_DONE = False

            ret = None

            # Try to register user preferences class.
            reg_pref_err_msg = ""
            try:
                bpy.utils.register_class(pref_cls)
            except ValueError as err:
                reg_pref_err_msg = err
            except AttributeError as err:
                reg_pref_err_msg = err
            except RuntimeError as err:
                reg_pref_err_msg = err
            else:
                # Check Blender version for compatibility with current addon.
                earliest_tested = earliest_tested_version()
                latest_tested = latest_tested_version()

                if bpy.app.version < earliest_tested:
                    print("{0}{_addon_name} WARNING: Current Blender version ({_b_ver_str}) is less than older tested "
                          "({_earltested}). Registered only addon user preferences, which warn user about that.\n"
                          "Please, visit the addon documentation:\n{_addon_doc_url}{1}".format(
                              _log.log.WARNING,  # Warning start.
                              _log.log.END,  # Warning end.
                              _addon_name=addon_display_name(),
                              _b_ver_str=bpy.app.version_string,
                              _earltested=version_string(earliest_tested),
                              _addon_doc_url=addon_doc_url(),
                          ))

                elif bpy.app.version > latest_tested:
                    print(
                        "{0}{_addon_name} WARNING: Current Blender version ({_b_ver_str}) is greater than latest "
                        "tested ({_lattested}).\nPlease, visit the addon documentation:\n{_addon_doc_url}{1}".format(
                            _log.log.WARNING,  # Warning start.
                            _log.log.END,  # Warning end.
                            _addon_name=addon_display_name(),
                            _b_ver_str=bpy.app.version_string,
                            _lattested=version_string(latest_tested),
                            _addon_doc_url=addon_doc_url(),
                        ))
                else:
                    # Try to call addon registration methods.
                    reg_func_err_msg = ""
                    try:
                        ret = reg_func(*args, **kwargs)
                    except ValueError as err:
                        reg_func_err_msg = err
                    except AttributeError as err:
                        reg_func_err_msg = err
                    except RuntimeError as err:
                        reg_func_err_msg = err
                    else:
                        _FULL_REGISTRATION_DONE = True
                        _log.log(f"{_log.log.CYAN}Registered addon: \"{addon_display_name()}\"")

                    if reg_func_err_msg:
                        print(
                            "{0}{_addon_name} WARNING: Unable to register addon for reason:\n"
                            "{_reg_func_err_msg}\n\n"
                            "Please, try again in debug mode (add 'DEBUG.txt' file to addon root directory).{1}".format(
                                _log.log.FAIL,  # Failure start.
                                _log.log.END,  # Failure end.
                                _addon_name=addon_display_name(),
                                _reg_func_err_msg=reg_func_err_msg
                            )
                        )

            if reg_pref_err_msg:
                print(
                    "{0}{_addon_name} WARNING: Unable to register addon user preferences class "
                    "for reason:\n{_reg_pref_err_msg}{1}".format(
                        _log.log.WARNING,  # Warning start.
                        _log.log.END,  # Warning end.
                        _addon_name=addon_display_name(),
                        _reg_pref_err_msg=reg_pref_err_msg,
                    )
                )

            return ret

        return _wrapper
    return _register_outer


def unregister(pref_cls: bpy.types.AddonPreferences):
    """Helper decorator for addon ``unregister`` function. Handles un-registration
    process after :py:func:`register` registration
    process.

    Args:
        pref_cls (`bpy.types.AddonPreferences`_): Addon user preferences class.
    """
    def _unregister_outer(unreg_func):
        @ functools.wraps(unreg_func)
        def _wrapper(*args, **kwargs):
            global _FULL_REGISTRATION_DONE

            _FULL_REGISTRATION_DONE = False

            ret = None

            unreg_func_err_msg = ""
            try:
                ret = unreg_func(*args, **kwargs)
            except ValueError as err:
                unreg_func_err_msg = err
            except AttributeError as err:
                unreg_func_err_msg = err
            except RuntimeError as err:
                unreg_func_err_msg = err
            else:
                unreg_pref_err_msg = ""
                try:
                    bpy.utils.unregister_class(pref_cls)
                except ValueError as err:
                    unreg_pref_err_msg = err
                except AttributeError as err:
                    unreg_pref_err_msg = err
                except RuntimeError as err:
                    unreg_pref_err_msg = err
                else:
                    _log.log(f"{_log.log.CYAN}Unregistered addon: \"{addon_display_name()}\"")

                if unreg_pref_err_msg:
                    print(
                        "{0}Unable to unregister addon \"{_addon_name}\" user preferences for reason:\n"
                        "{_unreg_func_err_msg}\n"
                        "Please, try again in debug mode (add 'DEBUG.txt' file to addon root directory).{1}".format(
                            _log.log.FAIL,  # Failure start.
                            _log.log.END,  # Failure end.
                            _addon_name=addon_display_name(),
                            _unreg_func_err_msg=unreg_func_err_msg,
                        )
                    )

            if unreg_func_err_msg:
                print(
                    "{0}Unable to unregister addon \"{_addon_name}\" for reason:\n"
                    "{_unreg_func_err_msg}\n"
                    "Please, try again in debug mode (add 'DEBUG.txt' file to addon root directory).{1}".format(
                        _log.log.FAIL,  # Failure start.
                        _log.log.END,  # Failure end.
                        _addon_name=addon_display_name(),
                        _unreg_func_err_msg=unreg_func_err_msg,
                    )
                )
        return _wrapper
    return _unregister_outer


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
    for bpy_type, attr_name, prop_type, cls in register_queue:
        try:
            bpy.utils.register_class(cls)
        except ValueError as err:
            _log.log(f"{_log.log.WARNING}Unable to register extension to "
                     f"bpy.types.{bpy_type} for reason:\n{_log.log.FAIL}")
            raise ValueError(err)
        else:
            if hasattr(bpy_type, attr_name):
                _log.log(f"{_log.log.WARNING}Unable to set property of bpy.type ({bpy_type}) to "
                         "attribute with name \"{attr_name}\". Its already registered.")
                raise AttributeError(f"Property \"{attr_name}\" already exists.")
            else:
                setattr(bpy_type, attr_name, prop_type(type=cls))

    _log.log(f"{_log.log.CYAN}Registered extend bpy types")


def unregister_extend_bpy_types(register_queue: tuple) -> None:
    """Helper function for extend `bpy.types`_ un-registration.

    Args:
        register_queue (tuple): tuple of tuples (`bpy.types`_.[class], attr_name, prop_type, cls)
    """
    for bpy_type, attr_name, _prop_type, cls in register_queue:
        try:
            bpy.utils.unregister_class(cls)
        except ValueError as err:
            print(f"{_log.log.WARNING} Unable to unregister class {cls} for reason:\n{err}")
        else:
            if hasattr(bpy_type, attr_name):
                delattr(bpy_type, attr_name)
            else:
                print(f"{_log.log.WARNING}Unable to delete attribute \"{attr_name}\" "
                      "from class {bpy_type} because it have no such attribute")

        _log.log(f"{_log.log.CYAN}Unregistered extend bpy types")
