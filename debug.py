#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import colony

__title__ = "ResizingCanvas"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class DeBug(object):
    def __init__(self, parent):
        self.parent = parent
        self.counter = 10

        self.state = False

        # This will draw text next to the mouse pointer that contains the mouse position
        # self.parent.parent.canvas.bind("<Motion>", self.mouse_location)

        self.update()

    def update(self):
        if self.state:
            self.parent.canvas.delete("debug")
            self.counter = 10

            self.add_debug_line(text="Selected: {}".format(self.find_selected()))
            if not self.parent.entities and self.parent.entities[0].entity_type == "resource":
                self.add_debug_line(text="Selected Gender: {}".format(self.find_selected_gender()))
            self.add_debug_line(text="Selected Location: {}".format(self.find_selected_location()))
            self.add_debug_line(text="Selected Action: {}".format(self.find_selected_action()))
            self.add_debug_line(text="Selected Inventory: {}".format(self.find_selected_inventory()))
            self.counter += 15
            self.add_debug_line(text="Selected Tool: {}".format(self.parent.selected_tool))
            self.counter += 15
            self.add_debug_line(text="Colonists: {}".format(len(self.parent.colonists)))
            self.add_debug_line(text="Animals: {}".format(len(self.parent.animals)))
            self.add_debug_line(text="Items: {}".format(len(self.parent.items)))

        elif not self.state:
            self.parent.canvas.delete("debug")
            self.parent.canvas.delete("mouse")

        self.parent.parent.debug_update = self.parent.parent.after(colony.interval.get_interval(), self.update)

    def add_debug_line(self, text: str = ""):
        self.parent.canvas.create_text(5, self.counter, anchor="w", text=text, tag="debug")
        self.counter += 15

    def find_selected(self):
        for item in self.parent.entities.values():
            if item.selected:
                return "{}: {}".format(item.entity_type, item.name if not isinstance(item.name, type(dict())) else item.get_name())

    def find_selected_gender(self):
        for item in self.parent.entities.values():
            if item.selected:
                return item.gender

    def find_selected_location(self):
        for item in self.parent.entities.values():
            if item.selected:
                return "x={0[0]}, y={0[1]}".format(self.parent.selected_entity[0].find_coordinates_own())

    def find_selected_action(self):
        for entity in self.parent.entities.values():
            if entity.selected:
                if entity.entity_type == "colonist" or entity.entity_type == "animal":
                    return entity.action

                elif entity.entity_type == "item":
                    return None

    def find_selected_inventory(self):
        for entity in self.parent.entities.values():
            if entity.selected:
                if entity.entity_type == "colonist" or entity.entity_type == "animal":
                    return entity.inventory

                elif entity.entity_type == "item":
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
