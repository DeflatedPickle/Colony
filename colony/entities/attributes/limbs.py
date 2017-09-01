#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

__title__ = "Limbs"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Limbs(object):
    """Gives an entity limbs."""

    def __init__(self):
        self.limbs = {}

    def add_limb(self, limb: str):
        self.limbs[limb] = {"damage": 0, "state": 0}

    def damage_limb(self, limb: str, amount: int):
        self.limbs[limb]["damage"] = amount

    def remove_limb(self, limb: str):
        del self.limbs[limb]
