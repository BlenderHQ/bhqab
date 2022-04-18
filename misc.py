import typing
import random
import string


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
