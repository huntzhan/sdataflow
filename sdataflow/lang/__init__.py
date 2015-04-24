# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from six import text_type, binary_type
from .lexer import create_lexer
from .parser import create_parser
from .analysis import DataFlow


__all__ = ['parse']


# input: `doc` with type of six.binary_type or six.text_type.
# output: linear ordering of dataflow.
def parse(doc):
    # prepare `doc`.
    if isinstance(doc, binary_type):
        doc = doc.decode('utf-8')
    elif isinstance(doc, text_type):
        # it's good, do nothing.
        pass
    else:
        raise RuntimeError('parse: doc should be six.binary_type'
                           ' or six.text_type')
    # parse doc.
    lexer = create_lexer()
    parser = create_parser()
    lexer.input(doc)
    rules = parser.parse(lexer=lexer)

    # analyze `rules`.
    dataflow = DataFlow(rules)
    return dataflow.generate_linear_ordering()
