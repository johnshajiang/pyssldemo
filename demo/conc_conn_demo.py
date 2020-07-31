# -*- coding: utf-8 -*-

"""
Multiple clients connect to one server concurrently.
"""

import ssl

from pyssldemo import utils
from pyssldemo.client import Client, ClientThread
from pyssldemo.params import Protocols, CipherSuites
from pyssldemo.server import Server, ServerThread


def run_case(protocol, cipher_suite):
    _context = utils.create_context(min_protocol=protocol,
                                    max_protocol=protocol,
                                    cipher_suites=(cipher_suite,))
    _c_thread = ClientThread(Client(context=_context), _port)
    _c_thread.start()
    return _c_thread


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

                # If the cipher suite is not supported by the TLS protocol,
                # the case just be ignored.
                if not _cipher_suite.supported_by(_protocol):
                    continue

                _c_threads.append(run_case(_protocol, _cipher_suite))

        for _c_thread in _c_threads:
            _c_thread.join()
