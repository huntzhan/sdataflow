# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from six import text_type
from sdataflow.shared import Entity, Outcome
from sdataflow.debug.mermaid_page import (generate_definition, generate_link,
                                          get_js, render_template)

A = Entity('A')
t = Outcome('type')


def test_generate_definition():
    assert 'id1{Entity: A}' == generate_definition(A)
    assert 'id2(Outcome: type)' == generate_definition(t)


def test_generate_link():
    assert 'id1 --> id2' == generate_link(A, t)
    assert 'id2 --> id1' == generate_link(t, A)


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
