#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from colony.entities.actingentity import ActingEntity
from colony.entities.attributes import Limbs
# from .references import get_interval
from colony.references import interval

__title__ = "MovingEntity"
__author__ = "DeflatedPickle"
__version__ = "1.0.3"


class MovingEntity(ActingEntity, Limbs):
    """Creates an entity capable of movement."""

    def __init__(self, parent, x: int = 0, y: int = 0, entity_type: str = "moving entity"):
        ActingEntity.__init__(self, parent, x, y, entity_type)
        Limbs.__init__(self)
        self.parent = parent
        # TODO: Actually use the colonist speed.
        self.move_speed = 2
        # TODO: Add body parts that will have effects if lost.

        self.moving = self.move_until
        self.after_actions.append(self.moving)

    def move_entity(self, x, y):
        """Moves the entity."""
        self.parent.game_area.move(self.entity, x, y)
        self.parent.game_area.move(self.entity_name, x, y)
        self.parent.game_area.move(self.entity_health, x, y)

        self.set_coordinates(self.find_coordinates_own()[0], self.find_coordinates_own()[1])

    def move_to(self, x, y, because):
        self.stop_actions()
        entity_location = self.parent.game_area.coords(self.entity)

        move_x = (x - entity_location[0])
        direction_x = True  # Forwards

        if move_x < 0:
            move_x = abs(move_x)
            direction_x = False  # Backwards

        move_y = (y - entity_location[1])
        direction_y = True  # Down

        if move_y < 0:
            move_y = abs(move_y)
            direction_y = False  # Up

        self.action = because
        self.move_until(x, y, move_x, move_y, direction_x, direction_y)

    def move_until(self, prev_x, prev_y, x, y, direction_x, direction_y):
        self.reached_destination = False

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

        self.decrease_energy(0.02)

        if self.find_coordinates_own() == [prev_x, prev_y]:
            # print("Stopped!")
            self.parent.parent.after_cancel(self.moving)
            if self.action == "going to work":
                self.action = "working"

            else:
                self.action = "standing around"

            self.reached_destination = True

        else:
            # print("Not the same!")
            self.after_actions.remove(self.moving)
            self.moving = self.parent.parent.after(interval.get_interval(), lambda: self.move_until(prev_x, prev_y, x, y, direction_x, direction_y))
            self.after_actions.append(self.moving)
