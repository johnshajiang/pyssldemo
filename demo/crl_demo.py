# -*- coding: utf-8 -*-

"""A simple demo on basic connection with CRL checking.
"""

import ssl

from pyssldemo import utils
from pyssldemo.certs import CertGroups
from pyssldemo.client import Client
from pyssldemo.server import Server, ServerThread

if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    _server = Server(utils.create_context(
        cert_group=CertGroups.RSA_GROUP))
    _server.set_peer_auth(True)
    _server.check_crl(True)

    with ServerThread(_server) as _s_thread:
        _s_thread.start()

        _port = _s_thread.server.get_port()

        with Client(utils.create_context(
                cert_group=CertGroups.RSA_GROUP)) as _client:
            _client.check_crl(True)
            _client.connect(port=_port)
