# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class InfoBase(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<{0}: {1}>'.format(type(self).__name__, self.name)


class Entry(InfoBase):
    pass


class OutcomeType(InfoBase):
    pass
