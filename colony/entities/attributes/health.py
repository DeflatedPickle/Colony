#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Health"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Health(object):
    """Gives an entity health."""

    def __init__(self, health: int=100, lowest_health: int=0, highest_health: int=100):
        self._health = health
        self._lowest_health = lowest_health
        self._highest_health = highest_health

    def increase_health(self, amount):
        self._health += amount

    def decrease_health(self, amount):
        self._health -= amount

    def get_health(self):
        return self._health

    def get_lowest_health(self):
        return self._lowest_health

    def get_highest_health(self):
        return self._highest_health
