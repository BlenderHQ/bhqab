import types
import random
import string
import typing

import bpy


def earliest_tested_version(bl_info: dict) -> tuple:
    """The ``earliest`` of the tested and approved versions of the Blender for addon. Data about it will be taken from
    the addon module ``bl_info["blender"]`` attribute according to the design of the module.

    Args:
        bl_info (dict): Addon module attribute.

    Returns:
        tuple: Blender version as tuple.
    """
    return bl_info["blender"]


def latest_tested_version(bl_info: dict) -> tuple:
    """The ``latest`` of the tested and approved versions of the Blender for addon. Data about it will be taken from the
    addon module ``bl_info["version"]`` attribute according to the design of the module.

    Args:
        bl_info (dict): Addon module attribute.

    Returns:
        tuple: Blender version as tuple.
    """
    return bl_info["version"]


def _version_str(ver: typing.Iterable[int]):
    return '.'.join(ver)


def register_versioning(bl_info: dict) -> types.FunctionType:
    """Decorator to be used for the addon registration method. If the current version of Blender is lower than the one
    previously tested and approved for use, the registration method will not be called, but a registration error will be
    caused. If the current version is more than the last approved, you will only be notified in the console.

    Args:
        bl_info (dict): Addon module attribute.

    Returns:
        types.FunctionType: Decorated ``register`` addon module-level method.
    """
    def _register_outer(reg_func):
        from functools import wraps

        @wraps(reg_func)
        def _wrapper(*args, **kwargs):
            earliest_tested = earliest_tested_version(bl_info=bl_info)
            latest_tested = latest_tested_version(bl_info=bl_info)
            addon_name = bl_info["name"]

            if bpy.app.version < earliest_tested:
                raise RuntimeError(
                    f"\"{addon_name}\": Current Blender version ({_version_str(bpy.app.version)}) is less than "
                    f"earliest tested ({_version_str(earliest_tested)})."
                )
            elif bpy.app.version > latest_tested:
                print(
                    f"\"{addon_name}\": Current Blender version ({_version_str(bpy.app.version)}) is greater than "
                    f"latest tested ({_version_str(latest_tested)}). Use it on your own risk.")
            else:
                reg_func(*args, **kwargs)
        return _wrapper
    return _register_outer


def unique_name(collection: typing.Iterable, prefix="", suffix="") -> str:
    """Generates a random name that will be unique in this collection. It can be
    used to create a random unique name with the specified suffix and prefix for
    this collection. It can be used with ``bpy.data.[...].new (name)`` or to
    register temporary properties of data blocks, etc.

    Args:
        collection (typing.Iterable): A collection of objects for which a unique new name must be generated.
        prefix (str, optional): Name prefix. Defaults to "".
        suffix (str, optional): Name suffix. Defaults to "".

    Returns:
        str: Generated unique name.
    """
    ret = prefix + str().join(random.sample(string.ascii_letters, k=5)) + suffix

    if hasattr(collection, ret) or (isinstance(collection, typing.Iterable) and ret in collection):
        return unique_name(collection, prefix, suffix)
    return ret


def register_properties(register_queue: typing.Iterable) -> None:
    """Function to simplify the registration of properties of ``bpy_struct`` sub-classes.

    Args:
        register_queue (typing.Iterable): Iterable of iterables in format:
            ((

                * ``struct_type`` (`bpy.types.bpy_struct`_) - Blender data structure.

                * ``attr_name`` (str) - Attribute name to be set.

                * ``prop_cls`` - `bpy.props.PointerProperty`_ or `bpy.props.CollectionProperty`_.

                * ``cls`` (`bpy.types.PropertyGroup`_) - Properties class.

            ), ...)

    """
    for struct_type, attr_name, prop_cls, cls in register_queue:
        bpy.utils.register_class(cls)
        setattr(struct_type, attr_name, prop_cls(type=cls))


def unregister_properties(register_queue: typing.Iterable) -> None:
    """Function to simplify the un-registration of properties of ``bpy_struct`` sub-classes.

    Args:
        register_queue (typing.Iterable): Iterable of iterables in format:
            ((

                * ``struct_type`` (`bpy.types.bpy_struct`_) - Blender data structure.

                * ``attr_name`` (str) - Attribute name to be set.

                * ``prop_cls`` - `bpy.props.PointerProperty`_ or `bpy.props.CollectionProperty`_.

                * ``cls`` (`bpy.types.PropertyGroup`_) - Properties class.

            ), ...)
    """
    for struct_type, attr_name, _prop_cls, cls in register_queue:
        bpy.utils.unregister_class(cls)
        delattr(struct_type, attr_name)


def register_properties_factory(register_queue: typing.Iterable) -> tuple[types.FunctionType, types.FunctionType]:
    """Return's ``register`` and ``unregister`` functions using :py:func:`register_properties` and
    :py:func:`unregister_properties`.

    Args:
        register_queue (typing.Iterable): Iterable of iterables in format:
            ((

                * ``struct_type`` (`bpy.types.bpy_struct`_) - Blender data structure.

                * ``attr_name`` (str) - Attribute name to be set.

                * ``prop_cls`` - `bpy.props.PointerProperty`_ or `bpy.props.CollectionProperty`_.

                * ``cls`` (`bpy.types.PropertyGroup`_) - Properties class.

            ), ...)

    Returns:
        tuple[types.FunctionType, types.FunctionType]: _description_
    """
    def register():
        register_properties(register_queue=register_queue)

    def unregister():
        unregister_properties(register_queue=register_queue)

    return register, unregister
