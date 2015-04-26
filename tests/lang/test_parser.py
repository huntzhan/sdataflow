# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from pytest import fixture
from sdataflow.shared import Entity, Outcome
from sdataflow.lang.lexer import create_lexer
from sdataflow.lang.parser import create_parser


@fixture
def parser():
    return create_parser()


def get_rules(parser, doc):
    lexer = create_lexer()
    lexer.input(doc)
    rules = parser.parse(lexer=lexer)
    return rules


def test_entity_to_entity(parser):
    doc = 'A --> B'
    assert [(Entity('A'), Entity('B'))] == get_rules(parser, doc)


def test_entity_to_outcome(parser):
    doc = 'A --> [type]'
    assert [(Entity('A'), Outcome('type'))] == get_rules(parser, doc)


def test_outcome_to_entity(parser):
    doc = '[type] --> A'
    assert [(Outcome('type'), Entity('A'))] == get_rules(parser, doc)


def test_entity_to_entity_with_outcome(parser):
    doc = 'A --[type]--> B'
    print(get_rules(parser, doc))
    assert [
        (Entity('A'), Outcome('type')),
        (Outcome('type'), Entity('B')),
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
        (Entity('A'), Entity('B')),
        (Entity('A'), Entity('C')),
        (Entity('A'), Entity('D')),
        # section 2.
        (Entity('B'), Entity('A')),
        (Entity('C'), Entity('A')),
        (Entity('D'), Entity('A')),
        # section 3.
        (Entity('A'), Outcome('type1')),
        (Entity('A'), Outcome('type2')),
        (Outcome('type1'), Entity('B')),
        (Outcome('type2'), Entity('C')),
        # section 4.
        (Entity('A'), Outcome('type1')),
        (Outcome('type1'), Entity('B')),
        (Entity('A'), Outcome('type2')),
        (Outcome('type2'), Entity('C')),
        # section 5.
        (Entity('A'), Outcome('type1')),
        (Entity('A'), Outcome('type2')),
        (Outcome('type1'), Entity('B')),
        (Outcome('type1'), Entity('C')),
        (Outcome('type2'), Entity('D')),
        (Outcome('type2'), Entity('E')),
        # section 6.
        (Entity('A'), Outcome('type1')),
        (Entity('B'), Outcome('type1')),
        (Outcome('type1'), Entity('C')),
    ]
    assert expected_rules == get_rules(parser, doc)
