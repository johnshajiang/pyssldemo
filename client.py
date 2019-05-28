# -*- coding: utf-8 -*-

"""
TLS client
"""

import socket
import ssl
from params import Protocols, CipherSuites
from certs import CertGroups
from peer import Peer
import utils


class Client(Peer):
    """ TLS client on specified TLS protocol and cipher suite """

    def __init__(
            self,
            min_protocol=Protocols.TLSV1_0,
            max_protocol=Protocols.TLSV1_2,
            cert_group=CertGroups.RSA_GROUP,
            cipher_suites=(CipherSuites.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,),
            check_cert=True,
            check_servername=False):
        super(Client, self).__init__(
            min_protocol,
            max_protocol,
            cert_group,
            cipher_suites,
            check_cert)

        self.context.check_hostname = check_servername

    def connect(self, host, port, msg):
        with self.context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _c_socket:
            _c_socket.connect((host, port))
            self.log('Connected to server')

            _c_socket.sendall(msg)
            self.log('Send request')
            self.log(f'Response: {_c_socket.recv(1024)}')


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _host = 'localhost'
    _port = 65443
    try:
        _client = Client(
            cert_group=CertGroups.ECDSA_GROUP,
            cipher_suites=(
                CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA))
        _client.connect(_host, _port, b'Hello')
        _client.connect(_host, _port, utils.SERVER_EXIT_FLAG)
    except KeyboardInterrupt:
        print('Client exited')
