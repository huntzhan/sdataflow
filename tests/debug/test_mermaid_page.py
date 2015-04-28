# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from six import text_type
from sdataflow.shared import Entity, Outcome
from sdataflow.debug.mermaid_page import (
    get_js, render_template, MermaidPageGenerator, DefaultMode,
    OutcomeAsLinkTextMode, IgnoreOutcomeMode, NameContainer,
)


def init_page_generators(lo):
    NameContainer.clear()
    return DefaultMode(lo), OutcomeAsLinkTextMode(lo), IgnoreOutcomeMode(lo)


def test_render_template():
    expected = '''
<html>
<head>
<script>
js
</script>
</head>
<body>
<div class="mermaid">
line 1
line 2
line 3
</div>
</body>
</html>
'''
    actual = render_template(
        'js',
        [
            'line 1',
            'line 2',
            'line 3',
        ],
    )
    assert expected == actual


def test__get_js():
    js = get_js()
    assert isinstance(js, text_type)
    assert len(js) > 0


def test_modify_linear_ordering():
    default, outcome_as_text, ignore_outcome = init_page_generators(
        [Entity('A'), Outcome('x'), Entity('B'), Outcome('y')],
    )
    assert len(default.linear_ordering) == 4
    assert len(outcome_as_text.linear_ordering) == 2
    assert len(ignore_outcome.linear_ordering) == 2


def test_render_definition():
    default, outcome_as_text, ignore_outcome = init_page_generators([])
    A = Entity('A')
    t = Outcome('type')

    assert 'id1{Entity: A}' == default.render_definition(A)
    assert 'id2(Outcome: type)' == default.render_definition(t)

    assert 'id1(Entity: A)' == outcome_as_text.render_definition(A)
    assert not hasattr(outcome_as_text, 'OUTCOME_DEFINITION')

    assert 'id1(Entity: A)' == ignore_outcome.render_definition(A)
    assert not hasattr(ignore_outcome, 'OUTCOME_DEFINITION')


def test_render_link():
    default, outcome_as_text, ignore_outcome = init_page_generators([])
    A = Entity('A')
    B = Entity('B')
    t = Outcome('type')

    assert 'id1 --> id2' == default.render_link(A, t)
    assert 'id2 --> id1' == default.render_link(t, A)

    assert 'id1 -->|type| id3' == outcome_as_text.render_link(A, t, B)
    assert 'id1 --> id3' == ignore_outcome.render_link(A, t, B)
