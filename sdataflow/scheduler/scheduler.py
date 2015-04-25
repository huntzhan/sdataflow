# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import sys
# import inspect.getargspec(py2) or inspect.getfullargspec(py3)
if sys.version_info.major == 2:
    from inspect import getargspec
elif sys.version_info.major == 3:
    from inspect import getfullargspec as getargspec

from copy import deepcopy
from sdataflow.shared import Entry, OutcomeType


# user defined can define two kinds of callback:
# 1. A normal function returns an iterable object, of which the element is a
# (key, value) tuple, with key as the name of outcome type and value as user
# defined object.
# 2. A generator yield the element same as (1).
#
# input: registered linear ordering.
def scheduler(linear_ordering):

    for element in linear_ordering:
        if isinstance(element, Entry):
            run_callback_of_entry(element)
        elif isinstance(element, OutcomeType):
            pass_outcome_to_entry(element)


def run_callback_of_entry(entry):
    # get outcome.
    args_size = len(getargspec(entry.callback).args)
    if args_size == 0:
        callback_outcome = entry.callback()
    elif args_size == 1:
        callback_outcome = entry.callback(entry.input_data)
    else:
        raise RuntimeError(
            'Wrong args size of {0}.'.format(entry.callback.__name__))

    # allow callback that return nothing.
    if callback_outcome is None:
        return

    # store outcome.
    for name, obj in callback_outcome:
        outcome_type = entry.outcome_types.get(name, None)
        if outcome_type is None:
            msg_template = '{0} genreated wrong outcome type [{1}]'
            raise RuntimeError(msg_template.format(entry, name))
        outcome_type.data_cache.append(
            (name, obj),
        )


def pass_outcome_to_entry(outcome_type):
    for pair in outcome_type.data_cache:
        for entry in outcome_type.entries:
            entry.input_data.append(deepcopy(pair))
