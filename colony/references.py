#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from tkinter import font

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


def get_references():
    references = {
        "icons": {
            "pawn": u"\u25AF",  # WHITE VERTICAL RECTANGLE
            "block": u"\u25FB",  # WHITE MEDIUM SQUARE
            "item": u"\u25FD"  # WHITE MEDIUM SMALL SQUARE
        }
    }
    return references


def get_size():
    return 25


def get_fonts():
    fonts = {
        "pawn": {
            "normal": font.Font(family="Arial", size=get_size()),
            "selected": font.Font(family="Arial", size=get_size(), weight="bold")
        },
        "item": {
            "normal": font.Font(family="Arial", size=get_size()),
            "selected": font.Font(family="Arial", size=get_size(), weight="bold")
        },
        "text": {
            "normal": font.Font(family="Arial", size=get_size() // 4),
            "selected": font.Font(family="Arial", size=get_size() // 4, weight="bold")
        }
    }
    return fonts


def get_interval():
    return 100
