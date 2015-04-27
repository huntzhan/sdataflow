#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from io import open
from docopt import docopt
from .metadata import version
from sdataflow.lang import parse
from sdataflow.debug.mermaid_page import generate_mermaid_page


DOC = '''
Usage:
    sdataflow <file>
'''


def entry_point():
    arguments = docopt(DOC, version=version)

    # load dataflow definition.
    file_path = arguments['<file>']
    doc = None
    try:
        doc = open(file_path, encoding='utf-8').read()
    except:
        print('Cannot open file {0}'.format(file_path))

    # parse.
    linear_ordering, _ = parse(doc)
    # generated page.
    removed_ext, _ = os.path.splitext(file_path)
    output_file_name = os.path.basename(removed_ext) + '.html'
    with open(output_file_name, encoding='utf-8', mode='w') as fout:
        fout.write(generate_mermaid_page(linear_ordering))


if __name__ == '__main__':
    entry_point()
