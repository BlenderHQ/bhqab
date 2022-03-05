About Tests
=======================================================

Testing the module is not an easy task as there are many interdependencies.

Currently, the main method of testing is to install the module as an add-on to
the Blender. This can be done in different ways, but here we describe the method
used.

Since addons are tested on all official releases and pre-releases of Blender, it
is first necessary to test this basic module. So, we have all versions of
Blender installed on the hard drive and separately, in our case on another
physical drive - the directory with supported addons. The directory with addons
is called "addons", it is important in the following. Using symbolic file system
links, this directory is available in all custom Blender folders. This is the
easiest way to maintain and supplement existing addons.

Since the main file system has already been described, then - regarding the
testing of the module. There is also a symbolic link to this module in the
addons folder. At the same time, it is obvious that not for a module in the
directory of any of the addons, but for a separate local copy of the git
repository. In this way, the module will be available as a separate addon with
the required functionality for testing.