# -*- coding: utf-8 -*-

"""
TLS client
"""

from threading import Thread
import socket
import ssl
from pyssldemo.peer import Peer
from pyssldemo import utils


class Client(Peer):

    def __init__(self, context=None, session=None, server_auth=True):
        super(Client, self).__init__(context)
        self.set_peer_auth(server_auth)
        self.session = session
        self.c_socket = None  # Client-side SSL socket
        self.server_name = None  # Indicated server hostname

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_session(self):
        return self.c_socket.session

    def is_session_resumed(self):
        return self.c_socket.session_reused

    def set_app_protocols(self, *app_protocols):
        self.context.set_alpn_protocols(app_protocols)

    def get_app_protocol(self):
        return self.c_socket.selected_alpn_protocol()

    def connect(self, host='localhost', port=443, msg=b'Hello'):
        self.log(f'Connecting to {host}:{port}')
        self.c_socket = self.context.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        if self.session is not None:
            self.c_socket.session = self.session

        if self.server_name is not None:
            self.c_socket.server_hostname = self.server_name

        self.c_socket.connect((host, port))
        self.log('Connected to server')

        self.c_socket.sendall(msg)
        self.log('Send request')
        self.log(f'Response: {self.c_socket.recv(1024)}')

    def close(self):
        self.c_socket.close()
        self.log('Closed')

    def get_log_path(self):
        return 'client.log'


class ClientThread(Thread):
    def __init__(self, client, port):
        Thread.__init__(self)
        self.client = client
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def run(self):
        self.client.connect(port=self.port)


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _host = 'localhost'
    _port = 65443
    try:
        with Client() as _client:
            _client.connect(_host, _port, b'Hello')

        Client.signal_close_server(_client.context, _host, _port)
    except KeyboardInterrupt:
        print('Client exited')
