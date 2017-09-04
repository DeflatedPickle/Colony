#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from _tkinter import TclError
import random

from colony.entities.entity import Entity
# from .references import get_interval
from colony.references import interval

__title__ = "ActingEntity"
__author__ = "DeflatedPickle"
__version__ = "1.1.3"


class ActingEntity(Entity):
    """Creates an entity capable of actions."""

    def __init__(self, parent, x: int = 0, y: int = 0, entity_type: str = "acting entity"):
        Entity.__init__(self, parent, x, y, entity_type)
        self.parent = parent
        self.action = None
        self.working_on = None

        self.reached_destination = False
        self._move_direction = False

        self.actions = []
        self.after_actions = []

        self.waiting_actions = ["standing around", "wandering"]
        self.looking_actions = ["looking for work"]
        self.doing_actions = ["chopping a tree", "mining a rock"]

    def move_to(self, x, y, because):
        pass

    def look_for_closest(self, x, y, tag):
        # Credit: User9123 on StackOverflow
        canvas = tk.Canvas(self.parent.parent)

        for entity in self.parent.game_area.find_withtag(tag):
            if self.parent.game_area.type(entity) == "text":
                text = canvas.create_text

                config = {opt: self.parent.game_area.itemcget(entity, opt) for opt in self.parent.game_area.itemconfig(entity)}
                config["tags"] = str(entity)
                text(*self.parent.game_area.coords(entity), **config)

                item = canvas.find_closest(x, y)

                if item:
                    item = int(canvas.gettags(*item)[0])

                else:
                    item = None

                return item

            else:
                continue

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
                        self.move_to(entity_location[0] + random.randint(-15, 15), entity_location[1] + random.randint(-15, 15), "wandering")
                    except TclError:
                        pass

                except IndexError:
                    pass

                self.decide_action()

            elif self.action == "moving":
                # print("{} is moving.".format(self.get_name()))
                pass

            elif self.action == "looking for work":
                closest = self.look_for_closest(self.location["x"], self.location["y"], "deconstruct")
                # print(self.parent.game_area.gettags(closest))
                # print(closest)

                if closest is not None and "taken by {}".format(self.entity) not in self.parent.game_area.gettags(closest):
                    coords = self.parent.game_area.coords(closest)

                    x, y = coords
                    if self.entity is not None:
                        self.move_to(x, y, "going to work")
                        self.parent.game_area.itemconfig(closest, tags=self.parent.game_area.itemcget(closest, "tags") + "taken by {}".format(self.entity))
                        self.working_on = self.parent.canvas_ids[closest]

                else:
                    self.decide_action()

            elif self.action == "working":
                if self._move_direction:
                    # print("Forwards")
                    self.move_to(self.location["x"] + 5, self.location["y"], "going to work")

                    if self.working_on.get_health() > 0:
                        self.working_on.decrease_health(5)
                    else:
                        self.action = "standing around"

                    self._move_direction = False

                elif not self._move_direction:
                    # print("Backwards")
                    self.move_to(self.location["x"] - 5, self.location["y"], "going to work")
                    self._move_direction = True

        self.parent.parent.after(interval.get_interval(), self.check_action)

    def decide_action(self):
        """Decides an action for the colonist to perform."""
        random_number = random.randint(0, 100)

        if self.entity_type == "colonist" or self.entity_type == "animal":
            if self.action in self.waiting_actions:
                self.action = "looking for work"

            elif random_number in range(0, 15):
                # Standing Around
                self.action = "standing around"

            elif random_number in range(20, 30):
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
