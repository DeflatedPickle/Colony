#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import tkinter as tk

import pkinter as pk

__title__ = "Window"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Window(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.parent.bind("<Configure>", lambda event: pk.center_on_parent(self))
        self.protocol("WM_DELETE_WINDOW", self.close)

    def set_up_for(self, window_type: str):
        if window_type == "information":
            pass

        return self

    def set_information(self, entity):
        self.title("Information")
        self.geometry("200x250")

    def close(self):
        self.parent.unbind("<Configure>")
        self.destroy()


def main():
    app = tk.Tk()
    Window(app)
    app.mainloop()


if __name__ == "__main__":
    main()
