#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk
from string import capwords

import pkinter as pk
from .references import OptionFrame

__title__ = "Window"
__author__ = "DeflatedPickle"
__version__ = "1.3.0"


class BaseWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.resizable(False, False)
        self.geometry("200x250")
        self.transient(parent)
        self.grab_set()

        self.current_row = 0

        self.frame_widget = ttk.Frame(self)
        self.frame_widget.pack(fill="both", expand=True)
        self.frame_widget.rowconfigure(0, weight=1)
        self.frame_widget.columnconfigure(0, weight=1)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.pack(fill="x")
        ttk.Button(self.frame_buttons, text="Close", command=self.close).pack(side="left")

        self.parent.bind("<Configure>", self.center)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.center()

    def center(self, event=None):
        pk.center_on_parent(self)

        del event

    def close(self):
        self.parent.unbind("<Configure>")
        self.destroy()

    def create_label(self, parent, title_text, value_text):
        ttk.Label(parent, text=capwords(title_text) + ":").grid(row=self.current_row, column=0, sticky="w")
        ttk.Label(parent, text=value_text).grid(row=self.current_row, column=1, sticky="e")

        self.current_row += 1


class OptionWindow(BaseWindow):
    def __init__(self, parent, *args, **kwargs):
        BaseWindow.__init__(self, parent, *args, **kwargs)
        self.title("Options")

        self.variable_debug = self.parent.variable_debug
        self.variable_scrollbars = self.parent.variable_scrollbars
        self.variable_grid = self.parent.variable_grid

        OptionFrame(self.frame_widget, self).pack(fill="both", expand=True)

        ttk.Button(self.frame_buttons, text="OK", command=self.ok).pack(side="right")
        ttk.Button(self.frame_buttons, text="Apply", command=self.apply).pack(side="right")

    def apply(self):
        self.parent.start.scenarios.game.draw_widgets()

    def ok(self):
        self.apply()
        self.close()


class InformationWindow(BaseWindow):
    def __init__(self, parent, *args, **kwargs):
        BaseWindow.__init__(self, parent, *args, **kwargs)
        self.title("Information")

        self.frame_basic = ttk.LabelFrame(self.frame_widget, text="Basics")
        self.frame_basic.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

    def set_information(self, entity):
        for value in entity.entity_values["basic"]:
            self.create_label(self.frame_basic, value, entity.entity_values["basic"][value])


def main():
    app = tk.Tk()
    # BaseWindow(app)
    InformationWindow(app)
    OptionWindow(app)
    app.mainloop()


if __name__ == "__main__":
    main()
