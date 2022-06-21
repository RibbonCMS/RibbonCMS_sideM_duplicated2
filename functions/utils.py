""" 簡単な関数の置き場．format_time()とか
"""

import os
import pip
import site
import importlib
from importlib import import_module

from datetime import datetime, timedelta


def format_time(t):
    if t=="":
        return ""
    return (datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)).strftime('%Y年%m月%d日 %H時%M分')

def is_future_than(t1, t2):
    t1 = datetime.strptime(t1, '%Y年%m月%d日 %H時%M分')
    t2 = datetime.strptime(t2, '%Y年%m月%d日 %H時%M分')
    return t1 > t2

def color(text, color):
    class Color():
        BLACK = "\033[0;30m"
        RED = "\033[0;31m"
        GREEN = "\033[0;32m"
        BROWN = "\033[0;33m"
        BLUE = "\033[0;34m"
        PURPLE = "\033[0;35m"
        CYAN = "\033[0;36m"
        LIGHT_GRAY = "\033[0;37m"
        DARK_GRAY = "\033[1;30m"
        LIGHT_RED = "\033[1;31m"
        LIGHT_GREEN = "\033[1;32m"
        YELLOW = "\033[1;33m"
        LIGHT_BLUE = "\033[1;34m"
        LIGHT_PURPLE = "\033[1;35m"
        LIGHT_CYAN = "\033[1;36m"
        LIGHT_WHITE = "\033[1;37m"
        BOLD = "\033[1m"
        FAINT = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        NEGATIVE = "\033[7m"
        CROSSED = "\033[9m"
        END = "\033[0m"
    color = eval(f'Color.{color}')
    return f'{color}{text}{Color.END}'


def import_module_with_install(module):
    path = module.replace('.', '/')
    assert os.path.exists(path), f"Module '{module}' not exists."
    if os.path.exists(f'{path}/requirements.txt'):
        pip.main(['install', '-r', f'{path}/requirements.txt'])
        importlib.reload(site)
    return import_module(module)


