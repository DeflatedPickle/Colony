#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from .item import Item
from .entity import Entity
from .references import *

__title__ = "Resource"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Resource(Entity):
    """Creates a resource."""

    def __init__(self, parent, name: str = "", health: float = 0.0, resource: Item = None, resource_amount: int = 0, type_: str = "", x: int = 0, y: int = 0):
        Entity.__init__(self, parent, x, y, entity_type="resource")
        self.parent = parent
        self.name = name
        self.health = health
        self.resource = resource
        self.resource_amount = resource_amount
        self.resource.amount = self.resource_amount
        self.type = type_

    def mark_for_deconstruct(self):
        self.parent.game_area.create_text(self.location["x"],
                                          self.location["y"],
                                          text="D",
                                          state="disabled",
                                          font=get_fonts()["text"]["normal"],
                                          tag="extra")

    def deconstruct(self):
        self.destroy()
        self.resource.draw()

    def draw_entity_buttons(self):
        self.parent.game_area.create_window(48, self.parent.canvas.winfo_height() - 48, window=ttk.Button(self.parent.parent, text="Deconstruct", command=self.mark_for_deconstruct), anchor="nw", tags="Buttons")

    def remove_entity_buttons(self):
        self.parent.game_area.delete("Buttons")
