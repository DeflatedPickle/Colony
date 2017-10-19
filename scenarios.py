#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk
import random
from ast import literal_eval

import colony
from game import Game

__title__ = "ResizingCanvas"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Scenarios(object):
    def __init__(self, parent):
        self.parent = parent
        self.canvas = self.parent.canvas

        # TODO: Add an easy way for others to make new scenarios without editing code.

        self.scenario_list = []
        self.current_scenarios = 0
        self.selected_scenario = 0

        self.parent.canvas.bind("<Configure>", self.draw_widgets, "+")

        self.canvas.create_text(5, 5, text="Scenarios", anchor="nw", font=colony.get_fonts()["menu"]["title"])

        self.frame_listbox = ttk.Frame(self.parent.canvas)

        self.treeview = ttk.Treeview(self.frame_listbox, show="tree")
        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview.bind("<<TreeviewSelect>>", self.select_scenario)
        self.treeview.bind("<Double-Button-1>", self.start_game)
        scrollbar_treeview = ttk.Scrollbar(self.frame_listbox, command=self.treeview.yview)
        scrollbar_treeview.pack(side="right", fill="y", expand=True)
        self.treeview.configure(yscrollcommand=scrollbar_treeview.set)

        self.frame_text = ttk.Frame(self.parent.canvas)

        self.text = tk.Text(self.frame_text, wrap="word", width=0, height=12)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar_text = ttk.Scrollbar(self.frame_text, command=self.text.yview)
        scrollbar_text.pack(side="right", fill="y", expand=False)
        self.text.configure(yscrollcommand=scrollbar_text.set)

        self.game = None

        self.draw_widgets()
        self.default_scenarios()

    def draw_widgets(self, event=None):
        self.parent.canvas.delete("UI")

        self.canvas.create_window(5, 50, window=self.frame_listbox, anchor="nw", height=self.parent.winfo_height() - 90, tags="UI")
        self.canvas.create_window(230, 50, window=self.frame_text, anchor="nw", width=self.parent.winfo_width() - 235, height=self.parent.winfo_height() - 90, tags="UI")

        self.canvas.create_window(5, self.parent.winfo_height() - 30, window=ttk.Button(self.parent.canvas, text="Back", command=self.parent.start_menu_title), anchor="nw", tags="UI")
        self.canvas.create_window(self.parent.winfo_width() - 80, self.parent.winfo_height() - 30, window=ttk.Button(self.canvas, text="Start", command=self.start_game), anchor="nw", tags="UI")

        del event

    def default_scenarios(self):
        self.scenario_list.append(self.treeview.insert("", "end", text="-----Default-----"))

        colony.Scenario(self,
                        self.treeview,
                        title="Lonely Bean",
                        description="Just you, yourself and you.",
                        contents={"colonists": 1})  # , "items": {"wood": 50, "stone": 20}})

        colony.Scenario(self,
                        self.treeview,
                        title="Partners In Crime",
                        description="You and your partner are outlaws, on the run. However, you have been on the run for so long, you two need a break. You find a nice patch of land to settle on for a while.",
                        contents={"colonists": 2})

        colony.Scenario(self,
                        self.treeview,
                        title="Weekend Camp Gone Wrong",
                        description="You were camping with your friends when suddenly... you were still camping but it was boring.",
                        contents={"colonists": 3})

        colony.Scenario(self,
                        self.treeview,
                        title="Wimps From Yonder",
                        description="Your previous town was ransacked by pirates, all your friends and family were murdered, but you and a few others managed to escape.",
                        contents={"colonists": 7})

        colony.Scenario(self,
                        self.treeview,
                        title="Not Without My Animal",
                        description="You have an animal. That's it.",
                        contents={"colonists": 2, "animals": {"cat": 1}})

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
            self.text.insert("end", "Description: {}\n\n".format(self.treeview.item(self.treeview.focus())["values"][0]))

            contents = literal_eval(self.treeview.item(self.treeview.focus())["values"][1])
            contents_show = []

            for key, value in contents.items():
                if key != "items" and key != "animals":
                    if 0 < value <= 1:
                        key = "colonist"
                    contents_show.append("{} {}".format(value, key))

                elif key == "items":
                    for items_key, items_value in contents["items"].items():
                        contents_show.append("{} {}".format(items_value, items_key))

                elif key == "animals":
                    for animal_key, animal_value in contents["animals"].items():
                        contents_show.append("{} {}".format(animal_value, animal_key))

            # print(", ".join(contents_show))

            self.text.insert("end", "Contents: {}\n\n".format(", ".join(contents_show)))

            self.selected_scenario = int(self.treeview.selection()[0][-1:]) - 1

        del args

    def start_game(self, *args):
        if self.treeview.focus() != "":
            if not self.treeview.item(self.treeview.focus())["text"].startswith("-"):
                self.parent.canvas.delete("all")

                self.parent.canvas.unbind("<Configure>")
                self.parent.canvas.bind("<Configure>", self.parent.canvas.on_resize)

                self.game = Game(self.parent)
                self.spawn(self.scenario_list[self.selected_scenario])
                self.game.update_families()

                self.game.recreate_taskbar()

        del args

    def spawn(self, scenario):
        self.parent.start.scenarios.game.game_area.update()

        canvas_x = self.parent.start.scenarios.game.game_area.winfo_width()
        canvas_y = self.parent.start.scenarios.game.game_area.winfo_height()

        drop_x = (canvas_x // 2) + 25
        drop_y = (canvas_y // 2) + 25

        # NOTE: Scenarios can exist without colonists.
        if "colonists" in scenario.contents:
            for amount in range(scenario.contents["colonists"]):
                colony.Colonist(self.game, x=drop_x + random.randint(-25, 25), y=drop_y + random.randint(-25, 25)).generate_random().draw().add_to_colonist_bar()

            for colonist in self.parent.start.scenarios.game.colonists:
                colonist.generate_random_relationship()

        # NOTE: Scenarios can exist without animals.
        if "animals" in scenario.contents:
            for animal in scenario.contents["animals"]:
                if animal == "random":
                    reg_animal = self.game.register_animals[random.choice(list(self.game.register_animals().keys()))]

                else:
                    reg_animal = self.game.register_animals[animal]

                reg_animal.location["x"] = drop_x + random.randint(-25, 25)
                reg_animal.location["y"] = drop_y + random.randint(-25, 25)

                reg_animal.generate_random().draw()

        # NOTE: Scenarios can exist without items.
        if "items" in scenario.contents:
            for item in scenario.contents["items"]:
                if item == "random":
                    reg_item = self.game.register_items[random.choice(list(self.game.register_items.keys()))]

                else:
                    reg_item = self.game.register_items[item]

                reg_item.amount = scenario.contents["items"][item]

                reg_item.location["x"] = drop_x + random.randint(-25, 25)
                reg_item.location["y"] = drop_y + random.randint(-25, 25)

                reg_item.draw()
