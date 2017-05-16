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
    def __init__(self, parent, title: str="", description: str="", contents: dict={}):
        self.parent = parent
        self.title = title
        self.description = description
        self.contents = contents

        self.parent.insert("", "end", text=self.title, values=[self.description, self.contents])
