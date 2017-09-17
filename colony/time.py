#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import IntVar

__title__ = "Time"
__author__ = "DeflatedPickle"
__version__ = "1.3.0"


class Time(object):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self._hours = IntVar(value=hours)
        self._minutes = IntVar(value=minutes)
        self._seconds = IntVar(value=seconds)

        self.check_time()

    def get_time(self):
        return int("".join(map(str, [self._hours.get(), self._minutes.get(), self._seconds.get()])))

    def get_time_formatted(self):
        return "{}:{}:{}".format(self._hours.get(), self._minutes.get(), self._seconds.get())

    def get_hours(self):
        return self._hours

    def get_minutes(self):
        return self._minutes

    def get_seconds(self):
        return self._seconds

    def set_time(self, hours, minutes, seconds):
        self._hours.set(hours)
        self._minutes.set(minutes)
        self._seconds.set(seconds)

        self.check_time()

    def increase_time(self, hours, minutes, seconds):
        self._hours.set(self._hours.get() + hours)
        self._minutes.set(self._minutes.get() + minutes)
        self._seconds.set(self._seconds.get() + seconds)

        self.check_time()

    def check_time(self):
        if self._seconds.get() >= 60:
            self._seconds.set(0)
            self._minutes.set(self._minutes.get() + 1)

        if self._minutes.get() >= 60:
            self._minutes.set(0)
            self._hours.set(self._hours.get() + 1)

        if self._hours.get() >= 24:
            self._hours.set(0)
