#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from random import randint

from .entity import Entity
from .references import get_male_names, get_female_names, get_surnames

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.5.1"


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
        self.action = None
        self.inventory = []

        self.location = {"x": x,
                         "y": y}

        self.parent.entities.append(self)
        self.parent.pawns.append(self)

    def move_entity(self, x, y):
        self.parent.canvas.move(self.entity, x, y)
        self.parent.canvas.move(self.entity_name, x, y)
        self.parent.canvas.move(self.entity_health, x, y)

        self.set_coordinates(self.find_coordinates_own()[0], self.find_coordinates_own()[1])

    def move_by(self, x: int=0, y: int=0):
        self.parent.canvas.move(self.entity, x, y)

    def move_to(self, item):
        pawn_location = self.parent.canvas.coords(self.entity)
        item_location = self.parent.canvas.coords(item.entity)

        self.move_entity(item_location[0] - pawn_location[0], item_location[1] - pawn_location[1])

    def move_to_mouse(self):
        pawn_location = self.parent.canvas.coords(self.entity)
        mouse_x, mouse_y = self.parent.parent.get_mouse_position()

        move_x = (mouse_x - pawn_location[0])
        move_y = (mouse_y - pawn_location[1])

        self.move_entity(move_x, move_y)

    def generate_random(self):
        self.gender = randint(0, 1)
        if self.gender:
            self.name["forename"] = get_male_names()[randint(0, len(get_male_names()) - 1)]
        elif not self.gender:
            self.name["forename"] = get_female_names()[randint(0, len(get_female_names()) - 1)]
        self.name["surname"] = get_surnames()[randint(0, len(get_surnames()) - 1)]
        self.age = randint(14, 90)

        return self
