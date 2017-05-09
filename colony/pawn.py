#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from .entity import Entity

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.4.0"


class Pawn(Entity):
    """Creates a pawn."""
    # TODO: Finish this class
    def __init__(self, parent, forename: str="", surname: str="", age: int=0, gender: bool=False, health: int=100, total_health: int=100, x: int=0, y: int=0):
        Entity.__init__(self, parent, x, y, entity_type="pawn")
        self.parent = parent
        self.name = {"forename": forename,
                     "surname": surname}
        self.age = age
        self.gender = gender  # False: Female, True: Male
        self.health = health
        self.total_health = total_health
        self.move_speed = 2

        self.location = {"x": x,
                         "y": y}

        self.selected = False
        self.type = "pawn"

        self.parent.entities.append(self)
        self.parent.pawns.append(self)

        self.draw()

    def move_entity(self, x, y):
        self.parent.canvas.move(self.entity, x, y)
        self.parent.canvas.move(self.entity_name, x, y)
        self.parent.canvas.move(self.entity_health, x, y)

    def move_by(self, x: int=0, y: int=0):
        self.parent.canvas.move(self.entity, x, y)

    def move_to(self, item):
        pawn_location = self.parent.canvas.coords(self.entity)
        item_location = self.parent.canvas.coords(item.entity)

        self.move_entity(pawn_location[0] - item_location[0], pawn_location[1] - item_location[1])

    def move_to_mouse(self):
        pawn_location = self.parent.canvas.coords(self.entity)
        mouse_x, mouse_y = self.parent.get_mouse_position()

        move_x = (mouse_x - pawn_location[0])
        move_y = (mouse_y - pawn_location[1])

        self.move_entity(move_x, move_y)
