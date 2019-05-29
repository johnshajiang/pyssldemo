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

    def set_app_protocols(self, *app_protocols):
        self.context.set_alpn_protocols(app_protocols)

    def connect(self, host='localhost', port=443, msg=b'Hello'):
        with self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _ssl_socket:
            if self.session is not None:
                _ssl_socket.session = self.session

            _ssl_socket.connect((host, port))
            self.log('Connected to server')

            self.session = _ssl_socket.session
            self.session_reused = _ssl_socket.session_reused
            self.negotiated_app_protocol = _ssl_socket.selected_alpn_protocol()

            _ssl_socket.sendall(msg)
            self.log('Send request')
            self.log(f'Response: {_ssl_socket.recv(1024)}')


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
