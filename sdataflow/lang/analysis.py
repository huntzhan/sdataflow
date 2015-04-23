# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from .element import Entry, OutcomeType


class DataFlow(object):

    def __init__(self, rules):
        self.rules = rules
        self.entry_table = {}
        self.outcome_type_table = {}

    def get_unique_element(self, element):
        # target table.
        element_table = None
        if isinstance(element, Entry):
            element_table = self.entry_table
        elif isinstance(element, OutcomeType):
            element_table = self.outcome_type_table
        else:
            raise RuntimeError('get_unique_element')

        # retrieve or register element.
        if element.name in element_table:
            # retrieve.(ensure uniqueness)
            return element_table[element.name]
        else:
            # register.
            element_table[element.name] = element
            return element

    def build_DAG(self):
        for src, dst in self.rules:
            src = self.get_unique_element(src)
            dst = self.get_unique_element(dst)
            if isinstance(src, Entry) and isinstance(dst, Entry):
                # transform `EntryA --> EntryB` to
                # `EntryA --> [EntryA]` and `[EntryA] --> EntryB`.
                outcome_type = self.get_unique_element(OutcomeType(src.name))
                src.add_outcome_type(outcome_type)
                outcome_type.add_entry(dst)
            elif isinstance(src, Entry) and isinstance(dst, OutcomeType):
                # add outcome_type to entry.
                src.add_outcome_type(dst)
            elif isinstance(src, OutcomeType) and isinstance(dst, Entry):
                # add entry to outcome_type.
                src.add_entry(dst)
            else:
                raise RuntimeError('build_DAG')

    def topology_sort(self):
        pass
