#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import Canvas
from random import randint

from colony.entities.entity import Entity

__title__ = "Sound"
__author__ = "DeflatedPickle"
__version__ = "1.0.1"


class Sound(object):
    def __init__(self, producer: Entity, canvas: Canvas, sound: int=10, linger: int=100):
        self._producer = producer
        self._canvas = canvas
        self._sound = sound
        self._linger = linger

        self._sound_object = None

    def create_given_sound(self, sound):
        """Creates a sound at the given sound level."""
        self._sound_object = self._canvas.create_oval(self._producer.location["x"] - sound,
                                                      self._producer.location["y"] - sound,
                                                      self._producer.location["x"] + sound,
                                                      self._producer.location["y"] + sound,
                                                      tags="sound")

        self._canvas.master.after(self._linger, self.destroy_sound)

    def create_sound(self):
        """Creates a sound at the set sound level."""
        self.create_given_sound(self._sound)

    def create_random_sound(self):
        """Creates a sound between a little under the set level and a little over it."""
        self.create_given_sound(randint(self._sound - randint(0, 5), self._sound + randint(0, 5)))

    def resize_sound(self, x0, y0, x1, y1):
        self._canvas.master.coords(self._sound_object, self._producer.location["x"] - x0, self._producer.location["y"] - y0, self._producer.location["x"] + x1, self._producer.location["y"] + y1)

    def resize_sound_by(self, amount):
        self.resize_sound(amount, amount, amount, amount)

    def destroy_sound(self):
        """Destroys a sound."""
        self._canvas.delete(self._sound_object)

    def dissipate_sound(self):
        """Slowly makes the sound quieter till it's gone."""
        pass
