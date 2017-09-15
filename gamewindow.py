#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk

from resizingcanvas import ResizingCanvas
from start import Start

__title__ = "GameWindow"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class GameWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Colony")
        self.geometry("650x300")
        self.option_add('*tearOff', False)

        self.minsize(400, 300)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.game_width = 500
        self.game_height = 500

        self.canvas = ResizingCanvas(self)
        self.canvas.grid(row=0, column=0)
        self.background = self.canvas["background"]

        self.variable_debug = tk.BooleanVar(value=0)
        self.variable_scrollbars = tk.BooleanVar(value=1)
        self.variable_grid = tk.BooleanVar(value=0)
        self.variable_grid_highlight = tk.BooleanVar(value=0)
        self.variable_highlight_colour = tk.StringVar(value="white")
        self.variable_extra_speed_arrows = tk.BooleanVar(value=0)

        self.start = None

        self.start_menu_title()

    def start_menu_title(self):
        self.canvas.delete("all")
        self.canvas.configure(background=self.background)
        self.canvas.unbind("<Configure>")
        self.canvas.bind("<Configure>", self.canvas.on_resize)

        try:
            self.after_cancel(self.debug_update)
        except AttributeError:
            pass

        self.start = Start(self)

    def get_mouse_position(self):
        try:
            mouse_x_raw = self.start.scenarios.game.game_area.winfo_pointerx()
            mouse_y_raw = self.start.scenarios.game.game_area.winfo_pointery()

            mouse_x = mouse_x_raw - self.start.scenarios.game.game_area.winfo_rootx()
            mouse_y = mouse_y_raw - self.start.scenarios.game.game_area.winfo_rooty()

            return mouse_x, mouse_y

        except AttributeError:
            return [0, 0], [0, 0]
