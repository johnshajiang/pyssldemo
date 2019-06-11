# -*- coding: utf-8 -*-

"""
A basic connection demo with different TLS protocols and cipher suites.
"""

import ssl
from pyssldemo.params import Protocols, CipherSuites
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client
from pyssldemo import utils


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    for _protocol in (Protocols.TLSV1_2, Protocols.TLSV1_3):
        for _cipher_suite in (CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                              CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
                              CipherSuites.TLS_AES_256_GCM_SHA384,
                              CipherSuites.TLS_AES_128_GCM_SHA256):

            # If the cipher suite is not supported by the TLS protocol, the case just be ignored.
            if not _cipher_suite.supportedBy(_protocol):
                continue

            print('========== Case start ==========')
            print(f'Protocol: {_protocol}\nCipher suite: {_cipher_suite}')

            with ServerThread(Server()) as _s_thread:
                _s_thread.start()

                _port = _s_thread.server.get_port()

                _context = utils.create_context(min_protocol=_protocol,
                                                max_protocol=_protocol,
                                                cipher_suites=(_cipher_suite,))
                with Client(context=_context) as _client:
                    _client.connect(port=_port)

                Client.signal_close_server(context=_client.context, port=_port)
