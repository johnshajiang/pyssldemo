# -*- coding: utf-8 -*-

"""
TLS peer
"""

from abc import ABCMeta, abstractmethod
import os
import ssl
from pyssldemo import utils


class Peer(metaclass=ABCMeta):

    """ TLS peer on specified parameters """

    def __init__(self, context=None):
        if context is None:
            self.context = utils.create_context()
        else:
            self.context = context

    @staticmethod
    def get_session(self):
        """ Return current SSL session """

    @staticmethod
    def is_session_resumed(self):
        """ Check if the session is resumed """

    def set_peer_auth(self, peer_auth):
        """ Set if the peer's certificate must be verified """

        if peer_auth:
            self.context.verify_mode = ssl.CERT_REQUIRED
        else:
            self.context.verify_mode = ssl.CERT_NONE

    @staticmethod
    def get_server_name(self):
        """ Return the selected server name """

    @staticmethod
    def set_app_protocols(self, *app_protocols):
        """ Set the supported application protocols """

    @staticmethod
    def get_app_protocol(self):
        """ Return the negotiated application protocol """

    @abstractmethod
    def close(self):
        """ Close the peer """

    @abstractmethod
    def get_log_path(self):
        """ Specify the local log file path  """

    def print_log(self):
        """ Print the local log file content """

        _log_path = self.get_log_path()
        if os.path.isfile(_log_path):
            with open(_log_path, 'r') as _file:
                for _line in _file.readlines():
                    print(_line)
        else:
            print(f'Not found log file: {_log_path}')

    def delete_log(self):
        """ Delete the local log file """

        _log_path = self.get_log_path()
        if os.path.isfile(_log_path):
            os.remove(_log_path)
        else:
            print(f'Not found log file: {_log_path}')

    def log(self, msg):
        print(f'[{type(self).__name__}] {msg}')
