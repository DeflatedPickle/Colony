#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Time"
__author__ = "DeflatedPickle"
__version__ = "1.3.0"


class Time(object):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

        self.check_time()

    def get_time(self):
        return int("".join(map(str, [self._hours, self._minutes, self._seconds])))

    def get_time_formatted(self):
        return "{}:{}:{}".format(self._hours, self._minutes, self._seconds)

    def get_hours(self):
        return self._hours

    def get_minutes(self):
        return self._minutes

    def get_seconds(self):
        return self._seconds

    def set_time(self, hours, minutes, seconds):
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

        self.check_time()

    def increase_time(self, hours, minutes, seconds):
        self._hours += hours
        self._minutes += minutes
        self._seconds += seconds

        self.check_time()

    def check_time(self):
        if self._seconds >= 60:
            self._seconds = 0
            self._minutes += 1

        if self._minutes >= 60:
            self._minutes = 0
            self._hours += 1

        if self._hours >= 24:
            self._hours = 0
