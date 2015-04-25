# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.shared import to_unicode, Entity


def hook_callbacks(linear_ordering, name_callback_mapping):
    # deal with utf-8 binary.
    cache_mapping = name_callback_mapping
    name_callback_mapping = {to_unicode(name): entity
                             for name, entity in cache_mapping.items()}
    # collect entity from `linear_ordering`.
    entity_table = {e.name: e for e in linear_ordering
                   if isinstance(e, Entity)}
    # check.
    consistency_checker(entity_table, name_callback_mapping)
    # attach callback to entity of `entity_table`.
    for name, callback in name_callback_mapping.items():
        entity_table[name].callback = callback


def consistency_checker(entity_table, name_callback_mapping):
    names_of_entity_table = set(entity_table.keys())
    names_of_callback_hooks = set(name_callback_mapping.keys())

    if names_of_entity_table != names_of_callback_hooks:
        msg_template = ('entity not match:\n'
                        'linear_ordering: {0}\n'
                        'callback: {1}')
        msg = msg_template.format(
            names_of_entity_table,
            names_of_callback_hooks,
        )
        raise RuntimeError(msg)
