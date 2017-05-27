#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk
from random import randint, choice
import sys
from ast import literal_eval

import colony

__title__ = "Colony"
__author__ = "DeflatedPickle"
__version__ = "1.18.0"


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


class TaskBar(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.option_menu = tk.Menu(self.parent)
        self.option_menu.add_command(label="Back To Menu", command=self.parent.start_menu_title)
        self.option_menu.add_command(label="Exit", command=lambda: sys.exit())

        self.add_button("Options", self.option_menu)

    def add_button(self, text: str = "", menu: tk.Menu = None):
        button = ttk.Menubutton(self, text=text, menu=menu, direction="above")
        button.pack(side="left", fill="x", expand=True)

        return button


class ColonistBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent.parent, **kwargs)
        self.parent = parent

    def add_colonist(self, colonist):
        canvas = tk.Canvas(self, width=50, height=50)
        canvas.create_text(25, 20, text=colony.get_references()["icons"]["colonist"],
                           font=colony.get_fonts()["colonist"]["colonistbar"])
        canvas.create_text(25, 40, text=colonist.name["forename"], anchor="center",
                           font=colony.get_fonts()["text"]["colonistbar"])
        canvas.pack(side="left")

        canvas.bind("<ButtonRelease-1>", colonist.select, "+")
        canvas.bind("<Button-1>", self.parent.unselect_all, "+")
        # TODO: Make the colonist on the bar that represents the colonist turn bold when the colonist is selected.

        return canvas


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
                                         window=ttk.Button(self.parent.canvas, text="Exit", command=lambda: sys.exit()),
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
        self.entities = {}
        self.colonists = []
        self.items = []

        self.canvas = self.parent.canvas
        self.canvas.bind("<Configure>", self.draw_widgets, "+")

        self.selected_item = None

        self.debug = DeBug(self)
        self.colonist_bar = ColonistBar(self)
        self.draw_widgets()

    def register_items(self):
        # NOTE: Might not be the best idea to register items like this.
        return {"wood": colony.Item(self, name="Wood", stack_size=100),
                "stone": colony.Item(self, name="Stone", stack_size=100),
                "ore_iron": colony.Item(self, name="Iron Ore", stack_size=100),
                "ingot_iron": colony.Item(self, name="Iron Ingot", stack_size=100)}

    def draw_widgets(self, event=None):
        self.canvas.delete("HUD")

        self.canvas.create_window(self.canvas.winfo_width() // 2, 30, window=self.colonist_bar, anchor="center",
                                  tags="HUD")

        self.canvas.create_window(0, self.parent.winfo_height() - 23, window=TaskBar(self.parent), anchor="nw",
                                  width=self.canvas.winfo_width(), tags="HUD")

        # TODO: Create a frame to hold information that is shown when an entity is selected.
        # TODO: Move the upper and lower buttons to the previously mentioned frame.
        self.canvas.create_window(0, self.parent.winfo_height() - 48,
                                  window=ttk.Button(self.parent, text="/\\", width=3,
                                                    command=lambda: self.select_around(True)), anchor="nw",
                                  tags="HUD")
        self.canvas.create_window(28, self.parent.winfo_height() - 48,
                                  window=ttk.Button(self.parent, text="\/", width=3,
                                                    command=lambda: self.select_around(False)), anchor="nw",
                                  tags="HUD")

        del event

    def select_around(self, layer):
        # print(self.entities)
        for entity in self.parent.canvas.find_withtag("entity"):
            # print("Entity: {}".format(entity))
            # print("Selected: {}".format(self.selected_item.entity))
            if not layer:
                # print("Below: {}".format(self.parent.canvas.find_below(self.selected_item.entity)[0]))
                if entity <= self.parent.canvas.find_below(self.selected_item.entity)[0]:
                    self.unselect_all()
                    self.entities[entity].select()

            if layer:
                # print("Above: {}".format(self.parent.canvas.find_above(self.selected_item.entity)[0]))
                if entity >= self.parent.canvas.find_above(self.selected_item.entity)[0]:
                    self.unselect_all()
                    self.entities[entity].select()

    def unselect_all(self, *args):
        for colonist in self.canvas.find_withtag("entity"):
            if self.entities[colonist].entity_type == "colonist":
                self.entities[colonist].unselect()

        del args


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
        self.scenario_list.append(self.treeview.insert("", "end", text="-----Default-----"))

        colony.Scenario(self,
                        self.treeview,
                        title="Lonely Bean",
                        description="Just you, yourself and you.",
                        contents={"colonists": 1, "items": {"wood": 50, "stone": 20}})
        colony.Scenario(self,
                        self.treeview,
                        title="Weekend Camp Gone Wrong",
                        description="You were camping with your friends when suddenly... you were still camping but it"
                                    "was boring.",
                        contents={"colonists": 3})

        colony.Scenario(self,
                        self.treeview,
                        title="Wimps From Yonder",
                        description="Your previous town was ransacked by pirates, all your friends and family were"
                                    "murdered, but you and a few others managed to escape.",
                        contents={"colonists": 7})

        self.scenario_list.append(self.treeview.insert("", "end", text="-----Debug-----"))

        colony.Scenario(self,
                        self.treeview,
                        title="Nothing",
                        description="You spawn with nothing.",
                        contents={})

        colony.Scenario(self,
                        self.treeview,
                        title="Random Items",
                        description="Spawns some random items.",
                        contents={"colonists": 1, "items": {"random": 30}})

        self.scenario_list.append(self.treeview.insert("", "end", text="-----Third-Party-----"))

    def select_scenario(self, *args):
        self.text.delete(1.0, "end")
        if not self.treeview.item(self.treeview.focus())["text"].startswith("-"):
            self.text.insert("end", "{}\n\n".format(self.treeview.item(self.treeview.focus())["text"]))
            self.text.insert("end",
                             "Description: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][0]))

            contents = literal_eval(self.treeview.item(self.treeview.focus())["values"][1])
            contents_show = []

            for key, value in contents.items():
                if key != "items":
                    if 0 < value <= 1:
                        key = "colonist"
                    contents_show.append("{} {}".format(value, key))
                else:
                    for items_key, items_value in contents["items"].items():
                        contents_show.append("{} {}".format(items_value, items_key))

            # print(", ".join(contents_show))

            self.text.insert("end", "Contents: {}\n\n".format(", ".join(contents_show)))

            self.selected_scenario = int(self.treeview.selection()[0][-1:]) - 1

        del args

    def start_game(self, *args):
        if self.treeview.focus() != "":
            if not self.treeview.item(self.treeview.focus())["text"].startswith("-"):
                self.parent.canvas.delete("all")
                self.game = Game(self.parent)
                self.spawn(self.scenario_list[self.selected_scenario])

        del args

    def spawn(self, scenario):
        canvas_x = self.parent.canvas.winfo_width()
        canvas_y = self.parent.canvas.winfo_height()

        drop_x = randint((canvas_x // 2) + 25, (canvas_x // 2) + 25)
        drop_y = randint((canvas_y // 2) + 25, (canvas_y // 2) + 25)

        # NOTE: Scenarios can exist without colonists.
        if "colonists" in scenario.contents:
            for amount in range(scenario.contents["colonists"]):
                colony.Colonist(self.game,
                                x=drop_x + randint(-25, 25),
                                y=drop_y + randint(-25, 25)).generate_random().draw().add_to_colonist_bar()

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
            self.add_debug_line(text="Colonists: {}".format(len(self.parent.colonists)))
            self.add_debug_line(text="Items: {}".format(len(self.parent.items)))

        elif not self.state:
            self.parent.canvas.delete("debug")
            self.parent.canvas.delete("mouse")

        self.parent.parent.debug_update = self.parent.parent.after(colony.get_interval(), self.update)

    def add_debug_line(self, text: str = ""):
        self.parent.canvas.create_text(5, self.counter, anchor="w", text=text, tag="debug")
        self.counter += 15

    def find_selected(self):
        for item in self.parent.entities.values():
            if item.selected:
                return "{}: {}".format(item.entity_type, item.name if not isinstance(item.name,
                                                                                     type(dict())) else item.get_name())

    def find_selected_location(self):
        for item in self.parent.entities.values():
            if item.selected:
                return "x={0[0]}, y={0[1]}".format(self.parent.selected_item.find_coordinates_own())

    def find_selected_action(self):
        for item in self.parent.entities.values():
            if item.selected:
                if item.entity_type == "colonist":
                    return item.action

                elif item.entity_type == "item":
                    return None

    def find_selected_inventory(self):
        for item in self.parent.entities.values():
            if item.selected:
                if item.entity_type == "colonist":
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
            self.parent.canvas.create_text(mouse_x - 40, mouse_y, text="{}, {}".format(mouse_x, mouse_y), tag="mouse")


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
