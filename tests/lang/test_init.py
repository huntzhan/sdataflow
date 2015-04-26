# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.lang import parse
from sdataflow.shared import Entity, Outcome


def test_parse_six_text_type():
    doc = 'B --> C A --> B'
    assert [
        Entity('A'), Outcome('A'),
        Entity('B'), Outcome('B'),
        Entity('C'),
    ] == parse(doc)


def test_parse_six_binary_type():
    doc = b'B --> C A --> B'
    assert [
        Entity('A'), Outcome('A'),
        Entity('B'), Outcome('B'),
        Entity('C'),
    ] == parse(doc)
