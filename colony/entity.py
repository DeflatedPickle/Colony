#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import tkinter as tk

from .references import *

__title__ = "Entity"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Entity(object):
    """Creates a pawn."""
    # TODO: Finish this class
    def __init__(self, parent, x: int=0, y: int=0, type: str=""):
        self.parent = parent
        self.name = ""
        self.health = 0
        self.total_health = 0

        self.location = {"x": x,
                         "y": y}

        self.selected = False
        self.type = type

        self.entity = None
        self.entity_name = None
        self.entity_health = None

        self.menu = tk.Menu(self.parent)

    def draw(self):
        self.entity = self.parent.canvas.create_text(self.location["x"], self.location["y"], text=get_references()["icons"][self.type], font=get_fonts()[self.type]["normal"])
        if self.type == "pawn":
            self.entity_name = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 17, text="{} {}".format(self.name["forename"], self.name["surname"]), font=get_fonts()["text"]["normal"])
            self.entity_health = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 27, text="{}/{}".format(self.health, self.total_health), font=get_fonts()["text"]["normal"])
        elif self.type == "item":
            self.entity_name = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 10, text=self.name, font=get_fonts()["text"]["normal"])

        self.parent.canvas.tag_bind(self.entity, "<ButtonRelease-1>", self.select, "+")
        self.parent.canvas.tag_bind(self.entity, "<Button-3>", self.show_menu, "+")
        self.parent.canvas.tag_bind(self.entity, "<Enter>", self.enter, "+")
        self.parent.canvas.tag_bind(self.entity, "<Leave>", self.leave, "+")

        self.parent.canvas.bind("<Button-1>", self.unselect, "+")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def select(self, event):
        self.parent.canvas.itemconfigure(self.entity, font=get_fonts()[self.type]["selected"])
        self.parent.canvas.itemconfigure(self.entity_name, font=get_fonts()["text"]["selected"])
        if self.type == "pawn":
            self.parent.canvas.itemconfigure(self.entity_health, font=get_fonts()["text"]["selected"])

        self.selected = True

    def unselect(self, event):
        self.parent.canvas.itemconfigure(self.entity, font=get_fonts()[self.type]["normal"])
        self.parent.canvas.itemconfigure(self.entity_name, font=get_fonts()["text"]["normal"])
        if self.type == "pawn":
            self.parent.canvas.itemconfigure(self.entity_health, font=get_fonts()["text"]["normal"])

        self.selected = False

    def enter(self, event):
        self.parent.canvas.configure(cursor="hand2")

    def leave(self, event):
        self.parent.canvas.configure(cursor="arrow")
