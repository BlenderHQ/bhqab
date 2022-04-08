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


if "bpy" in locals():
    from importlib import reload

    if "registration" in locals():
        reload(registration)
    if "shaders" in locals():
        reload(shaders)
    if "ui" in locals():
        reload(ui)

    del reload

import bpy

from . import registration
from . import shaders
from . import ui
