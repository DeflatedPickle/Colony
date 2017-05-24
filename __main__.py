#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk
from random import randint, choice

import colony

__title__ = "Colony"
__author__ = "DeflatedPickle"
__version__ = "1.14.1"


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

        self.start = None

        self.start_menu_title()

    def start_menu_title(self):
        self.canvas.delete("all")
        try:
            self.after_cancel(self.debug_update)
        except AttributeError:
            pass
        self.start = Start(self)

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
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.option_menu = tk.Menu(self.parent)
        self.option_menu.add_command(label="Back To Menu", command=self.parent.start_menu_title)
        self.option_menu.add_command(label="Exit", command=self.parent.exit)

        self.add_button("Options", self.option_menu)

    def add_button(self, text: str = "", menu: tk.Menu = None):
        button = ttk.Menubutton(self, text=text, menu=menu, direction="above")
        button.pack(side="left", fill="x", expand=True)

        return button


class Start(object):
    def __init__(self, parent):
        self.parent = parent

        self.parent.canvas.create_text(5, 5, text="Colony", anchor="nw", font=colony.get_fonts()["menu"]["title"])
        self.parent.canvas.create_text(5, 45,
                                       text="A simple colony simulator created by Dibbo, inspired by RimWorld and Dwarf"
                                            "Fortress.",
                                       anchor="nw", font=colony.get_fonts()["menu"]["subtitle"])

        self.parent.canvas.create_window(5, 70,
                                         window=ttk.Button(self.parent.canvas, text="Start", command=self.start_game),
                                         anchor="nw")
        self.parent.canvas.create_window(5, 100, window=ttk.Button(self.parent.canvas, text="Options",
                                                                   command=self.start_options), anchor="nw")
        self.parent.canvas.create_window(5, 130,
                                         window=ttk.Button(self.parent.canvas, text="Exit", command=self.parent.exit),
                                         anchor="nw")

        self.scenarios = None
        self.options = None

    def start_game(self):
        self.parent.canvas.delete("all")
        self.scenarios = Scenarios(self.parent)

    def start_options(self):
        self.parent.canvas.delete("all")
        self.options = Options(self.parent)


class Game(object):
    def __init__(self, parent):
        self.parent = parent
        self.entities = []
        self.pawns = []
        self.items = []

        self.canvas = self.parent.canvas
        self.canvas.bind("<Configure>", self.on_resize, "+")

        self.selected_item = None

        self.debug = DeBug(self)
        self.on_resize()

    def register_items(self):
        # NOTE: Might not be the best idea to register items like this.
        return {"wood": colony.Item(self, name="Wood", stack_size=100),
                "stone": colony.Item(self, name="Stone", stack_size=100),
                "ore_iron": colony.Item(self, name="Iron Ore", stack_size=100),
                "ingot_iron": colony.Item(self, name="Iron Ingot", stack_size=100)}

    def on_resize(self, event=None):
        self.canvas.delete("taskbar")
        self.canvas.create_window(0, self.parent.winfo_height() - 23, window=TaskBar(self.parent), anchor="nw",
                                  width=self.canvas.winfo_width(), tags="taskbar")
        self.canvas.create_window(0, self.parent.winfo_height() - 48,
                                  window=ttk.Button(self.parent, text="/\\", width=3,
                                                    command=lambda: self.find_around(True)), anchor="nw",
                                  tags="taskbar")
        self.canvas.create_window(28, self.parent.winfo_height() - 48,
                                  window=ttk.Button(self.parent, text="\/", width=3,
                                                    command=lambda: self.find_around(False)), anchor="nw",
                                  tags="taskbar")

        del event

    def find_around(self, layer):
        # TODO: Have this function search around the selected object and then select the found object
        pass


class Options(object):
    def __init__(self, parent):
        self.parent = parent

        # TODO: Add options.

        self.parent.canvas.create_window(5, 130, window=ttk.Button(self.parent.canvas, text="Back",
                                                                   command=self.parent.start_menu_title), anchor="nw")


class Scenarios(object):
    def __init__(self, parent):
        self.parent = parent

        # TODO: Add an easy way for others to make new scenarios without editing code.

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

        self.parent.canvas.create_window(510, 260, window=ttk.Button(self.parent.canvas, text="Start",
                                                                     command=self.start_game), anchor="nw")

        self.game = None

        self.default_scenarios()

    def default_scenarios(self):
        colony.Scenario(self,
                        self.treeview,
                        title="Lonely Bean",
                        description="Just you, yourself and you.",
                        contents={"pawns": 1, "items": {"wood": 50, "stone": 20}})
        colony.Scenario(self,
                        self.treeview,
                        title="Weekend Camp Gone Wrong",
                        description="You were camping with your friends when suddenly... you were still camping but it"
                                    "was boring.",
                        contents={"pawns": 3})

    def select_scenario(self, *args):
        self.text.delete(1.0, "end")
        self.text.insert("end", "{}\n\n".format(self.treeview.item(self.treeview.focus())["text"]))
        self.text.insert("end", "Description: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][0]))
        # TODO: Show contents as string with commas separating each item.
        self.text.insert("end", "Contents: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][1]))

        self.selected_scenario = int(self.treeview.selection()[0][-1:]) - 1

        del args

    def start_game(self, *args):
        if self.treeview.focus() != "":
            self.parent.canvas.delete("all")
            self.game = Game(self.parent)
            self.spawn(self.scenario_list[self.selected_scenario])

        del args

    def spawn(self, scenario):
        canvas_x = self.parent.canvas.winfo_width()
        canvas_y = self.parent.canvas.winfo_height()

        drop_x = randint((canvas_x // 2) + 25, (canvas_x // 2) + 25)
        drop_y = randint((canvas_y // 2) + 25, (canvas_y // 2) + 25)

        # NOTE: Scenarios can exist without pawns.
        if "pawns" in scenario.contents:
            for amount in range(scenario.contents["pawns"]):
                colony.Pawn(self.game,
                            x=drop_x + randint(-25, 25),
                            y=drop_y + randint(-25, 25)).generate_random().draw()

        # NOTE: Scenarios can exist without items.
        if "items" in scenario.contents:
            for item in scenario.contents["items"]:
                if item == "random":
                    reg_item = self.game.register_items()[choice(list(self.game.register_items().keys()))]
                else:
                    reg_item = self.game.register_items()[item]

                reg_item.amount = scenario.contents["items"][item]

                reg_item.location["x"] = drop_x + randint(-25, 25)
                reg_item.location["y"] = drop_y + randint(-25, 25)

                reg_item.draw()


class DeBug(object):
    def __init__(self, parent):
        self.parent = parent
        self.counter = 10

        self.state = True
        self.parent.parent.bind("<Escape>", self.change_state)
        # This will draw text next to the mouse pointer that contains the mouse position
        # self.parent.parent.canvas.bind("<Motion>", self.mouse_location)

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

        self.parent.parent.debug_update = self.parent.parent.after(colony.get_interval(), self.update)

    def add_debug_line(self, text: str = ""):
        self.parent.canvas.create_text(5, self.counter, anchor="w", text=text, tag="debug")
        self.counter += 15

    def find_selected(self):
        for item in self.parent.entities:
            if item.selected:
                return "{}: {}".format(item.entity_type, item.name if not isinstance(item.name,
                                                                                     type(dict())) else item.get_name())

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

        del args

    def mouse_location(self, event):
        self.parent.canvas.delete("mouse")

        if self.state:
            mouse_x = self.parent.parent.canvas.canvasx(event.x)
            mouse_y = self.parent.parent.canvas.canvasx(event.y)
            self.parent.canvas.create_text(mouse_x - 40, mouse_y, text="{}, {}".format(mouse_x, mouse_y),
                                           tag="mouse")


class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, highlightthickness=0, **kwargs)
        self.parent = parent
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.configure(width=self.parent.winfo_width(), height=self.parent.winfo_height())

        del event


def main():
    app = GameWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
