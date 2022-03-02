Addon Registration (bhq_addon_base)
=======================================================

To simplify the understanding of further functions, we give a simple example of use:

.. code-block:: python

    # This means that this is the root file of the addon module (__init__.py).

    bl_info = {
        "name": "Sample Addon",
        # Maximal tested Blender version. Newer versions would not be stop any
        # registration process, because (as a rule), newer versions hold older Python
        # API for backward compatibility.
        "version": (3, 1, 0),
        # Minimal tested (and supported as well) Blender version. Blender Python API
        # before this value do not guaranteed that some functions works as expected,
        # because of found during development process bugs from Blender side, which was
        # fixed in later versions.
        "blender": (2, 83, 0),
        "category": "Render",
        # NOTE: For compatibility reasons both keys should be kept.
        "wiki_url": "https://...",
        "doc_url": "https://...",
    }

    import bpy

    from . import bhq_addon_base

    
    class SA_SceneProperties(bpy.types.PropertyGroup):
        my_int: bpy.props.IntProperty()


    class SA_ScenePanel(bpy.types.Panel):
        bl_label = "Sample"
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = "scene"
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            self.layout.prop(context.scene.my_attr, "my_int")


    class SamplePreferences(bpy.types.AddonPreferences):
        bl_idname = __package__

        @bhq_addon_base.preferences_draw_versioning_helper("https://...compatibility-link")
        def draw(self, context):
            ...

    _register_queue = (
        (bpy.types.Scene, "my_attr", bpy.props.PointerProperty, SA_SceneProperties),
    )

    _classes = (
        SA_ScenePanel,
    )

    _cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


    @bhq_addon_base.submodule_registration_helper("UI classes registered", "UI classes registration failed")
    def some_outer_register():
        _cls_register()


    @bhq_addon_base.submodule_registration_helper("UI classes unregistered", "UI classes unregister failed")
    def some_outer_unregister():
        _cls_unregister()


    @bhq_addon_base.register_helper(SamplePreferences)
    def register():
        bhq_addon_base.register_extend_bpy_types(register_queue=_register_queue)
        some_outer_unregister()
    
    
    @bhq_addon_base.unregister_helper(SamplePreferences)
    def unregister():
        bhq_addon_base.unregister_extend_bpy_types(register_queue=_register_queue)
        some_outer_unregister()


.. automodule:: bhq_addon_base
    :members:

* :ref:`genindex`
* :ref:`modindex`

.. _bpy.types:
        https://docs.blender.org/api/current/bpy.types.html

.. _bpy.types.AddonPreferences:
        https://docs.blender.org/api/current/bpy.types.AddonPreferences.html#bpy.types.AddonPreferences

.. _bpy.types.Scene:
    https://docs.blender.org/api/current/bpy.types.Scene.html#bpy.types.Scene


.. _bpy.types.PropertyGroup:
    https://docs.blender.org/api/current/bpy.types.PropertyGroup.html#bpy.types.PropertyGroup


.. _bpy.props.CollectionProperty:
    https://docs.blender.org/api/current/bpy.props.html#bpy.props.CollectionProperty


.. _bpy.props.PointerProperty:
    https://docs.blender.org/api/current/bpy.props.html#bpy.props.PointerProperty

.. _bpy.utils.register_class:
    https://docs.blender.org/api/current/bpy.utils.html#bpy.utils.register_class
