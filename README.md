# BlenderHQ Addon Base
 
The design of the module is aimed at unifying the important functions used in several add-ons for the Blender 2.8+ series.

The module was created primarily to simplify addon maintenance. For example, our organization needs to service several released addons. This is not an easy task, as updates to Blender are released relatively often, studios or individual users can use both previous (sometimes not even LTS releases of Blender) and not yet fully ready pre-release (beta) versions of Blender. In any case, much of the testing of addons before releases is done manually, consistently on major versions of the Blender. Of course, it is necessary to repeat from time to time testing the functionality of addons on earlier versions of Blender, as well as on those versions that have not yet been released. But this is all the time that can be spent on developing new functionality and optimization.

The main purpose of the module is to simplify the procedure for error handling when calling addon registration methods.

In any case, there may be a situation where the addon for some reason can not be used or testing has not been conducted for the latest version of Blender. For this purpose the basic principles are allocated:

* If the user runs the addon on the Blender earlier than the minimum tested and approved for use:

    In this case, no addon registration methods will be called, and only the user preference class will be registered. In this case, the preferences will not display any addon settings, but will display a message stating that its addon cannot be used in this version of Blender.

* If the user runs the addon on the Blender of the newer version than the last tested and approved:

    In this case, there will be an attempt to register the addon, but even if no errors occurred during registration - in the user preferences of the addon will first display a warning about it

Basic functions are also provided to simplify the output of log messages through the command line and the drawing of the user interface.

* If the version with which the addon is used is tested and approved, everything will be as usual.

## Branches

* `main` - Contains the main distributable project code.
* `dev` - Branch of project development and also support of online and offline API project documentation.

## Maintenance of Addons Using the Module

Module can be added to existing addon repository with command:

`git submodule add https://github.com/BlenderHQ/bhq_addon_base`

The addon which uses module as a sub-module can be cloned

`git clone [repository url] --recursive`

They also should be updated with command:

`git submodule foreach git pull origin main`

## Links
* [BlenderHQ](https://github.com/BlenderHQ)
* [Git Repository](https://github.com/BlenderHQ/bhq_addon_base)
* [Patreon](https://www.patreon.com/BlenderHQ)
