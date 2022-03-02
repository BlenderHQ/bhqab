# <pep8 compliant>

_is_bpy_exists = False
try:
    import bpy
    import blf
    from bl_ui import space_statusbar  # Just to validate it exists
except ImportError:
    pass  # Skip import error for (at least) documentation purposes.
else:
    # 'bpy' may be a fake module.
    if bpy.app.version is not None and blf.MONOCHROME is not None:
        _is_bpy_exists = True


_is_module_used_by_the_addon = False

_pkg_spl = __package__.split('.')
if _is_bpy_exists and len(_pkg_spl) > 1:
    _is_module_used_by_the_addon = True

_addon = None
_bl_info = None

if _is_module_used_by_the_addon:
    _addon = __import__(_pkg_spl[0])

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


def is_module_used_by_the_addon():
    return _is_module_used_by_the_addon


def addon_owner():
    return _addon


def addon_bl_info():
    return _bl_info
