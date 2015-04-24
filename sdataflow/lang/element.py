# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class InfoBase(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<{0}: {1}>'.format(type(self).__name__, self.name)


class Entry(InfoBase):

    def __init__(self, name):
        super(Entry, self).__init__(name)
        # contains mapping from the name(a string) of outcome to a outcome
        # object.
        self.outcome_types = {}

    def add_outcome_type(self, outcome_type):
        self.outcome_types[outcome_type.name] = outcome_type

    def get_adjacent_vertices(self):
        return self.outcome_types.values()


class OutcomeType(InfoBase):

    def __init__(self, name):
        super(OutcomeType, self).__init__(name)
        # contains a set of entries that accept current type as input value.
        self.entries = set()

    def add_entry(self, entry):
        self.entries.add(entry)

    def get_adjacent_vertices(self):
        return self.entries
