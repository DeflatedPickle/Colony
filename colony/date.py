#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import IntVar

__title__ = "Date"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Date(object):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self._years = IntVar(value=hours)
        self._months = IntVar(value=minutes)
        self._days = IntVar(value=seconds)

        self.check_time()

    def get_date(self):
        return int("".join(map(str, [self._years.get(), self._months.get(), self._days.get()])))

    def get_date_formatted(self):
        return "{}/{}/{}".format(self._years.get(), self._months.get(), self._days.get())

    def get_years(self):
        return self._years

    def get_months(self):
        return self._months

    def get_days(self):
        return self._days

    def set_time(self, years, months, days):
        self._years.set(years)
        self._months.set(months)
        self._days.set(days)

        self.check_time()

    def increase_time(self, years, months, days):
        self._years.set(self._years.get() + years)
        self._months.set(self._months.get() + months)
        self._days.set(self._days.get() + days)

        self.check_time()

    def check_time(self):
        if self._days.get() >= 30:
            self._days.set(0)
            self._months.set(self._months.get() + 1)

        if self._months.get() >= 12:
            self._months.set(0)
            self._years.set(self._years.get() + 1)
