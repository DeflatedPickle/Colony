#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk

__title__ = "MenuDebug"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class MenuDebug(tk.Menu):
    def __init__(self, parent, **kwagrs):
        tk.Menu.__init__(self, parent, **kwagrs)
        self.parent = parent

        self.debug_spawn_menu = tk.Menu(self)
        self.add_cascade(label="Spawn", menu=self.debug_spawn_menu)

        self.debug_spawn_entity_menu = tk.Menu(self)
        self.debug_spawn_menu.add_cascade(label="Entity", menu=self.debug_spawn_entity_menu)

        self.debug_spawn_entity_item_menu = tk.Menu(self)
        self.debug_spawn_entity_menu.add_cascade(label="Item", menu=self.debug_spawn_entity_item_menu)

        for item in self.parent.game.register_items:
            self.debug_spawn_entity_item_menu.add_command(label=self.parent.game.register_items[item].name, command=lambda current_item=item: self.parent.game.set_tool("spawn:entity:item:{}".format(current_item)))

        self.debug_spawn_entity_resource_menu = tk.Menu(self)
        self.debug_spawn_entity_menu.add_cascade(label="Resource", menu=self.debug_spawn_entity_resource_menu)

        for resource in self.parent.game.register_resources:
            self.debug_spawn_entity_resource_menu.add_command(label=self.parent.game.register_resources[resource].name, command=lambda current_resource=resource: self.parent.game.set_tool("spawn:entity:resource:{}".format(current_resource)))

        self.debug_spawn_entity_actingentity_menu = tk.Menu(self.debug_spawn_entity_menu)
        self.debug_spawn_entity_menu.add_cascade(label="ActingEntity", menu=self.debug_spawn_entity_actingentity_menu)

        self.debug_spawn_entity_actingentity_movingentity_menu = tk.Menu(self.debug_spawn_entity_menu)
        self.debug_spawn_entity_actingentity_menu.add_cascade(label="MovingEntity", menu=self.debug_spawn_entity_actingentity_movingentity_menu)
        self.debug_spawn_entity_actingentity_movingentity_menu.add_command(label="Colonist", command=lambda: self.parent.game.set_tool("spawn:entity:actingentity:movingentity:colonist"))

        self.debug_spawn_acting_movingentity_animal_menu = tk.Menu(self.debug_spawn_entity_actingentity_movingentity_menu)
        self.debug_spawn_entity_actingentity_movingentity_menu.add_cascade(label="Animal", menu=self.debug_spawn_acting_movingentity_animal_menu)

        for animal in self.parent.game.register_animals:
            self.debug_spawn_acting_movingentity_animal_menu.add_command(label=self.parent.game.register_animals[animal].species, command=lambda current_animal=animal: self.parent.game.set_tool("spawn:entity:actingentity:movingentity:animal:{}".format(current_animal.lower())))

        self.debug_destroy_menu = tk.Menu(self)
        self.debug_destroy_menu.add_command(label="Entity",
                                            command=lambda: self.parent.game.set_tool("destroy:entity"))
        self.add_cascade(label="Destroy", menu=self.debug_destroy_menu)
