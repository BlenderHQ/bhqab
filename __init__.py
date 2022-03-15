# BlenderHQ addon base module.
# Copyright (C) 2022  Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__version__ = (1, 0)

__author__ = "Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)"
__copyright__ = "Copyright (C) 2022  Vlad Kuzmin (ssh4), Ivan Perevala (ivpe)"
__maintainer__ = "Ivan Perevala (ivpe)"
__credits__ = ["Vlad Kuzmin (ssh4)", ]
__license__ = "GPLv3"

bl_info = {
    "name": "BlenderHQ Addon Base Test",
    # Maximal tested Blender version. Newer versions would not be stop any
    # registration process, because (as a rule), newer versions hold older Python
    # API for backward compatibility.
    "version": (3, 1, 0),
    # Minimal tested (and supported as well) Blender version. Blender Python API
    # before this value do not guaranteed that some functions works as expected,
    # because of found during development process bugs from Blender side, which was
    # fixed in later versions.
    "blender": (2, 80, 0),
    "category": "Development",
    "warning": "This addon is exclusively part of the module testing",
    # NOTE: For compatibility reasons both keys should be kept.
    # (see https://developer.blender.org/T85675)
    "wiki_url": "https://github.com/BlenderHQ/bhq_addon_base",
    "doc_url": "https://github.com/BlenderHQ/bhq_addon_base",
}

if "bpy" in locals():
    from importlib import reload

    reload(registration)
    reload(extend_bpy_types)
    reload(shaders)
    reload(ui)

    del reload

from . import registration
from . import extend_bpy_types
from . import shaders
from . import ui

try:
    from . import tests
except ImportError:
    pass
else:
    register = tests.register
    unregister = tests.unregister
