# -*- coding: utf-8 -*-

"""
TLS client
"""

import socket
import ssl
from params import Protocols, CipherSuites
from peer import Peer
import utils


def log(msg):
    print('[Client] ' + msg)


class Client(Peer):
    """ TLS client on specified TLS protocol and cipher suite """

    def __init__(self, protocol, cipher_suite):
        super(Client, self).__init__(protocol, cipher_suite)

    def connect(self, host, port, msg):
        with self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _c_socket:
            _c_socket.connect((host, port))
            log('Connected to server')

            _c_socket.sendall(msg)
            log('Send request')
            log(f'Response: {_c_socket.recv(1024)}')


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        client = Client(
            Protocols.TLSV1_2,
            CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384)
        host = 'localhost'
        port = 9443
        client.connect(host, port, b'This is client')
        client.connect(host, port, utils.SERVER_EXIT_FLAG)
    except KeyboardInterrupt:
        print('Client exited')
