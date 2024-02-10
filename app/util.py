from datetime import datetime, timedelta
import sys

def get_week_str():
    # next monday
    this_week = datetime.now() + timedelta(days=7 - datetime.now().weekday())
    # format as MM/DD
    return this_week.strftime("%m/%d")

def printc(text, color, end="\n"):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    if color not in colors:
        raise ValueError(f"Invalid color '{color}'")

    sys.stdout.write(f"{colors[color]}{text}{colors['reset']}{end}")
    sys.stdout.flush()