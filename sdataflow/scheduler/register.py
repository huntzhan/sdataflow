# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.shared import Entry


def hook_callbacks(linear_ordering, name_callback_mapping):
    # collect entry from `linear_ordering`.
    entry_table = {e.name: e for e in linear_ordering
                   if isinstance(e, Entry)}
    # check.
    consistency_checker(entry_table, name_callback_mapping)
    # attach callback to entry of `entry_table`.
    for name, callback in name_callback_mapping.items():
        entry_table[name].callback = callback


def consistency_checker(entry_table, name_callback_mapping):
    names_of_entry_table = set(entry_table.keys())
    names_of_callback_hooks = set(name_callback_mapping.keys())

    if names_of_entry_table != names_of_callback_hooks:
        msg_template = ('entry not match:\n'
                        'linear_ordering: {0}\n'
                        'callback: {1}')
        msg = msg_template.format(
            names_of_entry_table,
            names_of_callback_hooks,
        )
        raise RuntimeError(msg)
