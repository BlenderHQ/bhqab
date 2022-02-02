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

from functools import wraps
from typing import Iterable

if "bpy" in locals():
    from importlib import reload

    del reload
else:
    pass

import bpy

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
    return BL_INFO["name"]


def addon_doc_url() -> str:
    if bpy.app.version < (3, 0, 0):
        return BL_INFO["wiki_url"]
    else:
        return BL_INFO["doc_url"]


def earliest_tested_version() -> tuple:
    return BL_INFO["blender"]


def latest_tested_version() -> tuple:
    return BL_INFO["version"]


def version_string(ver: Iterable) -> str:
    return '.'.join((str(_) for _ in ver))


def register_helper(pref_cls=None):
    def register_helper_outer(reg_func):
        @wraps(reg_func)
        def wrapper(*args, **kwargs):
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
                return
            elif bpy.app.version > latest_tested:
                print(
                    "{0} WARNING: Current Blender version ({1}) is greater than latest tested ({2}).\n"
                    "Please, visit the addon documentation:\n{3}".format(
                        addon_name(), bpy.app.version_string, version_string(latest_tested), addon_doc_url()
                    )
                )

            return reg_func(*args, **kwargs)

        return wrapper
    return register_helper_outer


def unregister_helper():
    def wrapper(func):
        func()
    return wrapper
