#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Energy"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Energy(object):
    """Gives an entity energy."""

    def __init__(self, energy: int=100, lowest_energy: int=0, highest_energy: int=100):
        self._energy = energy
        self._lowest_energy = lowest_energy
        self._highest_energy = highest_energy

    def increase_energy(self, amount):
        self._energy += amount

    def decrease_energy(self, amount):
        self._energy -= amount

    def get_energy(self):
        return self._energy

    def get_lowest_energy(self):
        return self._lowest_energy

    def get_highest_energy(self):
        return self._highest_energy
