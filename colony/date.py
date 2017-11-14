#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from tkinter import IntVar

__title__ = "Date"
__author__ = "DeflatedPickle"
__version__ = "1.0.1"


class Date(object):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self._years = IntVar(value=hours)
        self._months = IntVar(value=minutes)
        self._days = IntVar(value=seconds)

        self.check_time()

    def get_date(self):
        """Returns the date."""
        return int("".join(map(str, [self._years.get(), self._months.get(), self._days.get()])))

    def get_date_formatted(self):
        """Returns the date formatted for readability."""
        return "{}/{}/{}".format(self._years.get(), self._months.get(), self._days.get())

    def get_years(self):
        """Returns the years."""
        return self._years

    def get_months(self):
        """Returns the months."""
        return self._months

    def get_days(self):
        """Returns the days."""
        return self._days

    def set_time(self, years, months, days):
        """Sets the time."""
        if years > 0:
            self._years.set(years)

        if months > 0:
            self._months.set(months)

        if days > 0:
            self._days.set(days)

        self.check_time()

    def increase_time(self, years, months, days):
        """Increases the time by an amount."""
        self.set_time(self._years.get() + years, self._months.get() + months, self._days.get() + days)

        self.check_time()

    def check_time(self):
        """Checks the date and increments it if it's over."""
        if self._days.get() >= 30:
            self._days.set(0)
            self._months.set(self._months.get() + 1)

        if self._months.get() >= 12:
            self._months.set(0)
            self._years.set(self._years.get() + 1)
