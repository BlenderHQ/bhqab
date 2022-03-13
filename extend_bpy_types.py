import typing
import random
import string


_UNIQUE_NAME_K = 5


def unique_name(collection: typing.Iterable, prefix="", suffix="") -> str:
    """Generates random name which would be unique in given collection. This can
    be used for Generates a random unique name with a specified suffix and
    prefix for the given collection. It can be used for
    ``bpy.data.[collection].new(name)`` or for registration of temporary
    properties of data blocks, etc.

    Args:
        collection (typing.Iterable): A collection of objects for which a unique new name must be generated.
        prefix (str, optional): Name prefix. Defaults to "".
        suffix (str, optional): Name suffix. Defaults to "".

    Returns:
        str: Generated unique name.
    """
    ret = prefix + str().join(random.sample(string.ascii_letters, k=_UNIQUE_NAME_K)) + suffix

    if hasattr(collection, ret) or (isinstance(collection, typing.Iterable) and ret in collection):
        return unique_name(collection, prefix, suffix)
    return ret
