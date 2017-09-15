#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from random import randint

from zope.interface import implementer

from colony.entities.attributes import IAge, Health, Inventory, Gender
from colony.entities import MovingEntity
from colony.references import get_male_animal_names, get_female_animal_names

__title__ = "Animal"
__author__ = "DeflatedPickle"
__version__ = "1.10.1"


@implementer(IAge)
class Animal(MovingEntity, Health, Inventory, Gender):
    """Creates an animal."""

    def __init__(self, parent, species: str = "", name: str = "", highest_age: int = 10, wild: bool = True,
                 tame_chance: float = 100.0, owner=None, x: int = 0,
                 y: int = 0):
        MovingEntity.__init__(self, parent, x, y, entity_type="animal")
        Health.__init__(self)
        Inventory.__init__(self)
        Gender.__init__(self)
        self.parent = parent
        self.species = species
        self.name = name
        self.wild = wild
        self.tame_chance = tame_chance
        self.owner = owner

        # Interface Variables
        self._age = 0

        self.check_action()

    def draw(self):
        MovingEntity.draw(self)
        self.parent.animals.append(self)

        return self

    def generate_random(self):
        """Generates a random animal."""
        self.set_gender(randint(0, 1))

        if self.get_gender():
            self.name = get_male_animal_names()[randint(0, len(get_male_animal_names()) - 1)]

        elif not self.get_gender():
            self.name = get_female_animal_names()[randint(0, len(get_female_animal_names()) - 1)]

        self._age = randint(self.get_lowest_age(), self.get_highest_age())

        return self

    # Interface Stuff

    def get_age(self):
        return self._age

    def get_lowest_age(self):
        return 0

    def get_highest_age(self):
        return 100

