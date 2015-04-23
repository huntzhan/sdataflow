# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from pytest import fixture
from sdataflow.lang.lexer import create_lexer
from sdataflow.lang.parser import create_parser
from sdataflow.lang.element import Entry, OutcomeType


@fixture
def parser():
    return create_parser()


def get_rules(parser, doc):
    lexer = create_lexer()
    lexer.input(doc)
    rules = parser.parse(lexer=lexer)
    return rules


def test_entry_to_entry(parser):
    doc = 'A --> B'
    assert [(Entry('A'), Entry('B'))] == get_rules(parser, doc)


def test_entry_to_outcome_type(parser):
    doc = 'A --> [type]'
    assert [(Entry('A'), OutcomeType('type'))] == get_rules(parser, doc)


def test_outcome_type_to_entry(parser):
    doc = '[type] --> A'
    assert [(OutcomeType('type'), Entry('A'))] == get_rules(parser, doc)


def test_entry_to_entry_with_outcome_type(parser):
    doc = 'A --[type]--> B'
    print(get_rules(parser, doc))
    assert [
        (Entry('A'), OutcomeType('type')),
        (OutcomeType('type'), Entry('B')),
    ] == get_rules(parser, doc)


def test_multiple_stats(parser):
    doc = '''
# one-to-more
A --> B
A --> C
A --> D

# more-to-one
B --> A
C --> A
D --> A

# one way.
A --> [type1]
A --> [type2]
[type1] --> B
[type2] --> C

# another way.
A --[type1]--> B
A --[type2]--> C

# one-to-more example.
A --> [type1]
A --> [type2]
[type1] --> B
[type1] --> C
[type2] --> D
[type2] --> E

# more-to-one example.
A --> [type1]
B --> [type1]
[type1] --> C'''
    expected_rules = [
        # section 1.
        (Entry('A'), Entry('B')),
        (Entry('A'), Entry('C')),
        (Entry('A'), Entry('D')),
        # section 2.
        (Entry('B'), Entry('A')),
        (Entry('C'), Entry('A')),
        (Entry('D'), Entry('A')),
        # section 3.
        (Entry('A'), OutcomeType('type1')),
        (Entry('A'), OutcomeType('type2')),
        (OutcomeType('type1'), Entry('B')),
        (OutcomeType('type2'), Entry('C')),
        # section 4.
        (Entry('A'), OutcomeType('type1')),
        (OutcomeType('type1'), Entry('B')),
        (Entry('A'), OutcomeType('type2')),
        (OutcomeType('type2'), Entry('C')),
        # section 5.
        (Entry('A'), OutcomeType('type1')),
        (Entry('A'), OutcomeType('type2')),
        (OutcomeType('type1'), Entry('B')),
        (OutcomeType('type1'), Entry('C')),
        (OutcomeType('type2'), Entry('D')),
        (OutcomeType('type2'), Entry('E')),
        # section 6.
        (Entry('A'), OutcomeType('type1')),
        (Entry('B'), OutcomeType('type1')),
        (OutcomeType('type1'), Entry('C')),
    ]
    assert expected_rules == get_rules(parser, doc)
