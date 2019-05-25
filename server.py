# -*- coding: utf-8 -*-

"""
TLS server
"""

import ssl
from params import Protocols, CipherSuites
from peer import Peer


class Server(Peer):
    """ TLS server on specified protocol, cipher suite and port """

    def __init__(self, protocol, cipher_suite, port):
        super(Server, self).__init__(protocol, cipher_suite)
        self.port = port

    def start(self):
        self.socket.bind(('localhost', self.port))
        self.socket.listen()
        print(f'Server is listening {str(self.socket.getsockname()[1])}')

        with self.context.wrap_socket(self.socket, server_side=True) as _server:
            while True:
                _conn, _addr = _server.accept()

                print(f'Client address: {str(_addr)}')
                print(f'Negotiated protocol: {_conn.version()}')
                print(f'Negotiated cipher suite: {_conn.cipher()}')

                print(f'Request: {_conn.recv(1024)}')
                _conn.sendall('This is server'.encode())


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    try:
        server = Server(
            Protocols.TLSV1_2,
            CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
            9443)
        server.start()
    except KeyboardInterrupt:
        print('Server exited')
