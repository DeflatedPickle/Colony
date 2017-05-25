#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from random import randint

from .movingentity import MovingEntity
from .references import get_interval, get_male_names, get_female_names, get_surnames

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.9.2"


class Pawn(MovingEntity):
    """Creates a pawn."""
    def __init__(self, parent, forename: str="", surname: str="", age: int=0, gender: bool=False, health: int=100,
                 total_health: int=100, x: int=0, y: int=0):
        MovingEntity.__init__(self, parent, x, y, entity_type="pawn")
        self.parent = parent
        # TODO: Add nicknames.
        # TODO: Add middle names.
        self.name = {"forename": forename,
                     "surname": surname}
        self.age = age
        # NOTE: Maybe use an Enum class instead of a boolean.
        self.gender = gender  # False: Female, True: Male
        self.health = health
        self.total_health = total_health
        self.move_speed = 2
        # TODO: Add more pawn actions.
        self.inventory = []
        # TODO: Add pawn relationships.

        self.parent.pawns.append(self)

        self.check_action()

    def get_name(self):
        """Returns the name of the pawn."""
        return "{} {}".format(self.name["forename"], self.name["surname"])

    def generate_random(self):
        """Generates a random pawn."""
        self.gender = randint(0, 1)

        if self.gender:
            self.name["forename"] = get_male_names()[randint(0, len(get_male_names()) - 1)]

        elif not self.gender:
            self.name["forename"] = get_female_names()[randint(0, len(get_female_names()) - 1)]

        self.name["surname"] = get_surnames()[randint(0, len(get_surnames()) - 1)]
        self.age = randint(14, 90)

        return self

    def check_action(self):
        """Checks the pawns current action."""
        if self.action is None:
            self.action = "standing around"

        elif self.action == "standing around":
            # print("{} is standing around.".format(self.get_name()))
            self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()
            self.decide_action()

        elif self.action == "wandering":
            # print("{} is wandering.".format(self.get_name()))
            try:
                entity_location = self.parent.canvas.coords(self.entity)
                self.move_to(entity_location[0] + randint(-15, 15), entity_location[1] + randint(-15, 15), "wandering")

            except IndexError:
                pass

            self.decide_action()

        elif self.action == "moving":
            # print("{} is moving.".format(self.get_name()))
            pass

        self.parent.parent.after(get_interval(), self.check_action)

    def decide_action(self):
        """Decides an action for the pawn to perform."""
        random = randint(0, 100)

        if random in range(0, 15):
            # Standing Around
            self.action = "standing around"

        elif random in range(20, 30):
            # Wandering
            self.action = "wandering"

        self.stop_actions()
