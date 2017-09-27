#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Sound"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class Sound(object):
    """Lets an entity hear sound."""

    def __init__(self, lowest_sound: int=0, highest_sound: int=200, pain_cap: int=140):
        self._lowest_sound = lowest_sound
        self._highest_sound = highest_sound
        self._pain_cap = pain_cap

    def get_lowest_sound(self):
        return self._lowest_sound

    def get_highest_sound(self):
        return self._highest_sound

    def get_pain_cap(self):
        return self._pain_cap
