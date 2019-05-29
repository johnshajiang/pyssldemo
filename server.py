# -*- coding: utf-8 -*-

"""
TLS server
"""

from threading import Thread
import socket
import ssl
from peer import Peer
import utils


class Server(Peer):

    def __init__( self, context=None, port=0):
        super(Server, self).__init__(context)
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def set_client_auth(self, client_auth):
        if client_auth:
            self.context.verify_mode = ssl.CERT_REQUIRED
        else:
            self.context.verify_mode = ssl.CERT_NONE

    def set_app_protocols(self, *app_protocols):
        self.context.set_alpn_protocols(app_protocols)

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
            _socket, _addr = self.s_socket.accept()

            self.log(f'Client address: {_addr}')
            self.log(f'Negotiated protocol: {_socket.version()}')
            self.log(f'Negotiated cipher suite: {_socket.cipher()}')

            with _socket:
                request = _socket.recv(1024)
                self.log(f'Request: {request}')
                if request == utils.SERVER_EXIT_FLAG:
                    _socket.sendall(b'Exiting ...')
                    break
                else:
                    _socket.sendall(b'Client said: ' + request)
                    self.log('Send response')

    def close(self):
        self.s_socket.close()
        self.log('Closed')


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
