# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from .element import Entry, OutcomeType


class DataFlow(object):

    def __init__(self, rules):
        self.rules = rules
        self.entry_table = {}
        self.outcome_type_table = {}

    def _retrieve_or_record_element(self, table_name, element):
        element_table = getattr(self, table_name)
        if element.name in element_table:
            # retrieve.(ensure uniqueness)
            return element_table[element.name]
        else:
            # register.
            element_table[element.name] = element
            return element

    def get_entry(self, entry):
        return self._retrieve_or_record_element('entry_table', entry)

    def get_outcome_type(self, entry):
        return self._retrieve_or_record_element('outcome_type_table', entry)

    def build_DAG(self):
        for src, dst in self.rules:
            if isinstance(src, Entry) and isinstance(dst, Entry):
                src = self.get_entry(src)
                dst = self.get_entry(dst)
                # transform `EntryA --> EntryB` to
                # `EntryA --> [EntryA]` and `[EntryA] --> EntryB`.
                outcome_type = self.get_outcome_type(OutcomeType(src.name))
                src.add_outcome_type(outcome_type)
                outcome_type.add_entry(dst)
            elif isinstance(src, Entry) and isinstance(dst, OutcomeType):
                src = self.get_entry(src)
                dst = self.get_outcome_type(dst)
                # add outcome_type to entry.
                src.add_outcome_type(dst)
            elif isinstance(src, OutcomeType) and isinstance(dst, Entry):
                src = self.get_outcome_type(src)
                dst = self.get_entry(dst)
                # add entry to outcome_type.
                src.add_entry(dst)
            else:
                raise RuntimeError('build_DAG')

    def topology_sort(self):
        pass
