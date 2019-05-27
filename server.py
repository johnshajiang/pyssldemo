# -*- coding: utf-8 -*-

"""
TLS server
"""

from threading import Thread
import socket
import ssl
from params import Protocols, CipherSuites
from peer import Peer
import utils


def log(msg):
    print('[Server] ' + msg)


class Server(Peer):
    """ TLS server on specified protocol, cipher suite and port """

    def __init__(self, protocol, cipher_suite, port=0):
        super(Server, self).__init__(protocol, cipher_suite)
        self.s_socket = self.context.wrap_socket(
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM),
            server_side=True)
        self.s_socket.bind(('127.0.0.1', port))
        self.s_socket.listen()
        log(f'Listening {self.get_port()}')

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_port(self):
        return self.s_socket.getsockname()[1]

    def accept(self):
        log('Accepting connection ...')
        while True:
            _socket, _addr = self.s_socket.accept()

            log(f'Client address: {_addr}')
            log(f'Negotiated protocol: {_socket.version()}')
            log(f'Negotiated cipher suite: {_socket.cipher()}')

            with _socket:
                request = _socket.recv(1024)
                log(f'Request: {request}')
                if request == utils.SERVER_EXIT_FLAG:
                    _socket.sendall(b'Exiting ...')
                    break
                else:
                    _socket.sendall(b'Client said: ' + request)
                    log('Send response')

    def close(self):
        self.s_socket.close()
        log('Closed')


class ServerThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        self.server.accept()


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        server = Server(
            Protocols.TLSV1_2,
            CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
            9443)
        server.accept()
    except KeyboardInterrupt:
        print('Server exited')
    finally:
        server.close()
