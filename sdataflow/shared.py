# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from six import text_type, binary_type


def to_unicode(doc):
    if isinstance(doc, binary_type):
        doc = doc.decode('utf-8')
    elif isinstance(doc, text_type):
        # it's good, do nothing.
        pass
    else:
        doc = None
    return doc


class InfoBase(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<{0}: {1}>'.format(type(self).__name__, self.name)

    def __hash__(self):
        return id(self)


class Entity(InfoBase):

    def __init__(self, name):
        super(Entity, self).__init__(name)
        # contains mapping from the name(a string) of outcome to a outcome
        # object.
        self.outcome_types = {}
        # container of input of callback.
        self.input_data = []

    def add_outcome_type(self, outcome_type):
        self.outcome_types[outcome_type.name] = outcome_type

    def get_adjacent_vertices(self):
        return self.outcome_types.values()


class OutcomeType(InfoBase):

    def __init__(self, name):
        super(OutcomeType, self).__init__(name)
        # contains a set of entities that accept current type as input value.
        self.entities = set()
        # cache of outcome.
        self.data_cache = []

    def add_entity(self, entity):
        self.entities.add(entity)

    def get_adjacent_vertices(self):
        return self.entities
