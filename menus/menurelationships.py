#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import tkinter as tk
from string import capwords

import colony

__title__ = "MenuRelationships"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


class MenuRelationships(tk.Menu):
    def __init__(self, parent, **kwagrs):
        tk.Menu.__init__(self, parent, **kwagrs)
        self.parent = parent

        self.add_command(label="Show All Relationships", command=lambda: colony.RelationshipsWindow(self.parent.parent))

    def add_relation(self, colonist):
        menu = tk.Menu(self)

        for relationship_type in colonist.relationships:
            if isinstance(colonist.relationships[relationship_type], dict):
                menu_relations = tk.Menu(menu)

                for relationship in colonist.relationships[relationship_type]:
                    if isinstance(colonist.relationships[relationship_type][relationship], list):
                        menu_sibling = tk.Menu(menu_relations)

                        for sibling in colonist.relationships[relationship_type][relationship]:
                            menu_sibling.add_command(label=capwords(sibling.get_name()))

                        if colonist.relationships[relationship_type][relationship]:
                            menu_relations.add_cascade(label=capwords(relationship), menu=menu_sibling)

                    else:
                        if colonist.relationships[relationship_type][relationship]:
                            menu_relations.add_command(label=capwords(relationship))

                menu.add_cascade(label=capwords(relationship_type), menu=menu_relations)

        self.add_cascade(label=colonist.get_name(), menu=menu)
