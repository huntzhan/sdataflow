# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.shared import to_unicode
from .lexer import create_lexer
from .parser import create_parser
from .analysis import Dataflow


__all__ = ['parse']


# input: `doc` with type of six.binary_type or six.text_type.
# output: linear ordering and root nodes of dataflow.
def parse(doc):
    # prepare `doc`.
    doc = to_unicode(doc)
    if doc is None:
        raise RuntimeError('parse: doc should be six.binary_type'
                           ' or six.text_type')
    # parse doc.
    lexer = create_lexer()
    parser = create_parser()
    lexer.input(doc)
    rules = parser.parse(lexer=lexer)

    # analyze `rules`.
    dataflow = Dataflow(rules)
    return dataflow.analyze()
