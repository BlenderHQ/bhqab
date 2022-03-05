BlenderHQ Addon Base API
================================================

The design of the module is aimed at unifying the important functions used in several add-ons for the Blender 2.8+ series.

Links:
   * `GitHub Repository <https://github.com/BlenderHQ/bhq_addon_base>`_
   * `BlenderHQ GitHub <https://github.com/BlenderHQ>`_
   * `BlenderHQ Patreon <https://www.patreon.com/BlenderHQ>`_

For licensing information see `./LICENSE` file in repository root directory (GPLv3).

Addon Maintenance
******************

To add a module to the addon, you can use the command:
::

   git submodule add https://github.com/BlenderHQ/bhq_addon_base


To clone the addon repository to a local machine, the following command:
::

   git clone [repository url] --recursive


To update the addon repository from the remote:
::

   git submodule foreach git pull origin main


.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   pages/registration
   pages/utils_ui
   pages/utils_shader

.. toctree::
   :maxdepth: 2
   :caption: Tests

   pages/tests
   pages/test_wrapped_text


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
