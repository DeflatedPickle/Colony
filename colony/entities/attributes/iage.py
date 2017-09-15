#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from zope.interface import Interface

__title__ = "Age"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class IAge(Interface):
    """Gives an entity age."""

    def get_age(self):
        """Gets the age."""

    def set_age(self, amount):
        """Sets the age."""

    def get_lowest_age(self):
        """Gets the lowest age."""

    def get_highest_age(self):
        """Gets the highest age."""
