#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from io import open
from docopt import docopt
from .metadata import version
from sdataflow.lang import parse
from sdataflow.debug.mermaid_page import (
    MODE_DEFAULT, MODE_OUTCOME_AS_LINK_TEXT, MODE_IGNORE_OUTCOME,
    generate_mermaid_page,
)


DOC = '''
Usage:
    sdataflow [-m <mode>] <file>

Options:
    -m <mode>  <mode> could be 1, 2 or 3. `-m1` is default mode; `-m2` prints
               outcome as text of link; `-m3` ignore outcomes.
'''


def entry_point():
    arguments = docopt(DOC, version=version)
    mode_mapping = {
        '1': MODE_DEFAULT,
        '2': MODE_OUTCOME_AS_LINK_TEXT,
        '3': MODE_IGNORE_OUTCOME,
    }

    # load dataflow definition.
    file_path = arguments['<file>']
    mode = mode_mapping[arguments['-m'] or '1']

    doc = None
    try:
        doc = open(file_path, encoding='utf-8').read()
    except:
        print('Cannot open file {0}'.format(file_path))
        return

    # parse.
    linear_ordering, _ = parse(doc)

    # generated page.
    removed_ext, _ = os.path.splitext(file_path)
    output_file_name = os.path.basename(removed_ext) + '.html'
    with open(output_file_name, encoding='utf-8', mode='w') as fout:
        fout.write(
            generate_mermaid_page(linear_ordering, mode),
        )


if __name__ == '__main__':
    entry_point()
