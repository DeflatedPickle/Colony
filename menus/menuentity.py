#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk

__title__ = "MenuEntity"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class MenuEntity(tk.Menu):
    def __init__(self, parent, **kwagrs):
        tk.Menu.__init__(self, parent, **kwagrs)
        self.parent = parent
