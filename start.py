#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import ttk
import sys

import colony
from options import Options
from scenarios import Scenarios

__title__ = "Start"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Start(object):
    def __init__(self, parent):
        self.parent = parent

        self.parent.canvas.create_text(5, 5, text="Colony", anchor="nw", font=colony.get_fonts()["menu"]["title"])
        self.parent.canvas.create_text(5, 45, text="A simple colony simulator created by Dibbo, inspired by RimWorld and Dwarf Fortress.", anchor="nw", font=colony.get_fonts()["menu"]["subtitle"])

        self.parent.canvas.create_window(5, 70, window=ttk.Button(self.parent.canvas, text="Start", command=self.start_game), anchor="nw")
        self.parent.canvas.create_window(5, 100, window=ttk.Button(self.parent.canvas, text="Options", command=self.start_options), anchor="nw")
        self.parent.canvas.create_window(5, 130, window=ttk.Button(self.parent.canvas, text="Exit", command=lambda: sys.exit()), anchor="nw")

        self.scenarios = None
        self.options = None

    def start_game(self):
        self.parent.canvas.delete("all")
        self.scenarios = Scenarios(self.parent)

    def start_options(self):
        self.parent.canvas.delete("all")
        self.options = Options(self.parent)
