#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from random import randint

from .movingentity import MovingEntity
from .references import get_male_names, get_female_names, get_surnames

__title__ = "Colonist"
__author__ = "DeflatedPickle"
__version__ = "1.10.1"


class Colonist(MovingEntity):
    """Creates a colonist."""
    def __init__(self, parent, species: str="Human", forename: str="", surname: str="", age: int=0, highest_age: int=80,
                 gender: bool=False, health: int=100,
                 total_health: int=100, x: int=0, y: int=0):
        MovingEntity.__init__(self, parent, x, y, entity_type="colonist")
        self.parent = parent
        self.species = species
        # TODO: Add nicknames.
        # TODO: Add middle names.
        self.name = {"forename": forename,
                     "surname": surname}
        self.age = age
        self.lowest_age = 0
        self.highest_age = highest_age
        # NOTE: Maybe use an Enum class instead of a boolean.
        self.gender = gender  # False: Female, True: Male
        self.health = health
        self.total_health = total_health
        self.move_speed = 2
        # TODO: Add more colonist actions.
        self.inventory = []
        # TODO: Add colonist relationships.

        self.parent.colonists.append(self)

        self.check_action()

    def add_to_colonist_bar(self):
        self.parent.colonist_bar.add_colonist(self)

        return self

    def get_name(self):
        """Returns the name of the colonist."""
        return "{} {}".format(self.name["forename"], self.name["surname"])

    def generate_random(self):
        """Generates a random colonist."""
        self.gender = randint(0, 1)

        if self.gender:
            self.name["forename"] = get_male_names()[randint(0, len(get_male_names()) - 1)]

        elif not self.gender:
            self.name["forename"] = get_female_names()[randint(0, len(get_female_names()) - 1)]

        self.name["surname"] = get_surnames()[randint(0, len(get_surnames()) - 1)]
        self.age = randint(self.lowest_age, self.highest_age)

        return self
