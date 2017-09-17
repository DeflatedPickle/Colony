#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import colony

__title__ = "GameTime"
__author__ = "DeflatedPickle"
__version__ = "1.1.0"


class GameTime(object):
    def __init__(self, parent):
        self.parent = parent

        self._time = colony.Time(0, 0, 0)
        self._date = colony.Time(0, 0, 1)  # Hours = Year, Month = Minute, Day = Seconds.

        # self._time.increase_time(23, 45, 0)

        # self._time.get_seconds().trace_variable("w")

        self.update_time()

    def get_world_time_string(self):
        if 0 <= self._time.get_hours().get() <= 12:
            return "Morning"

        elif 12 <= self._time.get_hours().get() <= 18:
            return "Afternoon"

        elif 18 <= self._time.get_hours().get() <= 24:
            return "Evening"

    def update_time(self):
        self._time.increase_time(0, 0, 1)
        self._time.check_time()

        self.parent.time_frame.time_formatted_variable.set(self._time.get_time_formatted())
        self.parent.time_frame.time_world_variable.set(self.get_world_time_string())

        if self._time.get_hours() == 0 and self._time.get_minutes() == 0 and self._time.get_seconds() == 0:
            self._date.increase_time(0, 0, 1)

        self.parent.parent.after(colony.interval.get_interval(), self.update_time)
