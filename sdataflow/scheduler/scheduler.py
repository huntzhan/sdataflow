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
from sdataflow.shared import Entity, OutcomeType


# user can define two kinds of callback:
# 1. A normal function returns an iterable object, of which the element is a
# (key, value) tuple, with key as the name of outcome type and value as user
# defined object.
# 2. A generator yield the element same as (1).
#
# input: registered linear ordering.
def scheduler(linear_ordering):

    for element in linear_ordering:
        if isinstance(element, Entity):
            run_callback_of_entity(element)
        elif isinstance(element, OutcomeType):
            pass_outcome_to_entity(element)


def run_callback_of_entity(entity):
    # get outcome.
    args_size = len(getargspec(entity.callback).args)
    if args_size == 0:
        callback_outcome = entity.callback()
    elif args_size == 1:
        callback_outcome = entity.callback(entity.input_data)
    else:
        raise RuntimeError(
            'Wrong args size of {0}.'.format(entity.callback.__name__))

    # allow callback that return nothing.
    if callback_outcome is None:
        return

    # store outcome.
    for name, obj in callback_outcome:
        outcome_type = entity.outcome_types.get(name, None)
        if outcome_type is None:
            msg_template = '{0} genreated wrong outcome type [{1}]'
            raise RuntimeError(msg_template.format(entity, name))
        outcome_type.data_cache.append(
            (name, obj),
        )


def pass_outcome_to_entity(outcome_type):
    for pair in outcome_type.data_cache:
        for entity in outcome_type.entities:
            entity.input_data.append(deepcopy(pair))
