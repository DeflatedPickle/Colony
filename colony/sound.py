#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import Canvas
from random import randint

__title__ = "Sound"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Sound(object):
    def __init__(self, producer, canvas: Canvas, sound: int=10):
        self._producer = producer
        self._canvas = canvas
        self._sound = sound

    def create_given_sound(self, sound):
        """Creates a sound at the given sound level."""
        pass

    def create_sound(self):
        """Creates a sound at the set sound level."""
        self.create_given_sound(self._sound)

    def create_random_sound(self):
        """Creates a sound between a little under the set level and a little over it."""
        self.create_given_sound(randint(self._sound - randint(0, 5), self._sound + randint(0, 5)))
