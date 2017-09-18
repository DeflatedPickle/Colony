#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from tkinter import ttk

import colony
from timeframe import TimeFrame
from gametime import GameTime
from colonistbar import ColonistBar
from taskbar import TaskBar
from debug import DeBug

__title__ = "Game"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class Game(object):
    def __init__(self, parent):
        self.parent = parent
        self.ids = {}
        self.canvas_ids = {}

        self.entities = {}
        self.colonists = []
        self.animals = []
        self.items = []
        self.families = []
        self.event_hours = [8, 20]

        self.highest_id = 0

        self.time_frame = TimeFrame(self)
        self.time = GameTime(self)

        self.register_items = {
            "wood": colony.Item(self, name="Wood", stack_size=100),
            "stone": colony.Item(self, name="Stone", stack_size=100),
            # Iron
            "ore_iron": colony.Item(self, name="Iron Ore", stack_size=100),
            "ingot_iron": colony.Item(self, name="Iron Ingot", stack_size=100),
            # Marble
            "crushed_marble": colony.Item(self, name="Crushed Marble", stack_size=100),
            "brick_marble": colony.Item(self, name="Marble Bricks", stack_size=100),
            # Limestone
            "crushed_limestone": colony.Item(self, name="Crushed Limestone", stack_size=100),
            "brick_limestone": colony.Item(self, name="Limestone Bricks", stack_size=100)
        }

        # Animals registered here, though not drawn, still decide actions to do.
        # This could be causing lag for the game, or cause more lag when more animals are added.
        self.register_animals = {
            "cat": colony.Animal(self, species="Cat", tame_chance=80, highest_age=10),
            "babirusa": colony.Animal(self, species="Babirusa", tame_chance=30, highest_age=10),

            # Extinct
            "castoroides": colony.Animal(self, species="Castoroides", tame_chance=20, highest_age=23),
            "dodo": colony.Animal(self, species="Dodo", tame_chance=20, highest_age=7)
        }

        self.register_resources = {
            "tree": colony.Resource(self, name="Tree", health=50, resource=self.register_items["wood"], resource_amount=50),
            "marble": colony.Resource(self, name="Marble", health=80, resource=self.register_items["crushed_marble"], resource_amount=1, type_="Rock"),
            "limestone": colony.Resource(self, name="Limestone", health=80, resource=self.register_items["crushed_limestone"], resource_amount=1, type_="Rock")
        }

        self.canvas = self.parent.canvas
        self.canvas.configure(background="light gray")
        self.canvas.bind("<Configure>", self.draw_widgets, "+")
        self.game_area = tk.Canvas(self.canvas, width=self.parent.game_width + 1, height=self.parent.game_height + 1, scrollregion=(0, 0, self.parent.game_width, self.parent.game_height))

        self.grid_dictionary = {}

        # self.selected_entity = None
        self.selected_entity = []

        self.selected_tool = None
        self.select_area = None
        self.game_area.bind("<Button-1>", self.check_tool, "+")
        self.game_area.bind("<ButtonRelease-3>", self.reset_tool, "+")
        self.game_area.bind("<Motion>", self.select_grid_cell, "+")

        self.game_scrollbar_x = ttk.Scrollbar(self.parent, orient="horizontal", command=self.game_area.xview)
        self.game_scrollbar_y = ttk.Scrollbar(self.parent, command=self.game_area.yview)
        self.game_area.configure(xscrollcommand=self.game_scrollbar_x.set, yscrollcommand=self.game_scrollbar_y.set)

        self.colonist_bar = ColonistBar(self)
        self.taskbar = TaskBar(self.parent, self)
        self.debug = DeBug(self)

        self.draw_widgets()
        self.draw_grid()

    def draw_widgets(self, event=None):
        self.canvas.delete("HUD")
        self.canvas.delete("game")
        self.canvas.delete("scrollbar")

        self.canvas.create_window(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, window=self.game_area, anchor="center", tags="game")

        if self.parent.variable_grid.get():
            for value in self.grid_dictionary.values():
                self.game_area.itemconfigure(value, width=1)

        else:
            for value in self.grid_dictionary.values():
                self.game_area.itemconfigure(value, width=0)

        if self.parent.variable_scrollbars.get():
            self.canvas.create_window(56, self.canvas.winfo_height() - 40, window=self.game_scrollbar_x, anchor="nw", width=self.canvas.winfo_width() - 73, tags="scrollbar")
            self.canvas.create_window(self.canvas.winfo_width() - 17, 0, window=self.game_scrollbar_y, anchor="nw", height=self.canvas.winfo_height() - 40, tags="scrollbar")

            self.canvas.create_rectangle(self.canvas.winfo_width() - 17, self.canvas.winfo_height() - 40, self.canvas.winfo_width() - 1, self.canvas.winfo_height() - 24, outline=self.parent.background, fill=self.parent.background, tags="game")

        else:
            pass

        # Comment: This creates the colonist bar.
        self.canvas.create_window(self.canvas.winfo_width() // 2, 30, window=self.colonist_bar, anchor="center", tags="HUD")

        # Comment: This creates the taskbar.
        self.recreate_taskbar()
        self.canvas.create_window(0, self.parent.winfo_height() - 23, window=self.taskbar, anchor="nw", width=self.canvas.winfo_width(), tags="HUD")

        self.canvas.create_window(0, self.parent.winfo_height() - 48,  window=ttk.Button(self.parent, text="/\\", width=3, command=lambda: self.select_around(True)), anchor="nw", tags="HUD")
        self.canvas.create_window(28, self.parent.winfo_height() - 48, window=ttk.Button(self.parent, text="\/", width=3, command=lambda: self.select_around(False)), anchor="nw", tags="HUD")

        self.canvas.create_window(0, self.parent.winfo_height() - 120, window=self.time_frame, anchor="nw", tags="HUD")

        if self.parent.variable_debug.get():
            self.debug.state = True

        else:
            self.debug.state = False

        del event

    def recreate_taskbar(self):
        del self.taskbar
        self.taskbar = TaskBar(self.parent, self)

    def draw_grid(self):
        self.game_area.update()
        self.game_area.delete("grid")
        width = self.game_area.winfo_width()
        height = self.game_area.winfo_height()

        for column in range(width // 10):
            for row in range(height // 10):
                x1 = column * 10
                y1 = row * 10

                x2 = x1 + 10
                y2 = y1 + 10

                self.grid_dictionary[row, column] = self.game_area.create_rectangle(x1, y1, x2, y2, width=0, tags="grid")

        self.game_area.tag_lower("grid")

    def selection_tool(self, x, y, event):
        self.game_area.delete("select")

        self.game_area.create_rectangle(x, y, event.x, event.y, tags="select")
        self.select_area = [x, y, event.x, event.y]

    def release(self, event):
        self.game_area.tag_raise("select")

        try:
            for entity in self.game_area.find_overlapping(self.select_area[0], self.select_area[1], self.select_area[2], self.select_area[3]):
                if "entity" in self.game_area.gettags(entity):
                    self.entities[entity].select()

        except TypeError:
            pass

        self.game_area.delete("select")

        self.selected_tool = None
        self.select_area = None

        del event

    def check_tool(self, *args):
        mouse_x, mouse_y = self.parent.get_mouse_position()

        if self.selected_tool is None:
            self.selected_tool = "select"

            self.game_area.bind("<B1-Motion>", lambda event: self.selection_tool(mouse_x, mouse_y, event), "+")
            self.game_area.bind("<ButtonRelease-1>", self.release, "+")

        elif self.selected_tool is not None:
            tool = self.selected_tool.split(":")

            self.game_area.unbind("<B1-Motion>")
            self.game_area.unbind("<ButtonRelease-1>")

            if "spawn" in tool:
                if "entity" in tool:
                    if "item" in tool:
                        item = self.register_items[tool[-1]]

                        item.location["x"] = mouse_x
                        item.location["y"] = mouse_y

                        item.draw()

                    if "resource" in tool:
                        resource = self.register_resources[tool[-1]]

                        item = self.game_area.find_closest(mouse_x, mouse_y)[0]

                        if "grid" in self.game_area.gettags(item):
                            resource.location["x"] = self.game_area.coords(item)[0]
                            resource.location["y"] = self.game_area.coords(item)[1]

                        resource.draw()

                    elif "actingentity" in tool:
                        if "movingentity" in tool:
                            if "colonist" in tool:
                                colony.Colonist(self, x=mouse_x, y=mouse_y).generate_random().draw().add_to_colonist_bar()

                            elif "animal" in tool:
                                animal = self.register_animals[tool[-1]]

                                animal.location["x"] = mouse_x
                                animal.location["y"] = mouse_y

                                animal.generate_random().draw()

            elif "destroy" in tool:
                if "entity" in tool:
                    closest = self.game_area.find_closest(mouse_x, mouse_y, halo=1)[0]
                    try:
                        if isinstance(self.entities[closest], colony.Entity):
                            self.entities[closest].remove_from_colonist_bar()
                            self.entities[closest].destroy()

                    except KeyError:
                        pass

        del args

    def set_tool(self, tool_type):
        self.selected_tool = tool_type

    def reset_tool(self, *args):
        self.selected_tool = None

        del args

    def select_grid_cell(self, event):
        if self.parent.variable_grid_highlight.get():
            self.game_area.delete("highlight")

            mouse = self.parent.get_mouse_position()
            item = self.game_area.find_closest(mouse[0] - 5, mouse[1] - 5)[0]

            if "grid" in self.game_area.gettags(item):
                coords = self.game_area.coords(item)
                self.game_area.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=self.parent.variable_highlight_colour.get(), stipple="gray50", width=0, tags="highlight")

        del event

    def select_around(self, layer):
        # print(self.entities)
        for entity in self.game_area.find_withtag("entity"):
            # print("Entity: {}".format(entity))
            # print("Selected: {}".format(self.selected_entity.entity))
            if self.selected_entity is None:
                return

            if not layer:
                # print("Below: {}".format(self.parent.canvas.find_below(self.selected_entity.entity)[0]))
                try:
                    if entity <= self.game_area.find_below(self.selected_entity[0].entity)[0]:
                        self.unselect_all()
                        self.entities[entity].select()

                except IndexError:
                    pass

            if layer:
                # print("Above: {}".format(self.parent.canvas.find_above(self.selected_entity.entity)[0]))
                try:
                    if entity >= self.game_area.find_above(self.selected_entity[0].entity)[0]:
                        self.unselect_all()
                        self.entities[entity].select()

                except IndexError:
                    pass

    def unselect_all(self, *args):
        for entity in self.game_area.find_withtag("entity"):
            self.entities[entity].unselect()

        del args

    def update_families(self):
        for colonist in self.colonists:
            if colonist.name["surname"] not in self.families:
                self.families.append(colonist.name["surname"])

    def set_relationships(self):
        # TODO: Finish working out relationships.
        for family in self.families:
            for colonist in self.colonists:
                pass

    def get_selected(self):
        for entity in self.entities.values():
            if entity.selected:
                return entity

    def generate_id(self, instance):
        self.highest_id += 1
        self.ids[self.highest_id] = instance
        return self.highest_id
