#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Inventory"
__author__ = "DeflatedPickle"
__version__ = "1.0.1"


class Inventory(object):
    """Gives an entity an inventory."""

    def __init__(self):
        self._inventory = []

    def get_inventory(self):
        return self._inventory

    def give_item(self, item):
        self._inventory.append(item)

    def remove_item(self, item):
        self._inventory.remove(item)
