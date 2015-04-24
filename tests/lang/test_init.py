# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.lang import parse
from sdataflow.shared import Entry, OutcomeType


def test_parse_six_text_type():
    doc = 'B --> C A --> B'
    assert [
        Entry('A'), OutcomeType('A'),
        Entry('B'), OutcomeType('B'),
        Entry('C'),
    ] == parse(doc)


def test_parse_six_binary_type():
    doc = b'B --> C A --> B'
    assert [
        Entry('A'), OutcomeType('A'),
        Entry('B'), OutcomeType('B'),
        Entry('C'),
    ] == parse(doc)
