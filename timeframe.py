#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk

import colony

__title__ = "TimeFrame"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class TimeFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent.parent, **kwargs)
        self.parent = parent

        self.time_formatted_variable = tk.StringVar()
        ttk.Label(self, textvariable=self.time_formatted_variable).grid(row=0, column=0)

        self.time_world_variable = tk.StringVar()
        ttk.Label(self, textvariable=self.time_world_variable).grid(row=1, column=0)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=2, column=0, sticky="nesw")

        ttk.Button(self.frame_buttons, text="< <", command=lambda: colony.interval.set_interval(500), width=3).pack(side="left")
        ttk.Button(self.frame_buttons, text=" < ", command=lambda: colony.interval.set_interval(250), width=3).pack(side="left")

        ttk.Button(self.frame_buttons, text="| |", command=lambda: colony.interval.set_interval(0), width=3, state="disabled").pack(side="left")
        ttk.Button(self.frame_buttons, text=" > ", command=lambda: colony.interval.set_interval(100), width=3).pack(side="left")
        ttk.Button(self.frame_buttons, text="> >", command=lambda: colony.interval.set_interval(50), width=3).pack(side="left")

        self.frame_extra = ttk.Frame(self.frame_buttons)

        ttk.Button(self.frame_extra, text=">>>", command=lambda: colony.interval.set_interval(25), width=4).pack(side="left")
        ttk.Button(self.frame_extra, text=">>>>>", command=lambda: colony.interval.set_interval(15), width=7).pack(side="left")
        ttk.Button(self.frame_extra, text=">>>>>>>>>>>>>>", command=lambda: colony.interval.set_interval(1), width=19).pack(side="left")

        self.extra_arrows()

    def extra_arrows(self):
        if self.parent.parent.variable_extra_speed_arrows.get():
            self.frame_extra.pack(side="left")

        else:
            self.frame_extra.pack_forget()
