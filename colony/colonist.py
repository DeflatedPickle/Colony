#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import random
from string import capwords
from textwrap import indent

from colony.entities.attributes import Age, Joy, Health, Inventory, Gender
from colony.entities import Entity
from colony.entities import MovingEntity
from colony.references import get_male_names, get_female_names, get_surnames, get_male_relationship_types, \
    get_female_relationship_types, get_parent_types, get_sibling_types, get_child_types

__title__ = "Colonist"
__author__ = "DeflatedPickle"
__version__ = "1.13.1"


class Colonist(MovingEntity, Age, Joy, Health, Inventory, Gender):
    """Creates a colonist."""

    def __init__(self, parent, species: str = "Human", forename: str = "", surname: str = "", faction: str = "colony", x: int = 0, y: int = 0):
        MovingEntity.__init__(self, parent, x, y, entity_type="colonist")
        Age.__init__(self, parent.time, 1, 16, 100)
        Health.__init__(self)
        Inventory.__init__(self)
        Gender.__init__(self)
        self.parent = parent
        # Note: Maybe use an Enum for species instead of a string.
        self.species = species
        # TODO: Add nicknames.
        # TODO: Add middle names.
        self.name = {"title": None,
                     "forename": forename,
                     "middle names": [],
                     "nickname": None,
                     "surname": surname}
        # TODO: Add more colonist actions.
        # TODO: Add colonist relationships.
        self.relationships = {"family": {"mothers": [], "fathers": [], "sisters": [], "brothers": [], "daughters": [],
                                         "sons": []}}  # , "wives": [], "husbands": []}}
        # Note: Maybe use an Enum for faction instead of a string.
        self.faction = faction
        # TODO: Add colonist stats.
        # TODO: Add colonist buffs and debuffs, such as "Fast Walker" to improve move speed.

        self.check_action()

    def add_to_colonist_bar(self):
        self.parent.colonist_bar.add_colonist(self)

        return self

    def remove_from_colonist_bar(self):
        self.parent.colonist_bar.remove_colonist(self)

        return self

    def get_name(self):
        """Returns the name of the colonist."""
        return "{} {}".format(self.name["forename"], self.name["surname"])

    def get_forename_or_nickname(self):
        """Returns the nickname if their is one, and if not, the forename"""
        return self.name["nickname"] if self.name["nickname"] else self.name["forename"]

    def get_gender_string(self):
        """Returns the gender of the colonist as "Female" or "Male"."""
        return "Female" if not self.get_gender() else "Male"

    def draw(self):
        MovingEntity.draw(self)
        self.parent.colonists.append(self)

        return self

    def generate_random(self):
        """Generates a random colonist."""
        self.set_gender(random.randint(0, 1))

        if self.get_gender():
            self.name["forename"] = get_male_names()[random.randint(0, len(get_male_names()) - 1)]

        elif not self.get_gender():
            self.name["forename"] = get_female_names()[random.randint(0, len(get_female_names()) - 1)]

        self.name["surname"] = get_surnames()[random.randint(0, len(get_surnames()) - 1)]
        self._age = random.randint(self.get_lowest_age(), self.get_highest_age())

        return self

    def generate_random_relationship(self):
        """Generates a random relationship."""
        if len(self.parent.colonists) != 1:
            for relationship_header in self.relationships:
                relationship = random.choice(list(self.relationships[relationship_header].keys()))
                colonist = random.choice(self.parent.colonists)
                this = self.parent.colonists[self.parent.colonists.index(self)]

                if colonist != this:
                    if not colonist.get_gender() and relationship in get_female_relationship_types() or colonist.get_gender() and relationship in get_male_relationship_types():
                        if relationship in get_parent_types() and colonist.get_age() > this.get_age() or relationship in get_child_types() and colonist.get_age() < this.get_age() or relationship in get_sibling_types():
                            self.relationships[relationship_header][relationship].append(colonist)
                            self.parent.taskbar.menu_relationships.add_relation(self)

                            if relationship in get_parent_types():
                                # This colonist is a parent of the random colonist.
                                colonist.relationships[relationship_header][get_child_types()[int(self.get_gender())]].append(
                                    self)

                            elif relationship in get_sibling_types():
                                # This colonist is a sibling of the random colonist.
                                colonist.relationships[relationship_header][get_sibling_types()[int(this.get_gender())]].append(
                                    self)

                            elif relationship in get_child_types():
                                # This colonist is a child of the random colonist.
                                colonist.relationships[relationship_header][get_parent_types()[int(self.get_gender())]].append(
                                    self)

                        else:
                            # print("Thrown Out: " + relationship + " relationship |", "Between: " + colonist.get_name() + " And " + self.get_name() + " - Reason: Too young or too old.")
                            self.generate_random_relationship()

                    else:
                        # print("Thrown Out: " + relationship + " relationship |", "Between: " + colonist.get_name() + " And " + self.get_name() + " - Reason: Wrong genders.")
                        self.generate_random_relationship()

                else:
                    # print("Thrown Out: " + relationship + " relationship |", "Between: " + colonist.get_name() + " And " + self.get_name() + " - Reason: Same Colonist")
                    self.generate_random_relationship()

    def generate_random_relationship_to(self, entity: Entity):
        """Generates a random relationship to an entity."""
        for relationship_header in self.relationships:
            self.relationships[relationship_header][
                random.choice(list(self.relationships[relationship_header].keys()))].append(entity)

        self.parent.taskbar.menu_relationships.add_relation(self)

    def generate_specific_relationship(self, relationship: str):
        """Generates a specific relationship."""
        for relationship_header in self.relationships:
            if relationship in self.relationships[relationship_header]:
                self.relationships[relationship_header][relationship].append(random.choice(self.parent.colonists))

        self.parent.taskbar.menu_relationships.add_relation(self)

    def generate_specific_relationship_to(self, relationship: str, entity: Entity):
        """Generate a specific relationship to an entity."""
        for relationship_header in self.relationships:
            if relationship in self.relationships[relationship_header]:
                self.relationships[relationship_header][relationship].append(entity)

        self.parent.taskbar.menu_relationships.add_relation(self)

    def get_relationships(self):
        """Gets all the relationships of this pawn."""
        return self.relationships

    def get_relationship(self, relation: str):
        """Gets a specific relationship of this pawn."""
        return self.relationships[relation]

    def get_relation_to(self, entity: Entity):
        """Gets a relationship to another pawn."""
        # TODO: Make this function do something.
        pass

    def get_pretty_relationships(self):
        string = list()

        for relationship_header in self.relationships:
            string.append(capwords(relationship_header) + ":")
            for relationship_type in self.relationships[relationship_header]:
                string.append(indent(capwords(relationship_type) + ":", " " * 4))
                string.append(indent("\n".join(
                    [colonist.get_name() for colonist in self.relationships[relationship_header][relationship_type]]),
                                     " " * 8))

        return "\n".join(string)

    def get_pretty_information(self):
        string = list()

        string.append(self.get_name() + ":")
        for item in ["Species: " + self.species, "Age: " + str(self.get_age()), "Gender: " + self.get_gender_string(),
                     "Faction: " + self.faction]:
            string.append(indent(item, " " * 4))
        string.append(indent(self.get_pretty_relationships(), " " * 4))

        return "\n".join(string)
