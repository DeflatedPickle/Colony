#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from random import randint

from .entity import Entity
from .references import get_interval, get_male_names, get_female_names, get_surnames

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.9.0"


class Pawn(Entity):
    """Creates a pawn."""
    def __init__(self, parent, forename: str="", surname: str="", age: int=0, gender: bool=False, health: int=100,
                 total_health: int=100, x: int=0, y: int=0):
        Entity.__init__(self, parent, x, y, entity_type="pawn")
        self.parent = parent
        self.name = {"forename": forename,
                     "surname": surname}
        self.age = age
        # NOTE: Maybe use an Enum class instead of a boolean.
        self.gender = gender  # False: Female, True: Male
        self.health = health
        self.total_health = total_health
        self.move_speed = 2
        self.action = None
        self.inventory = []

        self.parent.entities.append(self)
        self.parent.pawns.append(self)

        self.move_x = 0
        self.move_y = 0

        self.direction_x = True
        self.direction_y = True

        self.check_action()

    def get_name(self):
        return "{} {}".format(self.name["forename"], self.name["surname"])

    def move_entity(self, x, y):
        self.parent.canvas.move(self.entity, x, y)
        self.parent.canvas.move(self.entity_name, x, y)
        self.parent.canvas.move(self.entity_health, x, y)

        self.set_coordinates(self.find_coordinates_own()[0], self.find_coordinates_own()[1])

    def move_to(self, x, y, because):
        self.stop_actions()
        pawn_location = self.parent.canvas.coords(self.entity)
        # mouse_x, mouse_y = self.parent.parent.get_mouse_position()

        move_x = (x - pawn_location[0])
        self.direction_x = True  # Forwards
        if move_x < 0:
            move_x = abs(move_x)
            self.direction_x = False  # Backwards
        move_y = (y - pawn_location[1])
        self.direction_y = True  # Down
        if move_y < 0:
            move_y = abs(move_y)
            self.direction_y = False  # Up

        self.action = because
        self.move_until(x, y, move_x, move_y)

    def move_until(self, prev_x, prev_y, x, y):
        if self.find_coordinates_own()[0] != self.last_mouse_x:
            # print("X: {}\nPrev X: {}".format(x, prev_x))
            if x < prev_x and self.direction_x:
                # print("Moved right.")
                self.move_entity(1, 0)
                x -= 1

            elif x < prev_x and not self.direction_x:
                # print("Moved left.")
                self.move_entity(-1, 0)
                x -= 1

        if self.find_coordinates_own()[1] != self.last_mouse_y:
            # print("Y: {}\nPrev Y: {}".format(y, prev_y))
            if y < prev_y and self.direction_y:
                # print("Moved down.")
                self.move_entity(0, 1)
                y -= 1

            elif y < prev_y and not self.direction_y:
                # print("Moved up.")
                self.move_entity(0, -1)
                y -= 1

        if self.find_coordinates_own() == [prev_x, prev_y]:
            # print("Stopped!")
            self.parent.parent.after_cancel(self.moving)
            self.action = "standing around"

        else:
            self.moving = self.parent.parent.after(get_interval(), lambda: self.move_until(prev_x, prev_y, x, y))

    def generate_random(self):
        self.gender = randint(0, 1)
        if self.gender:
            self.name["forename"] = get_male_names()[randint(0, len(get_male_names()) - 1)]
        elif not self.gender:
            self.name["forename"] = get_female_names()[randint(0, len(get_female_names()) - 1)]
        self.name["surname"] = get_surnames()[randint(0, len(get_surnames()) - 1)]
        self.age = randint(14, 90)

        return self

    def check_action(self):
        if self.action is None:
            self.action = "standing around"

        elif self.action == "standing around":
            # print("{} is standing around.".format(self.get_name()))
            self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()
            self.decide_action()

        elif self.action == "wandering":
            # print("{} is wandering.".format(self.get_name()))
            try:
                self.move_to(self.parent.canvas.coords(self.entity)[0] + randint(-15, 15), self.parent.canvas.coords(self.entity)[1] + randint(-15, 15), "wandering")
            except IndexError:
                pass
            self.decide_action()

        elif self.action == "moving":
            # print("{} is moving.".format(self.get_name()))
            pass

        self.parent.parent.after(get_interval(), self.check_action)

    def decide_action(self):
        random = randint(0, 100)
        if random in range(0, 15):
            # Standing Around
            self.action = "standing around"
        elif random in range(20, 30):
            # Wandering
            self.action = "wandering"

        self.stop_actions()

    def stop_actions(self):
        try:
            self.parent.parent.after_cancel(self.moving)
        except AttributeError:
            pass
