#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import tkinter as tk
from tkinter import ttk
from random import randint

import colony

__title__ = "Colony"
__author__ = "DeflatedPickle"
__version__ = "1.13.0"


class GameWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Colony")
        self.geometry("600x300")
        self.option_add('*tearOff', False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = ResizingCanvas(self)
        self.canvas.grid(row=0, column=0)

        self.start_menu_title()

    def start_menu_title(self):
        # TODO: Have the TaskBar be removed upon restart.
        self.canvas.delete("all")
        self.start = Start(self)
        try:
            self.start.scenarios.game.taskbar.destroy()
        except AttributeError:
            pass

    def get_mouse_position(self):
        mouse_x_raw = self.winfo_pointerx()
        mouse_y_raw = self.winfo_pointery()

        mouse_x = mouse_x_raw - self.winfo_rootx()
        mouse_y = mouse_y_raw - self.winfo_rooty()

        return mouse_x, mouse_y

    def exit(self, *args):
        raise SystemExit


class TaskBar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.option_menu = tk.Menu(self.parent)
        self.option_menu.add_command(label="Back To Menu", command=self.parent.start_menu_title)
        self.option_menu.add_command(label="Exit", command=self.parent.exit)

        self.add_button("Options", self.option_menu)

    def add_button(self, text: str="", menu: tk.Menu=None):
        button = ttk.Menubutton(self, text=text, menu=menu, direction="above")
        button.pack(side="left", fill="x", expand=True)

        return button


class Start(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.parent.canvas.create_text(5, 5, text="Colony", anchor="nw", font=colony.get_fonts()["menu"]["title"])
        self.parent.canvas.create_text(5, 45, text="A simple colony simulator created by Dibbo, inspired by RimWorld and Dwarf Fortress.", anchor="nw", font=colony.get_fonts()["menu"]["subtitle"])

        self.parent.canvas.create_window(5, 70, window=ttk.Button(self.parent.canvas, text="Start", command=self.start_game), anchor="nw")
        self.parent.canvas.create_window(5, 100, window=ttk.Button(self.parent.canvas, text="Options", command=self.start_options), anchor="nw")
        self.parent.canvas.create_window(5, 130, window=ttk.Button(self.parent.canvas, text="Exit", command=self.parent.exit), anchor="nw")

    def start_game(self):
        self.parent.canvas.delete("all")
        self.scenarios = Scenarios(self.parent)

    def start_options(self):
        self.parent.canvas.delete("all")
        self.options = Options(self.parent)


class Game(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.entities = []
        self.pawns = []
        self.items = []

        self.canvas = self.parent.canvas

        self.selected_item = None

        self.debug = DeBug(self)
        self.taskbar = TaskBar(self.parent).grid(row=1, column=0, sticky="nesw")

        # pawn = colony.Pawn(self, forename="Frank", surname="Lyatut", gender=True, x=90, y=50).draw()
        # pawn_2 = colony.Pawn(self, forename="Ima", surname="Nothrpwn", gender=False, x=130, y=70).draw()
        # pawn_random = colony.Pawn(self, x=270, y=130).generate_random().draw()

        # item = colony.Item(self, name="Broken Sword", x=250, y=30).draw()
        # item_2 = colony.Item(self, name="Wood", x=230, y=90).draw()

    def register_items(self):
        return {"wood": colony.Item(self, name="Wood"),
                "stone": colony.Item(self, name="Stone")}


class Options(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.parent.canvas.create_window(5, 130, window=ttk.Button(self.parent.canvas, text="Back", command=self.parent.start_menu_title), anchor="nw")


class Scenarios(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.scenario_list = []
        self.current_scenarios = 0
        self.selected_scenario = 0

        frame_listbox = ttk.Frame(self.parent.canvas)
        self.treeview = ttk.Treeview(frame_listbox, show="tree")
        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview.bind("<<TreeviewSelect>>", self.select_scenario)
        self.treeview.bind("<Double-Button-1>", self.start_game)
        scrollbar_treeview = ttk.Scrollbar(frame_listbox, command=self.treeview.yview)
        scrollbar_treeview.pack(side="right", fill="y", expand=True)
        self.treeview.configure(yscrollcommand=scrollbar_treeview.set)

        self.parent.canvas.create_window(5, 5, window=frame_listbox, anchor="nw")

        frame_text = ttk.Frame(self.parent.canvas)
        self.text = tk.Text(frame_text, width=30, height=12)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar_text = ttk.Scrollbar(frame_text, command=self.text.yview)
        scrollbar_text.pack(side="right", fill="y", expand=True)
        self.text.configure(yscrollcommand=scrollbar_text.set)

        self.parent.canvas.create_window(230, 5, window=frame_text, anchor="nw")

        self.parent.canvas.create_window(510, 260, window=ttk.Button(self.parent.canvas, text="Start", command=self.start_game), anchor="nw")

        self.default_scenarios()

    def default_scenarios(self):
        colony.Scenario(self, self.treeview, title="Lonely Bean", description="Just you, yourself and you.", contents={"pawns": 1, "items": {"wood": 50}})
        colony.Scenario(self, self.treeview, title="Weekend Camp Gone Wrong", description="You were camping with your friends when suddenly... you were still camping but it was boring.", contents={"pawns": 3})

    def select_scenario(self, *args):
        self.text.delete(1.0, "end")
        self.text.insert("end", "{}\n\n".format(self.treeview.item(self.treeview.focus())["text"]))
        self.text.insert("end", "Description: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][0]))
        self.text.insert("end", "Contents: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][1]))

        self.selected_scenario = int(self.treeview.selection()[0][-1:]) - 1

    def start_game(self, *args):
        if self.treeview.focus() != "":
            self.parent.canvas.delete("all")
            self.game = Game(self.parent)
            self.spawn(self.scenario_list[self.selected_scenario])

    def spawn(self, scenario):
        if "pawns" in scenario.contents:
            for amount in range(scenario.contents["pawns"]):
                canvas_x = self.parent.canvas.winfo_width()
                canvas_y = self.parent.canvas.winfo_height()

                drop_x = randint((canvas_x // 2) + 25, (canvas_x // 2) + 25)
                drop_y = randint((canvas_y // 2) + 25, (canvas_y // 2) + 25)

                colony.Pawn(self.game, x=drop_x + randint(-25, 25), y=drop_y + randint(-25, 25)).generate_random().draw()

        if "items" in scenario.contents:
            for item in scenario.contents["items"]:
                for amount in range(scenario.contents["items"][item]):
                    self.game.register_items()[item].draw()


class DeBug(object):
    def __init__(self, parent):
        self.parent = parent
        self.counter = 10

        self.state = True
        self.parent.parent.bind("<Escape>", self.change_state)
        self.parent.parent.canvas.bind("<Motion>", self.mouse_location)

        self.update()

    def update(self):
        if self.state:
            self.parent.canvas.delete("debug")
            self.counter = 10

            self.add_debug_line(text="Selected: {}".format(self.find_selected()))
            self.add_debug_line(text="Selected Location: {}".format(self.find_selected_location()))
            self.add_debug_line(text="Selected Action: {}".format(self.find_selected_action()))
            self.add_debug_line(text="Selected Inventory: {}".format(self.find_selected_inventory()))
            self.counter += 15
            self.add_debug_line(text="Pawns: {}".format(len(self.parent.pawns)))
            self.add_debug_line(text="Items: {}".format(len(self.parent.items)))

        elif not self.state:
            self.parent.canvas.delete("debug")
            self.parent.canvas.delete("mouse")

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

    def change_state(self, *args):
        self.state = not self.state

    def mouse_location(self, event):
        self.parent.canvas.delete("mouse")

        mouse_x = self.parent.parent.canvas.canvasx(event.x)
        mouse_y = self.parent.parent.canvas.canvasx(event.y)
        self.parent.canvas.create_text(mouse_x + 10, mouse_y + 25, text="{}, {}".format(mouse_x, mouse_y), tag="mouse")


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
