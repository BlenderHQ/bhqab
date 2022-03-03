Addon Registration (bhq_addon_base)
=======================================================

The module was created primarily to simplify addon maintenance. For example, our organization needs to service several released addons. This is not an easy task, as updates to Blender are released relatively often, studios or individual users can use both previous (sometimes not even LTS releases of Blender) and not yet fully ready pre-release (beta) versions of Blender. In any case, much of the testing of addons before releases is done manually, consistently on major versions of the Blender. Of course, it is necessary to repeat from time to time testing the functionality of addons on earlier versions of Blender, as well as on those versions that have not yet been released. But this is all the time that can be spent on developing new functionality and optimization.

The main purpose of the module is to simplify the procedure for error handling when calling addon registration methods.

In any case, there may be a situation where the addon for some reason can not be used or testing has not been conducted for the latest version of Blender. For this purpose the basic principles are allocated:

* If the user runs the addon on the Blender earlier than the minimum tested and approved for use:

    In this case, no addon registration methods will be called, and only the user preference class will be registered. In this case, the preferences will not display any addon settings, but will display a message stating that its addon cannot be used in this version of Blender.

* If the user runs the addon on the Blender of the newer version than the last tested and approved:

    In this case, there will be an attempt to register the addon, but even if no errors occurred during registration - in the user preferences of the addon will first display a warning about it

Basic functions are also provided to simplify the output of log messages through the command line and the drawing of the user interface.

* If the version with which the addon is used is tested and approved, everything will be as usual.


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
