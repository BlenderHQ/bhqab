BlenderHQ Addon Base API
================================================

The design of the module is aimed at unifying the important functions used in several add-ons for the Blender 2.8+ series.

Addon Maintenance
================================================

To add a module to the addon, you can use the command:

.. code-block:: console

   git submodule add https://github.com/BlenderHQ/bhq_addon_base


To clone the addon repository to a local machine, the following command:

.. code-block:: console

   git clone [repository url] --recursive


To update the addon repository from the remote:

.. code-block:: console

   git submodule foreach git pull origin main


Links
================================================

   .. figure:: images/qr_bhqab_github.svg
      :align: center
      :target: https://github.com/BlenderHQ/bhq_addon_base
      :alt: https://github.com/BlenderHQ/bhq_addon_base
      :width: 450
      
      GitHub Repository

   .. figure:: images/qr_bhq_github.svg
      :align: center
      :target: https://github.com/BlenderHQ
      :alt: https://github.com/BlenderHQ
      :width: 450
      
      BlenderHQ on GitHub

   .. figure:: images/qr_bhq_patreon.svg
      :align: center
      :target: https://www.patreon.com/BlenderHQ
      :alt: https://www.patreon.com/BlenderHQ
      :width: 450
      
      BlenderHQ on Patreon


For licensing information see `./LICENSE` file in repository root directory (GPLv3).


.. toctree::
   :maxdepth: 2
   :caption: API Reference

   pages/registration
   pages/ui
   pages/shaders
   pages/extend_bpy_types

.. toctree::
   :maxdepth: 2
   :caption: Tests

   pages/tests
   pages/tests_unit_tests
   pages/test_user_interface

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
