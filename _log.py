import os
import ctypes

import bpy

from . import registration


class _log_meta(type):
    @property
    def TAB(cls):
        return cls._TAB

    @property
    def BLUE(cls):
        return cls._BLUE

    @property
    def CYAN(cls):
        return cls._CYAN

    @property
    def GREEN(cls):
        return cls._GREEN

    @property
    def WARNING(cls):
        return cls._WARNING

    @property
    def FAIL(cls):
        return cls._FAIL

    @property
    def END(cls):
        return cls._END


class log(object, metaclass=_log_meta):
    """
    The module also provides opportunities to simplify the debugging and output
    of more detailed messages to the console. It is clear that from the user
    experience for ordinary users it may not be very necessary (usually they do
    not like consoles), this part is focused more on those who will set up
    addons on many computers, etc.

    There is a class :py:class:`log` for outputting such debug messages.
    In order for it to display the message, you must either manually set the
    variable ``_DEBUG`` to a positive value, or put in the root folder of the
    addon an empty file called ``DEBUG``, ``DEBUG.txt``, ``_DEBUG`` or
    ``_DEBUG.txt``.

    .. Note:: This workaround allows to make the addon maintenance faster because
        the developer should not set variable before each public commit. Obvious
        that possible existing file always should be in ``./.gitignore``, so its
        would not present by default on user installations.

    A class behaves similarly to the ``print`` function in a python except that
    the message will only be entered if debug mode is active. The class contains
    several attributes for displaying colored text in messages, they can be used
    when formatting the line before the call (but in this case, the
    initialization of the class instance).

    Attributes:
        TAB (readonly): One level of tabs in the message.
        BLUE (readonly): Blue message color.
        CYAN (readonly): Cyan message color.
        GREEN (readonly): Green message color.
        WARNING (readonly): Orange warning message color.
        FAIL (readonly): Red fail message color.
        END (readonly): End of message color formatting.
    """
    _TAB = ' ' * 2
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _WARNING = '\033[93m'
    _FAIL = '\033[91m'

    _END = '\033[0m'

    def __init__(self, *args, **kwargs) -> None:
        if registration.is_debug():
            if os.name == 'nt':
                w32dll = ctypes.windll.kernel32
                w32dll.SetConsoleMode(w32dll.GetStdHandle(-11), 7)

            args += (log.END,)
            print(*args, **kwargs)
