# -*- coding: utf-8 -*-

"""
TLS client
"""

import socket
import ssl
from peer import Peer
import utils


class Client(Peer):

    def __init__(self, context=None, session=None):
        super(Client, self).__init__(context)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.session = session
        self.c_socket = None  # Client-side SSL socket

        self.negotiated_app_protocol = None
        self.session_resumed = None

    def set_app_protocols(self, *app_protocols):
        self.context.set_alpn_protocols(app_protocols)

    def connect(self, host='localhost', port=443, msg=b'Hello'):
        with self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as self.c_socket:
            if self.session is not None:
                self.c_socket.session = self.session

            self.c_socket.connect((host, port))
            self.log('Connected to server')

            self.session = self.c_socket.session
            self.session_resumed = self.c_socket.session_reused
            self.negotiated_app_protocol = self.c_socket.selected_alpn_protocol()

            self.c_socket.sendall(msg)
            self.log('Send request')
            self.log(f'Response: {self.c_socket.recv(1024)}')

    def signal_close_server(self, host='localhost', port=443):
        self.connect(host, port, msg=utils.SERVER_EXIT_FLAG)


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _host = 'localhost'
    _port = 65443
    try:
        _client = Client()
        _client.connect(_host, _port, b'Hello')
        _client.connect(_host, _port, utils.SERVER_EXIT_FLAG)
    except KeyboardInterrupt:
        print('Client exited')
