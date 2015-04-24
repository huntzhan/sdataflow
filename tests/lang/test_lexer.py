# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from pytest import fixture
from sdataflow.lang.lexer import create_lexer


@fixture
def lexer():
    return create_lexer()


def get_types_and_values(lexer, doc):
    extract_types = lambda tokens: [t.type for t in tokens]
    extract_values = lambda tokens: [t.value for t in tokens]

    lexer.input(doc)
    tokens = []
    while True:
        token = lexer.token()
        if token:
            tokens.append(token)
        else:
            break
    return extract_types(tokens), extract_values(tokens)


def check_types(expected, result):
    if len(expected) == 1:
        return set(expected) == set(result)
    else:
        return expected == result


def test_simple_case(lexer):
    doc = ('entry_a --> ENTRY_B\n'
           'A -->[type]\n'
           'A --[type]--> B\n')
    types, values = get_types_and_values(lexer, doc)
    assert check_types(
        [
            # 1st.
            'ID', 'ARROW', 'ID',
            # 2nd.
            'ID', 'ARROW', 'BRACKET_LEFT', 'ID', 'BRACKET_RIGHT',
            # 3rd.
            'ID', 'DOUBLE_HYPHENS',
            'BRACKET_LEFT', 'ID', 'BRACKET_RIGHT',
            'ARROW', 'ID',
        ],
        types,
    )
    assert ['entry_a', '-->', 'ENTRY_B',
            'A', '-->', '[', 'type', ']',
            'A', '--', '[', 'type', ']', '-->', 'B'] == values
