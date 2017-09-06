#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import colony

__title__ = "GameTime"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class GameTime(object):
    def __init__(self, parent):
        self.parent = parent

        self._time = colony.Time(0, 0, 0)
        # self._date = colony.Time(0, 0, 0)

        self.update_time()

    def get_world_time_string(self):
        if 0 <= self._time._hours <= 12:
            return "Morning"

        elif 12 <= self._time._hours <= 18:
            return "Afternoon"

        elif 18 <= self._time._hours <= 24:
            return "Evening"

    def update_time(self):
        self._time._seconds += 1
        self._time.check_time()

        self.parent.time_frame.time_formatted_variable.set(self._time.get_time_formatted())
        self.parent.time_frame.time_world_variable.set(self.get_world_time_string())

        self.parent.parent.after(colony.interval.get_interval(), self.update_time)
