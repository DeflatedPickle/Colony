#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from .time import Time

__title__ = "Age"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Age(object):
    """Creates a colonist."""

    def __init__(self, time: Time, age: int=0, lowest_age: int=0, highest_age: int=0):
        self.time = time
        self.age = age
        self.lowest_age = lowest_age
        self.highest_age = highest_age
