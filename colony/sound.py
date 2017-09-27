#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from random import randint

__title__ = "Sound"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Sound(object):
    def __init__(self, sound: int=10):
        self._sound = sound

    def create_sound(self):
        """Creates a sound at the set sound level."""
        pass

    def create_random_sound(self):
        """Creates a sound between a little under the set level and a little over it."""
        pass
