"""
Module provide command line log messages utilities.

If variable bellow ('_DEBUG') is set to True or one of files exists in the
same directory as the addon root (in this case, it would be set to True),
debugging functionalities would be available (log messages, ect).

NOTE: This workaround allows to make the addon maintenance faster because
the developer should not set variable before each public commit. Obvious that
possible existing file always should be in `.gitignore`, so its would not
present by default on user installations.
"""

_DEBUG = False

import os

from ._import_utils import (is_module_used_by_the_addon,
                            addon_owner,
                            addon_bl_info)


def __dbg_exists(name: str) -> bool:
    return (is_module_used_by_the_addon()
            and os.path.isfile(os.path.join(os.path.dirname(addon_owner().__file__), name)))


for __n in ("DEBUG", "DEBUG.txt", "_DEBUG", "_DEBUG.txt"):
    if __dbg_exists(__n):
        _DEBUG = True


class log:
    """asdasd
    """
    TAB = ' ' * 2

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def __init__(self, *args, **kwargs) -> None:
        """asdasd
        """
        if _DEBUG:
            args += (log.END,)
            print(*args, **kwargs)


if is_module_used_by_the_addon():
    log(log.CYAN, "{0} {1} Debug mode".format(addon_bl_info()["name"], addon_bl_info()["version"]))
