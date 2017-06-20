#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from _tkinter import TclError
from random import randint

from .entity import Entity
from .references import get_interval

__title__ = "ActingEntity"
__author__ = "DeflatedPickle"
__version__ = "1.0.3"


class ActingEntity(Entity):
    """Creates an entity capable of actions."""

    def __init__(self, parent, x: int = 0, y: int = 0, entity_type: str = "acting entity"):
        Entity.__init__(self, parent, x, y, entity_type)
        self.parent = parent
        self.action = None

        self.actions = []
        self.after_actions = []

    def move_to(self, x, y, because):
        pass

    def check_action(self):
        """Checks the colonists current action."""
        if self.entity_type == "colonist" or self.entity_type == "animal":
            if self.action is None:
                self.action = "standing around"

            elif self.action == "standing around":
                # print("{} is standing around.".format(self.get_name()))
                try:
                    self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()

                except AttributeError:
                    pass

                self.decide_action()

            elif self.action == "wandering":
                # print("{} is wandering.".format(self.get_name()))
                try:
                    try:
                        entity_location = self.parent.game_area.coords(self.entity)
                        self.move_to(entity_location[0] + randint(-15, 15), entity_location[1] + randint(-15, 15), "wandering")
                    except TclError:
                        pass

                except IndexError:
                    pass

                self.decide_action()

            elif self.action == "moving":
                # print("{} is moving.".format(self.get_name()))
                pass

        self.parent.parent.after(get_interval(), self.check_action)

    def decide_action(self):
        """Decides an action for the colonist to perform."""
        random = randint(0, 100)

        if self.entity_type == "colonist" or self.entity_type == "animal":
            if random in range(0, 15):
                # Standing Around
                self.action = "standing around"

            elif random in range(20, 30):
                # Wandering
                self.action = "wandering"

        self.stop_actions()

    def stop_actions(self):
        """Stops all current actions."""
        try:
            for action in self.after_actions:
                self.parent.parent.after_cancel(action)

        except AttributeError:
            pass
