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
        # color for DFS search.
        WHITE = 0
        GRAY = 1
        BLACK = 2

        # dict for storing the color of vertices.
        color = {}
        for entry in self.entry_table.values():
            color[entry] = WHITE
        for outcome_type in self.outcome_type_table.values():
            color[outcome_type] = WHITE

        # result of topology search.
        self.linear_ordering = []

        def DFS_visit(u):
            color[u] = GRAY
            for v in u.get_adjacent_vertices():  # explore edge (u, v)
                if color[v] == WHITE:
                    DFS_visit(v)
                elif color[v] == GRAY:
                    # discover back edge.
                    raise RuntimeError(
                        'Detected back edge: {0} to {1}.'.format(u, v))
            color[u] = BLACK
            self.linear_ordering.insert(0, u)

        # DFS.
        for u in color.keys():
            if color[u] == WHITE:
                DFS_visit(u)

    def generate_linear_ordering(self):
        self.build_DAG()
        self.topology_sort()
        return self.linear_ordering
