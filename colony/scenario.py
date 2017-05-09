#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from .entity import Entity

__title__ = "Scenario"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Scenario(object):
    """Create a new scenario."""
    def __init__(self, parent, description: str="", items: list=[]):
        self.parent = parent
        self.description = description
        self.items = items
