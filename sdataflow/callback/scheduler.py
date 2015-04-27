# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from copy import deepcopy
from sdataflow.shared import Entity, Outcome


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
        elif isinstance(element, Outcome):
            pass_outcome_to_entity(element)


def run_callback_of_entity(entity):
    # get outcome.
    callback_outcome = entity.callback(entity.input_data)
    # allow callback that return nothing.
    if callback_outcome is None:
        return

    # store outcome.
    for name, obj in callback_outcome:
        outcome = entity.outcomes.get(name, None)

        if outcome is None:
            raise RuntimeError(
                '{0} genreated wrong outcome type [{1}]'.format(entity, name))

        outcome.data_cache.append(
            (name, obj),
        )


def pass_outcome_to_entity(outcome):
    for pair in outcome.data_cache:
        for entity in outcome.entities:
            entity.input_data.append(deepcopy(pair))
