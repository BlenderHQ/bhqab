# <pep8 compliant>

"""
The module also provides opportunities to simplify the debugging and output of
more detailed messages to the console. It is clear that from the user experience
for ordinary users it may not be very necessary (usually they do not like
consoles), this part is focused more on those who will set up addons on many
computers, etc.

There is a class :py:class:`log` for outputting such debug messages. In order
for it to display the message, you must either manually set the variable
``_DEBUG`` to a positive value, or put in the root folder of the addon an empty
file called ``DEBUG``, ``DEBUG.txt``, ``_DEBUG`` or ``_DEBUG.txt``.

.. Note:: This workaround allows to make the addon maintenance faster because
    the developer should not set variable before each public commit. Obvious
    that possible existing file always should be in ``./.gitignore``, so its
    would not present by default on user installations.
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
    """A class that behaves similarly to the ``print`` function in a python
    except that the message will only be entered if debug mode is active.
    The class contains several attributes for displaying colored text in
    messages, they can be used when formatting the line before the call
    (but in this case, the initialization of the class instance).

    Attributes:
        TAB: One level of tabs in the message.
        BLUE: Blue message color.
        CYAN: Cyan message color.
        GREEN: Green message color.
        WARNING: Orange warning message color.
        FAIL: Red fail message color.
        END: End of message color formatting.
    """
    TAB = ' ' * 2

    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    END = '\033[0m'

    # UNDERLINE = '\033[4m'
    # BOLD = '\033[1m'
    # HEADER = '\033[95m'

    def __init__(self, *args, **kwargs) -> None:
        if _DEBUG:
            args += (log.END,)
            print(*args, **kwargs)


if is_module_used_by_the_addon():
    log(log.CYAN, "{0} {1} Debug mode".format(addon_bl_info()["name"], addon_bl_info()["version"]))
