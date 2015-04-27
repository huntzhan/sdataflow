# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

# import inspect.getargspec(py2) or inspect.getfullargspec(py3)
import sys
if sys.version_info.major == 2:
    from inspect import getargspec
elif sys.version_info.major == 3:
    from inspect import getfullargspec as getargspec

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
        entity_table[name].callback = normalize_callback(callback)


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


# if callback is legal, return 0 indicates callback accepts no argument, return
# 1 indicates callback accepts exactly one argument.
def callback_form_checker(callback):
    # Since inspect.isfunction and inspect.ismethod is buggy in Python 2.7,
    # test callback's attribute directly instead.
    is_callable = hasattr(callback, '__call__')
    is_method = hasattr(callback, '__self__')
    is_bound_method = bool(getattr(callback, '__self__', False))

    if not is_callable:
        raise RuntimeError('{} is not callable.'.format(callback))
    if is_method and not is_bound_method:
        raise RuntimeError('{} is unbound method.'.format(callback))

    # test length of callback's args.
    args_size = len(getargspec(callback).args)
    if is_bound_method:
        # uncount the first bound arg.
        args_size = args_size - 1

    # test length of argument.
    if args_size in [0, 1]:
        return args_size
    else:
        raise RuntimeError(
            ('{0} should accept 0 or 1 argument'
             ' instead of {1}.').format(callback, args_size)
        )


def normalize_callback(callback):

    def zero_arg_callback(items):
        return callback()

    if callback_form_checker(callback) == 0:
        return zero_arg_callback
    else:
        return callback
