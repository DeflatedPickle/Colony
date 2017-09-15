#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from tkinter import ttk
from tkinter import font

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.9.0"


def get_frame_rate():
    return 10


def get_references():
    references = {
        "icons": {
            "colonist": u"\u25AF",  # WHITE VERTICAL RECTANGLE
            "animal": u"\u25AD",  # WHITE RECTANGLE
            "resource": u"\u25B3",  # White Up Pointing Triangle
            "block": u"\u25FB",  # WHITE MEDIUM SQUARE
            "item": u"\u25FD"  # WHITE MEDIUM SMALL SQUARE
        }
    }
    return references


def get_size():
    return 25


def get_fonts():
    family = "Arial"
    fonts = {
        "colonist": {
            "normal": font.Font(family=family, size=get_size()),
            "selected": font.Font(family=family, size=get_size(), weight="bold"),
            "bar_normal": font.Font(family=family, size=get_size() - 5),
            "bar_selected": font.Font(family=family, size=get_size() - 5, weight="bold")
        },
        "animal": {
            "normal": font.Font(family=family, size=get_size()),
            "selected": font.Font(family=family, size=get_size(), weight="bold")
        },
        "resource": {
            "normal": font.Font(family=family, size=get_size() - 9),
            "selected": font.Font(family=family, size=get_size() - 9, weight="bold")
        },
        "item": {
            "normal": font.Font(family=family, size=get_size()),
            "selected": font.Font(family=family, size=get_size(), weight="bold")
        },
        "text": {
            "normal": font.Font(family=family, size=get_size() // 4),
            "selected": font.Font(family=family, size=get_size() // 4, weight="bold"),
            "bar_normal": font.Font(family=family, size=get_size() - 15),
            "bar_selected": font.Font(family=family, size=get_size() - 15, weight="bold")
        },
        "menu": {
            "title": font.Font(family=family, size=get_size(), weight="bold"),
            "subtitle": font.Font(family=family, size=get_size() - 15),
        }
    }
    return fonts


# def get_interval():
#     return 100

# Note: Could probably have just used a tkinter.IntVar for this.
class Interval(object):
    def __init__(self):
        self._interval = 100

    def set_interval(self, value):
        self._interval = value

    def get_interval(self):
        return self._interval

interval = Interval()


def get_male_names():
    # TODO: Add more male names.
    return [
        "Frank", "Dan",  # Random names
        "Tarn", "Zach",  # Dwarf Fortress references
        "Tynan"  # RimWorld references
    ]


def get_female_names():
    # TODO: Add more female names.
    return [
        "Amy", "Shara", "Rose"  # Random names
    ]


def get_nicknames():
    # TODO: Add more nicknames.
    return [
        ""  # Random names
    ]


def get_middle_names():
    # TODO: Add more middle names.
    return [
        ""  # Random names
    ]


def get_surnames():
    # TODO: Add more surnames names.
    return [
        "Wright", "Smith", "Brown",  # Random names
        "Adams",  # Dwarf Fortress references
        "Sylvester"  # RimWorld references
    ]


def get_male_animal_names():
    # TODO: Add more animal names.
    return [
        "Jayson", "Jack"
    ]


def get_female_animal_names():
    # TODO: Add more animal names.
    return [
        "Bella", "Molly"
    ]


def get_male_relationship_types():
    return [
        "fathers", "brothers", "sons"
    ]


def get_female_relationship_types():
    return [
        "mothers", "sisters", "daughters"
    ]


def get_parent_types():
    return [
        "mothers", "fathers"
    ]


def get_sibling_types():
    return [
        "sisters", "brothers"
    ]


def get_child_types():
    return [
        "daughters", "sons"
    ]


class OptionFrame(ttk.Frame):
    def __init__(self, parent, option, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.option = option

        # TODO: Add more options.

        ttk.Checkbutton(self, text="Debugging Mode", variable=self.option.variable_debug).grid(row=0, column=0, sticky="we")
        ttk.Checkbutton(self, text="Scrollbars", variable=self.option.variable_scrollbars).grid(row=1, column=0, sticky="we")
        ttk.Checkbutton(self, text="Grid", variable=self.option.variable_grid).grid(row=2, column=0, sticky="we")
        ttk.Checkbutton(self, text="Grid Highlight", variable=self.option.variable_grid_highlight).grid(row=3, column=0, sticky="we")

        frame_colour = ttk.Frame(self)
        ttk.Label(frame_colour, text="Highlight Colour").grid(row=0, column=0)
        ttk.Combobox(frame_colour, textvariable=self.option.variable_highlight_colour, values=["white", "red", "blue", "yellow", "green", "purple", "orange", "pink"], state="readonly", width=7).grid(row=0, column=1)
        frame_colour.grid(row=4, column=0, sticky="we")

        ttk.Checkbutton(self, text="Extra Speed Arrows", variable=self.option.variable_extra_speed_arrows).grid(row=5, column=0, sticky="we")
