from typing import (
    Iterable,
)
import random
import string

_IMAGE_EXTENSIONS = (
    ".bmp",
    ".sgi", ".rgb", ".bw",
    ".png",
    ".jpg", ".jpeg",
    ".jp2", ".j2c",
    ".tga",
    ".cin", ".dpx",
    ".exr",
    ".hdr",
    ".tif", ".tiff",
    ".psd",
)


def supported_image_extensions() -> tuple:
    """Blender supported image extensions.
    https://docs.blender.org/manual/en/latest/files/media/image_formats.html

    Returns:
        tuple: Tuple of lowercase extensions:

            ``.bmp``,
            ``.sgi``, ``.rgb``, ``.bw``,
            ``.png``,
            ``.jpg``, ``.jpeg``,
            ``.jp2``, ``.j2c``,
            ``.tga``,
            ``.cin``, ``.dpx``,
            ``.exr``,
            ``.hdr``,
            ``.tif``, ``.tiff``,
            ``.psd``,
    """
    return _IMAGE_EXTENSIONS


def unique_name(collection: Iterable, prefix="", suffix="") -> str:
    """Generates a random name that will be unique in this collection. It can be
    used to create a random unique name with the specified suffix and prefix for
    this collection. It can be used with ``bpy.data.[...].new (name)`` or to
    register temporary properties of data blocks, etc.

    Args:
        collection (Iterable): A collection of objects for which a unique new name must be generated.
        prefix (str, optional): Name prefix. Defaults to "".
        suffix (str, optional): Name suffix. Defaults to "".

    Returns:
        str: Generated unique name.
    """
    ret = prefix + str().join(random.sample(string.ascii_letters, k=5)) + suffix

    if hasattr(collection, ret) or (isinstance(collection, Iterable) and ret in collection):
        return unique_name(collection, prefix, suffix)
    return ret
