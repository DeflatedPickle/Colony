#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from colony.time import Time

__title__ = "Age"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Age(object):
    """Gives an entity age."""

    def __init__(self, time: Time, age: int=0, lowest_age: int=0, highest_age: int=0):
        self._time = time
        self._age = age
        self._lowest_age = lowest_age
        self._highest_age = highest_age

    def increase_age(self, amount):
        self._age += amount

    def get_age(self):
        return self._age

    def get_lowest_age(self):
        return self._lowest_age

    def get_highest_age(self):
        return self._highest_age
