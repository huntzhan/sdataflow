# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import pytest
from sdataflow.shared import Entity, Outcome
from sdataflow.scheduler import hook_callbacks


def callback_generator(name):
    def _callback():
        return name
    return _callback


def test_hook():
    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    name_callback_mapping = {
        'A': callback_generator('callback of A'),
        'C': callback_generator('callback of C'),
    }
    hook_callbacks(linear_ordering, name_callback_mapping)

    assert linear_ordering[0].callback() == 'callback of A'
    assert linear_ordering[2].callback() == 'callback of C'
    assert getattr(linear_ordering[1], 'callback', None) is None


def test_utf8():
    linear_ordering = [Entity('中文')]
    name_callback_mapping = {
        b'\xe4\xb8\xad\xe6\x96\x87': callback_generator('match utf-8'),
    }
    hook_callbacks(linear_ordering, name_callback_mapping)

    assert linear_ordering[0].callback() == 'match utf-8'


def test_inconsistent_case1():
    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    # missing C.
    name_callback_mapping = {
        'A': None,
    }
    with pytest.raises(RuntimeError):
        hook_callbacks(linear_ordering, name_callback_mapping)


def test_inconsistent_case2():
    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    # B, D not exist.
    name_callback_mapping = {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
    }
    with pytest.raises(RuntimeError):
        hook_callbacks(linear_ordering, name_callback_mapping)
