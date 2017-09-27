#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Sound"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Sound(object):
    """Gives an entity sound."""

    def __init__(self, sound: int=100, quietest_sound: int=0, loudest_sound: int=100):
        self._sound = sound
        self._quietest_sound = quietest_sound
        self._loudest_sound = loudest_sound

    def increase_sound(self, amount):
        self._sound += amount

    def decrease_sound(self, amount):
        self._sound -= amount

    def get_sound(self):
        return self._sound

    def get_quietest_sound(self):
        return self._quietest_sound

    def get_loudest_sound(self):
        return self._loudest_sound
