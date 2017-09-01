#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Joy"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Joy(object):
    """Gives an entity joy."""

    def __init__(self, joy: int=80, lowest_joy: int=0, highest_joy: int=100):
        self._joy = joy
        self._lowest_joy = lowest_joy
        self._highest_joy = highest_joy

    def increase_joy(self, amount):
        self._joy += amount

    def decrease_joy(self, amount):
        self._joy -= amount

    def get_joy(self):
        return self._joy

    def get_lowest_joy(self):
        return self._lowest_joy

    def get_highest_joy(self):
        return self._highest_joy
