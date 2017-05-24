#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

from random import randint

from .entity import Entity
from .references import get_interval, get_male_names, get_female_names, get_surnames

__title__ = "Pawn"
__author__ = "DeflatedPickle"
__version__ = "1.9.2"


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
        # TODO: Add more pawn actions.
        self.action = None
        self.inventory = []
        # TODO: Add pawn relationships.

        self.parent.pawns.append(self)

        self.move_x = 0
        self.move_y = 0

        self.moving = self.move_until

        self.check_action()

    def get_name(self):
        """Returns the name of the pawn."""
        return "{} {}".format(self.name["forename"], self.name["surname"])

    def move_entity(self, x, y):
        """Moves the pawn."""
        self.parent.canvas.move(self.entity, x, y)
        self.parent.canvas.move(self.entity_name, x, y)
        self.parent.canvas.move(self.entity_health, x, y)

        self.set_coordinates(self.find_coordinates_own()[0], self.find_coordinates_own()[1])

    def move_to(self, x, y, because):
        self.stop_actions()
        pawn_location = self.parent.canvas.coords(self.entity)

        move_x = (x - pawn_location[0])
        direction_x = True  # Forwards

        if move_x < 0:
            move_x = abs(move_x)
            direction_x = False  # Backwards

        move_y = (y - pawn_location[1])
        direction_y = True  # Down

        if move_y < 0:
            move_y = abs(move_y)
            direction_y = False  # Up

        self.action = because
        self.move_until(x, y, move_x, move_y, direction_x, direction_y)

    def move_until(self, prev_x, prev_y, x, y, direction_x, direction_y):
        try:
            if self.find_coordinates_own()[0] != prev_x:
                # print("X: {}\nPrev X: {}".format(x, prev_x))
                if x < prev_x and direction_x:
                    # print("Moved right.")
                    self.move_entity(1, 0)
                    x -= 1

                elif x < prev_x and not direction_x:
                    # print("Moved left.")
                    self.move_entity(-1, 0)
                    x -= 1

        except IndexError:
            pass

        try:
            if self.find_coordinates_own()[1] != prev_y:
                # print("Y: {}\nPrev Y: {}".format(y, prev_y))
                if y < prev_y and direction_y:
                    # print("Moved down.")
                    self.move_entity(0, 1)
                    y -= 1

                elif y < prev_y and not direction_y:
                    # print("Moved up.")
                    self.move_entity(0, -1)
                    y -= 1

        except IndexError:
            pass

        if self.find_coordinates_own() == [prev_x, prev_y]:
            # print("Stopped!")
            self.parent.parent.after_cancel(self.moving)
            self.action = "standing around"

        else:
            self.moving = self.parent.parent.after(get_interval(), lambda: self.move_until(prev_x, prev_y, x, y,
                                                                                           direction_x, direction_y))

    def generate_random(self):
        """Generates a random pawn."""
        self.gender = randint(0, 1)

        if self.gender:
            self.name["forename"] = get_male_names()[randint(0, len(get_male_names()) - 1)]

        elif not self.gender:
            self.name["forename"] = get_female_names()[randint(0, len(get_female_names()) - 1)]

        self.name["surname"] = get_surnames()[randint(0, len(get_surnames()) - 1)]
        self.age = randint(14, 90)

        return self

    def check_action(self):
        """Checks the pawns current action."""
        if self.action is None:
            self.action = "standing around"

        elif self.action == "standing around":
            # print("{} is standing around.".format(self.get_name()))
            self.last_mouse_x, self.last_mouse_y = self.parent.parent.get_mouse_position()
            self.decide_action()

        elif self.action == "wandering":
            # print("{} is wandering.".format(self.get_name()))
            try:
                entity_location = self.parent.canvas.coords(self.entity)
                self.move_to(entity_location[0] + randint(-15, 15), entity_location[1] + randint(-15, 15), "wandering")

            except IndexError:
                pass
            self.decide_action()

        elif self.action == "moving":
            # print("{} is moving.".format(self.get_name()))
            pass

        self.parent.parent.after(get_interval(), self.check_action)

    def decide_action(self):
        """Decides an action for the pawn to perform."""
        random = randint(0, 100)

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
            self.parent.parent.after_cancel(self.moving)

        except AttributeError:
            pass
