import sys
from typing import Callable, Optional

import colors


def log(fmt: str,
        *args,
        file=sys.stderr,
        color: Optional[Callable[[str], str]] = None,
        **kwargs,
        ):
    """Print a log message.

    Formats the message with the given arguments and keyword arguments, and
    prints it to the given file. If a color function is given, the message is
    transformed with it before printing.
    
    :file: The file to print to. Defaults to stderr.
    :color: A function that takes a string and returns a colorized string (with ANSI escape codes).
    """

    s = fmt.format(*args, **kwargs)

    if color:
        s = color(s)

    print(s, file=file)


def debug(fmt: str, *args, **kwargs):
    log('[debug] ' + fmt, *args, **kwargs)


def info(fmt: str, *args, **kwargs):
    log('[info] ' + fmt, *args, **kwargs)


def warn(fmt: str, *args, **kwargs):
    log('[warn] ' + fmt, color=colors.yellow, *args, **kwargs)


def err(fmt: str, *args, **kwargs):
    log('[err]  ' + fmt, color=colors.red, *args, **kwargs)
