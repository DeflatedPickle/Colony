#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import tkinter as tk

from .references import *

__title__ = "Entity"
__author__ = "DeflatedPickle"
__version__ = "1.3.4"


class Entity(object):
    """Creates a pawn."""
    def __init__(self, parent, x: int=0, y: int=0, entity_type: str=""):
        self.parent = parent
        self.name = ""
        self.health = 0
        self.total_health = 0

        self.location = {"x": x,
                         "y": y}

        self.selected = False
        self.entity_type = entity_type

        self.entity = None
        self.entity_name = None
        self.entity_health = None
        self.entity_amount = None

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.menu = tk.Menu(self.parent.parent)

        self.parent.parent.update()
        self.parent.parent.update_idletasks()

    def draw(self):
        self.entity = self.parent.canvas.create_text(self.location["x"], self.location["y"], text=get_references()["icons"][self.entity_type], font=get_fonts()[self.entity_type]["normal"], tags=[self])
        if self.entity_type == "pawn":
            self.entity_name = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 17, text="{} {}".format(self.name["forename"], self.name["surname"]), state="disabled", font=get_fonts()["text"]["normal"], tag="extra")
            self.entity_health = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 27, text="{}/{}".format(self.health, self.total_health), state="disabled", font=get_fonts()["text"]["normal"], tag="extra")
        elif self.entity_type == "item":
            pass
            # self.entity_name = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 10, text=self.name, state="disabled", font=get_fonts()["text"]["normal"], tag="extra")
            # self.entity_amount = self.parent.canvas.create_text(self.location["x"], self.location["y"] + 20, text=self.amount, state="disabled", font=get_fonts()["text"]["normal"], tag="extra")

        self.parent.canvas.tag_bind(self.entity, "<ButtonRelease-1>", self.select, "+")
        self.parent.canvas.tag_bind(self.entity, "<Enter>", self.enter, "+")
        self.parent.canvas.tag_bind(self.entity, "<Leave>", self.leave, "+")

        self.parent.canvas.bind("<Button-1>", self.unselect, "+")
        self.parent.canvas.bind("<Button-1>", self.delete_all, "+")

        self.parent.canvas.tag_raise(self)

        return self

    def find_coordinates_own(self):
        return self.parent.canvas.coords(self.entity)

    def find_coordinates_other(self, item):
        return self.parent.canvas.coords(item)

    def set_coordinates(self, x, y):
        self.location["x"] = x
        self.location["y"] = y

    def show_menu(self, event, background: bool=False):
        self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()

        self.delete_all()

        if self.parent.selected_item is not None:
            if background:
                if self.entity_type == "pawn":
                    self.menu.add_command(label="Move Here", command=lambda: self.parent.selected_item.move_to(self.last_mouse_x, self.last_mouse_y, "moving"))
            elif not background:
                if self.entity_type == "pawn":
                    self.menu.add_command(label="Information", command=None)
                elif self.entity_type == "item":
                    self.menu.add_command(label="Pick Up", command=None)

        self.menu.post(event.x_root, event.y_root)

    def delete_all(self, *args):
        try:
            for item in range(self.menu.index("end") + 1):
                self.menu.delete(item)
        except TypeError:
            pass

    def select(self, event=None):
        self.parent.canvas.itemconfigure(self.entity, font=get_fonts()[self.entity_type]["selected"])
        self.parent.canvas.itemconfigure(self.entity_name, font=get_fonts()["text"]["selected"])
        if self.entity_type == "pawn":
            self.parent.canvas.itemconfigure(self.entity_health, font=get_fonts()["text"]["selected"])
        elif self.entity_type == "item":
            self.parent.canvas.itemconfigure(self.entity_amount, font=get_fonts()["text"]["selected"])

        self.parent.selected_item = self
        self.selected = True

    def unselect(self, event):
        self.parent.canvas.itemconfigure(self.entity, font=get_fonts()[self.entity_type]["normal"])
        self.parent.canvas.itemconfigure(self.entity_name, font=get_fonts()["text"]["normal"])
        if self.entity_type == "pawn":
            self.parent.canvas.itemconfigure(self.entity_health, font=get_fonts()["text"]["normal"])
        elif self.entity_type == "item":
            self.parent.canvas.itemconfigure(self.entity_amount, font=get_fonts()["text"]["normal"])

        self.parent.selected_item = None
        self.selected = False

    def enter(self, event):
        self.parent.canvas.configure(cursor="hand2")

        self.parent.canvas.unbind("<Button-3>")
        self.parent.canvas.tag_bind(self.entity, "<ButtonRelease-3>", lambda event: self.show_menu(event, background=False), "+")

    def leave(self, event):
        self.parent.canvas.configure(cursor="arrow")

        self.parent.canvas.bind("<Button-3>", lambda event: self.show_menu(event, background=True))
        self.parent.canvas.tag_unbind(self.entity, "<ButtonRelease-3>")
