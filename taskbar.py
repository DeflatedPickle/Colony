#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk

import menus

__title__ = "TaskBar"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class TaskBar(ttk.Frame):
    def __init__(self, parent, game, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.game = game

        self.add_button("Construction")

        self.menu_colonists = menus.MenuColonists(self)
        self.add_button("Colonists", self.menu_colonists)

        self.add_button("Animals")
        self.add_button("Wildlife")

        self.menu_relationships = menus.MenuRelationships(self)
        self.add_button("Relationships", self.menu_relationships)

        if self.parent.variable_debug.get():
            self.menu_debug = menus.MenuDebug(self)
            self.add_button("Debug", self.menu_debug)

        self.option_menu = menus.MenuOptions(self)
        self.add_button("Menu", self.option_menu)

    def add_button(self, text: str = "", menu: tk.Menu = None):
        button = ttk.Menubutton(self, text=text, menu=menu, direction="above")
        button.pack(side="left", fill="x", expand=True)

        return button
