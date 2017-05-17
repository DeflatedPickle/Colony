#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from .entity import Entity

__title__ = "Scenario"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class Scenario(object):
    """Create a new scenario."""
    def __init__(self, parent, widget, title: str="", description: str="", contents: dict={}):
        self.parent = parent
        self.widget = widget
        self.id = self.parent.current_scenarios
        self.title = title
        self.description = description
        self.contents = contents

        self.widget.insert("", "end", text=self.title, values=[self.description, self.contents])
        self.parent.scenario_list.append(self)
        self.parent.current_scenarios += 1
