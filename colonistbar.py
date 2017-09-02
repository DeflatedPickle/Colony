#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from _tkinter import TclError
from tkinter import ttk

import colony

__title__ = "ColonistBar"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class ColonistBar(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent.parent, **kwargs)
        self.parent = parent

        # TODO: Make the colonist bar wrap to the next line when the the previous line is full of colonists.

        self.colonists = {}
        self.canvas_list = []

    def add_colonist(self, colonist):
        canvas = tk.Canvas(self, width=50, height=50)
        canvas.create_text(25, 20, text=colony.get_references()["icons"]["colonist"], font=colony.get_fonts()["colonist"]["bar_normal"], tag="colonist")
        canvas.create_text(25, 40, text=colonist.get_forename_or_nickname(), anchor="center", font=colony.get_fonts()["text"]["bar_normal"], tag="name")
        canvas.pack(side="left")

        canvas.bind("<ButtonRelease-1>", lambda *args: self.select_colonist(colonist), "+")
        canvas.bind("<Button-1>", self.unselect_colonist, "+")

        self.parent.taskbar.menu_colonists.add_command(label=colonist.get_name(), command=lambda the_colonist=colonist: [self.parent.unselect_all(), the_colonist.select()])
        # self.parent.taskbar.menu_relationships.add_relation(colonist)

        self.colonists[colonist.entity] = canvas
        self.canvas_list.append(canvas)

        return canvas

    def remove_colonist(self, colonist):
        self.colonists[colonist.entity].destroy()
        self.canvas_list.remove(self.colonists[colonist.entity])
        self.colonists.pop(colonist.entity)

        self.parent.game_area.configure(cursor="arrow")

    def select_colonist(self, colonist):
        colonist.select()
        self.select_current_colonist(colonist)

    def unselect_colonist(self, *args):
        self.parent.unselect_all()
        self.unselect_all_colonists()

        del args

    def select_current_colonist(self, colonist):
        self.colonists[colonist.entity].itemconfigure(self.colonists[colonist.entity].find_withtag("colonist"), font=colony.get_fonts()["colonist"]["bar_selected"])
        self.colonists[colonist.entity].itemconfigure(self.colonists[colonist.entity].find_withtag("name"), font=colony.get_fonts()["text"]["bar_selected"])

    def unselect_all_colonists(self):
        for canvas in self.canvas_list:
            try:
                canvas.itemconfigure(canvas.find_withtag("colonist"), font=colony.get_fonts()["colonist"]["bar_normal"])
                canvas.itemconfigure(canvas.find_withtag("name"), font=colony.get_fonts()["text"]["bar_normal"])
            except TclError:
                pass
