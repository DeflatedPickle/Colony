#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from colony.entities.attributes import Age, Health
from colony.entities import Entity
from colony.item import Item
from colony.references import *

__title__ = "Resource"
__author__ = "DeflatedPickle"
__version__ = "1.0.2"


class Resource(Entity, Age, Health):
    """Creates a resource."""

    def __init__(self, parent, name: str = "", health: float = 0.0, resource: Item = None, resource_amount: int = 0,
                 type_: str = "", x: int = 0, y: int = 0):
        Entity.__init__(self, parent, x, y, entity_type="resource")
        Age.__init__(self, parent.time, 1, 0, -1)
        Health.__init__(self)
        self.parent = parent
        self.name = name
        self.health = health
        self.resource = resource
        self.resource_amount = resource_amount
        try:
            self.resource.amount = self.resource_amount
        except AttributeError:
            self.resource_amount = 0
        self.type = type_

    def mark_for_deconstruct(self):
        """Marks the resource for deconstruction."""
        if "deconstruct" not in self.parent.game_area.itemcget(self.entity, "tags"):
            self.entity_deconstruct = self.parent.game_area.create_text(self.location["x"],
                                                                        self.location["y"],
                                                                        text="D",
                                                                        state="disabled",
                                                                        font=get_fonts()["text"]["normal"],
                                                                        tag="extra")

            self.parent.game_area.itemconfigure(self.entity, tag="deconstruct")

    def deconstruct(self):
        """Deconstructs the resource."""
        self.destroy()

        self.resource.location = {"x": self.location["x"],
                                  "y": self.location["y"]}

        self.resource.draw()

    def draw_entity_buttons(self):
        """Draws the buttons for the entity."""
        self.parent.game_area.create_window(48, self.parent.canvas.winfo_height() - 48,
                                            window=ttk.Button(self.parent.parent, text="Deconstruct",
                                                              command=self.mark_for_deconstruct), anchor="nw",
                                            tags="Buttons")

    def remove_entity_buttons(self):
        """Removes the entity buttons."""
        self.parent.game_area.delete("Buttons")

    def decrease_health(self, amount):
        """Decreases the enity by a given amount."""
        Health.decrease_health(self, amount)
        self.parent.game_area.itemconfig(self.entity_health, text="{}/{}".format(self.get_health(), self.get_highest_health()))
        if self.get_health() <= 0:
            self.deconstruct()
