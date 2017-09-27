#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from colony.entities.entity import Entity
from .animal import Animal
# from .actingentity import ActingEntity
# from .movingentity import MovingEntity
from .colonist import Colonist
from .item import Item
from .references import *
from .resource import Resource
# TODO: Add a Weapon class.
# TODO: Add an Armour class.
from .scenario import Scenario
from .time import Time
from .date import Date
from .sound import Sound
# TODO: Add an Event class.
# TODO: Add a Zone class.
from .window import OptionWindow, InformationWindow, RelationshipsWindow

__title__ = "Colony"

__author__ = "DeflatedPickle/Dibbo"
__copyright__ = "Copyright (c) 2017 Dibbo"
__credits__ = ["DeflatedPickle/Dibbo"]

__license__ = "MIT"
__version__ = "1.16.0"
__maintainer__ = "DeflatedPickle/Dibbo"
__email__ = "DeflatedPickle@gmail.com"
__status__ = "Development"
