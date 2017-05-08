#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from .entity import Entity

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class Pawn(Entity):
    """Creates a pawn."""
    # TODO: Finish this class
    def __init__(self, parent, forename: str="", surname: str="", age: int=0, gender: bool=False, health: int=100, total_health: int=100, x: int=0, y: int=0):
        Entity.__init__(self, parent, x, y, type="pawn")
        self.parent = parent
        self.name = {"forename": forename,
                     "surname": surname}
        self.age = age
        self.gender = gender  # False: Female, True: Male
        self.health = health
        self.total_health = total_health

        self.location = {"x": x,
                         "y": y}

        self.selected = False
        self.type = "pawn"

        self.parent.entities.append(self)
        self.parent.pawns.append(self)

        self.draw()
