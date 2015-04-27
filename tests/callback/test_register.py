# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import sys
import pytest
from sdataflow.shared import Entity, Outcome
from sdataflow.callback import hook_callbacks, register_callback


def callback_generator(name):
    def _callback():
        return name
    return _callback


class HooksTester(object):

    def __init__(self, entity_names):
        self.entity_names = entity_names

    def callback_generator(self, name):
        def _callback():
            return name
        return _callback

    def get_name_callback_mapping(self):
        return {name: self.callback_generator(i)
                for i, name in enumerate(self.entity_names)}

    def check_hook_of_entity(self, entity):
        return entity.callback(None) == self.entity_names.index(entity.name)

    @classmethod
    def check_outcome(cls, outcome):
        return getattr(outcome, 'callback', None) is None


def test_hook():
    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]

    ht = HooksTester(['A', 'C'])
    hook_callbacks(linear_ordering, ht.get_name_callback_mapping())

    assert ht.check_hook_of_entity(linear_ordering[0])
    assert ht.check_hook_of_entity(linear_ordering[2])
    assert ht.check_outcome(linear_ordering[1])


def test_utf8():
    linear_ordering = [Entity('中文')]
    name_callback_mapping = {
        b'\xe4\xb8\xad\xe6\x96\x87': callback_generator('match utf-8'),
    }
    hook_callbacks(linear_ordering, name_callback_mapping)
    assert linear_ordering[0].callback(None) == 'match utf-8'


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


def test_func():

    def zero_arg():
        return 0

    def one_arg(items):
        return 1

    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    name_callback_mapping = {
        'A': zero_arg,
        'C': one_arg,
    }
    hook_callbacks(linear_ordering, name_callback_mapping)
    assert linear_ordering[0].callback(None) == 0
    assert linear_ordering[2].callback(None) == 1


def test_illegal_func():

    def two_arg(items, whatever):
        pass

    linear_ordering = [Entity('A')]
    name_callback_mapping = {
        'A': two_arg,
    }
    with pytest.raises(RuntimeError):
        hook_callbacks(linear_ordering, name_callback_mapping)


def test_method_case1():

    class TestClass(object):

        def zero_arg(self):
            return 0

        def one_arg(self, items):
            return 1

    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    name_callback_mapping = {
        'A': TestClass().zero_arg,
        'C': TestClass().one_arg,
    }
    hook_callbacks(linear_ordering, name_callback_mapping)
    assert linear_ordering[0].callback(None) == 0
    assert linear_ordering[2].callback(None) == 1


def test_method_case2():

    class TestClass(object):

        @classmethod
        def zero_arg(cls):
            return 0

        @classmethod
        def one_arg(cls, items):
            return 1

    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    name_callback_mapping = {
        'A': TestClass.zero_arg,
        'C': TestClass.one_arg,
    }
    hook_callbacks(linear_ordering, name_callback_mapping)
    assert linear_ordering[0].callback(None) == 0
    assert linear_ordering[2].callback(None) == 1


@pytest.mark.skipif(
    sys.version_info.major == 3,
    reason='`TestClass.zero_arg` is a funtion in py3, not an unbound method.')
def test_unbound_method():

    class TestClass(object):
        pass

    def zero_arg():
        return 0

    TestClass.zero_arg = zero_arg

    linear_ordering = [Entity('A')]
    name_callback_mapping = {
        'A': TestClass.zero_arg,
    }
    with pytest.raises(RuntimeError):
        hook_callbacks(linear_ordering, name_callback_mapping)


def test_function_decorator_registration():

    @register_callback('A')
    def zero_arg():
        return 0

    @register_callback('C')
    def should_not_be_registered(items):
        return 1

    def one_arg(items):
        return 42

    linear_ordering = [Entity('A'), Outcome('B'), Entity('C')]
    hook_callbacks(linear_ordering, {'C': one_arg})
    assert linear_ordering[0].callback(None) == 0
    assert linear_ordering[2].callback(None) == 42


def test_function_decorator_code_injection():

    @register_callback('A', 'type1', 'type2')
    def func():
        return func.type1(1), func.type2(2)

    assert (
        ('type1', 1),
        ('type2', 2),
    ) == func()
