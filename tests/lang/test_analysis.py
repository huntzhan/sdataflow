# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import pytest
from sdataflow.shared import Entity, Outcome
from sdataflow.lang.analysis import Dataflow
from test_parser import parser, get_rules


def prepare_dataflow(parser, doc):
    rules = get_rules(parser, doc)
    df = Dataflow(rules)
    df._build_DAG()
    df._topology_sort()
    return df


def get_tables(parser, doc):
    df = prepare_dataflow(parser, doc)
    return df.entity_table, df.outcome_table


def get_linear_ordering(parser, doc):
    df = prepare_dataflow(parser, doc)
    return df.linear_ordering


def get_roots(parser, doc):
    df = prepare_dataflow(parser, doc)
    return df.roots


def check_roots(expected, actual):
    # test type.
    assert set([Entity]) == {type(e) for e in expected}
    assert set([Entity]) == {type(e) for e in actual}
    # test name.
    assert {e.name for e in expected} == {e.name for e in actual}


def test_transform(parser):
    doc = 'A --> B'
    et, ot = get_tables(parser, doc)
    A = et['A']
    B = et['B']
    OA = ot['A']
    assert len(et) == 2
    assert len(ot) == 1
    assert A.outcomes == {'A': OA}
    assert OA.entities == set([B])


def test_one_to_more(parser):
    doc = ('A --> B '
           'A --> C '
           'A --> D ')
    et, ot = get_tables(parser, doc)
    A = et['A']
    B = et['B']
    C = et['C']
    D = et['D']
    OA = ot['A']
    assert len(et) == 4
    assert len(ot) == 1
    assert A.outcomes == {'A': OA}
    assert OA.entities == set([B, C, D])


def test_more_to_one(parser):
    doc = ('B --> [type] '
           'C --> [type] '
           'D --> [type] '
           '[type] --> A ')
    et, ot = get_tables(parser, doc)
    A = et['A']
    B = et['B']
    C = et['C']
    D = et['D']
    Otype = ot['type']
    assert len(et) == 4
    assert len(ot) == 1
    assert B.outcomes == {'type': Otype}
    assert C.outcomes == {'type': Otype}
    assert D.outcomes == {'type': Otype}
    assert Otype.entities == set([A])


def test_cycle_case1(parser):
    doc = 'A --> B B --> A '
    with pytest.raises(RuntimeError):
        get_linear_ordering(parser, doc)


def test_cycle_case2(parser):
    doc = 'A --> B B --> C C --> D D --> A'
    with pytest.raises(RuntimeError):
        get_linear_ordering(parser, doc)


def test_acyclic_case1(parser):
    doc = 'B --> C A --> B'
    assert [
        Entity('A'), Outcome('A'),
        Entity('B'), Outcome('B'),
        Entity('C'),
    ] == get_linear_ordering(parser, doc)


def test_roots_case1(parser):
    doc = 'B --> C A --> B'
    check_roots(
        [Entity('A')],
        get_roots(parser, doc),
    )


def test_roots_case2(parser):
    doc = ('B --> [type] '
           'C --> [type] '
           'D --> [type] '
           '[type] --> A ')
    check_roots(
        [
            Entity('B'),
            Entity('C'),
            Entity('D'),
        ],
        get_roots(parser, doc),
    )
