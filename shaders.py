import os

import bpy


_SUFFIX_VERTEX = "vert"
_SUFFIX_FRAGMENT = "frag"
_SUFFIX_GEOMETRY = "geom"
_SUFFIX_DEFINES = "def"
_SUFFIX_LIBRARY = "lib"


def suffix_vertex() -> str:
    """File name suffix for vertex shader.

    Returns:
        str: Constant ``"vert"``
    """
    return _SUFFIX_VERTEX


def suffix_fragment() -> str:
    """File name suffix for fragment shader.

    Returns:
        str: Constant ``"frag"``
    """
    return _SUFFIX_FRAGMENT


def suffix_geometry() -> str:
    """File name suffix for geometry shader.

    Returns:
        str: Constant ``"geom"``
    """
    return _SUFFIX_GEOMETRY


def suffix_defines() -> str:
    """File name suffix for shader defines.

    Returns:
        str: Constant ``"def"``
    """
    return _SUFFIX_DEFINES


def suffix_library() -> str:
    """File name suffix for common shader library.

    Returns:
        str: Constant ``"lib"``
    """
    return _SUFFIX_LIBRARY


class shader:
    """Shader utility class. After calling the
        :py:func:`generate_shaders`
        method of the class, the shaders will be available as class attributes.

        For example, there are shader files ``my_shader_vert.glsl`` and
        ``my_shader_frag.glsl``. After generating the shaders, the access to the
        shader will be done through the

        .. code-block:: python

            from .bhq_addon_base.utils_shader import shader
            my_shader = shader.my_shader

        Which would return instance of `gpu.types.GPUShader`_.
    """
    @classmethod
    def generate_shaders(cls, dir_path: str) -> bool:
        """Generate shaders cache.

        Args:
            dir_path (str): Directory to read shader files from.

        Raises:
            NameError: If name of shader file is incorrect.

        Returns:
            bool: True means that shader cache was generated.
        """
        if bpy.app.background:
            return False

        import gpu

        shader_endings = (
            _SUFFIX_VERTEX,
            _SUFFIX_FRAGMENT,
            _SUFFIX_GEOMETRY,
            _SUFFIX_DEFINES,
            _SUFFIX_LIBRARY
        )

        _shader_dict = {}
        _shader_library = ""
        _defines_library = ""

        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename)

            if not os.path.isfile(filepath):
                continue

            name, extension = os.path.splitext(filename)

            if extension != ".glsl":
                continue

            name_split = name.split('_')

            if len(name_split) == 1:
                raise NameError("Shader file name should have [some_name]_[type].glsl pattern")
            if len(name_split) == 2:
                shader_name, shader_type = name_split
            else:
                shader_type = name_split[-1]
                shader_name = '_'.join(name_split[:-1])

            if shader_type in shader_endings[0:2]:
                if shader_name not in _shader_dict:
                    _shader_dict[shader_name] = [None for _ in range(5)]

                shader_index = shader_endings.index(shader_type)
                with open(filepath, 'r') as code:
                    data = code.read()
                    _shader_dict[shader_name][shader_index] = data

            elif shader_type == _SUFFIX_LIBRARY:
                with open(filepath, 'r') as code:
                    data = code.read()
                    _shader_library += "\n\n%s" % data

            elif shader_type == _SUFFIX_DEFINES:
                with open(filepath, 'r') as code:
                    data = code.read()
                    _defines_library += "\n\n%s" % data

        for shader_name in _shader_dict.keys():
            shader_code = _shader_dict[shader_name]
            vertex_code, frag_code, geo_code, lib_code, defines = shader_code
            if _shader_library:
                lib_code = _shader_library
            if _defines_library:
                defines = _defines_library

            kwargs = dict(
                vertexcode=vertex_code,
                fragcode=frag_code,
                geocode=geo_code,
                libcode=lib_code,
                defines=defines
            )

            kwargs = dict(filter(lambda item: item[1] is not None, kwargs.items()))

            data = gpu.types.GPUShader(**kwargs)
            setattr(cls, shader_name, data)

        return True
