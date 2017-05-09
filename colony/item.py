#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from .entity import Entity

__title__ = "Item"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class Item(Entity):
    """Creates an item."""
    # TODO: Finish this class
    def __init__(self, parent, name: str="", x: int=0, y: int=0):
        Entity.__init__(self, parent, x, y, entity_type="item")
        self.parent = parent
        self.name = name

        self.location = {"x": x,
                         "y": y}

        self.type = "item"

        self.parent.entities.append(self)
        self.parent.items.append(self)

        self.draw()
