import os

import bpy
import gpu


class shader_meta(type):
    @property
    def SHADER_FILE_EXTENSION(cls):
        return cls._SHADER_FILE_EXTENSION

    @property
    def SEPARATOR_CHAR(cls):
        return cls._SEPARATOR_CHAR

    @property
    def SUFFIX_VERTEX(cls):
        return cls._SUFFIX_VERTEX

    @property
    def SUFFIX_FRAGMENT(cls):
        return cls._SUFFIX_FRAGMENT

    @property
    def SUFFIX_GEOMETRY(cls):
        return cls._SUFFIX_GEOMETRY

    @property
    def SUFFIX_DEFINES(cls):
        return cls._SUFFIX_DEFINES

    @property
    def SUFFIX_LIBRARY(cls) -> str:
        return cls._SUFFIX_LIBRARY


class shader(metaclass=shader_meta):
    """Shader utility class. After calling the
    :py:func:`bhqab.shaders.shader.generate_shaders`
    method of the class, the shaders will be available as class attributes.

    For example, there are shader files ``my_shader_vert.glsl`` and
    ``my_shader_frag.glsl``. After generating the shaders, the access to the
    shader will be done through the ``shader.my_shader``.

    Which would return instance of `gpu.types.GPUShader`_.

    Attributes:
        SHADER_FILE_EXTENSION (str): Constant ``".glsl"`` (readonly).
        SEPARATOR_CHAR (str): Constant ``'_'`` (readonly).
        SUFFIX_VERTEX (str): Constant ``"vert"`` (readonly).
        SUFFIX_FRAGMENT (str): Constant ``"frag"`` (readonly).
        SUFFIX_GEOMETRY (str): Constant ``"geom"`` (readonly).
        SUFFIX_DEFINES (str): Constant ``"def"`` (readonly).
        SUFFIX_LIBRARY (str): Constant ``"lib"`` (readonly).
    """

    _SHADER_FILE_EXTENSION = ".glsl"
    _SEPARATOR_CHAR = '_'
    _SUFFIX_VERTEX = "vert"
    _SUFFIX_FRAGMENT = "frag"
    _SUFFIX_GEOMETRY = "geom"
    _SUFFIX_DEFINES = "def"
    _SUFFIX_LIBRARY = "lib"

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

        shader_endings = (
            cls.SUFFIX_VERTEX,
            cls.SUFFIX_FRAGMENT,
            cls.SUFFIX_GEOMETRY,
            cls.SUFFIX_DEFINES,
            cls.SUFFIX_LIBRARY
        )

        _shader_dict = {}
        _shader_library = ""
        _defines_library = ""

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            if not os.path.isfile(file_path):
                continue

            name, extension = os.path.splitext(file_name)

            if extension != cls.SHADER_FILE_EXTENSION:
                continue

            name_split = name.split(cls.SEPARATOR_CHAR)

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
                with open(file_path, 'r') as code:
                    data = code.read()
                    _shader_dict[shader_name][shader_index] = data

            elif shader_type == cls.SUFFIX_LIBRARY:
                with open(file_path, 'r') as code:
                    data = code.read()
                    _shader_library += "\n\n%s" % data

            elif shader_type == cls.SUFFIX_DEFINES:
                with open(file_path, 'r') as code:
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
