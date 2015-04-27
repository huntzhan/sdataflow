# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow import metadata
from sdataflow.lang import parse
from sdataflow.callback import hook_callbacks, scheduler


__all__ = ['DataflowHandler']


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


# merge of lang and scheduler.
class DataflowHandler(object):

    def __init__(self, doc, name_callback_mapping):
        self.linear_ordering, _ = parse(doc)
        hook_callbacks(self.linear_ordering, name_callback_mapping)

    def run(self):
        scheduler(self.linear_ordering)
