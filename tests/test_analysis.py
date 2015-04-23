# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.lang.analysis import DataFlow
from test_parser import parser, get_rules


def get_tables(parser, doc):
    rules = get_rules(parser, doc)
    df = DataFlow(rules)
    df.build_DAG()
    return df.entry_table, df.outcome_type_table


def test_transform(parser):
    doc = 'A --> B'
    et, ot = get_tables(parser, doc)
    A = et['A']
    B = et['B']
    OA = ot['A']
    assert len(et) == 2
    assert len(ot) == 1
    assert A.outcome_types == {'A': OA}
    assert OA.entries == set([B])


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
    assert A.outcome_types == {'A': OA}
    assert OA.entries == set([B, C, D])


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
    assert B.outcome_types == {'type': Otype}
    assert C.outcome_types == {'type': Otype}
    assert D.outcome_types == {'type': Otype}
    assert Otype.entries == set([A])
