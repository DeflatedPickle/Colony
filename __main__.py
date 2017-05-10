#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import tkinter as tk
from tkinter import ttk

import colony

__title__ = "Colony"
__author__ = "DeflatedPickle"
__version__ = "1.11.0"


class GameWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Colony")
        self.option_add('*tearOff', False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = ResizingCanvas(self)
        self.canvas.grid(row=0, column=0)

        self.start_menu_title()

    def start_menu_title(self):
        self.canvas.create_text(5, 20, text="Colony", anchor="w", font=colony.get_fonts()["menu"]["title"])
        self.canvas.create_text(5, 45, text="A simple colony simulator created by Dibbo, inspired by RimWorld and Dwarf Fortress.", anchor="w", font=colony.get_fonts()["menu"]["subtitle"])

        self.canvas.create_window(5, 70, window=ttk.Button(self.canvas, text="Start", command=self.start_game), anchor="w")
        self.canvas.create_window(5, 100, window=ttk.Button(self.canvas, text="Options"), anchor="w")
        self.canvas.create_window(5, 130, window=ttk.Button(self.canvas, text="Exit"), anchor="w")

    def start_game(self):
        self.canvas.delete("all")
        Game(self)

    def get_mouse_position(self):
        mouse_x_raw = self.winfo_pointerx()
        mouse_y_raw = self.winfo_pointery()

        mouse_x = mouse_x_raw - self.winfo_rootx()
        mouse_y = mouse_y_raw - self.winfo_rooty()

        return mouse_x, mouse_y


class Game(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.entities = []
        self.pawns = []
        self.items = []

        self.canvas = self.parent.canvas

        self.selected_item = None

        debug = DeBug(self)

        pawn = colony.Pawn(self, forename="Frank", surname="Lyatut", gender=True, x=70, y=50).draw()
        pawn_2 = colony.Pawn(self, forename="Ima", surname="Nothrpwn", gender=False, x=130, y=70).draw()
        pawn_random = colony.Pawn(self, x=270, y=130).generate_random().draw()

        item = colony.Item(self, name="Broken Sword", x=250, y=30).draw()
        item_2 = colony.Item(self, name="Wood", x=230, y=90).draw()


class DeBug(object):
    def __init__(self, parent):
        self.parent = parent
        self.counter = 10

        self.update()

    def update(self):
        self.parent.canvas.delete("debug")
        self.counter = 10

        self.add_debug_line(text="Selected: {}".format(self.find_selected()))
        self.add_debug_line(text="Selected Location: {}".format(self.find_selected_location()))
        self.add_debug_line(text="Selected Action: {}".format(None))
        self.add_debug_line(text="Selected Inventory: {}".format(self.find_selected_inventory()))
        self.counter += 15
        self.add_debug_line(text="Pawns: {}".format(len(self.parent.pawns)))
        self.add_debug_line(text="Items: {}".format(len(self.parent.items)))

        self.parent.parent.after(colony.get_interval(), self.update)

    def add_debug_line(self, text: str=""):
        self.parent.canvas.create_text(5, self.counter, anchor="w", text=text, tag="debug")
        self.counter += 15

    def find_selected(self):
        for item in self.parent.entities:
            if item.selected:
                return "{}: {}".format(item.entity_type, item.name if not isinstance(item.name, type(dict())) else "{} {}".format(item.name["forename"], item.name["surname"]))

    def find_selected_location(self):
        for item in self.parent.entities:
            if item.selected:
                return "x={0[0]}, y={0[1]}".format(self.parent.selected_item.find_coordinates_own())

    def find_selected_action(self):
        for item in self.parent.entities:
            if item.selected:
                if item.entity_type == "pawn":
                    return item.action
                elif item.entity_type == "item":
                    return None

    def find_selected_inventory(self):
        for item in self.parent.entities:
            if item.selected:
                if item.entity_type == "pawn":
                    return item.inventory
                elif item.entity_type == "item":
                    return None

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, highlightthickness=0, **kwargs)
        self.parent = parent
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.configure(width=self.parent.winfo_width(), height=self.parent.winfo_height())


def main():
    app = GameWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
