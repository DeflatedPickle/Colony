#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from .entity import Entity

__title__ = "Item"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class Item(Entity):
    """Creates an item."""

    def __init__(self, parent, name: str = "", stack_size: int = 100, amount: int = 0, x: int = 0, y: int = 0):
        Entity.__init__(self, parent, x, y, entity_type="item")
        self.parent = parent
        self.name = name
        self.stack_size = stack_size
        self.amount = amount

    def draw(self):
        Entity.draw(self)
        self.parent.items.append(self)
