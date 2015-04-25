# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from sdataflow.lang import parse
from sdataflow.scheduler import hook_callbacks, scheduler, create_data_wrapper


def run(doc, name_callback_mapping):
    linear_ordering = parse(doc)
    hook_callbacks(linear_ordering, name_callback_mapping)
    scheduler(linear_ordering)


def test_dispatch_and_merge():
    doc = ('A --[odd]--> B '
           'A --[even]--> C '
           'B --> D '
           'C --> D ')

    def a():
        odd = create_data_wrapper('odd')
        even = create_data_wrapper('even')
        for i in range(1, 10):
            if i % 2 == 0:
                yield even(i)
            else:
                yield odd(i)

    def b(items):
        default = create_data_wrapper('B')
        # remove 1.
        for outcome_name, number in items:
            if number == 1:
                continue
            yield default(number)

    def c(items):
        default = create_data_wrapper('C')
        # remove 2.
        for outcome_name, number in items:
            if number == 2:
                continue
            yield default(number)

    def d(items):
        numbers = {i for _, i in items}
        assert set(range(3, 10)) == numbers

    name_callback_mapping = {
        'A': a,
        'B': b,
        'C': c,
        'D': d,
    }
    run(doc, name_callback_mapping)


def test_deepcopy():
    doc = ('A --> B '
           'A --> C '
           'B --> D '
           'C --> E ')

    class Whatever(object):
        pass

    def a():
        default = create_data_wrapper('A')
        w = Whatever()
        w.data = 42
        yield default(w)

    def b(items):
        default = create_data_wrapper('B')
        for _, w in items:
            w.data = 0
            yield default(w)

    def c(items):
        default = create_data_wrapper('C')
        for _, w in items:
            yield default(w)

    def d(items):
        for _, w in items:
            assert w.data == 0

    def e(items):
        for _, w in items:
            assert w.data == 42

    name_callback_mapping = {
        'A': a,
        'B': b,
        'C': c,
        'D': d,
        'E': e,
    }
    run(doc, name_callback_mapping)
