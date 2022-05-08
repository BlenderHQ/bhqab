GPU (gpu_extras)
=======================================================

The module provides an opportunity to simplify the use of shaders. This is
implemented by automatically generating shader objects from shader files located
in a specific folder. All shader files must have the extension ``*.glsl``.
File names must contain a shader name without spaces (only ``'_'`` is allowed)
and a separate type through the ``'_'`` character of the shader type at the end
of the file name.

.. automodule:: bhqab.gpu_extras
    :members:

.. _gpu.types.GPUShader:
    https://docs.blender.org/api/current/gpu.types.html#gpu.types.GPUShader
