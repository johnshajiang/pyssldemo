# -*- coding: utf-8 -*-

"""
Multiple clients connect to one server concurrently.
"""

import ssl
from pyssldemo.params import Protocols, CipherSuites
from pyssldemo.server import Server, ServerThread
from pyssldemo.client import Client, ClientThread
from pyssldemo import utils


if __name__ == '__main__':
    print(ssl.OPENSSL_VERSION)

    with ServerThread(Server()) as _s_thread:
        _s_thread.start()

        _port = _s_thread.server.get_port()

        _c_threads = []
        for _protocol in (Protocols.TLSV1_2, Protocols.TLSV1_3):
            for _cipher_suite in (CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                                  CipherSuites.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
                                  CipherSuites.TLS_AES_256_GCM_SHA384,
                                  CipherSuites.TLS_AES_128_GCM_SHA256):

                # If the cipher suite is not supported by the TLS protocol, the case just be ignored.
                if not _cipher_suite.supported_by(_protocol):
                    continue

                _context = utils.create_context(min_protocol=_protocol,
                                                max_protocol=_protocol,
                                                cipher_suites=(_cipher_suite,))
                _c_thread = ClientThread(Client(context=_context), _port)
                _c_threads.append(_c_thread)
                _c_thread.start()

        for _c_thread in _c_threads:
            _c_thread.join()