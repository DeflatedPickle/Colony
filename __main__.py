#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import tkinter as tk

import colony

__title__ = "Colony"
__author__ = "DeflatedPickle"
__version__ = "1.4.0"


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Colony")
        self.option_add('*tearOff', False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Motion>", self.update_mouse)

        self.entities = []
        self.pawns = []
        self.items = []

        self.mouse_x = 0
        self.mouse_y = 0

        self.selected_pawn = None

        debug = DeBug(self)

        pawn = colony.Pawn(self, forename="Frank", surname="Lyatut", gender=True, x=70, y=50)
        pawn2 = colony.Pawn(self, forename="Ima", surname="Nothrpwn", gender=False, x=130, y=70)

        item = colony.Item(self, name="Broken Sword", x=250, y=30)
        item2 = colony.Item(self, name="Wood", x=230, y=90)

    def update_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y


class DeBug(object):
    def __init__(self, parent):
        self.parent = parent

        self.update()

    def update(self, interval=colony.get_interval()):
        self.parent.canvas.delete("debug")

        self.parent.canvas.create_text(5, 10, anchor="w", text="Selected: {}".format(self.find_selected()), tag="debug")
        self.parent.canvas.create_text(5, 25, anchor="w", text="Pawns: {}".format(len(self.parent.pawns)), tag="debug")
        self.parent.canvas.create_text(5, 40, anchor="w", text="Items: {}".format(len(self.parent.items)), tag="debug")

        self.parent.after(interval, self.update)

    def find_selected(self):
        for item in self.parent.entities:
            if item.selected:
                return "{}: {}".format(item.type, item.name if not isinstance(item.name, type(dict())) else "{} {}".format(item.name["forename"], item.name["surname"]))


def main():
    app = Window()
    app.mainloop()

if __name__ == "__main__":
    main()
