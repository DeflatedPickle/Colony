#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Gender"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Gender(object):
    """Gives an entity age."""

    def __init__(self):
        self._gender = False

    def get_gender(self):
        return self._gender

    def set_gender(self, gender):
        self._gender = gender
