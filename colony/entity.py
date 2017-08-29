#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk
from _tkinter import TclError
from collections import OrderedDict

from .references import *
from .window import InformationWindow

__title__ = "Entity"
__author__ = "DeflatedPickle"
__version__ = "1.6.1"


class Entity(object):
    """Creates an entity."""

    def __init__(self, parent, x: int = 0, y: int = 0, entity_type: str = "entity"):
        self.parent = parent
        self.name = None
        self.health = 0
        self.total_health = 0

        self.location = {"x": x,
                         "y": y}

        self.selected = False
        self.entity_type = entity_type

        if self.entity_type == "colonist":
            self.name = {"forename": None,
                         "surname": None}

        if self.entity_type in ["colonist", "animal"]:
            self.species = None
            self.gender = 0
            self.age = 0

        elif self.entity_type == "item":
            self.amount = None

        self.relationships = {}

        self.entity_values = OrderedDict()
        self.entity_values_basic = OrderedDict()
        self.entity_values["basic"] = self.entity_values_basic

        self.entity = None
        self.entity_name = None
        self.entity_health = None
        self.entity_amount = None

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.menu = tk.Menu(self.parent.parent)

        try:
            self.parent.parent.update()
            self.parent.parent.update_idletasks()

        except TclError:
            pass

    def draw(self):
        """Draws the entity on the canvas."""
        self.entity = self.parent.game_area.create_text(self.location["x"],
                                                        self.location["y"],
                                                        text=get_references()["icons"][self.entity_type],
                                                        font=get_fonts()[self.entity_type]["normal"],
                                                        tags="entity")

        if self.entity_type == "colonist":
            self.entity_name = self.parent.game_area.create_text(self.location["x"],
                                                                 self.location["y"] + 17,
                                                                 text="{} {}".format(self.name["forename"],
                                                                                     self.name["surname"]),
                                                                 state="disabled",
                                                                 font=get_fonts()["text"]["normal"],
                                                                 tag="extra")

            self.entity_health = self.parent.game_area.create_text(self.location["x"],
                                                                   self.location["y"] + 27,
                                                                   text="{}/{}".format(self.health, self.total_health),
                                                                   state="disabled",
                                                                   font=get_fonts()["text"]["normal"],
                                                                   tag="extra")

        elif self.entity_type == "animal":
            self.entity_name = self.parent.game_area.create_text(self.location["x"],
                                                                 self.location["y"] + 10,
                                                                 text=self.name,
                                                                 state="disabled",
                                                                 font=get_fonts()["text"]["normal"],
                                                                 tag="extra")

            self.entity_health = self.parent.game_area.create_text(self.location["x"],
                                                                   self.location["y"] + 20,
                                                                   text="{}/{}".format(self.health, self.total_health),
                                                                   state="disabled",
                                                                   font=get_fonts()["text"]["normal"],
                                                                   tag="extra")

        elif self.entity_type == "item":
            self.entity_name = self.parent.game_area.create_text(self.location["x"],
                                                                 self.location["y"] + 10,
                                                                 text=self.name,
                                                                 state="disabled",
                                                                 font=get_fonts()["text"]["normal"],
                                                                 tag="extra")

            self.entity_amount = self.parent.game_area.create_text(self.location["x"],
                                                                   self.location["y"] + 20,
                                                                   text=self.amount,
                                                                   state="disabled",
                                                                   font=get_fonts()["text"]["normal"],
                                                                   tag="extra")

        elif self.entity_type == "resource":
            self.entity_name = self.parent.game_area.create_text(self.location["x"],
                                                                 self.location["y"] + 15,
                                                                 text=self.name,
                                                                 state="disabled",
                                                                 font=get_fonts()["text"]["normal"],
                                                                 tag="extra")

            self.entity_health = self.parent.game_area.create_text(self.location["x"],
                                                                   self.location["y"] + 20,
                                                                   text="{}/{}".format(self.health, self.total_health),
                                                                   state="disabled",
                                                                   font=get_fonts()["text"]["normal"],
                                                                   tag="extra")

        self.parent.entities[self.entity] = self

        self.parent.game_area.tag_bind(self.entity, "<ButtonRelease-1>", self.select, "+")
        self.parent.game_area.tag_bind(self.entity, "<Enter>", self.enter, "+")
        self.parent.game_area.tag_bind(self.entity, "<Leave>", self.leave, "+")

        self.parent.game_area.bind("<Button-1>", self.unselect, "+")
        self.parent.game_area.bind("<Button-1>", self.delete_all, "+")

        self.parent.game_area.bind("<Button-3>", lambda e: self.show_menu(e, background=True))
        self.parent.game_area.tag_bind(self.entity, "<ButtonRelease-3>", lambda e: self.show_menu(e, background=False),
                                       "+")

        self.parent.game_area.tag_raise(self)

        self.update_values()

        return self

    def get_name(self):
        return self.name

    def update_values(self):
        self.entity_values_basic["name"] = self.get_name()
        if self.entity_type in ["colonist", "animal"]:
            self.entity_values_basic["species"] = self.species
            self.entity_values_basic["gender"] = self.gender
            self.entity_values_basic["age"] = self.age
        self.entity_values_basic["health"] = self.health
        self.entity_values_basic["total health"] = self.total_health

    def destroy(self):
        self.parent.entities.pop(self.entity)
        # print([i for i in self.parent.entities.keys()])
        if self.entity_type == "colonist":
            self.parent.colonists.remove(self)
            # print([i.get_name() for i in self.parent.colonists])
        elif self.entity_type == "item":
            self.parent.items.remove(self)
            # print([i.name for i in self.parent.items])

        self.parent.game_area.delete(self.entity)
        self.parent.game_area.delete(self.entity_name)
        self.parent.game_area.delete(self.entity_health)
        self.parent.game_area.delete(self.entity_amount)

    def find_coordinates_own(self):
        """Returns the coordinates of the entity."""
        return self.parent.game_area.coords(self.entity)

    def set_coordinates(self, x, y):
        """Sets the coordinates of the entity."""
        self.location["x"] = x
        self.location["y"] = y

    def show_menu(self, event, background: bool = False):
        """Shows the menu for the entity."""
        self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()

        self.delete_all()

        if self.parent.selected_entity is not None:
            if background:
                if self.entity_type == "colonist":
                    self.menu.add_command(label="Move Here",
                                          command=lambda: [self.parent.selected_entity[
                                                               self.parent.selected_entity.index(item)].move_to(
                                              self.last_mouse_x,
                                              self.last_mouse_y,
                                              "moving") for item in self.parent.selected_entity])
            elif not background:
                if self.entity_type == "colonist":
                    pass

                elif self.entity_type == "item":
                    self.menu.add_command(label="Pick Up", command=None)

                self.menu.add_command(label="Information",
                                      command=lambda: InformationWindow(self.parent.parent).set_information(self))

        self.menu.post(event.x_root, event.y_root)

    def delete_all(self, *args):
        """Deletes all of the menu items."""
        try:
            for item in range(self.menu.index("end") + 1):
                self.menu.delete(item)
        except TypeError:
            pass

        del args

    def select(self, event=None):
        """Selects the entity."""
        self.parent.game_area.itemconfigure(self.entity, font=get_fonts()[self.entity_type]["selected"])
        self.parent.game_area.itemconfigure(self.entity_name, font=get_fonts()["text"]["selected"])

        if self.entity_type == "colonist":
            self.parent.game_area.itemconfigure(self.entity_health, font=get_fonts()["text"]["selected"])
            self.parent.colonist_bar.select_current_colonist(self)

        elif self.entity_type == "item":
            self.parent.game_area.itemconfigure(self.entity_amount, font=get_fonts()["text"]["selected"])
            self.parent.colonist_bar.unselect_all_colonists()

        if self.entity_type == "resource":
            self.draw_entity_buttons()

        # self.parent.selected_entity = self
        self.parent.selected_entity.append(self)
        self.selected = True

        del event

    def unselect(self, event=None):
        """Unselects the entity."""
        self.parent.game_area.itemconfigure(self.entity, font=get_fonts()[self.entity_type]["normal"])
        self.parent.game_area.itemconfigure(self.entity_name, font=get_fonts()["text"]["normal"])

        if self.entity_type == "colonist":
            self.parent.game_area.itemconfigure(self.entity_health, font=get_fonts()["text"]["normal"])

        elif self.entity_type == "item":
            self.parent.game_area.itemconfigure(self.entity_amount, font=get_fonts()["text"]["normal"])

        try:
            self.remove_entity_buttons()

        except AttributeError:
            pass

        self.parent.colonist_bar.unselect_all_colonists()
        # self.parent.selected_entity = None
        try:
            self.parent.selected_entity.remove(self)
        except ValueError:
            pass
        self.selected = False

        del event

    def enter(self, event):
        self.parent.game_area.configure(cursor="hand2")

        del event

    def leave(self, event):
        self.parent.game_area.configure(cursor="arrow")

        del event
