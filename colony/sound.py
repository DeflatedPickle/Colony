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
    """Creates a sound in the world."""

    def __init__(self, producer: Entity, canvas: Canvas, sound: int=10, linger: int=100):
        self._producer = producer
        self._canvas = canvas
        self._sound = sound
        self._linger = linger

        self._sound_object = None
        self.dissipate_number = 0

    def draw_sound(self, x0, y0, x1, y1):
        """Draws the sound on the canvas."""
        self._sound_object = self._canvas.create_oval(self._producer.location["x"] - x0,
                                                      self._producer.location["y"] - y0,
                                                      self._producer.location["x"] + x1,
                                                      self._producer.location["y"] + y1,
                                                      tags="sound")

    def create_given_sound(self, sound):
        """Creates a sound at the given sound level."""
        self.draw_sound(sound, sound, sound, sound)

        # self._canvas.master.after(self._linger, self.destroy_sound)
        self._canvas.master.after(self._linger // 2, self.dissipate_sound)

    def create_sound(self):
        """Creates a sound at the set sound level."""
        self.create_given_sound(self._sound)

    def create_random_sound(self):
        """Creates a sound between a little under the set level and a little over it."""
        self.create_given_sound(randint(self._sound - randint(0, 5), self._sound + randint(0, 5)))

    def resize_sound(self, x0, y0, x1, y1):
        """Resizes the sound."""
        self.destroy_sound()
        self.draw_sound(x0, y0, x1, y1)

    def resize_sound_by(self, amount):
        """Resizes the sound by a given amount."""
        self.resize_sound(amount, amount, amount, amount)

    def destroy_sound(self):
        """Destroys a sound."""
        self._canvas.delete(self._sound_object)

    def dissipate_sound(self):
        """Slowly makes the sound get quieter until it's gone."""
        self.dissipate_number += 1

        if self.dissipate_number <= 10:
            self.resize_sound_by(self.dissipate_number * -1)
            self._canvas.master.after(self._linger // 2, self.dissipate_sound)

        else:
            self.destroy_sound()
