# -*- coding: utf-8 -*-

"""
TLS server
"""

from threading import Thread
import socket
import ssl
from pyssldemo.peer import Peer
from pyssldemo import utils


class Server(Peer):

    def __init__(self, context=None, port=0):
        super(Server, self).__init__(context)
        self.port = port

        self.s_socket = None  # Server-side SSL socket
        self.c_socket = None  # Accepted SSL socket

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_session(self):
        return self.s_socket.session

    def is_session_resumed(self):
        return self.s_socket.session_reused

    def get_server_name(self):
        raise RuntimeError('Not implemented yet')

    def set_app_protocols(self, *app_protocols):
        self.context.set_alpn_protocols(app_protocols)

    def get_app_protocol(self):
        return self.s_socket.selected_alpn_protocol()

    def start(self):
        self.s_socket = self.context.wrap_socket(
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM),
            server_side=True)
        self.s_socket.bind(('127.0.0.1', self.port))
        self.s_socket.listen()
        self.log(f'Listening {self.get_port()}')

    def get_port(self):
        return self.s_socket.getsockname()[1]

    def accept(self):
        self.log('Accepting connection ...')
        while True:
            self.c_socket, _addr = self.s_socket.accept()

            self.log(f'Client address: {_addr}')
            self.log(f'Negotiated protocol: {self.c_socket.version()}')
            self.log(f'Negotiated cipher suite: {self.c_socket.cipher()}')

            with self.c_socket:
                request = self.c_socket.recv(1024)
                self.log(f'Request: {request}')
                if request == utils.SERVER_EXIT_FLAG:
                    self.c_socket.sendall(b'Exiting ...')
                    break
                else:
                    self.c_socket.sendall(b'Client said: ' + request)
                    self.log('Send response')

    def close(self):
        self.s_socket.close()
        self.log('Closed')

    def get_log_path(self):
        return 'server.log'


class ServerThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()

    def run(self):
        self.server.start()
        self.server.accept()


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        with Server(port=65443) as _server:
            _server.start()
            _server.accept()
    except KeyboardInterrupt:
        print('Server exited')
