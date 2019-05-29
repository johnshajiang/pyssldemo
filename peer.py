# -*- coding: utf-8 -*-

"""
TLS peer
"""

import utils


class Peer(object):
    """ TLS peer on specified parameters """

    def __init__(self, context):
        if context is None:
            self.context = utils.create_context()
        else:
            self.context = context

    def log(self, msg):
        print(f'[{type(self).__name__}] {msg}')
