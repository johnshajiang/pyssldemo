# -*- coding: utf-8 -*-

"""
TLS client
"""

import ssl
from params import Protocols, CipherSuites
from peer import Peer


class Client(Peer):
    """ TLS client on specified TLS protocol and cipher suite """

    def __init__(self, protocol, cipher_suite):
        super(Client, self).__init__(protocol, cipher_suite)

    def connect(self, host, port):
        with self.context.wrap_socket(self.socket) as _client:
            _client.connect((host, port))
            print('connected to server')

            _client.sendall('This is client'.encode())
            print("Response: %s" % str(_client.recv(1024)))


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        client = Client(
            Protocols.TLSV1_2,
            CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384)
        client.connect('localhost', 9443)
    except KeyboardInterrupt:
        print('Client exited')
