#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from random import randint

from .movingentity import MovingEntity
from .references import get_male_animal_names, get_female_animal_names

__title__ = "Animal"
__author__ = "DeflatedPickle"
__version__ = "1.10.1"


class Animal(MovingEntity):
    """Creates an animal."""

    def __init__(self, parent, species: str = "", name: str = "", age: int = 0, highest_age: int = 10, gender: bool = False, health: int = 100, total_health: int = 100, wild: bool = True, tame_chance: float = 100.0, owner=None, x: int = 0, y: int = 0):
        MovingEntity.__init__(self, parent, x, y, entity_type="animal")
        self.parent = parent
        self.species = species
        self.name = name
        self.age = age
        self.lowest_age = 0
        self.highest_age = highest_age
        self.gender = gender
        self.health = health
        self.total_health = total_health
        self.wild = wild
        self.tame_chance = tame_chance
        self.inventory = []
        self.owner = owner

        self.check_action()

    def draw(self):
        MovingEntity.draw(self)
        self.parent.animals.append(self)

        return self

    def generate_random(self):
        """Generates a random animal."""
        self.gender = randint(0, 1)

        if self.gender:
            self.name = get_male_animal_names()[randint(0, len(get_male_animal_names()) - 1)]

        elif not self.gender:
            self.name = get_female_animal_names()[randint(0, len(get_female_animal_names()) - 1)]

        self.age = randint(self.lowest_age, self.highest_age)

        return self
