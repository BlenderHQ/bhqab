# BlenderHQ Addon Base
 
The module is designed to unify some basic functions that are used in several addons.

Links:
* [BlenderHQ](https://github.com/BlenderHQ)
* [Git Repository](https://github.com/BlenderHQ/bhq_addon_base)

For licensing information see `./LICENSE` file in repository root directory (GPLv3).

# Addon Maintenance

Module can be added to existing addon repository with command:

`git submodule add https://github.com/BlenderHQ/bhq_addon_base`

The addon which uses module as a sub-module can be cloned

`git clone [repository url] --recursive`

They also should be updated with command:

`git submodule foreach git pull origin main`
