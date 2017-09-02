#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import ttk

import colony

__title__ = "Options"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Options(object):
    def __init__(self, parent):
        self.parent = parent
        self.canvas = self.parent.canvas

        self.canvas.bind("<Configure>", self.draw_widgets, "+")

        self.canvas.create_text(5, 5, text="Options", anchor="nw", font=colony.get_fonts()["menu"]["title"])
        self.canvas.create_window(5, 50, window=colony.OptionFrame(self.canvas, self.parent), anchor="nw")

        self.draw_widgets()

    def draw_widgets(self, event=None):
        self.canvas.delete("Widget")

        self.canvas.create_window(5, self.parent.winfo_height() - 30, window=ttk.Button(self.canvas, text="Back", command=self.parent.start_menu_title), anchor="nw", tags="Widget")

        del event
