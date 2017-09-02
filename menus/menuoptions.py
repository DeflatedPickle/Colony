#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
import sys
import io

from PIL import Image

import colony

__title__ = "MenuOptions"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class MenuOptions(tk.Menu):
    def __init__(self, parent, **kwagrs):
        tk.Menu.__init__(self, parent, **kwagrs)
        self.parent = parent

        self.add_command(label="Back To Start", command=self.start_menu)
        self.add_command(label="Take Screenshot", command=self.take_screenshot)
        self.add_command(label="Options", command=lambda: colony.OptionWindow(self.parent.parent))
        self.add_command(label="Exit", command=lambda: sys.exit())

    def start_menu(self):
        self.parent.parent.canvas.unbind("<Configure>")
        self.parent.parent.canvas.bind("<Configure>", self.parent.parent.canvas.on_resize)
        self.parent.parent.start_menu_title()

    def take_screenshot(self):
        postscript = self.parent.game.game_area.postscript(colormode="color")

        with Image.open(io.BytesIO(postscript.encode("utf-8"))) as image:
            image.save("./image.jpg")
            image.close()
