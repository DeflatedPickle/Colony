#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Event"
__author__ = "DeflatedPickle"
__version__ = "1.10.1"


class Event(object):
    """Creates an event."""

    def __init__(self, parent, name: str = "", type: str = "spawn", contents: dict = {}):
        self.parent = parent
        self.name = name
        self.type = type
        self.contents = contents
