# -*- coding: utf-8 -*-

"""
TLS peer
"""

import socket
import utils


class Peer(object):
    """ TLS peer on specified protocol and cipher suite """

    def __init__(self, protocol, cipher_suite):
        self.context = utils.create_context(protocol, cipher_suite)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
